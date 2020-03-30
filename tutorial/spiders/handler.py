# -*- coding:utf-8 -*-
"""
@Author: caizhanjin
@Time: 2020-03-30
@Detail: 
"""
import requests
import re
import time
import pandas as pd
import csv
import random


class TianyanchaHandle(object):

    def __init__(self):
        self.tianyancha_session = requests.session()
        self.header = {
            'Cookie': 'jsid=SEM-BAIDU-PZ2003-VI-000001; TYCID=e3f429d070c111ea9b344387b858cb90; undefined=e3f429d070c111ea9b344387b858cb90; ssuid=1985084156; _ga=GA1.2.1642559413.1585378866; tyc-user-phone=%255B%252218813937194%2522%255D; RTYCID=e1636f40d6064f71b74b217a016406e0; CT_TYCID=9aa8c1bfea954c67a8563e3dcb2a5f6c; aliyungf_tc=AQAAAGVjvV+OLAsAlenseNneKkKX8A2V; csrfToken=nivcGavwxw62c6kPE7iuZNa5; bannerFlag=false; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1585380066,1585530820; _gid=GA1.2.1249723819.1585530820; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522schoolGid%2522%253A%2522%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgxMzkzNzE5NCIsImlhdCI6MTU4NTUzMDg4MSwiZXhwIjoxNjE3MDY2ODgxfQ.35napIxHZfdaTOvtQAuSEY95RM1T7eVRTwEQLkpEIHIo4HZ_ncdsNxIZAZ1eg7fAvUClkCm3B1mqF9LR_2Hpxg%2522%252C%2522schoolAuthStatus%2522%253A%25222%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522companyAuthStatus%2522%253A%25222%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%259C%25B4%25E6%2581%25A9%25E6%2583%25A0%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522companyGid%2522%253A%2522%2522%252C%2522mobile%2522%253A%252218813937194%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgxMzkzNzE5NCIsImlhdCI6MTU4NTUzMDg4MSwiZXhwIjoxNjE3MDY2ODgxfQ.35napIxHZfdaTOvtQAuSEY95RM1T7eVRTwEQLkpEIHIo4HZ_ncdsNxIZAZ1eg7fAvUClkCm3B1mqF9LR_2Hpxg; token=637e1b968bcd46fb813c02ab8f65741e; _utm=4584c071e33a4ae8aead576a337b6096; cloud_token=132a3ba1047647cd91d655f66b5939cd; cloud_utm=3e80c7a8dfc141b3957d8525eac82cc9; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1585539303',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        df = pd.read_excel("E:\\code_storages\\tutorial\\tutorial\\data\\company_data.xls", encoding="utf-8")
        self.company_list = []
        for item in zip(df["id"], df["name"]):
            if not item[1]:
                break
            self.company_list.append({
                "id": item[0],
                "name": item[1],
            })

    def get_add(self):
        with open("E:\\code_storages\\tutorial\\tutorial\\data\\crawl_result.csv", "w", encoding="utf-8-sig", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["id", "name", "name1", "address1"])

            test_num = 0

            for item in self.company_list:
                name_1, address_1 = self.req_url(item["name"])
                csv_writer.writerow([
                    item["id"],
                    item["name"],
                    name_1,
                    address_1,
                ])
                print(f'{item["name"]} 爬取完成')

                # test_num += 1
                # if test_num == 10:
                #     break

    def req_url(self, company):
        MY_USER_AGENT = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]
        agent = random.choice(MY_USER_AGENT)

        self.header["User_Agent"] = agent

        req_url = "https://www.tianyancha.com/search?key=" + company
        name_1 = ""
        address_1 = ""

        try:
            res_list = self.tianyancha_session.get(url=req_url, timeout=6, headers=self.header)
            res_list.encoding = 'utf-8'
            res_list_text = res_list.text
            total_page_search = re.compile(r"""<div class="header"><a class="name  "
             tyc-event-click tyc-event-ch="CompanySearch.Company"
             href="(.*?)" target='_blank'""")

            result_list = total_page_search.search(res_list_text)
            company_item_url = result_list.group(1)
            if company_item_url:
                info_result = self.tianyancha_session.get(url=company_item_url, timeout=6, headers=self.header)
                info_result.encoding = 'utf-8'
                info_result_text = info_result.text

                name_search = re.compile(r"""<div class="header"><h1 class="name">(.*?)</h1>""")
                name_result = name_search.search(info_result_text)
                name_1 = name_result.group(1)

                address_search = re.compile(r"""<span class="label">地址：</span><div style='max-height:16px;' class="auto-folder" auto-folder="16"
     folder-type='custom'
><div>(.*?)</div>""")
                address_result = address_search.search(info_result_text)
                address_1 = address_result.group(1)

                time.sleep(2)

            else:
                print(f"{req_url} 请求失败 原因：无匹配结果")

        except Exception as error:
            print(f"{req_url} 请求失败 原因：{error}")

        return name_1, address_1


if __name__ == "__main__":
    tianyancha = TianyanchaHandle()
    tianyancha.get_add()

