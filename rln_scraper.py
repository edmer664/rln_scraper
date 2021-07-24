#! python3
import requests
from bs4 import *
from os import makedirs,getcwd,path
import tkinter as tk
from tkinter import ttk
import subprocess
from ebooklib import epub

#*GUI
class MainApp(tk.Frame):

    #? GUI fonts
    header_font=("sans-serif",24)
    body_font=("sans-serif",16)


    def __init__(self,master=None):
        super().__init__(master)
        self.pack(side="top")
        self.header_widgets()
        self.form_widgets()     
    

    def header_widgets(self):
        #? Header widgets
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
        self.progress = ttk.Progressbar(
            self,orient='horizontal',
            length=100,mode='determinate'
            )
        self.progress.pack(side="top")


    def submit(self):


        #? Validates input
        #? novel title
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
            errorMessage = "Directory already existing"
            try:
                self.error.destroy()
                root.update()
            except:
                pass
            self.error = tk.Label(self,text=errorMessage)
            self.error.pack()
            print(errorMessage)

        #? initialize book class
        url = f"https://www.readlightnovel.org/{self.input_title}/"
        book = epub.EpubBook()
        book.set_title(self.input_title)
        book.set_language('en')
        book.add_author("readlightnovel.org")
        #* iterate chapters
        chaps = []
        for chapter in range(1,self.input_chapters + 1):
            currentURL = url + f"chapter-{chapter}"
            #*get response
            response = requests.get(currentURL)
            if response.status_code == 200:
                print( f"Chapter {chapter} retrieved sucessfully")
            soup = BeautifulSoup(response.text,'html.parser')
            text = soup.select(".desc")

        #* bind all files    
        #*compiling to epub
            text ="<html> <body>" + str(text) + "</body></html>"
            c1 = epub.EpubHtml(title=f"Chapter {chapter}",file_name=f"temp_{chapter}.xhtml",lang="en",content=text,direction=book.direction)
        #? book.spine for ebook arrangement
            book.spine.append(c1)
            chaps.append(c1)
        #? progress_bar animation
            self.progress["value"] += 97/self.input_chapters
            root.update()
        #? adding chapters to book class
        for curr_chap in chaps:
            book.add_item(curr_chap)
            self.progress["value"] += 3/len(chaps)
            root.update()
        #? add navigation to book
        book.spine.insert(0,'nav')
        book.toc = tuple(chaps)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        #? finalizing output 
        epub.write_epub(path.join(f"{getcwd()}",f"{self.input_title}",f"{self.input_title}.epub"),book)
        self.label_pop["text"] = "Done"
        directory = path.join(f"{getcwd()}",f"{self.input_title}")
        #? opens file explorer after file creation
        subprocess.Popen(f'explorer "{directory}"')


#? Main 
root = tk.Tk()
root.title("RLN Scarper")
app = MainApp(master=root)
app.mainloop()