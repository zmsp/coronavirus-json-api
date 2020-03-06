import csv
import json
import datetime
import requests
import hashlib
import sys
CSV_PATH = "./latest.csv"
JSON_PRETTY_PATH = "./latest.json"
JSON_PATH = "./latest.json"
MD5_FILE_PATH = "./latest.md5"
README_PATH = "./README.md"

def dumpCsvToJson(CSV_FILE):
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        reader = csv.DictReader(f, headers)
        out = json.dumps([row for row in reader])
    with open('latest.json', "w") as f:
        f.write(out)

def dumpCsvToJsonPrettyPrint(CSV_FILE):
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        reader = csv.DictReader(f, headers)
        out = json.dumps([row for row in reader], sort_keys=True, indent=2, separators=(',', ':'))
    with open('latest_pretty_print.json', "w") as f:
        f.write(out)

def md5Checksum(filePath,url):
    m = hashlib.md5()
    if url==None:
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    else:
        r = requests.get(url)
        for data in r.iter_content(8192):
             m.update(data)
        return m.hexdigest()

def update_readme(first_line):
    with open(README_PATH) as f:
        lines = f.readlines()
    lines[0] =first_line
    with open(README_PATH, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    today = datetime.datetime.now()+datetime.timedelta(days=1)
    template_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{DATE}.csv"
    CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))

    status_code =0
    while( status_code != 200):
        CSV_URL = template_URL.format(DATE=today.strftime('%m-%d-%Y'))
        r = requests.get(CSV_URL)
        status_code = r.status_code
        today = today - datetime.timedelta(days=1)
    with open(CSV_PATH, 'wb') as f:
        f.write(r.content)

    with open(MD5_FILE_PATH, 'r') as file:
        local_md5 = file.read().replace('\n', '')

    latest_md5 = md5Checksum(CSV_PATH, None)
    if (latest_md5 != local_md5):
        dumpCsvToJson(CSV_PATH)
        dumpCsvToJsonPrettyPrint(CSV_PATH)
        with open(MD5_FILE_PATH, 'w') as file:
            file.write(latest_md5)
        update_readme("# Novel Coronavirus JSON data (Updated: {UPDATED}) \n".format(UPDATED=datetime.datetime.now().strftime('%d %B, %Y  %H:%M:%S')))
        print("updated")
    else:
        sys.exit('Local file is the latest, nothing was updated')




