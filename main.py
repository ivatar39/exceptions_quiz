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


def start_program():
    main_window = Toplevel(root)
    main_window.minsize(width=450, height=600)
    # Главный фрэйм приложения
    app_frame = Frame(main_window)
    app_frame.pack()


# Главное Приложение, запуск стартового экрана
root = Tk()
# Фрейм шапка экрана
start_bar_frame = Frame(root)
start_bar_frame.pack(side=TOP, padx=80, pady=14)
# Заголовок
student_text_label = Label(start_bar_frame, text='Тест по дисциплине "Программирование"')
student_text_label.pack(side=TOP)
# Тема теста
student_text_label = Label(start_bar_frame, text='Тема - "Обработка прерываний"')
student_text_label.pack(side=TOP)
# Фрейм тело экрана
start_frame = Frame(root)
start_frame.pack(side=BOTTOM, pady=40, expand=1)
# Ввода имени
input_year_frame = Frame(start_frame)
input_year_frame.pack(side=TOP, pady=4, anchor=E, expand=1)
input_year_text_label = Label(input_year_frame, text='Введите имя:')
input_year_text_label.pack(side=LEFT)
input_year_entry = Entry(input_year_frame, width=30)
input_year_entry.pack(side=RIGHT)
# Ввода группы
input_group_frame = Frame(start_frame)
input_group_frame.pack(side=TOP, pady=4, anchor=E, expand=1)
input_group_text_label = Label(input_group_frame, text='Введите группу:')
input_group_text_label.pack(side=LEFT)
input_group_entry = Entry(input_group_frame, width=30)
input_group_entry.pack(side=RIGHT)
# Кнопка начала теста
start_button = Button(start_frame, text='Начать тест', width=30, height=5, command=lambda: start_program())
start_button.pack(side=BOTTOM, expand=1, anchor=S)


lines = read_quiz_file('quiz.csv')
questions = convert_lines_to_questions(lines)
for question in questions:
    print(question.text)
# Главный цикл
root.mainloop()
