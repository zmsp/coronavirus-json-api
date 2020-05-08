# Novel Coronavirus JSON data (Updated: 07 May, 2020  23:50:33) 
This repository tracks Novel Coronavirus data and converts it into a JSON to be consumed by other applications. 
The data is updated from Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) repository. 
You can visit https://github.com/CSSEGISandData/COVID-19 for more information. 

This repository gets updated automatically on a daily basis.

#### Changelog
* all the previous files are deperacted. Please see ./v2/ folder for latest files. 


#### Visualization 

[coronavirusdashboard.live](http://coronavirusdashboard.live/) was created using the data API from this repository.



## How to use 

Please see https://www.jokecamp.com/blog/code-examples-api-http-get-json-different-languages/ on how to to fetch these data with different programing languages. 


## Files:
### csse_covid_19_data/directory contains source CSV

        csse_covid_19_data/csse_covid_19_daily_reports.csv

        csse_covid_19_data/time_series_19-covid-Confirmed.csv
        csse_covid_19_data/time_series_19-covid-Deaths.csv
        csse_covid_19_data/time_series_19-covid-Recovered.csv

### JSON files in the root directory contains api 
For each file there is a pretty_print and a condensed minified file. You can read the pretty_print file for the data structure. 


        metadata.json
        metadata_pretty_print.json
        csse_covid_19_daily_reports.json
        csse_covid_19_daily_reports_pretty_print.json
        time_series_19_covid_confirmed.json
        time_series_19_covid_confirmed_pretty_print.json
        time_series_19_covid_deaths.json
        time_series_19_covid_deaths_pretty_print.json
        time_series_19_covid_recovered.json
        time_series_19_covid_recovered_pretty_print.json
        update_data.py

### URLs
URLs should link to 'https://raw.githubusercontent.com/zmsp/coronavirus-json-api/' + file name.
Example : 
```
latest = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/latest.json"
metadata = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/metadata.json"
```




## File formats

### latest.json 
Provides record in a list format
```json
[
  {
    "Confirmed":"6593",
    "Country/Region":"South Korea",
    "Deaths":"42",
    "Last Update":"2020-03-06T13:33:03",
    "Latitude":"36.0000",
    "Longitude":"128.0000",
    "Province/State":"",
    "Recovered":"135"
  },
  {
    "Confirmed":"4747",
    "Country/Region":"Iran",
    "Deaths":"124",
    "Last Update":"2020-03-06T12:23:04",
    "Latitude":"32.0000",
    "Longitude":"53.0000",
    "Province/State":"",
    "Recovered":"913"
  }
...andmore
]

```

### metadata file
Metadata provides useful information about each column. Intended to help with statistical analysis of the data.

```json
{
  "columns_meta":{
    "Confirmed":{
      "max":"67592",
      "mean":"511.5577889447236",
      "median":"5.0",
      "min":"0",
      "std":"4828.578915044806",
      "unique":[]
    },
    "Country/Region":{
      "max":"",
      "mean":"",
      "median":"",
      "min":"",
      "std":"",
      "unique":[
        "Mainland China",
        "South Korea",
...and more
      ]
    },
...and more
  },
  "columns_name":[
    "Province/State",
...and more
  ],
  "country_meta":{
    "Afghanistan":{
      "alpha_2":"AF",
      "alpha_3":"AFG",
      "name":"Afghanistan"
    },
    "Algeria":{
      "alpha_2":"DZ",
      "alpha_3":"DZA",
      "name":"Algeria"
    }
  },
  "data_meta":{
    "md5":"4b2c3d9fd532d48f68e7a822c6ef9bb7",
    "updated":"07 March, 2020  00:20:13"
  }
}

```


### Daily Report
```json
{
    "Afghanistan": {
        "Province": [
            {
                "*": {
                    "Confirmed": 4,
                    "Country/Region": "Afghanistan",
                    "Deaths": 0,
                    "Last Update": "2020-03-08 04:53:03",
                    "Latitude": 33.0,
                    "Longitude": 65.0,
                    "Province/State": "",
                    "Recovered": 0
                }
            }
... and more 
        ],
        "total": {
            "Confirmed": 4,
            "Deaths": 0,
            "Last Update": "2020-03-08 04:53:03",
            "Latitude": 33.0,
            "Longitude": 65.0,
            "Province/State": 1,
            "Recovered": 0
        }
    },
... and more
```

### TimeSeries 

```json
{ "US": {
        "total": {
            "Province/State": 106.0,
            "Lat": 38.46143301886793,
            "Long": -95.28658490566035,
            "1/22/20": 1.0,
            "1/23/20": 1.0,
            "1/24/20": 2.0,
            "1/25/20": 2.0,
            "1/26/20": 5.0,
            "1/27/20": 5.0,
            "1/28/20": 5.0,
            "1/29/20": 5.0,
            "1/30/20": 5.0,
            "1/31/20": 7.0,
            "2/1/20": 8.0,
            "2/2/20": 8.0,
            "2/3/20": 11.0,
            "2/4/20": 11.0,
            "2/5/20": 12.0,
            "2/6/20": 12.0,
            "2/7/20": 12.0,
            "2/8/20": 12.0,
            "2/9/20": 12.0,
            "2/10/20": 12.0,
            "2/11/20": 13.0,
            "2/12/20": 13.0,
            "2/13/20": 15.0,
            "2/14/20": 15.0,
            "2/15/20": 15.0,
            "2/16/20": 15.0,
            "2/17/20": 15.0,
            "2/18/20": 15.0,
            "2/19/20": 15.0,
            "2/20/20": 15.0,
            "2/21/20": 35.0,
            "2/22/20": 35.0,
            "2/23/20": 35.0,
            "2/24/20": 53.0,
            "2/25/20": 53.0,
            "2/26/20": 59.0,
            "2/27/20": 60.0,
            "2/28/20": 62.0,
            "2/29/20": 70.0,
            "3/1/20": 76.0,
            "3/2/20": 101.0,
            "3/3/20": 121.0,
            "3/4/20": 152.0,
            "3/5/20": 220.0,
            "3/6/20": 277.0,
            "3/7/20": 416.0,
            "3/8/20": 538.0
        },
        "province": [
            {
                "King County, WA": {
                    "Province/State": "King County, WA",
                    "Country/Region": "US",
                    "Lat": 47.6062,
                    "Long": -122.3321,
                    "1/22/20": 1,
                    "1/23/20": 1,
                    "1/24/20": 1,
                    "1/25/20": 1,
                    "1/26/20": 1,
                    "1/27/20": 1,
                    "1/28/20": 1,
                    "1/29/20": 1,
                    "1/30/20": 1,
                    "1/31/20": 1,
                    "2/1/20": 1,
                    "2/2/20": 1,
                    "2/3/20": 1,
                    "2/4/20": 1,
                    "2/5/20": 1,
                    "2/6/20": 1,
                    "2/7/20": 1,
                    "2/8/20": 1,
                    "2/9/20": 1,
                    "2/10/20": 1,
                    "2/11/20": 1,
                    "2/12/20": 1,
                    "2/13/20": 1,
                    "2/14/20": 1,
                    "2/15/20": 1,
                    "2/16/20": 1,
                    "2/17/20": 1,
                    "2/18/20": 1,
                    "2/19/20": 1,
                    "2/20/20": 1,
                    "2/21/20": 1,
                    "2/22/20": 1,
                    "2/23/20": 1,
                    "2/24/20": 1,
                    "2/25/20": 1,
                    "2/26/20": 1,
                    "2/27/20": 1,
                    "2/28/20": 1,
                    "2/29/20": 6,
                    "3/1/20": 9,
                    "3/2/20": 14,
                    "3/3/20": 21,
                    "3/4/20": 31,
                    "3/5/20": 51,
                    "3/6/20": 58,
                    "3/7/20": 71,
                    "3/8/20": 83
                }
            },
            {
                "Cook County, IL": {
                    "Province/State": "Cook County, IL",
                    "Country/Region": "US",
                    "Lat": 41.7377,
                    "Long": -87.6976,
                    "1/22/20": 0,
                    "1/23/20": 0,
                    "1/24/20": 1,
                    "1/25/20": 1,
                    "1/26/20": 1,
                    "1/27/20": 1,
                    "1/28/20": 1,
                    "1/29/20": 1,
                    "1/30/20": 1,
                    "1/31/20": 2,
                    "2/1/20": 2,
                    "2/2/20": 2,
                    "2/3/20": 2,
                    "2/4/20": 2,
                    "2/5/20": 2,
                    "2/6/20": 2,
                    "2/7/20": 2,
                    "2/8/20": 2,
                    "2/9/20": 2,
                    "2/10/20": 2,
                    "2/11/20": 2,
                    "2/12/20": 2,
                    "2/13/20": 2,
                    "2/14/20": 2,
                    "2/15/20": 2,
                    "2/16/20": 2,
                    "2/17/20": 2,
                    "2/18/20": 2,
                    "2/19/20": 2,
                    "2/20/20": 2,
                    "2/21/20": 2,
                    "2/22/20": 2,
                    "2/23/20": 2,
                    "2/24/20": 2,
                    "2/25/20": 2,
                    "2/26/20": 2,
                    "2/27/20": 2,
                    "2/28/20": 2,
                    "2/29/20": 2,
                    "3/1/20": 3,
                    "3/2/20": 4,
                    "3/3/20": 4,
                    "3/4/20": 4,
                    "3/5/20": 5,
                    "3/6/20": 5,
                    "3/7/20": 6,
                    "3/8/20": 7
                },
... and more

         }
}

```


### Licensing and Terms:
The code is released under Apache License 2.0 license. [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) reserves the rights to the data.  

You are not to hold the owners and contributors accountable for any legal issues or damage. Data is provided as is provided as is without warranty.
