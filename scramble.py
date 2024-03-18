#!/usr/bin/env python3

# This code was written by Wyatt Schiefelbein for a friend.

from random import seed
from random import shuffle
from random import randint
from file_n_dirs import mk_dir
from file_n_dirs import rename_file
from pathlib import Path
from datetime import datetime
import csv
import sys


def write_exam(exam_file, answer_file, questions, answers):
    '''Writes questions and their shuffled answers to a file, defined by 
    the variable, exam_file, and calls write_answer_key().
    Input:  string, string, list[str], list[str]'''
    
    original_stdout = sys.stdout    # Store default stdout, terminal, to recover later
    answer_key = []

    with open(exam_file,'w') as file:
        sys.stdout = file

        for i in range(len(questions)):
            print('{}.  {}\n'.format(i+1,questions[i][0]))
            char_num = 97                   # i.e., char_num refers to "a"
            #TODO consider, ord('a') instead of 97

            for answer_options in answers[i]:

                if answer_options == '':    # Ignore blank answers
                    pass
                else:
                    char = chr(char_num)    # char = 'a'
                    print('\t{}.  {}'.format(char, answer_options))

                    if answer_options == questions[i][1]:   # if option is correct
                        answer_key.append(char)
                    char_num += 1            # iterate through alphabet
                
            print()

        sys.stdout = original_stdout        #TODO Is this unnecessary?
        write_answer_key(answer_file, answer_key)


def write_answer_key(answer_file, answer_key):
    '''Writes the correct answer's corresponding letter 
    to a file defined by the variable, answer_file.
    Input:  string, list[str]'''

    original_stdout = sys.stdout

    #TODO consider, replace "print" with "file.write"(appends to a file)? .stdout "peculiar", easier to do otherwise
    with open(answer_file,'w') as file:
        sys.stdout = file

        for i, val in enumerate(answer_key):
            print('{}.  {}'.format(i+1,val))

        sys.stdout = original_stdout


def shuffle_questions(question_list):
    '''Takes a 2d-list and shuffles the elements
    Shuffles the sub-list's elements around to randomize the order 
    questions will be printed in the exam
    Input:      list[list[str]]
    Returns:    list[list[str]]'''
    #TODO consider .shuffle() instead of .pop()
    shuffled_arr = len(question_list)

    for i in range(0,shuffled_arr):
        j = randint(0, shuffled_arr-1)
        element = question_list.pop(j)
        question_list.append(element)

    return question_list


def shuffle_answers(question_list, col, row):
    '''Takes a 2d-list and creates a sub-list (2d) of the elements after 
    the first index for each componant list. This corresponds to the
    answers for each question. Shuffles the sub-list's elements around
    to randomize the order answers will be printed in the exam
    Input:      list[list[str]], int, int
    Returns:    list[list[str]]'''

    seed(randint(0,100))
    shuffled_arr = init_2d_list(col, row)

    for num in range(len(question_list)):
        # Isolate and randomize just the answers in question_list
        sequence = [i for i in range(1,len(question_list[num]))]
        shuffle(sequence)

        for i, index in enumerate(sequence):
            # copies the value at index, shuffled by sequence,
            #   in question_list to shuffled_arr
            shuffled_arr[num][i] = question_list[num][index]

    return shuffled_arr


def get_csv_data(fileName, data_list):
    '''Extracts data from a csv file, fileName, excluding the header,
    and returns a 2d-list[str] storing the data.
    Input:      str, list[list[str]]
    Returns:    list[list[str]]'''

    header = []
    with open(fileName, encoding='utf-8') as file:
        count = 0
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list[count] = row
            count += 1

    return data_list


def init_2d_list(col, row):
    '''Initializes a list[list[str]] object, filling all elements with "0".
    Input   int, int
    Return  list[list[str]]'''

    arr = [["0" for i in range(col)] for j in range(row)]
    return arr


def count_rows_csv(file_name):
    '''Counts the number of rows in a CSV file, file_name.
    Input   str
    Return  int'''

    with open(file_name, encoding='utf-8') as file:
        for count, line in enumerate(file):
            pass
    return count


def scramble_exam(exam_name: str, exam_bank_file: str, num_ver: int, yn_shuffle_qs: str):

    home_path = Path.home()     # /Users/[name]/
    to_path = home_path / 'Documents'
    exam_dir = mk_dir(to_path / exam_name)

    exam_file = exam_dir / '{}.txt'.format(exam_name)           # Exam file
    rename_file(exam_file)   # Rename if exam_file exists at parent
    answer_file = exam_dir / '{}, Answer Key.txt'.format(exam_name)   # Answer Key file
    rename_file(answer_file) # Rename if answer_file exists at parent

    col = 4 # maximum number of possible answers, excl. of question
    row = count_rows_csv(exam_bank_file)    # Represents the number of exam questions

    # Text to print to terminal
    separator = '\n*********************************\n'
    print(separator)
    intro = "tân'si! I will scramble your exam now.\n"
    print(intro)

    # initialize a list of exam questions and answers, exam_questions
    exam_questions = init_2d_list(col, row)
    exam_questions = get_csv_data(exam_bank_file,exam_questions)

    #TODO Make multiple versions with a while loop, here.
    
    if yn_shuffle_qs == "1":    # If user wants to scramble the questions, too
        exam_questions = shuffle_questions(exam_questions)  # shuffle questions

    # shuffle answers
    shuffled = shuffle_answers(exam_questions, col, row)
    write_exam(exam_file, answer_file, exam_questions, shuffled)

    #TODO End while loop, here.

    #  print to terminal
    outro = '''Aaaaand, DONE!
    \nThe exam is called\t{},\nand the answer key is\t{}.\n\nêkosi mâka!\n
    Both can be found at {}\n\n'''
    print(outro.format(exam_file.name,answer_file.name,exam_dir))
    print(separator)