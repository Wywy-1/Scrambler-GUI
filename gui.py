import tkinter as tk
from tkinter import ttk

#from tkinter.messagebox import showinfo
#from tkinter.messagebox import showerror

#from randomizer import scramble_exam
from pathlib import Path
from file_n_dirs import get_document_dir
from file_n_dirs import make_exam_bank
from file_n_dirs import get_exam_bank
from file_n_dirs import append_to_file

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
instruction_blurple = '#8BABF1'

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

    def add_bank_tab(self):
        frame = exam_bank_tab(self.notebook)
        self.notebook.add(frame,text='New Exam Bank')
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

        text1 = '''tân'si, hello!\n\nMy name is Scrambler, and I am a program that helps instructors shuffle exams into unique versions. I also make answer keys for those versions!\n\nI am a simple progam in that all I do is: a) make a folder in your Documents called "Exam Bank", where I store exams; b) write your exams as templates in a format I can read, called CSV; and finally, c) take those templates and make unique versions of exams, printing them, along with an answer key, in a simple file format (.txt) that you can then copy and paste into word, pages, or docs to make pretty!\n\nThat is to say, I write files and I make folders in your Documents and Desktop. I don't delete folders or files, and I don't collect information about you or anything like that.\n\nIf you have comments or feedback, email my programmer, Wyatt, with the email in the "Contact / Support" tab. If you feel like it, you can also tip him with the paypal link in that same tab! (His favourite coffee is $5.45)'''

        self.intro_text_label = ttk.Label(self, text = text1,wraplength=700)
        self.intro_text_label.grid(row=0, column=0)


class exam_bank_tab(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        text_1 = """Let's set up your exam bank to get started!\nThe Exam Bank is a folder where I'll save all exam templates. When you click the button, below, I'll make a folder in your documents folder called 'Exam Bank.'\nAfter this, restart Scrambler and then we can create your first template! I'll use the templates to scramble exams in the future for you."""
        self.label = ttk.Label(self,text=text_1,justify='center',width=38,foreground=instruction_blurple,wraplength=350)
        self.label.grid(column=0,row=0,columnspan=2)
        self.btn3 = ttk.Button(self, text="Make Exam Bank", command= lambda : make_exam_bank())
        self.btn3.grid(row=1, column=0,columnspan=2)


class scramble_tab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)    # Gives scramble_frame the 'tk' attritbute

        ############# Instructions, Right Side ###########
        text_1 = """   Give the exam you want me to make a name, for example, 'Midterm 1, Psych 201', or 'Balinda.'\n   Then choose the exam you'd like to scramble and give the name. I look for exams in a folder, 'Exam Bank' in your documents. I only look for CSV files in that folder, though, so something like a word document (.docx) is basically invisiable to me.\n   Next, choose the number of versions you'd like me to make.\n   When you're ready, click 'send' and I'll make your exam! I'll put it in a folder on your desktop with the name you give me."""
        self.instruction_label = ttk.Label(self,text=text_1,justify='left',width=40,foreground=instruction_blurple,wraplength=350)
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

        try:
            for file in exam_bank.iterdir():
                if file.suffix == '.csv':
                    files.append(file.name)
        except (FileNotFoundError):     #TODO #4 make a more elegant solution for no Exam Bank?
            #exam_bank = make_exam_bank()
            files.append("Exam Bank is empty.")

        self.exam = write_in(self)

        self.exam['values'] = files
        self.exam['state'] = 'readonly'

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
        text1 = """Name the template something you'll remmebr; e.g.,'Midterm 2, Psych 101. Then press 'Send Exam Name. This will create your Exam template file for this exam, putting it in 'Exam Bank' in your documents folder.\n Then add questions and answers, one at a time, pressing 'Send Question and Answers' after each.\n\nFor 'all of the above' type questions, put 'all options' in the correct-answer box.\n\nFor essay questions, simply add one answer in the correct answer box."""
        self.instr_label = ttk.Label(self, text=text1,padding=20,wraplength=350,foreground=instruction_blurple)
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

        self.exam_path = get_exam_bank()

        ############# Send Template Name Button #############
        self.btn1 = ttk.Button(self,text='Send Name',\
                               command= lambda :((print("Exam name is: {}".format(self.exam_name.get())),self.exam_name.configure(state='disabled')),self.btn2.configure(state='active')))
        self.btn1.grid(row=1,column=1)
        
        ############# Send Question Button #############
        # Record question and answers within seperate double-quotations marks, then erases entries from ttk.Entry widgets
        self.btn2 = ttk.Button(self, state='disabled', text='Send Question and Answers',\
                              command= lambda : (\
                                append_to_file(\
                                    self.exam_path / str(self.exam_name.get() + '.csv'),\
                                        self.q.get(),\
                                            self.ca.get(),\
                                                self.ia_1.get(),\
                                                    self.ia_2.get(),\
                                                        self.ia_3.get()),\
                                self.q.delete(0,'end'),\
                                self.ca.delete(0,'end'),\
                                self.ia_1.delete(0,'end'),\
                                self.ia_2.delete(0,'end'),\
                                self.ia_3.delete(0,'end')))
        self.btn2.grid(row=7, column=0, columnspan=2)

        #Debug Button
        self.btn3 = ttk.Button(self,text="Test", command = lambda : (print("{}".format(self.exam_path / str(self.exam_name.get())))))
        self.btn3.grid(row=8,column=0)

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
    exam_bank = get_document_dir()
    exam_bank = exam_bank / "Exam Bank"

    nb.add_intro_tab()
    if exam_bank.exists():
        nb.add_scramble_tab()
        nb.add_new_exam_tab()
    else:
        nb.add_bank_tab()

    app.mainloop()

#scramble_exam(exam_nm,exam_csv,int(Combo2.get()))