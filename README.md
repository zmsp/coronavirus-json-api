# Novel Coronavirus JSON data (Updated: 07 March, 2020  00:20:13) 
This repository tracks Novel Coronavirus data and converts it into a json to be consumed by other applications. 
The data is updated form Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) repository. 
You can visit https://github.com/CSSEGISandData/COVID-19 for more information. 


This repository gets updated automatically. 

# How to use 
Please see https://www.jokecamp.com/blog/code-examples-api-http-get-json-different-languages/ on how to to fetch these data. 


### URLs
```
latest_pretty_print = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/latest_pretty_print.json"
latest = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/latest.json"
metadata = "https://raw.githubusercontent.com/zmsp/coronavirus-json-api/master/metadata.json"
```



## latest.json file
Provides record in an a list format
```
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
``
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
...and more
  },
  "data_meta":{
    "md5":"4b2c3d9fd532d48f68e7a822c6ef9bb7",
    "updated":"07 March, 2020  00:20:13"
  }
}
``