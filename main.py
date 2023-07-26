from tkinter import filedialog as fd
import customtkinter

import PyPDF2
import os

folderSelected = False
fileSelected = False
saveNameSelected = False

fileName = ""
folderName = ""
saveName = ""

def pdfToText():
  with open(fileName, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    pdf_text = ""
    
    for page in reader.pages:
      pdf_text += page.extract_text()
        
    file.close()
  
  return pdf_text

def saveText(textToSave):
  target = os.path.join(folderName, f"{saveNameEntry.get()}.txt")
  with open(target, "w") as file:
    file.write(textToSave)
    file.close()

def changeAppearance(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def changeScaling(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

def selectFile():
    try:
        fileTypes = (("PDF files","*.pdf"), ("all files","*.*"))
        global fileName
        fileName = fd.askopenfile(title="Open a file", filetypes=fileTypes).name
        pdfSelectLabel.configure(text=fileName)
        global fileSelected
        fileSelected = True
    except:
       progressLabel.configure(text="An error has occured! Please restart try again")

def selectFolder():
    try:
        global folderName
        folderName = fd.askdirectory()
        outputLabel.configure(text=folderName)
        global folderSelected
        folderSelected = True
    except:
       progressLabel.configure(text="An error has occured! Please try again")

def convert():
    try:
        progressLabel.configure(text="Converting...")
        global folderSelected
        global fileSelected
        global saveNameSelected

        saveNameSelected = saveNameEntry.get() != ""

        if not (folderSelected and fileSelected and saveNameSelected):
            progressLabel.configure(text="Progress: Aborted- Please select a file, folder as well as enter a text file name then retry.")
            return
    
        text = pdfToText()
        saveText(text)
        progressLabel.configure(text="Converted!")
    except:
       progressLabel.configure(text="An error has occured! Please try again")

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")
customtkinter.set_widget_scaling(1)

app = customtkinter.CTk()
app.geometry("920x680")
app.minsize(920, 680)
app.title("PdfToTxt")

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

sidebarFame = customtkinter.CTkFrame(master=app)
sidebarFame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

title = customtkinter.CTkLabel(master=sidebarFame, text="PDF to Text", font=customtkinter.CTkFont(size=20, weight="bold"))
title.grid(row=0, column=0, padx=20, pady=(20, 40))

appearenceLabel = customtkinter.CTkLabel(master=sidebarFame, text="Appearance Mode:")
appearenceOptions = customtkinter.CTkOptionMenu(master=sidebarFame, values=["Light", "Dark", "System"], command=changeAppearance)
appearenceLabel.grid(row=1, column=0)
appearenceOptions.set("Dark")
appearenceOptions.grid(row=2, column=0, pady=(0, 20))

scalingLabel = customtkinter.CTkLabel(master=sidebarFame, text="UI Scaling:")
scalingOptions = customtkinter.CTkOptionMenu(master=sidebarFame, values=["80%", "90%", "100%", "110%", "120%"], command=changeScaling)
scalingLabel.grid(row=3, column=0)
scalingOptions.set("100%")
scalingOptions.grid(row=4, column=0, pady=(0, 40))

tutorialTitleLabel = customtkinter.CTkLabel(master=sidebarFame, text="Tutorial")
tutorialTextLabel = customtkinter.CTkLabel(master=sidebarFame, text="1. Select the PDF to\nconvert to text\n2. Select the output\nfolder\n3. Type the name to\nsave the text file\nin the entry\n4. Hit convert")
tutorialTitleLabel.grid(row=5, column=0)
tutorialTextLabel.grid(row=6, column=0)

mainFrame = customtkinter.CTkFrame(master=app)
mainFrame.grid(row=0, column=1, sticky="nsew")

mainFrame.grid_columnconfigure((0, 1), weight=1)

pdfSelectButton = customtkinter.CTkButton(master=mainFrame, text="Select PDF", command=selectFile)
pdfSelectLabel = customtkinter.CTkLabel(master=mainFrame, text="PDF Selected: None")
pdfSelectButton.grid(row=0, column=0, padx=10, pady=30, sticky="nsew")
pdfSelectLabel.grid(row=0, column=1, padx=10, pady=30, sticky="nsew")

outputDirectoryButton = customtkinter.CTkButton(master=mainFrame, text="Select Output Folder", command=selectFolder)
outputLabel = customtkinter.CTkLabel(master=mainFrame, text="Folder Selected: None")
outputDirectoryButton.grid(row=1, column=0, padx=10, pady=30, sticky="nsew")
outputLabel.grid(row=1, column=1, padx=10, pady=30, sticky="nsew")

saveNameEntry = customtkinter.CTkEntry(master=mainFrame)
saveNameEntry.grid(row=2, columnspan=2, padx=100, pady=30, sticky="nsew")

convertButton = customtkinter.CTkButton(master=mainFrame, text="Convert", command=convert)
convertButton.grid(row=3, columnspan=2, padx=100, pady=30, sticky="nsew")

progressLabel = customtkinter.CTkLabel(master=mainFrame, text="Progress: Not started")
progressLabel.grid(row=5, columnspan=2, padx=10, pady=60, sticky="nsew")

app.mainloop()