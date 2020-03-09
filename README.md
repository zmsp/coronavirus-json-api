# Novel Coronavirus JSON data (Updated: 09 March, 2020  02:01:59) 
This repository tracks Novel Coronavirus data and converts it into a json to be consumed by other applications. 
The data is updated form Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) repository. 
You can visit https://github.com/CSSEGISandData/COVID-19 for more information. 


This repository gets updated automatically. 

# How to use 
Please see https://www.jokecamp.com/blog/code-examples-api-http-get-json-different-languages/ on how to to fetch these data. 


## Files:

        csse_covid_19_daily_reports.json
        csse_covid_19_daily_reports_pretty_print.json
        csse_covid_19_data/
        time_series_19-covid-Confirmed.json
        time_series_19-covid-Confirmed_pretty_print.json
        time_series_19-covid-Deaths.json
        time_series_19-covid-Deaths_pretty_print.json
        time_series_19-covid-Recovered.json
        time_series_19-covid-Recovered_pretty_print.json

### URLs
```
latest = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/latest.json"
metadata = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/metadata.json"
```
Note that each dataset has a pretty print and a condensed pair 



## 
Provides record in an a list format
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

## metadata file
Metadata provides useful information about each columns. Intended to help with statistical analysis of the data.


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

```json
{
 "US": {
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
        "Province": [
            {
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
            },
            {... and more}
]}
}

```