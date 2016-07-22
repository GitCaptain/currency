#!/usr/bin/env python3

import urllib.request as req
import tkinter as tk


def GetData():
    # легче забрать данные отсюда http://www.cbr.ru/
    # help(req)
    cbr = req.urlopen("http://www.cbr.ru/").read().decode("utf-8")
    dataStart = cbr.find("Курсы валют")
    Data = cbr[dataStart+20:]
    dataStart = Data.find("<table>")
    dataEnd = Data.find("</table>")
    Data = Data[dataStart:dataEnd]

    Data = Data.split("<tr>")[1:]

    dataStart = Data[0].find("date_req") + 9
    dataEnd = dataStart + 10
    Date = Data[0][dataStart:dataEnd]

    dataStart = Data[1].find("руб") + 16
    Data[1] = Data[1][dataStart:]
    dataEnd = Data[1].find("</td>")
    USD = Data[1][0:dataEnd]

    dataStart = Data[2].find("руб") + 16
    Data[2] = Data[2][dataStart:]
    dataEnd = Data[2].find("</td>")
    EUR = Data[2][0:dataEnd]

    return (Date, USD, EUR)


def setData(event):
    global info
    info["text"] = "По состоянию на {0}\nДоллар: {1} руб. \nЕвро: {2} руб.".format(*GetData())
    info.pack()


def setWindow():
    root = tk.Tk()
    refreshButton = tk.Button(root, text=" Обновить данные ")
    refreshButton.bind("<Button-1>", setData)
    refreshButton.pack()
    return root

root = setWindow()
info = tk.Label(root)
root.mainloop()
