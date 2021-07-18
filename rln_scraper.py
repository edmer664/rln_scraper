#! python3
from re import I
import requests
from bs4 import *
from os import makedirs,getcwd,path
import tkinter as tk

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
        ).pack(side="left")

    def submit(self):
        self.popup = tk.Toplevel()
        self.label_pop = tk.Label(
            self.popup,
            text="Processing",
            font=self.body_font,
            width=20
            )
        self.label_pop.pack(side="top")


        #? Validates input
        #* catch novel title
        try:
            input_title = self.title_form.get('1.0',"end-1c").strip()
            input_chapters = int(self.chapters_form.get('1.0',"end-1c"))
        except:
            raise Exception("Please enter a valid input.")
        if input_title == "" or input_chapters == 0:
            raise Exception("Please enter a valid input.")


        #* Url format
        input_title = input_title.replace(" ","-")

        #*make directory
        try:
            makedirs(f'.\\{input_title}')
        except:
            print("Directory already existing")
            pass
        url = f"https://www.readlightnovel.org/{input_title}/"

        #* iterate chapters
        for chapter in range(1,input_chapters + 1):
            currentURL = url + f"chapter-{chapter}"
            #*get response
            response = requests.get(currentURL)
            soup = BeautifulSoup(response.text,'html.parser')
            text = soup.select(".desc")

        #* bind all files    
            content = ""
            for char in text:
                #!print(char.getText())
                content += char.getText()
            try:
                with open(path.join(f"{getcwd()}",f"{input_title}",f"{input_title}-chapter{chapter}.txt"),'x',encoding="utf-8") as file:
                    file.write(content)
            except:
                print(f'File: "{input_title}-chapter{chapter}.txt" already exist')


root = tk.Tk()
root.title("RLN Scarper")
app = MainApp(master=root)
app.mainloop()