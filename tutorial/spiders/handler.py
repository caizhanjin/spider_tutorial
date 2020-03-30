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

