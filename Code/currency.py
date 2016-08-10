#!/usr/bin/env python3

import urllib.request as req
import tkinter as tk
from bs4 import BeautifulSoup as parse
import re


def GetData():
    # легче забрать данные отсюда http://www.cbr.ru/
    # help(req)
    cbr = req.urlopen("http://www.cbr.ru/").read().decode("utf-8")
    Data = parse(cbr, 'html.parser')
    CurUSDnEUR = Data.find_all('td', {"class": "weak"})
    CurUSD, CurEUR = CurUSDnEUR[0].get_text(), CurUSDnEUR[1].get_text()
    Date = Data.find_all('a', {"href": re.compile("\/currency_base\/daily\.aspx\?date_req=\d{2}\.\d{2}\.\d{4}")})
    CurDate, NextDate = Date[0].get_text(), Date[1].get_text()
    return (CurDate, CurUSD, CurEUR)


def setData(event):
    global info
    info["text"] = "По состоянию на {0}\nДоллар: {1} \nЕвро: {2}".format(*GetData())
    info.pack()

root = tk.Tk()
refreshButton = tk.Button(root, text=" Обновить данные ")
refreshButton.bind("<Button-1>", setData)
refreshButton.pack()
info = tk.Label(root)
root.mainloop()
