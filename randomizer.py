import csv
import random
import argparse


'''Originally developed by dnswrsrx. Incorporated March 19, 2024, from 
https://gitlab.com/dnswrsrx/shenanigans/-/blob/master/wyatts_assessment_randomizer/randomizer.py?ref_type=heads
'''


def collect_questions(file_name):
    with open(file_name) as f:
        reader = csv.reader(f)
        # Skip the header row
        next(reader)
        return [Question(row) for row in reader]


def as_alpha(index):
    return chr(index + ord('a'))


class Question:

    def __init__(self, row):
        self.question, self.correct, *self.incorrect = row
        # Remove empty string for incorrect options
        self.options = [self.correct, *(i for i in self.incorrect if i)]

    def append_to_test_file(self, test_file_fp, index, shuffle_options):
        test_file_fp.write(f'{index}. {self.question}\n')

        # Shuffle only if more than 2 options.
        if shuffle_options and len(self.options) > 2:
            random.shuffle(self.options)

        for option_index, option in enumerate(self.options):
            test_file_fp.write(f'\t{as_alpha(option_index)}. {option}\n')

        test_file_fp.write('\n')

    def append_to_answer_file(self, answer_file_fp, index):
        answer_file_fp.write(f'{index}. {as_alpha(self.options.index(self.correct))}\n')


def generate_tests(csv_file_name, shuffle_options, number_of_tests):

    questions = collect_questions(csv_file_name)

    for index in range(number_of_tests):
        # Add number into file name if more than one tests to be created
        index_addition = f'_{index+1}' if number_of_tests > 1 else ''
        test_file_name = f'test{index_addition}.txt'
        answer_file_name = f'answer{index_addition}.txt'

        # Opening multiple files within the same with block
        # so that as I go through each question,
        # I can write each question + options and the answer
        # to the test and answer file respectively.
        # Otherwise I need more code to keep track of the order of questions and answers
        with (open(test_file_name, 'w') as test_file,
              open(answer_file_name, 'w') as answer_file):

            random.shuffle(questions)

            for question_index, question in enumerate(questions, start=1):
                question.append_to_test_file(test_file, question_index, shuffle_options)
                question.append_to_answer_file(answer_file, question_index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('csv_file', help='CSV file with questions and options')

    parser.add_argument('-s', '--shuffle',
                        action='store_true',
                        help='To also shuffle options for each question')

    parser.add_argument('-n', '--number', required=False,
                        type=int,
                        default=1,
                        help='Number of differently shuffled tests to create')


    args = parser.parse_args()
    generate_tests(args.csv_file, args.shuffle, args.number)
