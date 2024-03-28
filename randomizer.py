import csv
import random
from file_n_dirs import mk_dir
from file_n_dirs import rename_file
from pathlib import Path

'''Originally developed by dnswrsrx. Incorporated March 19, 2024, from 
https://gitlab.com/dnswrsrx/shenanigans/-/blob/master/wyatts_assessment_randomizer/randomizer.py?ref_type=heads
'''

class Question:

    def __init__(self, row):
        self.question, self.correct, *self.incorrect = row
        # Remove empty string for incorrect options
        self.options = [self.correct, *(i for i in self.incorrect if i)]

    def append_to_test_file(self, exam_file_fp, index):
        exam_file_fp.write(f'{index}. {self.question}\n')

        # Shuffle only if more than 2 options.
        if len(self.options) > 1:
            random.shuffle(self.options)
            #print("In shuffle_options")        #For Debugging

        for option_index, option in enumerate(self.options):
            exam_file_fp.write(f'\t{as_alpha(option_index)}. {option}\n')

        exam_file_fp.write('\n')

    def append_to_answer_file(self, answer_file_fp, index):
        answer_file_fp.write(f'{index}. {as_alpha(self.options.index(self.correct))}\n')


def collect_questions(file_name: Path):
    '''Returns a list of Question items containing each line of a csv 
    file, except for the first line (the header).'''
    with open(file_name) as f:
        reader = csv.reader(f)
        # Skip the header row
        next(reader)
        return [Question(row) for row in reader]


def as_alpha(index):
    '''Returns the char corresponding to the passed int away from "a". 
    E.g., as_alpha(1) returns "b", as_alpha(4) returns "e". '''
    return chr(index + ord('a'))


def generate_tests(csv_file_name, name, number_of_tests):
    '''Creates txt files corresponding to test and answer key.
    - Parses csv data (questions/answers) into a list
    - Updates the names of exams if there will be multiple versions
    - Writes to exam and answer keys, shuffled'''

    questions = collect_questions(csv_file_name)

    # Shuffles questions/options and prints to exam and answer key files, repeating to
    # make multiple versions and storing these in a (new) shared directory
    for index in range(number_of_tests):
        # Add number into file name if more than one tests to be created
        index_addition = f' {index+1}' if number_of_tests > 1 else ''
        test_file_name = f'{name}{index_addition}.txt'
        answer_file_name = f'{name}{index_addition}, Answer Key.txt'

        # Opening multiple files within the same with block
        # so that as I go through each question,
        # I can write each question + options and the answer
        # to the test and answer file respectively.
        # Otherwise I need more code to keep track of the order of questions and answers
        with (open(test_file_name, 'w') as test_file,
              open(answer_file_name, 'w') as answer_file):

            random.shuffle(questions)

            for question_index, question in enumerate(questions, start=1):
                question.append_to_test_file(test_file, question_index)
                question.append_to_answer_file(answer_file, question_index)


def scramble_exam(exam_name: str, exam_bank_file: str, num_ver: int):
    '''Calls generate_tests function and prints exam and answer keys to documents folder.
    Prints a user friendly message to terminal and informs user of where the exams and
    keys can be found'''


    home_path = Path.home()     # /Users/[name]/
    print_to_path = home_path / 'Documents'
    exam_dir = mk_dir(print_to_path / exam_name)

    exam_name_path = exam_dir / exam_name

    # Text to print to terminal
    separator = '\n*********************************\n'
    intro = "tân'si! I will scramble your exam now.\n"
    print(separator)
    print(intro)

    generate_tests(exam_bank_file,exam_name_path,num_ver)

    #  print to terminal
    outro = '''Aaaaand, DONE!
    \nThe exam(s) and the answer key(s) can be found at\t{}.\n\nêkosi mâka!'''
    print(outro.format(exam_dir))
    print(separator)

scramble_exam('Test.4','Test2.csv',1)  # Test