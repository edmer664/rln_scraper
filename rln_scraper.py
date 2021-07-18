#! python3
from re import I
import requests
from bs4 import *
from os import makedirs,getcwd,path
import tkinter as tk
from tkinter import ttk

#*GUI
class MainApp(tk.Frame):
    header_font=("sans-serif",24)
    body_font=("sans-serif",16)
    def __init__(self,master=None):
        super().__init__(master)
        self.pack(side="top")
        self.header_widgets()
        self.form_widgets()     
    
    def header_widgets(self):
        self.load = tk.PhotoImage(file="./rln.png")
        self.logo = tk.Label(self,image=self.load).pack(side="top")
        self.mainTitle = tk.Label(
            self,
            text="RLN Scarper",
            width=25,
            font=self.header_font
            ).pack(
                side="top"
                )
    def form_widgets(self):
        self.label_title = tk.Label(
            self,
            text="Novel Title",
            font=self.body_font
            ).pack(
                side="top"
                )
        self.title_form = tk.Text(
            self,
            font=self.body_font,
            height=1
            )
        self.title_form.pack(
                side="top",
                fill='x',
                expand=True
                )
        self.label_chapters = tk.Label(
            self,
            text="Chapters to download",
            font=self.body_font
            ).pack(
                side="top"
                )
        self.chapters_form = tk.Text(
            self,
            font=self.body_font,
            height=1
            )
        self.chapters_form.pack(
                side="top",
                fill='x',
                expand=True
                )
        self.submit = tk.Button(
            self,
            font=self.body_font,
            height=1,
            command=self.submit,
            text="Submit",
            padx=5,
            pady=5
         ).pack(
             side="top"
         )
        self.quit = tk.Button(
            self,
            font=self.body_font,
            height=1,
            command=root.destroy,
            text="Quit",
            padx=5,
            pady=5
        ).pack(side="top")
    def progress_bar(self):
        try:
            self.progress.destroy()
            self.label_pop.destroy()
        except:
            pass
        self.label_pop = tk.Label(
            self,
            text="Processing",
            font=self.body_font,
            width=20
            )
        self.label_pop.pack(side="top")
        self.progress = ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')
        self.progress.pack(side="top")
    def submit(self):


        #? Validates input
        #* catch novel title
        try:
            self.input_title = self.title_form.get('1.0',"end-1c").strip()
            self.input_chapters = int(self.chapters_form.get('1.0',"end-1c"))
        except:
            raise Exception("Please enter a valid input.")
        if self.input_title == "" or self.input_chapters == 0:
            raise Exception("Please enter a valid input.")

        self.progress_bar()
        root.update()

        #* Url format
        self.input_title = self.input_title.replace(" ","-")

        #*make directory
        try:
            makedirs(f'.\\{self.input_title}')
        except:
            print("Directory already existing")
            pass
        url = f"https://www.readlightnovel.org/{self.input_title}/"

        #* iterate chapters
        for chapter in range(1,self.input_chapters + 1):
            currentURL = url + f"chapter-{chapter}"
            #*get response
            response = requests.get(currentURL)
            if response.status_code == 200:
                print( f"Chapter {chapter} retrieved sucessfully")
            soup = BeautifulSoup(response.text,'html.parser')
            text = soup.select(".desc")

        #* bind all files    
            content = ""
            for char in text:
                #!print(char.getText())
                content += char.getText()
            try:
                with open(path.join(f"{getcwd()}",f"{self.input_title}",f"{self.input_title}-chapter{chapter}.txt"),'x',encoding="utf-8") as file:
                    file.write(content)
            except:
                errorMessage = f'File: "{self.input_title}-chapter{chapter}.txt" already exist'
                self.error = tk.Label(self,text=errorMessage)
                print(errorMessage)
            self.progress["value"] += 100/self.input_chapters
            root.update()
        self.label_pop["text"] = "Done"



root = tk.Tk()
root.title("RLN Scarper")
app = MainApp(master=root)
app.mainloop()