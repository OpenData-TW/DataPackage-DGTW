# Data Package

# datapackage.json
```
{
  "name": "a-unique-human-readable-and-url-usable-identifier",
  "datapackage_version": "1.0-beta",
  "title": "A nice title",
  "description": "...",
  "version": "2.0",
  "keywords": ["name", "My new keyword"],
  "licenses": [{
    "url": "http://opendatacommons.org/licenses/pddl/",
    "name": "Open Data Commons Public Domain",
    "version": "1.0",
    "id": "odc-pddl"
  }],
  "sources": [{
    "name": "World Bank and OECD",
    "web": "http://data.worldbank.org/indicator/NY.GDP.MKTP.CD"
  }],
  "contributors":[ {
    "name": "Joe Bloggs",
    "email": "joe@bloggs.com",
    "web": "http://www.bloggs.com"
  }],
  "maintainers": [{
    // like contributors
  }],
  "publishers": [{
    // like contributors
  }],
  "dependencies": {
    "data-package-name": ">=1.0"
  },
  "resources": [
    {
      // ... see below ...
    }
  ],
  // extend your datapackage.json with attributes that are not
  // part of the data package spec
  // we add a views attribute to display Recline Dataset Graph Views
  // in our Data Package Viewer
  "views" : [
    {
      ... see below ...
    }
  ],
  // you can add your own attributes to a datapackage.json, too
  "my-own-attribute": "data-packages-are-awesome",
}
```

## data.gov.tw
- '資料集描述': 'DESC',
- '主要欄位說明': 'SCHEMA',
- '提供機關': 'AGENCY',
- '提供機關聯絡人': 'AGENCY_CONTACT',
- '更新頻率': 'UPDATE_FREQ',
- '授權方式': 'LICENCE',
- '計費方式': 'CHARGE',
- '上架日期': 'DATE_PUBLISH',
- '資料集類型': 'DATA_TYPE',
- '詮釋資料更新時間': 'DATE_UPDATE_META',
- '關鍵字': 'KEYWORDS',
- '主題分類': 'CATEGORY',
- '服務分類': 'SERVICE_TYPE',
- '相關網址': 'RELATED_URL',
- '備註': 'NOTES',
- '瀏覽次數': 'VIEWS',
- '下載次數': 'DOWNLOAD',
- '意見數': 'COMMENTS',
- '檔案格式': 'RES_FILETYPE',
- '編碼': 'RES_ENCODE',
- '資料量': 'REC_COUNT',
- '資源網址': 'RES_URL',
- '資源描述': 'RES_DESC',
- '資料資源更新時間': 'RES_DATE_UPDATE_META',
- 'CSV 下載': 'CSV',
- 'XLSX 下載': 'XLSX',
- 'ODS 下載': 'ODS',
- 'XML 下載': 'XML',
- 'JSON 下載': 'JSON',

