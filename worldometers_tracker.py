
from selenium import webdriver
from bs4 import BeautifulSoup as BSoup
from io import StringIO
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import sys, getopt, json
import time
import pycountry


from gspread_pandas import Spread, Client

def retrieve_data_bno(var_set):
    driver = webdriver.Chrome(executable_path= var_set['driver'])
    driver.get("https://www.worldometers.info/coronavirus/")
    time.sleep(2)

    row_count = len(driver.find_elements_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr')) - 1
    col_count = len(driver.find_elements_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]//tr[2]/td'))
    all_data = {}
    for i in range(1, row_count):
        data = []
        for j in range(1, col_count + 1) :
            content = driver.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text
            if j == 1:
                country = content
            else:
                data.append(content)
        all_data[country] = data
    return (all_data)

def create_dataframe_historic(data):
    time = datetime.now()
    time = time.strftime("%m/%d/%Y %H:%M:%S")
    # row = df.loc[df['datetime'] == time]
    list_column = []
    list_val = []
    for key, value in data.items():
        notes = ''
        for i, val in enumerate(value):
            if i == 0:
                list_val.append(val)
                list_column.append(key + '_cases')
            elif i == 1:
                list_val.append(val)
                list_column.append(key + '_new_cases')
            elif i == 2:
                list_column.append(key + '_deaths')
                list_val.append(val)
            elif i == 3:
                list_column.append(key + '_new_deaths')
                list_val.append(val)
            elif i == 4:
                list_column.append(key + '_recovered')
                list_val.append(val)
            elif i == 5:
                list_column.append(key + '_active_cases')
                list_val.append(val)
            elif i == 6:
                list_column.append(key + '_serious_critical')
                list_val.append(val)
            elif i==7:
                list_column.append(key + '_TOT_CASES_by_1M_pop')
                list_val.append(val)
    try :
        df = pd.read_excel('output2.xlsx', index_col='Unnamed: 0')
        for col in list_column:
            if col not in df.columns:
                df[col] = 0
        column_order = list_column
        df = df[column_order]
    except:
        df = pd.DataFrame(columns = list_column)
    df.loc[time] = list_val
    df.to_excel('output2.xlsx')
    return (df)

def push_to_google(df, var_set, current=False):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        var_set['credentials'], scope)
    gc = gspread.authorize(credentials)
    spreadsheets_key = var_set['key_sheet']
    wks_name = var_set['work_sheet_name'] + '_fulldata' if not current else var_set['work_sheet_name'] + '_current'
    # d2g.upload(df, spreadsheets_key, wks_name, credentials=credentials, row_names=True)
    x = Spread(spreadsheets_key, wks_name, creds=credentials)
    x.df_to_sheet(df, index=True, sheet=wks_name, replace=True)
    print("test")


def get_driver_and_credentials(opt_google):
    with open('path_driver.json', 'r') as dfile:
        driver = dfile.read()
        driver = json.loads(driver)
    with open('google_sheet_settings.json', 'r') as gs_file:
        settings = gs_file.read()
        settings = json.loads(settings)

    var_set = {}

    var_set['driver'] = driver["PATH_CHROME_DRIVER"]

    if opt_google:
        var_set['credentials'] = settings['CREDENTIALS']
        var_set['key_sheet'] = settings['KEY_SHEET']
        var_set['work_sheet_name'] = settings['WORK_SHEET_NAME']

    return (var_set)

def create_dataframe_current(data):
    df_current = pd.DataFrame.from_dict(data, orient='index',
                       columns=['confirmed', 'new_case', 'deaths', 'new_deaths', 'recovered', 'active_case', 'serious_case', 'case_per_1m'])

    df_new = df_current
    for i in df_current.columns:
        print(i)
        try:
            test = df_current[i].str.replace(',','')
            test = test.str.replace('+','')
            test = test.str.replace('-','')
            df_new[i]=pd.to_numeric(test, errors = 'coerce')
            df_new[i]=df_new[i].replace("", 0)

        except:
            print(i)


    return df_new.fillna(0)

def applyCorrection (df):
    #tmp error
    df = df.drop(['Vatican City'])
    return df
def main(argv):
    opt_google = True
    usage = """
    usage : corona_tracker.py [-h] [-p]

    optional arguments:
    -h, --help show usage then exit
    -p, --push-to-google will push the data to Google sheet if CREDENTIALS and
    KEY_SHEET is set correctly
    """
    try:
      opts, args = getopt.getopt(argv,"hp", ['help', 'push-to-google'])
    except getopt.GetoptError:
      print (usage)
      sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ("-p", "--push-to-goole"):
            opt_google = True
    var_set = get_driver_and_credentials(opt_google)
    data = retrieve_data_bno(var_set)

    import json

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=1)
    # df = create_dataframe_historic(data)
    df_current = create_dataframe_current(data)
    df_current.to_csv("current_country.csv")
    print(df_current.dtypes)
    # df_current = applyCorrection(df_current)
    if (len(df_current.index) > 50):
        update_meta(df_current)
        if opt_google:
            push_to_google(df_current, var_set, True)

def update_meta (df):
    length = len(df.index)
    if (len(df.index) > 50):


        meta = {}

        cols = ["confirmed", "deaths","recovered", "active_case", "new_case", "new_deaths", "serious_case"]

        count = 0
        correction = {"Mainland China": "China", "S. Korea": "Korea, Republic of", "UAE": "United Arab Emirates",
         "UK": "United Kingdom", "Republic of Ireland": "Ireland", "Taiwan*": "Taiwan", "Congo (Kinshasa)": "Congo",
         "occupied Palestinian territory": "Palestine", "Ivory Coast":"Côte d'Ivoire", "DRC":"Congo",  "St. Barth": "Saint Barthélemy", "St. Vincent Grenadines":"Saint Vincent and the Grenadine" }
        for i in df.index:
            if correction.__contains__(i):
                count +=1
                continue
            try:
                country = pycountry.countries.search_fuzzy(i)[0]
                print(i)
                print(country.name)
                count +=1
            except:

                print("exp {}".format( i))

        for i in range( cols.__len__()):
            meta[cols[i]]= str(int(df[cols[i]].sum()))

        meta["updated"] = datetime.now().strftime('%d %B, %Y  %H:%M:%S')
        meta["country"] = str(count)
        with open('c:/Users/zobai/PycharmProjects/COVID-19-Data-Formatter/combine_summary.json', 'w') as f:
           out =  json.dumps(meta,indent=1)
           f.write(out)
           print(out)

if __name__ == "__main__":
    main(sys.argv[1:])
