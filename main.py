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


def end_test():
    pass


def choose_answer():
    pass


def start_program():
    # Окно тестирования
    main_window = Toplevel(root)
    main_window.minsize(width=450, height=600)
    # Главный фрэйм приложения
    app_frame = Frame(main_window)
    app_frame.pack()
    # Верхняя область
    app_bar_frame = Frame(app_frame)
    app_bar_frame.pack(side=TOP)
    countdown_text_label = Label(app_bar_frame, text='Время до завершения попытки: ')
    countdown_text_label.pack(side=LEFT, anchor=W, expand=1)
    countdown_time = '0:59'
    countdown_label = Label(app_bar_frame, text=countdown_time)
    countdown_label.pack(side=LEFT)
    end_test_button = Button(app_bar_frame, text='Завершить попытку', width=30, height=4, command=lambda: end_test())
    end_test_button.pack(side=RIGHT, anchor=E)

    # Область теста
    app_quiz_frame = Frame(app_frame)
    app_quiz_frame.pack(side=BOTTOM)

    question_text = 'Текст вопроса 1'
    question_label = Label(app_quiz_frame, text=question_text)
    question_label.pack(side=TOP, pady=17)

    answer_1_button = Button(app_quiz_frame, text='Вариант 1', width=30, height=4, command=lambda: choose_answer())
    answer_1_button.pack(side=TOP)
    answer_2_button = Button(app_quiz_frame, text='Вариант 2', width=30, height=4, command=lambda: choose_answer())
    answer_2_button.pack(side=TOP)
    answer_3_button = Button(app_quiz_frame, text='Вариант 3', width=30, height=4, command=lambda: choose_answer())
    answer_3_button.pack(side=TOP)
    answer_4_button = Button(app_quiz_frame, text='Вариант 4', width=30, height=4, command=lambda: choose_answer())
    answer_4_button.pack(side=TOP)
    # Нижняя область
    app_bottom_frame = Frame(app_quiz_frame)
    app_bottom_frame.pack(side=BOTTOM)

    question_count_label = Label(app_bottom_frame, text='Вопрос 1 из 10')
    question_count_label.pack(side=LEFT, anchor=W, expand=1)

    student_info_frame = Frame(app_bottom_frame)
    student_info_frame.pack(side=RIGHT)
    name_text_label = Label(student_info_frame, text='Имя - Иванов')
    name_text_label.pack(side=TOP)
    group_text_label = Label(student_info_frame, text='Группа - 19-ИЭ-2')
    group_text_label.pack(side=BOTTOM)


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
