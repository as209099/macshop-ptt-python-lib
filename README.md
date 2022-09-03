# macshop-ptt-python-lib
PTT MacShop 蘋果二手商品交易版 - Python

## 簡介
本程式主要用於取得PTT MacShop之商品資料，方便於追蹤特定之商品文章。

## 使用方法

```python
# 初始化
>>> from crawler import Crawler
>>> crawler = Crawler()
```
```python
>>> # 下載三天內的所有文章資料
>>> data_list = crawler.download(days_limit = 3)
>>> print(data_list)
[' 9/03',
...
'/bbs/MacShop/M.1662073206.A.BAF.html'],
[' 9/02',
'Atomimic',
'[販售] 雙北 全新 AirPods 3   (已售出)',
'/bbs/MacShop/M.1662080737.A.A1B.html']]
```

## 使用之Library
- <a href="https://requests.readthedocs.io/en/latest/">Requests</a>
- <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup4</a>

## 安裝
### 使用到的Library
```
pip install requests
pip install beautifulsoup4
```
### 下載library
```
mkdir ptt-macshop
cd ptt-macshop
git clone git@github.com:as209099/macshop-ptt-python-lib.git
```
enjoy coding!

## 授權
採用<a href="https://zh.m.wikipedia.org/zh-tw/GNU%E9%80%9A%E7%94%A8%E5%85%AC%E5%85%B1%E8%AE%B8%E5%8F%AF%E8%AF%81">GNU GPL授權條款</a>，可以自行運用，也可以發起Issue或Pull Request給我。
