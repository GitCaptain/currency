#!/usr/bin/env python3
# encoding: utf-8

import urllib.request as req
import tkinter as tk
from bs4 import BeautifulSoup as parse
import re


# константы
WIDTH = "320"
HEIGHT = "240"


def GetData():
    """
    Функция парсит сайт банка России (www.cbr.ru) и возвращает кортеж строк
    (текущая дата, текущая цена доллара, текущая цена евро,
    следующая дата, ожидаемая цена доллара, ожидаемая цена евро).
    Документация по beautiful soup:
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree
    """

    # Получаем данные
    cbr = req.urlopen("http://www.cbr.ru/").read().decode("utf-8")
    Data = parse(cbr, 'html.parser')
    CurUSDnEUR = Data.find_all('td', {"class": "weak"})
    CurUSD, CurEUR = CurUSDnEUR[0].get_text(), CurUSDnEUR[1].get_text()
    NextUSDnEUR = Data.find_all('div', {"class": "w_data_wrap"})[:2]
    NextUSD, NextEUR = NextUSDnEUR[0].get_text(), NextUSDnEUR[1].get_text()
    pattern = re.compile("\/currency_base\/daily\.aspx\?date_req=\d{2}\.\d{2}\.\d{4}")
    Date = Data.find_all('a', {"href": pattern})
    CurDate, NextDate = Date[0].get_text(), Date[1].get_text()

    # Обрезаеем копейки до сотых
    CurUSD = CurUSD[:len(CurUSD)-2]
    CurEUR = CurEUR[:len(CurEUR)-2]
    NextUSD = NextUSD[:len(NextUSD)-2]
    NextEUR = NextEUR[:len(NextEUR)-2]

    return (CurDate, CurUSD, CurEUR, NextDate, NextUSD, NextEUR)


def setData(event):

    Data = GetData()
    CurDate['text'] = Data[0]
    CurUSD['text'] = Data[1]
    CurEUR['text'] = Data[2]
    NextDate['text'] = Data[3]
    NextUSD['text'] = Data[4]
    NextEUR['text'] = Data[5]
    print("here")


root = tk.Tk()
root.title("Курс валют")
root.geometry(WIDTH+'x'+HEIGHT)

CurDate = tk.Label(root, text = "Обновите данные чтобы начать")
CurDate.grid(row = 0, rowspan = 1, column = 0, columnspan = 2)

NextDate = tk.Label(root, text = "")
NextDate.grid(row = 0, rowspan = 1, column = 2, columnspan = 1)

USDtxt = tk.Label(root, text = "USD($)")
USDtxt.grid(row = 1, rowspan = 1, column = 0, columnspan = 1)

CurUSD = tk.Label(root, text = "")
CurUSD.grid(row = 1, rowspan = 1, column = 1, columnspan = 1)

NextUSD = tk.Label(root, text = "")
NextUSD.grid(row = 1, rowspan = 1, column = 2, columnspan = 1)

EURtxt = tk.Label(root, text = "EUR(€)")
EURtxt.grid(row = 2, rowspan = 1, column = 0, columnspan = 1)

CurEUR = tk.Label(root, text = "")
CurEUR.grid(row = 2, rowspan = 1, column = 1, columnspan = 1)

NextEUR = tk.Label(root, text = "")
NextEUR.grid(row = 2, rowspan = 1, column = 2, columnspan = 1)

refreshButton = tk.Button(root, text=" Обновить данные ")#, width = int(WIDTH))
refreshButton.bind("<Button-1>", setData)
refreshButton.grid( row = 3, rowspan = 1, columnspan = 3)

root.mainloop()
