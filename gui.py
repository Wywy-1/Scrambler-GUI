import tkinter as tk
from tkinter import ttk

#from tkinter.messagebox import showinfo
#from tkinter.messagebox import showerror

#from randomizer import scramble_exam
from pathlib import Path

'''References:
The code on this script is adapted from the following sources:

ttkboostrap,
https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/notebook.html

user Mark Tolonen on stackoverflow,
https://stackoverflow.com/questions/44745297/adding-notebook-tabs-in-tkinter-how-do-i-do-it-with-a-class-based-structure,

python tutorial.net,
https://www.pythontutorial.net/tkinter/tkinter-object-oriented-application/

https://www.pythontutorial.net/tkinter/ttk-style/
'''
beige = "#ffe5b4"
black = "black"

# Accessible Pallete #1
peach = '#FAAF90'
l_peach= '#FCC9B5'
lavender = '#D9E4FF'
periwinkle = '#B3C7F7'
blurple = '#8BABF1'

'''
# Accessible pallet #2
l_blue = '#BAE3F5'
vl_blue = '#CDEDFA'
peach = '#FFEBE2'
m_peach = '#FEDCCF'
d_peach = '#'FCCDBB'
'''

class app(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Scrambler')
        self.geometry('1200x900')

        # UI
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 11)}

        default_font = ('Times', 18)

        # Style
        self.configure(background=l_peach, relief=tk.RAISED)
        self.style = ttk.Style(self)
        self.style.configure('TLabel', background=lavender,font=default_font)
        self.style.configure('TNotebook', bg=lavender,font=default_font)


class Tstyle():
    def __init__(self,parent):
        self.style = ttk.Style(parent)
    
    def make_default(self):
        self.style.configure(background='green')


class tab:

    def __init__(self,parent):
        self.notebook = ttk.Notebook(parent)

    def add_tab(self,title,text):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame,text=title)
        label = ttk.Label(frame,text=text)
        label.grid(column=1,row=1)
        self.notebook.pack()

    def add_scramble_tab(self):
        frame = scramble_tab(self.notebook)
        self.notebook.add(frame,text='Scramble Exam')
        self.notebook.pack()

    def add_new_exam_tab(self):
        frame = new_exam(self.notebook)
        self.notebook.add(frame,text='New Exam Template')
        self.notebook.pack()

    def add_intro_tab(self):
        frame = intro_tab(self.notebook)
        self.notebook.add(frame,text='Introduction')
        self.notebook.pack()


class intro_tab(ttk.Frame):

    def __init__(self,parent):
        super().__init__(parent)    # Give intro frame the tk attribute

        text1 = '''tân'si, hello!\n\n\tMy name is Scrambler, I help shuffle
        exam questions (and answers) into new versions of an exam; I also make the
        subsequent answer keys!\n\n\tI am not a "smart" program, but I do
        just fine! I don't collect data about you, your device, or anything.
        I simply take input and work with it, but I can be a bit finicky about it, so
        please bear with me!\n\n\t
        
            You should see tabs above this text, they say "Introduction," "Scramble," 
        "Instructions," "New Exam / Move Exams," and "Support." The first tab, 
        "Scramble", is where you can create new versions. By default, I put new exams 
        I make into a folder in your Documents. If you give me a name, I'll call that 
        folder the name you give me! If you don't give me a name, I'll just call it 
        "Exam" and the date and time.
        
            "New Exam" is where you'll go to create a new exam! Because I am a simple
        program, I can't read word documents or anything like that. I can only read
        in an easy document-type called Comma-Separated Value, or CSV for short. When you
        click on the "New Exam" tab, I'll give you options to write exam question(s),
        a correct answer, and false answers. I'll then take these and save them as 
        a CSV file in a folder called "Exam Banks". This folder will be in your
        documents. If you want to edit a question in a specific exam, you can do that as
        follows:
                1) CSV is a simple text file that works like an excel spreadsheet
                2) each column of information is seperated by a comma (",")
                3) for example:

                    "information 1" ,  "information 2" ,  "information 3"

                4) Your exam is written like this:
                
                    "Question, can have commas within quotes","Correct Answer","Incorrect Answer"

                    and prints like this:

                    1) Question, can have commas within quotes
                        a) Correct Answer
                        b) Incorrect Answer
                    
                5) If you go to manually change the exam, you'll notice that sometimes there are
                    no double-quotes around questions: This is just short-hand, I only put double-
                    quotations when a question or answer has a comma in it that doesn't mean "next
                    information".
                    
                6) If you edit your exam and it no longer prints how you want, double check that
                    free commas (those not surrounded by double-quotes) only exist where you want
                    to seperate information.
                    
                7) My developer will be making an option to more easily edit exams with my 
                    descendants!'''

        self.intro_text_label = ttk.Label(self, text = text1)
        self.intro_text_label.grid(row=0, column=0)


class scramble_tab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)    # Gives scramble_frame the 'tk' attritbute

        ############# Instructions, Right Side ###########
        text_1 = """   Give the exam you want me to make a name, for example, 'Midterm 1, Psych 201', or 'Balinda.'\n   Then choose the exam you'd like to scramble and give the name. I look for exams in a folder, 'Exam Bank' in your documents. I only look for CSV files in that folder, though, so something like a word document (.docx) is basically invisiable to me.\n   Next, choose the number of versions you'd like me to make.\n   When you're ready, click 'send' and I'll make your exam! I'll put it in a folder on your desktop with the name you give me."""
        self.instruction_label = ttk.Label(self,text=text_1,justify='left',width=40,foreground=blurple,wraplength=350)
        self.instruction_label.grid(column=1, rowspan=6, padx=5, pady=10)


        ############# Exam Name #############
        # Label
        self.exam_name_label = ttk.Label(self, text="What name should I give the new exam?")
        self.exam_name_label.grid(row=0, column=0, sticky=tk.W)

        # Entry
        self.exam_name = usr_input(self)
        self.exam_name.grid(row=1,column=0)

        ############# Exam Bank CSV to Scramble #############
        # Label
        self.exam_name_label = ttk.Label(self, text="Which exam should I scramble?")
        self.exam_name_label.grid(row=2, column=0, sticky=tk.W)

        # Combobox
        files = []

        home_path = Path.home()     # /Users/[name]
        exam_bank = home_path / 'Documents' / 'Exam Bank'

        for file in exam_bank.iterdir():
            if file.suffix == '.csv':
                files.append(file.name)

        self.exam = write_in(self)
        self.exam['values'] = files
        self.exam.grid(row=3,column=0)
        self.exam.current()
        
        ############# Number of Versions to Make #############
        # Label
        self.exam_name_label = ttk.Label(self, text="How many versions would you like?")
        self.exam_name_label.grid(row=4, column=0, sticky=tk.W)

        # Combobox
        nums = [1,2,3,4,5,6,7,8,9]
        self.num_versions = write_in(self)
        self.num_versions['values'] = nums
        self.num_versions.grid(row=5,column=0)
       
        ############# Send Button #############
        # Button
        self.btn = ttk.Button(self, text='Send',\
                              command= lambda : \
                                print("user input is\t{},{},{}".format(\
                                    self.exam_name.get(),\
                                    self.exam.get(),\
                                    self.num_versions.get())))
        self.btn.grid(row=6, column=0)


class new_exam(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)    # Gives scramble_frame the 'tk' attritbute

        ############# Instructions #############
        text1 = """Name the template something you'll remmebr; e.g., 'Midterm 2, Psych 101. Then press 'Send Exam Name. This will create your Exam template file for this exam, putting it in 'Exam Bank' in your documents folder.\n Then add questions and answers, one at a time, pressing 'Send Question and Answers' after each.\n\nFor 'all of the above' type questions, put 'all options' in the correct-answer box.\n\nFor essay questions, simply add one answer in the correct answer box."""
        self.instr_label = ttk.Label(self, text=text1,padding=20,wraplength=350,foreground=blurple)
        self.instr_label.grid(row=0,column=3,rowspan=8)
        ############# Exam Name #############
        # Label
        self.exam_name_label = ttk.Label(self, text="What would you like to call this exam template?",justify='center')
        self.exam_name_label.grid(row=0, column=0, columnspan=2)

        # Entry
        self.exam_name = usr_input(self)
        self.exam_name.grid(row=1,column=0, pady=30)

        ############# Questions #############
        # Label
        self.q_label = ttk.Label(self, text="Question:")
        self.q_label.grid(row=2, column=0, sticky=tk.W)

        # Entry
        self.q = usr_input(self)
        self.q.grid(row=2,column=1)

        ############# Correct Answer #############
        # Label
        self.ca_label = ttk.Label(self, text="Correct Answer:")
        self.ca_label.grid(row=3, column=0, pady=30, sticky=tk.W)

        # Entry
        self.ca = usr_input(self)
        self.ca.grid(row=3,column=1)

        ############# Incorrect Answer(s) #############
        # Label
        self.ia_label = ttk.Label(self, text="Incorrect Answer(s):")
        self.ia_label.grid(row=4, column=0, sticky=tk.W)

        # Entry
        self.ia_1 = usr_input(self)
        self.ia_1.grid(row=4,column=1)

        self.ia_2 = usr_input(self)
        self.ia_2.grid(row=5,column=1)

        self.ia_3 = usr_input(self)
        self.ia_3.grid(row=6,column=1)

        ############# Send Template Name Button #############
        self.btn1 = ttk.Button(self,text='Send Name',\
                               command= lambda : (print("Exam name is: {}".format(self.exam_name.get())),self.exam_name.configure(state='disabled')))
        self.btn1.grid(row=1,column=1)
    
        ############# Send Question Button #############
        # Record question and answers within seperate double-quotations marks, then erases entries from ttk.Entry widgets
        self.btn2 = ttk.Button(self, text='Send Question and Answers',\
                              command= lambda : (\
                                print('"{}","{}","{}","{}","{}"'.format(\
                                    self.q.get(),\
                                    self.ca.get(),\
                                    self.ia_1.get(),\
                                    self.ia_2.get(),\
                                    self.ia_3.get())),\
                                self.q.delete(0,'end'),\
                                self.ca.delete(0,'end'),\
                                self.ia_1.delete(0,'end'),\
                                self.ia_2.delete(0,'end'),\
                                self.ia_3.delete(0,'end')))
        self.btn2.grid(row=7, column=0, columnspan=2)


#   Entry Class
class usr_input(tk.Entry):
    def __init__(self, container):
        super().__init__(container)
        input = tk.StringVar()

    def get_str(self):
        return self.input.get()


#   Combo Box Class
class write_in(ttk.Combobox):
    def __init__(self, container):
        super().__init__(container)
        item = tk.StringVar()
        textvariable = item
        print("{}".format(textvariable.get()))
    
    def get_str(self):
        return self.item.get()
    

if __name__ == "__main__":
    app = app()

    nb = tab(app)

    nb.add_intro_tab()
    nb.add_scramble_tab()
    nb.add_new_exam_tab()

    app.mainloop()

#scramble_exam(exam_nm,exam_csv,int(Combo2.get()))