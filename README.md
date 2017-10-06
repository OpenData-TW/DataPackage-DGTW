# DataPackage-DGTW
**http://data.gov.tw 資料集轉 [DataPackage](http://frictionlessdata.io/data-packages/)**

- [DataPackage](http://frictionlessdata.io/data-packages/)
- [HackFoldr](http://pro.odtw.org/2017ODProjects/https%253A%252F%252Fhackmd.io%252Fs%252Fr1kIyHzn-)
- [Github](https://github.com/OpenData-TW/DataPackage-DGTW)

# DGTW

http://data.gov.tw (DGTW) 是國發會所管理的政府開放資料平台。作為台灣政府的政府開放資料入口網站，國發會希望其他中央與地方政府的開放資料都能透過這個平台來發佈。所以目前台灣政府的開放資料主要以下列幾種方式發佈：
- 只發佈在 DGTW 網站上
- 同時發佈在 DGTW 與機關自建的平台上 (自動或手動介接)
- 發佈在自建平台上，部分資料透過介接發佈在 DGTW
- 只發佈在自建平台，完全不鳥 DGTW

為了有效管理資料，國發會也在這個平台上公布了。所有資料只要有發佈在 DGTW 上就會遵守這個規範 ：
1. 資料集詮釋資料標準規範 - https://data.gov.tw/node/18252
2. 資料集詮釋資料API開發指引 - https://data.gov.tw/node/18236

但是目前 DGTW 網站上前台並不會將「資料集詮釋資料標準規範」所要求的所有欄位都顯示出來。如資料集編號。或著顯示上會合併不同欄位的內容，例如提供機關上級機關名稱與提供機關名稱被合併為「提供機關」，機關聯絡人則整合了聯絡人名字，電話與電子郵件這三個欄位。

比較糟糕的或許是，許多重要的資訊都被整合或是忽略。例如資料資源的欄位說明，資料集相關網址，資料資源最後更新時間。

這些資料有的有，有的沒，有的只是沒人填寫。而缺乏這些資料都讓資料的實用性受到影響。

目前 DGTW 網站上有提供資料搜尋結果的資料清單下載（提供 csv/json/xml 三種格式），但是這個功能所提供的資料清單內缺少資料集欄位描述的內容，有些欄位的填寫也出現錯誤 (2017.10.07 last checked)。這份清單需要進一步「清洗」才能真正使用。

另外，為了提升資料的品質，2017 年起國發會開始推動[資料品質檢驗機制](https://hackmd.io/c/B12WA44Zb/https%3A%2F%2Fhackmd.io%2Fs%2FB1V0hPmVW) : http://quality.data.gov.tw 。透過這個檢驗，我們可以知道目前提供的資料是否：
1. 連結有效
2. 資料資源可直接下載
3. 資料資源內容與資料集描述吻合 (編碼，主要欄位等)
4. 資料資源是否為結構化資料 (可否直接轉 csv)

![](https://i.imgur.com/z8vz7od.png)

# DataPackage

DataPackage 是英國 OKFN 所設計的一種簡易的資料包裝模式 (package) 與管理機制。基本的 DataPackage 的內容包含了一個資料描述的檔案 (datapackage.json) 與結構化的資料資源 (csv / json / xml 等)。除了這兩個基礎的檔案與內容，我們也可加上 License 文件，README.md (markdown 格式) 的說明文件等。

![](https://docs.google.com/drawings/d/19DTSTlxkOdTgieTWhnTNLAZtxn_ie63DV-vEGW_TP_E/pub?w=400)

DataPackage 計畫目前也提供了包含 Viewer / Validator / Manager / Packagist 等眾多的[應用工具](http://frictionlessdata.io/tools/)。

# DGTW2DataPackage

目前臺灣中央和地方在推動開放資料時，主要還是透過平台上發佈的方式來公布資料。然後使用者需要自己找到資料下載連結（大部分資料可直接下載，但是還是有不少是需要點近不同網頁後，點選連結，才能下載）。下載回來的資料當數量開始變多時，如果再加上資料版本（內容經過清洗，擴增等），就會出現嚴重的管理問題。

也就是在整個資料應用的 pipeline 中，我們目前並沒有一個好的方式來連結從網站上找到的資料，到資料應用（視覺化，分析等）之間的管理程序。

最好的方式當然是自己架設一個 [ckan 平台](https://ckan.org/)來做資料的管理。這樣如果政府所使用的平台也採用 ckan 的標準提供資料介接的 API，就可全自動的處理資料的管理程序。但是，目前並沒有這樣的自動化程序，一般使用者自己要管理 ckan 平台也不是一件簡單的事情。(ckan 是個資料入口平台)

所以如果我們能將 DGTW 上所登錄的資料集（metadata）都轉為 DataPackage 的包裝，同時將相關資源也一併檢驗後下載存放在同一個位置（local 或是 remote，或是，直接[使用 Github 來做資料的管理與存放](http://data.okfn.org/doc/core-data-curators)）

有了 DataPackage 包裝的資料集，我們也可將資料集轉為 R package 或是其他應用需求的檔案格式。

# 目標與計畫執行 (ToDo)
## 目標
- 將 DGTW 資料轉為 DataPackage，包含 datapackage.json + resources files (structured data)
- 建立符合其他資料平台與網站的轉換機制

## 計畫執行
1. DGTW/node 轉 metadata.json
2. 透過 Quality.data.gov.tw 將 DGTW/node 檢驗結果轉 QD_resources.json
3. 結合 metadata.json + QD_resources.json 建立 DataPacakge 資料包裝
4. 資料管理 : 命名，時間戳記等
5. 資料包裝管理工具：建置服務，管理，下載
6. 其他開放資料平台
