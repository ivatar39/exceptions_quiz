# Импорт библиотеки tkinter для работы с GUI
from tkinter import *
from tkinter import filedialog as fd


class Student:
    right_answers = 0
    quiz_complete_percent = 0

    def __init__(self, name, group):
        self.name = name
        self.group = group


class Question:
    def __init__(self, text, answers):
        self.text = text
        self.answers = answers


class Answer:
    def __init__(self, text, is_right):
        self.text = text
        self.is_right = is_right


def read_quiz_file(file_name):
    try:
        file = open(file_name, encoding='UTF-8')
        file_lines = file.readlines()
        # Удаление заголовков
        file_lines.pop(0)
        processed_lines = []
        # Форматирование csv-файла
        for line in file_lines:
            processed_lines.append(line.replace('\n', '').rsplit(';'))
        file.close()
        return processed_lines
    except FileNotFoundError:
        print('Файл не найден')


def convert_lines_to_questions(processed_lines):
    converted_questions = []
    for row in processed_lines:
        answers = []
        for i in range(1, len(row)-1):
            a = Answer(text=row[i], is_right=i == 1)
            answers.append(a)
        q = Question(text=row[0], answers=answers)
        converted_questions.append(q)
    return converted_questions


lines = read_quiz_file('quiz.csv')
questions = convert_lines_to_questions(lines)
for question in questions:
    print(question.text)