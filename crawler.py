import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from typing import List

class Crawler:
    """
    PTT MacShop 爬蟲
    """
    base_url = "https://www.ptt.cc"

    def __init__(self) -> None:
        """
        PTT MacShop 爬蟲初始化

        Usage
        --------
        >>> from crawler import Crawler
        >>> crawler = Crawler()
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

        Return
        --------
        None
        """
        pass

    def __fetch__(self, url:str) -> BeautifulSoup:
        """
        獲取文章資料

        Parameter
        --------
        url:文章列表之url

        Response
        --------
        soup:Beautifulsoup
        """
        ptt_url = f"{Crawler.base_url}/{url}"
        response = requests.get(url = ptt_url)
        response.encoding = 'utf-8'
        html_doc = response.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup
        
    def __get_previous_page_url__(self, soup:BeautifulSoup) -> str:
        """
        獲取文章網頁中之上一頁的連結

        Parameter
        --------
        soup:Beautifulsoup

        Response
        --------
        url:文章列表之url
        """
        div_action_bar = soup.find("div", {"id":"action-bar-container"}).findChildren(
            name = "a"
        )
        previous_href = div_action_bar[3]
        if previous_href.has_attr('href'):
            return previous_href.get('href')[1:]
        return None

    def __get_date_list__(self, days_limit:int) -> List[str]:
        """
        獲取電腦日期之日期列表

        Parameter
        --------
        days_limit:距離本日之幾天內的資料

        Response
        --------
        list:電腦日期之日期列表
        """
        # refs:https://stackoverflow.com/questions/1712116/formatting-yesterdays-date-in-python
        date_list = []
        for limit in list(range(0, days_limit)):
            date_str = date.today() - timedelta(days=limit)
            date_str = date_str.strftime('%m/%d')
            if date_str[0] == '0':
                date_str = date_str[1:]
            date_list.append(date_str)
        return date_list

    def download(self, days_limit:int) -> List[str]:
        """
        下載PTT MacShop之文章列表資料

        Parameter
        --------
        days_limit:距離本日之幾天內的資料

        Response
        --------
        list:文章資料，包含[日期, 作者, 標題, 連結]

        Usage
        --------
        >>> from crawler import Crawler
        >>> crawler = Crawler()
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
        """
        date_list = self.__get_date_list__(days_limit=days_limit)
        result_list = []
        first_fetch = True
        while True:
            if first_fetch:
                url = "bbs/MacShop/index.html"
                first_fetch = False
            else:
                url = self.__get_previous_page_url__(soup=soup)
            print(date_list, url)
            if url is None:
                break

            soup = self.__fetch__(url=url)
            parser_result_list = self.__parser__(soup=soup, date_list=date_list)
            if len(parser_result_list) == 0:
                break
            result_list.extend(parser_result_list)
            print('獲取文章:', len(result_list), '總文章個數:', len(result_list))
        return result_list

    def __parser__(self, soup:BeautifulSoup, date_list:list) -> List[str]:
        """
        解析文章列表資料

        Parameter
        --------
        soup:fetch之BeautifulSoup
        days_limit:距離本日之幾天內的資料

        Response
        --------
        list:文章資料，包含[日期, 作者, 標題, 連結]
        """
        r_ent_elements = soup.find_all(
            name = "div",
            attrs = {"class" : "r-ent"}
        )
        
        parser_result_list = []
        for r_ent_element in r_ent_elements:
            a_element = r_ent_element.findChildren(
                name = "div",
                attrs = {"class" : "title"},
                recursive = False
            )[0].findChildren(name = "a")

            if len(a_element) == 0:
                continue

            a_element = a_element[0]
            title = a_element.text
            if '[公告]' in title:
                continue
            href = a_element['href']
            
            meta_element = r_ent_element.findChildren(
                name = "div",
                attrs = {"class" : "meta"},
                recursive = False
            )[0]
            author = meta_element.findChildren(
                name = "div",
                attrs = {"class" : "author"},
                recursive = False
            )[0].text
            date = meta_element.findChildren(
                name = "div",
                attrs = {"class" : "date"},
                recursive = False
            )[0].text
            if date.lstrip() not in date_list:
                break
            parser_result_list.append([date, author, title, href])
        return parser_result_list