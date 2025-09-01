from tkinter import *
from tkinter import ttk
import can
from can_data import *
import time

# from canid import CanId_Lookup

speedoMeter = 0
currentDraw = 0
StateOfCharge = 0

bus = can.interface.Bus(channel='can0', bustype='socketcan')
can_process = CanData()

tk_root = Tk()
tk_root.title("PSR Display")

#Column Definition
tk_root.columnconfigure(0, weight=1)
tk_root.columnconfigure(1, weight=1)

#Row Definition
tk_root.rowconfigure(0, weight=1)
tk_root.rowconfigure(1, weight=1)
tk_root.rowconfigure(2, weight=1)
tk_root.rowconfigure(3, weight=1)
tk_root.rowconfigure(4, weight=1)

def massTextUpdate():
    global SOC_text, speedoMeter, currentDraw_text, can_process
    SOC_text.set(f"Pack: {can_process.packSOC}%")
    speedoMeter_text.set(f"{can_process.motorVelocity}")
    currentDraw_text.set(f"{can_process.motorCurrent}")
    RaisedErrorAndWarning()

def RaisedErrorAndWarning():
    global can_process
    if (can_process.MainCurrentWarning == 1):
        MainCurrentWarning_Label.config(foreground="yellow", relief="raised")
    else:
        MainCurrentWarning_Label.config(foreground="grey", relief="sunken")

    if (can_process.MainOverCurrentError == 1):
        MainOverCurrent_Label.config(foreground="red", relief="raised")
    else:
        MainOverCurrent_Label.config(foreground="grey", relief="sunken")

    if (can_process.MainUnderVoltage == 1):
        MainVoltageLow_Label.config(foreground="red", relief="raised")
    else:
        MainVoltageLow_Label.config(foreground="grey", relief="sunken")

    if (can_process.MainOverVoltage == 1):
        MainVoltageHigh_Label.config(foreground="red", relief="raised")
    else:
        MainVoltageHigh_Label.config(foreground="grey", relief="sunken")

    if (can_process.AuxCurrentWarning == 1):
        AuxCurrentWarning_Label.config(foreground="yellow", relief="raised")
    else:
        AuxCurrentWarning_Label.config(foreground="grey", relief="sunken")

    if (can_process.AuxOverCurrent == 1):
        AuxOverCurrent_Label.config(foreground="red", relief="raised")
    else:
        AuxOverCurrent_Label.config(foreground="grey", relief="sunken")
    
    if (can_process.AuxUnderVoltage == 1):
        AuxVoltageLow_Label.config(foreground="red", relief="raised")
    else:
        AuxVoltageLow_Label.config(foreground="grey", relief="sunken")
    
    if (can_process.AuxOverVoltage == 1):
        AuxVoltageHigh_Label.config(foreground="red", relief="raised")
    else:
        AuxVoltageHigh_Label.config(foreground="grey", relief="sunken")

def CheckCanMessage():
    message = bus.recv(timeout=1)
    if message != None:
        can_process.updateCAN(message.arbitration_id, message.data)
        massTextUpdate()
        tk_root.after(20, CheckCanMessage)
    
def FullScreen():
    tk_root.attributes("-zoomed", True) #Used this for testing, Uncomment it out when finished
    # tk_root.attributes("-fullscreen", True) #Uncomment this for actual scripts

speedoMeter_text = StringVar()
speedoMeter_text.set(f"{speedoMeter}")

currentDraw_text = StringVar()
currentDraw_text.set(f"{currentDraw}")

SOC_text = StringVar()
SOC_text.set(f"Pack: {StateOfCharge}%")

speedoMeter_Title = Label(tk_root, text="VELOCITY (mph)", font=("Arial",40))
currentDraw_Title = Label(tk_root, text="CURRENT (A)", font=("Arial", 40))
speedoMeter_Label = Label(tk_root, textvariable=speedoMeter_text, font=("Arial",35))
currentDraw_Label = Label(tk_root, textvariable=currentDraw_text, font=("Arial",35))

errorwarning_Frame = Frame(tk_root)
errorwarning_Frame.columnconfigure(0, weight=1)
errorwarning_Frame.rowconfigure(0, weight=1)
errorwarning_Frame.rowconfigure(1, weight=1)
errorwarning_Frame.rowconfigure(2, weight=1)

errorwarning_Label = Label(errorwarning_Frame, text="Errors and Warnings", font=("Arial",20))
errorwarning_SOC = Label(errorwarning_Frame, textvariable=SOC_text, font=("Arial",20), foreground="green")
errorwarning_Seperator = ttk.Separator(errorwarning_Frame, orient="horizontal")

Error_Frame = Frame(tk_root)
Error_Frame.columnconfigure(0, weight=1)
Error_Frame.columnconfigure(1, weight=1)
Error_Frame.columnconfigure(2, weight=1)
Error_Frame.columnconfigure(3, weight=1)
Error_Frame.columnconfigure(4, weight=1)
Error_Frame.columnconfigure(5, weight=1)

Error_Frame.rowconfigure(0, weight = 1)
Error_Frame.rowconfigure(1, weight = 1)

MainCurrentWarning_Label = Label(Error_Frame, text="Main Batt High\nCurrent Warning!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
MainOverCurrent_Label    = Label(Error_Frame, text="Main Batt Over\nCurrent Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
MainVoltageLow_Label     = Label(Error_Frame, text="Main Batt Low\nVoltage Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
MainVoltageHigh_Label    = Label(Error_Frame, text="Main Batt Over\nVoltage Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)

AuxCurrentWarning_Label = Label(Error_Frame, text="Aux High\nCurrent Warning!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
AuxOverCurrent_Label    = Label(Error_Frame, text="Aux Over\nCurrent Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
AuxVoltageLow_Label     = Label(Error_Frame, text="Aux Low\nVoltage Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)
AuxVoltageHigh_Label    = Label(Error_Frame, text="Aux Over\nVoltage Error!!!", font=("Arial",20), foreground="grey", relief="sunken", padx=20, pady=20)

speedoMeter_Title.grid(row=0, column=0, sticky="nsew")
currentDraw_Title.grid(row=0, column=1, sticky="nsew")
speedoMeter_Label.grid(row=1, column=0, sticky="nsew")
currentDraw_Label.grid(row=1, column=1, sticky="nsew")

errorwarning_Frame.grid(row=2,column=0, columnspan=2, sticky="nsew")
errorwarning_SOC.grid(row = 0, column = 0)
errorwarning_Label.grid(row=1, column=0)
errorwarning_Seperator.grid(row=2, column=0, padx = 5, sticky="ew")

Error_Frame.grid(row=3, column=0, columnspan=2, rowspan=2,sticky="nsew")

MainCurrentWarning_Label.grid(row=0, column=2)
MainOverCurrent_Label.grid(row=1, column=0)
MainVoltageLow_Label.grid(row = 1, column=1)
MainVoltageHigh_Label.grid(row = 1, column=2)

AuxCurrentWarning_Label.grid(row=0, column=3)
AuxOverCurrent_Label.grid(row=1, column=3)
AuxVoltageLow_Label.grid(row = 1, column=4)
AuxVoltageHigh_Label.grid(row = 1, column=5)

tk_root.after(100, FullScreen)
tk_root.after(200, CheckCanMessage)
tk_root.mainloop()
