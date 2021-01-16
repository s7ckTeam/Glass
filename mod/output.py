# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   output.py
@Time  :   2020/12/27 05:55:34
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import os
import csv
import time
import json
import base64
import xlsxwriter
from config.config import Version
from config.data import Paths, OutInfos, logger, confs


class output():
    def __init__(self):
        self.nowTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.filename = self.nowTime + ".txt"
        self.filename_html = self.nowTime + ".html"
        self.filename_json = self.nowTime + ".json"
        self.filename_xls = self.nowTime + ".xls"
        self.filename_csv = self.nowTime + ".csv"
        self.path = os.path.join(Paths.output, self.filename)
        self.path_html = os.path.join(Paths.output, self.filename_html)
        self.path_json = os.path.join(Paths.output, self.filename_json)
        self.path_xls = os.path.join(Paths.output, self.filename_xls)
        self.path_csv = os.path.join(Paths.output, self.filename_csv)

    def outTxt(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            for key in OutInfos:
                f.write("{0} {1}\n".format(key, OutInfos[key]))
        print()
        logger.info("文件输出路径为：{0}".format(self.path))

    def outHtml(self):
        num = 0
        full = []
        reportTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Glass_html = "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KICA8aGVhZD4KICAgIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICAgIDxtZXRhIGh0dHAtZXF1aXY9IlgtVUEtQ29tcGF0aWJsZSIgY29udGVudD0iSUU9ZWRnZSI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEiPgoKICAgIDx0aXRsZT5HbGFzc+aJq+aPj+aKpeWRijwvdGl0bGU+CgogICAgPG1ldGEgbmFtZT0iZGVzY3JpcHRpb24iIGNvbnRlbnQ9IlNvdXJjZSBjb2RlIGdlbmVyYXRlZCB1c2luZyBsYXlvdXRpdC5jb20iPgogICAgPG1ldGEgbmFtZT0iYXV0aG9yIiBjb250ZW50PSJMYXlvdXRJdCEiPgoKICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cDovL2Nkbi5ib290Y3NzLmNvbS9ib290c3RyYXAvMy4zLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIj4gCiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHA6Ly9jZG4uYm9vdGNzcy5jb20vZm9udC1hd2Vzb21lLzQuMi4wL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyI+IAoKICA8L2hlYWQ+CiAgPGJvZHk+CgogICAgPGRpdiBjbGFzcz0iY29udGFpbmVyLWZsdWlkIj4KCTxkaXYgY2xhc3M9InJvdyI+CgkJPGRpdiBjbGFzcz0iY29sLW1kLTEyIj4KCQkJPGRpdiBjbGFzcz0icGFnZS1oZWFkZXIiPgoJCQkJPGgxPgoJCQkJCUdsYXNz5omr5o+P5oql5ZGKICA8c21hbGw+dnt7dmVyc2lvbn19PC9zbWFsbD4KCQkJCTwvaDE+CgkJCTwvZGl2PiA8c3BhbiBjbGFzcz0ibGFiZWwgbGFiZWwtcHJpbWFyeSI+55Sf5oiQ5pe26Ze077yae3tyZXBvcnRUaW1lfX08L3NwYW4+CiAgICAgICAgICAgIDwvYnI+PC9icj4KCQkJPHRhYmxlIGNsYXNzPSJ0YWJsZSI+CgkJCQk8dGhlYWQ+CgkJCQkJPHRyPgogICAgPHRoPiM8L3RoPgogICAgPHRoPlVybDwvdGg+CiAgICA8dGg+VGl0bGU8L3RoPgogICAgPHRoPkNtczwvdGg+CiAgICA8dGg+U2VydmVyPC90aD4KICAgIDx0aD5TdGF0dXM8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KCQkJCTwvdGhlYWQ+CiAgICAgICAgICAgICAgICAKCQkJCTx0Ym9keT4KICAgICAgICAgICAgICAgICAgICB7e2NvbnRlbnR9fQoJCQkJPC90Ym9keT4KCQkJPC90YWJsZT4KCQk8L2Rpdj4KCTwvZGl2Pgo8L2Rpdj4KICA8L2JvZHk+CjwvaHRtbD4="
        Glass_html = base64.b64decode(Glass_html).decode('utf-8')
        Glass_html = Glass_html.replace("{{reportTime}}", reportTime)
        Glass_html = Glass_html.replace("{{version}}", Version)
        for key in OutInfos:
            url = key
            num = num + 1
            infos = OutInfos[key]
            cms = infos[0]
            server = infos[1]
            status = infos[2]
            title = infos[3]
            tr = "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                num, url, title, cms, server, status)
            full.append(tr)

        Glass_html = Glass_html.replace("{{content}}", ''.join(full))
        with open(self.path_html, 'w', encoding='utf-8') as f:
            f.write(Glass_html)
        print()
        logger.info("文件输出路径为：{0}".format(self.path_html))

    def outJson(self):
        jsonDatas = {}
        for key in OutInfos:
            url = key
            infos = OutInfos[key]
            cms = infos[0]
            server = infos[1]
            status = infos[2]
            title = infos[3]
            jsonDatas[url] = {
                "Title": title,
                "Cms": cms,
                "Server": server,
                "Status": status,
            }
        json_data = json.dumps(jsonDatas, sort_keys=True,
                               indent=4, ensure_ascii=False)
        with open(self.path_json, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print()
        logger.info("文件输出路径为：{0}".format(self.path_json))

    def outXls(self):
        with xlsxwriter.Workbook(self.path_xls) as workbook:
            worksheet = workbook.add_worksheet('Glass扫描报告')
            bold = workbook.add_format({"bold": True})

            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.set_column('E:E', 30)

            worksheet.write('A1', 'Url', bold)
            worksheet.write('B1', 'Title', bold)
            worksheet.write('C1', 'Cms', bold)
            worksheet.write('D1', 'Server', bold)
            worksheet.write('E1', 'Status', bold)

            row = 1
            col = 0

            for key in OutInfos:
                url = key
                infos = OutInfos[key]
                cms = infos[0]
                server = infos[1]
                status = infos[2]
                title = infos[3]
                worksheet.write(row, col, url)
                worksheet.write(row, col+1, title)
                worksheet.write(row, col+2, cms)
                worksheet.write(row, col+3, server)
                worksheet.write(row, col+4, status)
                row += 1

        print()
        logger.info("文件输出路径为：{0}".format(self.path_xls))

    def outCsv(self):
        csv_table_names = ["Url", "Title", "Cms", "Server", "Status"]
        csv_table_values = []
        for key in OutInfos:
            url = key
            infos = OutInfos[key]
            cms = infos[0]
            server = infos[1]
            status = infos[2]
            title = infos[3]
            csv_table_values.append((url, title, cms, server, status))
        csv_table_name = sorted(set(csv_table_names),
                                key=csv_table_names.index)
        with open(self.path_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_table_name)
            writer.writerows(csv_table_values)

        print()
        logger.info("文件输出路径为：{0}".format(self.path_csv))


def outMain(types):
    start = output()
    if not os.path.isdir(Paths.output):
        os.mkdir(Paths.output)

    if types == "txt":
        start.outTxt()
    if types == "html":
        start.outHtml()
    if types == "json":
        start.outJson()
    if types == "xls":
        start.outXls()
    if types == "csv":
        start.outCsv()
