import tkinter
from tkinter import *
# from tkinter import ttk
import threading
import time
import requests
from datetime import datetime, timedelta

class LivePurpose:
    def __init__(self, master, confFile):
        self.master = master
        self.confFile = confFile
        self.liveFrame = Frame(self.master)
        self.liveFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        self.tickerV = StringVar()
        self.priceV = StringVar()
        self.amountV = StringVar()
        self.profitV = StringVar()

        self.LiquidationAndCash()
        self.tableWithScalp()
        self.currentOrders()
        self.buyOrder()
    
    def LiquidationAndCash(self):
        liquidCash = Frame(self.liveFrame)
        liquidCash.grid(row = 0, column = 0, columnspan = 3)
        self.netLiquidation = StringVar()
        self.netLiquidation.set('598009090.50')
        LiquidationTitle = Label(liquidCash, text = 'Net Liquidation Value:', fg = '#15427d', font = 'Times 14')
        LiquidationTitle.grid(row = 0, column = 0)
        Liquidation = Label(liquidCash, text = self.netLiquidation.get(), fg = '#21a343', font = 'Times 14')
        Liquidation.grid(row = 0, column = 1)
        spaceIn = Label(liquidCash, text = '                  ', fg = '#15427d', font = 'Times 14')
        spaceIn.grid(row = 0, column = 2)
        self.netCash = StringVar()
        self.netCash.set('$100000.19')
        cashValueTitle = Label(liquidCash, text = 'Cash:', fg = '#15427d', font = 'Times 14')
        cashValueTitle.grid(row = 0, column = 3)
        cashValue = Label(liquidCash, text = self.netCash.get(), fg = '#21a343', font = 'Times 14')
        cashValue.grid(row = 0, column = 4)
    
    def tableWithScalp(self):
        tableScalp = Frame(self.liveFrame)
        tableScalp.grid(row = 1, column = 0, columnspan = 3)
        tableArea = Canvas(tableScalp, width = 1000, height = 365, highlightthickness=0) #bg = '#eb4034', 
        tableArea.pack(side=LEFT, expand=True, fill=BOTH, pady = 5)
        yScrollBar = Scrollbar(tableScalp, orient = VERTICAL)
        yScrollBar.pack(side=RIGHT, fill=Y, padx = (0,10))
        yScrollBar.config(command=tableArea.yview)
        tableArea.config(yscrollcommand=yScrollBar.set)
        tableArea.bind('<Configure>', lambda e: tableArea.configure(scrollregion = tableArea.bbox("all")))
        tableFrame = Frame(tableArea)
        tableArea.create_window((0, 0), window = tableFrame, anchor = 'nw')

        tickerH = Entry(tableFrame, font = 'Times 16 bold', width=10)
        tickerH.insert(END, '  Ticker')
        tickerH.config(state = 'disabled')
        tickerH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#5236e0'})
        tickerH.grid(row = 0, column = 0, ipady = 8)
        cPriceH = Entry(tableFrame, font = 'Times 16 bold', width=13)
        cPriceH.insert(END, '  Current Price')
        cPriceH.config(state = 'disabled')
        cPriceH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#5236e0'})
        cPriceH.grid(row = 0, column = 1, ipady = 8)
        tbpH = Entry(tableFrame, font = 'Times 16 bold', width=16)
        tbpH.insert(END, '  Target Buy Price')
        tbpH.config(state = 'disabled')
        tbpH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#5236e0'})
        tbpH.grid(row = 0, column = 2, ipady = 8)
        addRadioH = Label(tableFrame, text = '  Add', font = 'Times 16 bold', fg = '#5236e0', width = 4)
        addRadioH.grid(row = 0, column = 3, ipady = 8, padx = 3)
        self.addRV = IntVar()

        spaceLabel = Label(tableFrame, text = '  ')
        spaceLabel.grid(row = 0, column = 4)

        self.sEnableDisable = IntVar()
        self.sEnableDisable.set(1)
        sEnable = Radiobutton(tableFrame, text='Enable', font = 'Times 16', variable = self.sEnableDisable, value = 1, command = self.populateBuy)
        sEnable.grid(row = 0, column = 5, columnspan = 4, pady = 10, padx = 10)
        sDisable = Radiobutton(tableFrame, text='Disable', font = 'Times 16', variable = self.sEnableDisable, value = 2, command = self.populateBuy)
        sDisable.grid(row = 0, column = 9, columnspan = 4, pady = 10, padx = 10)
        for tn in range(1, 45):
            self.tableRows(tableFrame, tn)

    def currentOrders(self):
        mainCurrentO = Frame(self.liveFrame)#, bg = '#c42173'
        mainCurrentO.grid(row = 2, column = 1, columnspan = 2)
        labelH = Label(mainCurrentO, text = 'Current Orders', font = 'Times 18 bold', fg = '#5236e0')
        labelH.grid(row = 0, column = 0, pady = 3)

        currentO = Frame(mainCurrentO)
        currentO.grid(row = 1, column = 0)
        buyArea = Canvas(currentO, width = 590, height = 190, highlightthickness=0)#, bg = '#a830f2'
        buyArea.pack(side=LEFT,expand=True)
        yScrollBar = Scrollbar(currentO, orient = VERTICAL)
        yScrollBar.pack(side=RIGHT, fill=Y, padx = (0,10))
        yScrollBar.config(command=buyArea.yview)
        buyArea.config(yscrollcommand=yScrollBar.set)
        buyArea.bind('<Configure>', lambda e: buyArea.configure(scrollregion = buyArea.bbox("all")))
        fForExisting = Frame(buyArea)
        buyArea.create_window((0, 0), window = fForExisting, anchor = 'nw')

        cancelOrder = Button(mainCurrentO, text = 'Cancel All Open Orders', font = 'Times 16')
        cancelOrder.grid(row = 2, column = 0, pady = (15,7), padx = 5)
        exOrders = ['Buy', 'Sell', 'Buy', 'Sell', 'Sell', 'Buy', 'Buy', 'Sell',]
        for cn in range(len(exOrders)):
            if exOrders[cn] == 'Sell':
                self.cSellO(fForExisting, cn)
            elif exOrders[cn] == 'Buy':
                self.cBuyO(fForExisting, cn)

    def cBuyO(self, fForExisting, cn):
        buyLabel = Label(fForExisting, text = 'Buy', width = 6, font = 'Times 14', fg = '#5236e0')
        buyLabel.grid(row = cn, column = 0, padx = (15,5), pady = 3)
        tickerLabel = Label(fForExisting, text = 'Ticker'+str(cn), width = 9, font = 'Times 14', fg = '#5236e0')
        tickerLabel.grid(row = cn, column = 1, padx = 5, pady = 3)
        priceLabel = Label(fForExisting, text = 'Price', width = 7, font = 'Times 14', fg = '#5236e0')
        priceLabel.grid(row = cn, column = 2, padx = 5, pady = 3)
        spaceLabel = Label(fForExisting, text = '     ')
        spaceLabel.grid(row = cn, column = 3, columnspan = 2, pady = 2, padx = (20,5))
        orderPrice = Label(fForExisting, text = 'price'+str(cn), font = 'Times 14', width=12)
        orderPrice.grid(row = cn, column = 5, padx = 5, pady = 1, ipady = 2)
        spaceLabel = Label(fForExisting, text = '    ')
        spaceLabel.grid(row = cn, column = 6, pady = 2, padx = (20,5))

        cancelOrderV = IntVar()
        cancelOrder = Checkbutton(fForExisting, text='C', fg = 'red', variable = cancelOrderV,  onvalue = 1, command = self.populateBuy)
        cancelOrder.grid(row = cn, column = 7, pady = 2, padx = (10,20))

    def cSellO(self, fForExisting, cn):
        buyLabel = Label(fForExisting, text = 'Sell', width = 6, font = 'Times 14', fg = '#5236e0')
        buyLabel.grid(row = cn, column = 0, padx = (15,5), pady = 3)
        tickerLabel = Label(fForExisting, text = 'Ticker'+str(cn), width = 9, font = 'Times 14', fg = '#5236e0')
        tickerLabel.grid(row = cn, column = 1, padx = 5, pady = 3)
        priceLabel = Label(fForExisting, text = 'Price', width = 7, font = 'Times 14', fg = '#5236e0')
        priceLabel.grid(row = cn, column = 2, padx = 5, pady = 3)
        sellP = Button(fForExisting, text = '+', font = 'Times 14')
        sellP.grid(row = cn, column = 3, pady = 2, padx = 5)
        sellM = Button(fForExisting, text = '-', font = 'Times 14')
        sellM.grid(row = cn, column = 4, pady = 2, padx = 5)

        orderPrice = Entry(fForExisting, font = 'Times 14', width=12)
        orderPrice.insert(END, 'price'+str(cn))
        orderPrice.grid(row = cn, column = 5, padx = 5, pady = 1, ipady = 2)
        
        modifyOrderV = IntVar()
        modifyOrder = Checkbutton(fForExisting, text='M', fg = 'blue', variable = modifyOrderV,  onvalue = 1, command = self.populateBuy)
        modifyOrder.grid(row = cn, column = 6, pady = 2, padx = (20,5))

        cancelOrderV = IntVar()
        cancelOrder = Checkbutton(fForExisting, text='C', fg = 'red', variable = cancelOrderV,  onvalue = 1, command = self.populateBuy)
        cancelOrder.grid(row = cn, column = 7, pady = 2, padx = (10,20))
    
    def buyOrder(self):
        buyO = Frame(self.liveFrame)
        buyO.grid(row = 2, column = 0)
        buyOne = Canvas(buyO, width = 350, height = 270, highlightthickness=0)#, bg = '#31f794'
        buyOne.pack(side=LEFT,expand=True,fill=BOTH, pady = 10, padx = 5)
        bFrame = Frame(buyOne)
        buyOne.create_window((0, 0), window = bFrame, anchor = 'nw')
        bTitle = Label(bFrame, text = 'Buy', font = 'Times 18 bold', fg = '#5236e0')
        bTitle.grid(row = 0, column = 1, pady = 5, padx = 5)

        tickerH = Label(bFrame, text = 'Ticker:', font = 'Times 14', fg = '#5236e0')
        tickerH.grid(row = 1, column = 0, pady = 4, padx = 9)
        tickerE = Entry(bFrame, textvariable = self.tickerV, font = 'Times 14', width = 16)
        tickerE.grid(row = 1, column = 1, pady = 4, padx = 6)

        priceH = Label(bFrame, text = 'Price:', font = 'Times 14', fg = '#5236e0')
        priceH.grid(row = 2, column = 0, pady = 4, padx = 8)
        priceE = Entry(bFrame, textvariable = self.priceV, font = 'Times 14', width = 16)
        priceE.grid(row = 2, column = 1, pady = 4, padx = 6)
        priceP = Button(bFrame, text = '+', font = 'Times 14')
        priceP.grid(row = 2, column = 2, pady = 4, padx = 8)
        priceM = Button(bFrame, text = '-', font = 'Times 14')
        priceM.grid(row = 2, column = 3, pady = 4, padx = (8,20))
        
        amountH = Label(bFrame, text = 'Amount:', font = 'Times 14', fg = '#5236e0')
        amountH.grid(row = 3, column = 0, pady = 4, padx = 8)
        amountE = Entry(bFrame, textvariable = self.amountV, font = 'Times 14', width = 16)
        amountE.grid(row = 3, column = 1, pady = 4, padx = 6)

        profitH = Label(bFrame, text = 'Profit %:', font = 'Times 14', fg = '#5236e0')
        profitH.grid(row = 4, column = 0, pady = 4, padx = 8)
        profitE = Entry(bFrame, textvariable = self.profitV, font = 'Times 14', width = 16)
        profitE.grid(row = 4, column = 1, pady = 4, padx = 6)
        profitP = Button(bFrame, text = '+', font = 'Times 14')
        profitP.grid(row = 4, column = 2, pady = 4, padx = 8)
        profitM = Button(bFrame, text = '-', font = 'Times 14')
        profitM.grid(row = 4, column = 3, pady = 4, padx = (8,20))

        placeOrder = Button(bFrame, text = 'Place Order', font = 'Times 16')
        placeOrder.grid(row = 5, column = 1, pady = 12, padx = 5)

    def tableRows(self, tableFrame, tn):
        tickerV = StringVar()
        tickerV.set('Ticker'+str(tn))
        tickerH = Entry(tableFrame, font = 'Times 14', width=12)
        tickerH.insert(END, tickerV.get())
        tickerH.config(state = 'disabled')
        tickerH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#080324'})
        tickerH.grid(row = tn, column = 0, pady = 4, padx = 5, ipady = 3)
        cPriceH = Entry(tableFrame, font = 'Times 14', width=16)
        cPriceH.insert(END, '  Current Price'+str(tn))
        cPriceH.config(state = 'disabled')
        cPriceH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#080324'})
        cPriceH.grid(row = tn, column = 1, pady = 4, padx = 5, ipady = 3)
        tbpH = Entry(tableFrame, font = 'Times 14', width=20)
        tbpH.insert(END, '  Target Buy Price'+str(tn))
        tbpH.config(state = 'disabled')
        tbpH.configure({"disabledbackground": '#f0f5ff', "disabledforeground": '#080324'})
        tbpH.grid(row = tn, column = 2, pady = 4, padx = 5, ipady = 3)

        addRadio = Radiobutton(tableFrame, text=tn, fg = 'blue', variable = self.addRV, value = tn, command = self.populateBuy)
        addRadio.grid(row = tn, column = 3, pady = 4, padx = 5)

        #Scalp
        lsButton = Button(tableFrame, text = 'Scalp', font = 'Times 14', fg = '#115c1f')
        lsButton.grid(row = tn, column = 5,pady = 4, padx = 5)
        lsMulti = Label(tableFrame, text = 'X', font = 'Times 14')
        lsMulti.grid(row = tn, column = 6, pady = 4, padx = 5)
        lsEntryV = IntVar()
        lsEntryV.set(1)
        lsEntry = Entry(tableFrame, textvariable = lsEntryV, width=2, font = 'Times 14', fg = '#080324')
        lsEntry.grid(row = tn, column = 7, pady = 4, padx = 5)
        lsButton = Button(tableFrame, text = '+', font = 'Times 14', fg = '#080324')
        lsButton.grid(row = tn, column = 8, pady = 4, padx = 5)
        lsButton = Button(tableFrame, text = '-', font = 'Times 14', fg = '#080324')
        lsButton.grid(row = tn, column = 9, pady = 4, padx = 5)
        spaceLabel = Label(tableFrame, text = ' ')
        spaceLabel.grid(row = tn, column = 10)
        ssButton = Button(tableFrame, text = 'Short Scalp', font = 'Times 14', fg = '#b53333')
        ssButton.grid(row = tn, column = 11, pady = 4, padx = 5)
        ssMulti = Label(tableFrame, text = 'X', font = 'Times 14', fg = '#080324')
        ssMulti.grid(row = tn, column = 12, pady = 4, padx = 5)
        ssEntryV = IntVar()
        ssEntryV.set(1)
        ssEntry = Entry(tableFrame, textvariable = ssEntryV, width=2, font = 'Times 14', fg = '#080324')
        ssEntry.grid(row = tn, column = 13, pady = 4, padx = 5)
        ssButton = Button(tableFrame, text = '+', font = 'Times 14', fg = '#080324')
        ssButton.grid(row = tn, column = 14, pady = 4, padx = 5)
        ssButton = Button(tableFrame, text = '-', font = 'Times 14', fg = '#080324')
        ssButton.grid(row = tn, column = 15, pady = 4, padx = 5)

    def populateBuy(self):
        print('selected')
        self.tickerV.set('hi')


















    def stockAndF(self):
        thridRowA = LabelFrame(self.liveFrame, text = "symbol pair", borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        thridRowA.grid(row = 0, column = 0)
        self.stocksEntered = StringVar(None)             #***************************** stock symbols
        stocksField = Entry(thridRowA, textvariable=self.stocksEntered, font = 'Times 14')
        stocksField.update()
        stocksField.pack(padx = (9,10), pady = (1,2), ipadx = 1)

        thridRowB = LabelFrame(self.liveFrame, text = 'frequency', borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        thridRowB.grid(row = 0, column = 1)
        frequencyList = ["1 minute", "5 minute", "10 minute", "15 minute", "30 minute", "1 day"] #, "1 hour", "2 hour", "4 hour"
        self.ftClicked = StringVar()                     #***************************** security type
        self.ftClicked.set("1 minute")
        ftOptions = OptionMenu(thridRowB, self.ftClicked, *frequencyList)
        ftOptions.config(width = 10) #width = 10
        ftOptions.config(font = 'Times 14')
        ftOptionsf = self.master.nametowidget(ftOptions.menuname)
        ftOptionsf.config(font= 'Times 14') # set the drop down menu font
        ftOptions.pack(padx = 20, pady = (0,2), ipadx = 14)

    def timeAndMA(self):
        fourthRowA = LabelFrame(self.liveFrame, text = 'start time (hh:mm)', borderwidth = 0, highlightthickness = 0,font = 'Times 16')
        fourthRowA.grid(row = 1, column = 0)
        self.startTimeV = StringVar(None)                     #***************************** start time
        self.startTimeV.set('09:30')
        startTime = Entry(fourthRowA, textvariable=self.startTimeV, font = 'Times 14')
        startTime.update()
        startTime.pack(padx = (9,8), pady = (1,2), ipadx = 2)
        fourthRowB = LabelFrame(self.liveFrame, text = 'moving average', borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        fourthRowB.grid(row = 1, column = 1)
        self.movingAverageV = StringVar(None)                     #*****************************investment
        movingAverage = Entry(fourthRowB, textvariable=self.movingAverageV, font = 'Times 14')
        movingAverage.update()
        movingAverage.pack(padx = (8,7), pady = (1,2), ipadx = 2)

    def peAndPx(self):
        eighthRowA = LabelFrame(self.liveFrame, text = 'delta percent entry', borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        eighthRowA.grid(row = 2, column = 0)
        self.dpEntryV = StringVar(None)                     #***************************** delta percent entry
        dpEntry = Entry(eighthRowA, textvariable=self.dpEntryV, font = 'Times 14')
        dpEntry.update()
        dpEntry.pack(padx = (9,8), pady = (3,7), ipadx = 2)
        eighthRowB = LabelFrame(self.liveFrame, text = 'delta percent exit', borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        eighthRowB.grid(row = 2, column = 1)
        self.dpExitV = StringVar(None)                     #***************************** delta percent exit
        dpExit = Entry(eighthRowB, textvariable=self.dpExitV, font = 'Times 14')
        dpExit.update()
        dpExit.pack(padx = (8,7), pady = (3,7), ipadx = 2)

    def AddAndsubmit(self):
        tenthRowA = LabelFrame(self.liveFrame, borderwidth = 0, highlightthickness = 0)
        tenthRowA.grid(row = 3, column = 0)
        self.addButton = Button(tenthRowA, text = 'Add', bg = '#C2FAB6',command = self.inputThreading, activebackground = "blue", font = 'Times 16')
        self.addButton.pack(padx = (1,1), pady = (9,1), ipadx = 30)
        tenthRowB = LabelFrame(self.liveFrame, borderwidth = 0, highlightthickness = 0)
        tenthRowB.grid(row = 3, column = 1)
        self.enterButton = Button(tenthRowB, text = 'Start', bg = '#69E64E',command = self.inputThreading, activebackground = "red", font = 'Times 16')
        self.enterButton.pack(padx = (1,1), pady = (9,1), ipadx = 45)
    
    def statusWidget(self):
        eleventhRow = LabelFrame(self.liveFrame, text = 'status...', font = 'Times 16')
        eleventhRow.grid(row = 4, column = 0, columnspan = 2)
        statusTextArea = Text(eleventhRow, width = 42, height = 13)
        statusTextArea.config(font=("Times", 14))
        ScrollBar = Scrollbar(eleventhRow)
        ScrollBar.config(command=statusTextArea.yview)
        statusTextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        statusTextArea.pack(expand=YES, fill=BOTH, padx = (2,3), pady = (5, 7))
        statusTextArea.insert(tkinter.END, '>add Pairs:\n')
        statusTextArea.config(state='disabled')

    def updateStatus(self, updatet):
        updatef = '{}\n'.format(updatet)
        statusTextArea.config(state='normal')
        statusTextArea.insert(tkinter.END, updatef)
        statusTextArea.see("end")
        statusTextArea.config(state='disabled')


    def inputThreading(self):
        # firstThread = threading.Thread(target = self.dataAndC)
        # firstThread.daemon = True
        # firstThread.start()
        print("I am inside")