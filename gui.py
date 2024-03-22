import tkinter as tk
from tkinter import ttk
from pathlib import Path
from scramble import scramble_exam
import datetime as dt
import re
#import scramble_menu

# Constants

peach = "#ffe5b4"
black = "black"

#TODO redefine Exam Bank directory to Documents? Get from settings file
exam_bank_dir = Path('/Users/wyattschiefelbein/Desktop/Hobby/Programming/Python/Exam Bank')


########## Command Methods ##########

def give_cookie():
    '''Creates a new label in the left frame on "give cookie" button press.
    - Input: None
    - Return: None'''
    cookie_lab = tk.Label(
        left_frame,
        text="YUM!",
        bg=black,
        fg=peach
    )
    cookie_lab.pack()


def handle_send_press():
    '''Takes user GUI-input and passes it to scramble_exam. Deletes punctuation
    from user's desired file name, excepting commas (","). Closes ttk window.
    - Input: None
    - Returns: None'''

    # Punctuation to be removed from user input
    forbidden_punctuation = '''!()-[]\{\};:'"\<>./?@#$%^&*_~'''

    enter_value = entr.get()
    exam_nm = ""

    # If user does not give a name for the exam file/directory, name it 
    #       "Exam, xxx-xx,xxxx,xx:xx:xx", where "x" are the date and time
    #       at send. Otherwise, take user's file name and remove punctuation.
    if enter_value == "":
        exam_nm = "Exam, {}".format(get_time())
    else:
        exam_nm = enter_value.translate(str.maketrans('','',forbidden_punctuation))

    #Debugging
    print("At 'send,' the exam file to scramble is:\t{}".format(Combo.get()))
    print("Call it\t{}".format(exam_nm))
    print("And the user says they want\t{} versions".format(Combo2.get()))

    exam_csv = exam_bank_dir / Combo.get()
    #scramble_exam(exam_nm,exam_csv,int(Combo2.get()),question_scramble.get())

    window.destroy()

# Creates a new label in the left frame on "give cookie" button
#   press.
def give_cookie():
    cookie_lab = tk.Label(
        left_frame,
        text="YUM!",
        bg=black,
        fg=peach
    )
    cookie_lab.pack()


def get_time():
    date = dt.datetime.now()
    print("Date is\t\t{}".format(date.strftime("%h-%d,%Y,%H:%M:%S")))
    return date.strftime("%h-%d,%Y,%H:%M:%S")

########## File Path Initialization ##########

files = []  # Will display all csv files in Exam folder TODO, mkdir then cd to exam folder

#exam_bank_dir = Path(__file__).parents[1].resolve() # Sets exam_bank_dir to parent of this script

for file in exam_bank_dir.iterdir():
    if file.suffix == '.csv':       # Only appends csv files to files list
        files.append(file.name)

########## Window Initialization ##########
        
# Defining GUI window
window = tk.Tk()
window.config(bg=peach)
window.title('Scrambler')

# Defining and packing frames
left_frame = tk.Frame(window, bg=black)
left_frame.pack(side="left")

right_frame = tk.Frame(window, bg=peach)
right_frame.pack(side="right")

snack = "Slice of Pie"
greeting = """tânisi,\n\tMy name is Scrambler. My job is
to take questions and answers which you give me, randomize
them, and then make a new exam and answer key for you!\n\n
I like to think I am a raccoon, you can always thank me 
by giving me a {}! You can also support my team with a 
tip or a positive review, too, if you want!
""".format(snack)


########## Left Frame ##########

# Greeting label
label = tk.Label(
    left_frame, 
    text = greeting,
    justify="left",
    bg = black,
    fg = peach,
)
label.pack(padx = 5, pady = 15)

# Give cookie button
snack_btn = tk.Button(
    left_frame,
    text="Give {}".format(snack),
    command=give_cookie,
)
snack_btn.pack()


########## Right Frame ###########

# Exam selector combobox
label = tk.Label(
    right_frame, 
    text="Which exam would you like me to scramble?",
    bg=peach
)
label.pack(padx = 5, pady = 15)

selected_item = tk.StringVar()
Combo = ttk.Combobox(
    right_frame,
    textvariable=selected_item,
    values=files
)
Combo.set("{}".format(files[0]))
Combo.pack()

# Exam Name Entry
#TODO limit size of entry
label = tk.Label(
    right_frame, 
    text="What would you like to call this exam?",
    bg=peach
)
label.pack(padx = 5, pady = 15)

entr = tk.Entry(
    right_frame,
    justify="center",
    #textvariable=exam_name
)
entr.pack()

# Number of versions combobox
label = tk.Label(
    right_frame, 
    text='How many versions of this exam do you want?',
    bg=peach
)
label.pack(padx = 5, pady = 15)

selected_item2 = tk.StringVar()
Combo2 = ttk.Combobox(
    right_frame,
    textvariable = selected_item2,
    values = [1,2,3,4,5,6]
)
Combo2.set(1)
Combo2.pack()

# "Scramble questions" checkbox
label = tk.Label(
    right_frame, 
    text='Would you like me to scramble the questions, or just the anwers?',
    bg=peach
)
label.pack(padx = 5, pady = 15)

question_scramble = tk.StringVar()
check = ttk.Checkbutton(
    right_frame,
    text='Scramble the questions, too.',
    variable=question_scramble,
    onvalue="1",
)
check.pack()

# Define Send Button
btn = tk.Button(right_frame,text="Send",command=handle_send_press)
btn.pack()

window.mainloop()