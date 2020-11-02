import tkinter
from tkinter import filedialog
from tkinter import *
import threading
import time
# import backtest
import livePurpose


class MainFunc:
    def __init__(self, master):
        self.master = master
        self.mainFrame = Frame(self.master)
        self.mainFrame.place(relx = 0.5, rely = 0.4, anchor = CENTER)
        self.config()
        self.startButton()

    def config(self):
        firstrow = LabelFrame(self.mainFrame, text = 'Please select the configuration file', borderwidth = 0, highlightthickness = 0, font = 'Times 16')
        firstrow.grid(row = 0, column = 0)
        self.confFile = StringVar()                  #***************************** config file
        self.confFile.set('D:/dev/pstockbotB/betterMethod/trash/config.txt')# comment out at the end
        confField = Entry(firstrow, textvariable=self.confFile, font = 'Times 14')
        confField.update()
        confField.focus_set()
        confField.pack(side = "left", padx = (0,10), pady = (0,2), ipadx = 100, ipady = 4)
        def configSelector():
            filename = filedialog.askopenfilename(parent = firstrow, title = 'Please select the configuration file')
            self.confFile.set(filename)
        confButton = Button(firstrow, text = 'Open', command = configSelector, font = 'Times 14')
        confButton.pack(side = "right", padx = 6, pady = (0,2), ipadx = 15)

    def startButton(self):
        startButton = Button(self.mainFrame, text = 'Start', command = self.startLiveGUI, font = 'Times 16', fg = "red")
        startButton.grid(row = 1, column = 0, pady = 20, ipadx = 35, ipady = 2)

    def startLiveGUI(self):
        print('working on it')
        # try:
        faCredentials = self.getConfFileV()
        if len(faCredentials) > 0:
            lp = livePurpose.LivePurpose(self.master, faCredentials)
            self.mainFrame.place_forget()
        else:
            raise Exception('invalid config file')
        # except Exception:
        #     varifyConfig = Label(self.mainFrame, text = 'Please select a valid config file', font = 'Times 14', fg = 'red')
        #     varifyConfig.grid(row = 2, column = 0)

    def getConfFileV(self):
        with open(self.confFile.get(), 'r', encoding="UTF-8") as f:
            content = f.readlines()
        faCredentials = {}
        for i in content:
            i1 = i.strip()
            i2 = i1.split('==>')
            i3 = i2[0].strip()
            i4 = i2[1].strip()
            faCredentials[i3] = i4
        return faCredentials

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("1032x700+300+50")
    # root.resizable(False, False)
    p1 = PhotoImage(file = 'logo.png')
    root.iconphoto(False, p1)
    root.title("stock bot")
    # root.configure(background='black')
    m = MainFunc(root)




    root.mainloop()