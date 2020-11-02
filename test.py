# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
 
# from functools import partial
 
# try:
#     # Tkinter for Python 2.xx
#     import Tkinter as tk
# except ImportError:
#     # Tkinter for Python 3.xx
#     import tkinter as tk
 
# APP_TITLE = "Srollable Canvas"
# APP_XPOS = 100
# APP_YPOS = 100
# APP_WIDTH = 325
# APP_HEIGHT = 425
 
# NUM_OF_BUTTONS = 20
# BUTTONS = ['Button-{0:02d}'.format(nr) for nr in range(1, NUM_OF_BUTTONS+1)]
 
 
# class Application(tk.Frame):
 
#     def __init__(self, master):
#         self.master = master
#         self.master.protocol("WM_DELETE_WINDOW", self.close)
#         tk.Frame.__init__(self, master)
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
               
#         self.canvas = tk.Canvas(self, bg='steelblue', highlightthickness=0)
#         self.canvas.grid(row=0, column=0, sticky='wesn')
         
#         self.yscrollbar = tk.Scrollbar(self, orient="vertical",
#             width=14, command=self.canvas.yview)
#         self.yscrollbar.grid(row=0, column=1, sticky='ns')
 
#         self.xscrollbar = tk.Scrollbar(self, orient="horizontal",
#             width=14, command=self.canvas.xview)
#         self.xscrollbar.grid(row=1, column=0, sticky='we')
         
#         self.canvas.configure(
#             xscrollcommand=self.xscrollbar.set,
#             yscrollcommand=self.yscrollbar.set)
 
#         self.button_frame = tk.Frame(self.canvas, bg=self.canvas['bg'])
#         self.button_frame.pack()
#         self.canvas.create_window((0,0), window=self.button_frame, anchor="nw")
         
#         for button in BUTTONS:
#             tk.Button(self.button_frame, text=button, highlightthickness=0,
#             command=partial(self.button_callback, button)).pack(padx=4, pady=2)
         
#         self.canvas.bind('<Configure>', self.update)
#         self.bind_mouse_scroll(self.canvas, self.yscroll)
#         self.bind_mouse_scroll(self.xscrollbar, self.xscroll)
#         self.bind_mouse_scroll(self.yscrollbar, self.yscroll)
         
#         self.canvas.focus_set()
         
#     def bind_mouse_scroll(self, parent, mode):
#         #~~ Windows only
#         parent.bind("<MouseWheel>", mode)
#         #~~ Unix only        
#         parent.bind("<Button-4>", mode)
#         parent.bind("<Button-5>", mode)
 
#     def yscroll(self, event):
#         if event.num == 5 or event.delta < 0:
#             self.canvas.yview_scroll(1, "unit")
#         elif event.num == 4 or event.delta > 0:
#             self.canvas.yview_scroll(-1, "unit")
 
#     def xscroll(self, event):
#         if event.num == 5 or event.delta < 0:
#             self.canvas.xview_scroll(1, "unit")
#         elif event.num == 4 or event.delta > 0:
#             self.canvas.xview_scroll(-1, "unit")
 
#     def update(self, event):
#         if self.canvas.bbox('all') != None:
#             region = self.canvas.bbox('all')
#             self.canvas.config(scrollregion=region)
             
#     def button_callback(self, button):
#         print(button)
                       
#     def close(self):
#         print("Application-Shutdown")
#         self.master.destroy()
 
     
# def main():
#     app_win = tk.Tk()
#     app_win.title(APP_TITLE)
#     app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
#     app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))
     
#     app = Application(app_win).pack(fill='both', expand=True)
     
#     app_win.mainloop()
  
  
# if __name__ == '__main__':
#     main()      
# Please also have a look at this page:
# PEP 8 -- Style Guide for Python Code



# try:
#     from tkinter import * 
# except ImportError:
#     from Tkinter import *

# root = Tk()

# height = 5
# width = 5
# for i in range(height): #Rows
#     for j in range(width): #Columns
#         b = Entry(root, text="")
#         b.grid(row=i, column=j)

# mainloop()

from tkinter import *

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)

root = Tk()
var = IntVar()
R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Option 2", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="Option 3", variable=var, value=3,
                  command=sel)
R3.pack( anchor = W)

label = Label(root)
label.pack()
root.mainloop()