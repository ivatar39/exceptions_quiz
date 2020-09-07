# Импорт библиотеки tkinter для работы с GUI
from tkinter import *
import random


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
        for i in range(1, len(row)):
            a = Answer(text=row[i], is_right=i == 1)
            print(a.text)
            print(a.is_right)
            answers.append(a)
        q = Question(text=row[0], answers=answers)
        converted_questions.append(q)
    return converted_questions


def exit_program():
    exit()


# Метод выборки вопроса в тесте
def choose_answer(main_window, student, current_index, answers, countdown_time):
    for children in main_window.winfo_children():
        children.destroy()

    if current_index >= len(questions) - 1:
        main_window.destroy()
        quiz_result(student, answers, countdown_time)
    else:
        start_quiz_by_index(main_window, student, current_index + 1, answers, countdown_time)


# Метод для запуска теста
def run():
    student = Student(name=input_name_entry.get(), group=input_group_entry.get())
    # Окно тестирования
    main_window = Toplevel(root)
    main_window.minsize(width=450, height=600)
    start_quiz_by_index(main_window, student, 0, [], 100)


# Старт теста на конкретном индексе
def start_quiz_by_index(main_window, student, current_question_index, answers, countdown_time):
    def update_timer():
        temp = int(seconds.get())
        print(temp)
        countdown_label.update()
        temp -= 1
        seconds.set(temp)
        if temp <= 0:
            quiz_result(student, answers, temp)
        app_frame.after(1000, update_timer)

    seconds = StringVar()
    seconds.set(countdown_time)
    # Главный фрэйм приложения
    app_frame = Frame(main_window)
    app_frame.pack()
    # Верхняя область
    app_bar_frame = Frame(app_frame)
    app_bar_frame.pack(side=TOP)
    countdown_text_label = Label(app_bar_frame, text='Время до завершения попытки: ')
    countdown_text_label.pack(side=LEFT, anchor=W, expand=1)
    countdown_label = Label(app_bar_frame, textvariable=seconds)
    countdown_label.pack(side=LEFT)

    end_test_button = Button(app_bar_frame, text='Завершить попытку', width=30, height=4,
                             command=lambda: (
                                 main_window.destroy(),
                                 quiz_result(student, answers, seconds.get())))
    end_test_button.pack(side=RIGHT, anchor=E)

    # Область теста
    app_quiz_frame = Frame(app_frame)
    app_quiz_frame.pack(side=BOTTOM)

    question_text = questions[current_question_index].text
    question_label = Label(app_quiz_frame, text=question_text, wraplength=220, justify=CENTER, )
    question_label.pack(side=TOP, pady=17)
    # Перемешивание вопросов
    available_answers = list.copy(questions[current_question_index].answers)
    random.shuffle(available_answers)

    # Кнопки ответов
    for answer in available_answers:
        answer_button = Button(app_quiz_frame, text=answer.text, width=30, height=6, wraplength=200,
                               justify=CENTER,
                               command=lambda: (
                                   answers.append(answer),
                                   choose_answer(main_window, student, current_question_index,
                                                 answers, seconds.get()),
                               )
                               )
        answer_button.pack(side=TOP)

    # Нижняя область
    app_bottom_frame = Frame(app_quiz_frame)
    app_bottom_frame.pack(side=BOTTOM)
    # Количество правильных ответов
    question_count_label = Label(app_bottom_frame, text='Вопрос {} из 10'.format(current_question_index + 1))
    question_count_label.pack(side=LEFT, anchor=W, expand=1)
    # Информация о студенте
    student_info_frame = Frame(app_bottom_frame)
    student_info_frame.pack(side=RIGHT)
    name_text_label = Label(student_info_frame, text='Имя - {}'.format(student.name))
    name_text_label.pack(side=TOP)
    group_text_label = Label(student_info_frame, text='Группа - {}'.format(student.group))
    group_text_label.pack(side=BOTTOM)
    # Запуск таймера
    update_timer()


# Вывод результата опросника
def quiz_result(student, answers, countdown_time):
    # Окно с результатами
    result_window = Toplevel(root)
    result_window.minsize(width=850, height=650)
    row_count = len(questions)
    table_frame = Frame(result_window)
    table_frame.pack(side=TOP, anchor=N)

    right_answers = 0
    # Прорисовка таблицы с правильными ответами
    for i in range(row_count):
        if len(answers) == 0 or answers[i] is None or not answers[i].is_right:
            color = 'red'
        else:
            color = 'green'
            right_answers += 1

        table_num_text = Label(table_frame, width=40, fg='black', text=i)
        table_num_text.grid(row=i + 1, column=0)
        table_your_answer_text = Label(
            table_frame, width=40, fg='black',
            text='Не выбрано'
            if len(answers) == 0
               or answers[i] is None
            else answers[i].text,
            bg=color,
            wraplength=250,
            justify=CENTER, )
        table_your_answer_text.grid(row=i + 1, column=1)
        table_right_answer_text = Label(table_frame, width=40, fg='black', text=questions[i].answers[0].text,
                                        wraplength=250,
                                        justify=CENTER, )
        table_right_answer_text.grid(row=i + 1, column=2)

    # Заголовки для таблицы
    header1_text = Label(table_frame, width=40, fg='black', text='#', wraplength=300, )
    header1_text.grid(row=0, column=0)
    header2_text = Label(table_frame, width=40, fg='black', text='Ваш ответ', wraplength=250, )
    header2_text.grid(row=0, column=1)
    header3_text = Label(table_frame, width=40, fg='black', text='Правильный ответ', wraplength=250, )
    header3_text.grid(row=0, column=2)

    # Нижнее меню
    bottom_frame = Frame(result_window)
    bottom_frame.pack(side=BOTTOM)
    # Кнопки управления (выход, главное меню)
    buttons_frame = Frame(bottom_frame)
    buttons_frame.pack(side=BOTTOM, anchor=S)
    exit_button = Button(buttons_frame, command=lambda: exit_program(), text='Выход', width=60, height=4)
    exit_button.pack(side=TOP)
    to_menu_button = Button(buttons_frame, command=lambda: (result_window.destroy()),
                            text='В главное меню', width=60, height=4)
    to_menu_button.pack(side=BOTTOM)
    # Результаты за тест
    results_frame = Frame(bottom_frame)
    results_frame.pack(side=TOP)
    right_answers_label = Label(results_frame,
                                text='Правильных ответов: {0} из {1}'.format(right_answers, len(questions)))
    right_answers_label.pack(side=TOP)
    time_label = Label(results_frame,
                       text='Время выполнения: {}'.format(str(countdown_time)))
    time_label.pack(side=BOTTOM)
    # Информация о студенте
    student_info_frame = Frame(results_frame)
    student_info_frame.pack(side=RIGHT)
    name_text_label = Label(student_info_frame, text='Имя - {}'.format(student.name))
    name_text_label.pack(side=TOP)
    group_text_label = Label(student_info_frame, text='Группа - {}'.format(student.group))
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
input_name_frame = Frame(start_frame)
input_name_frame.pack(side=TOP, pady=4, anchor=E, expand=1)
input_name_text_label = Label(input_name_frame, text='Введите имя:')
input_name_text_label.pack(side=LEFT)
input_name_entry = Entry(input_name_frame, width=30)
input_name_entry.pack(side=RIGHT)
# Ввода группы
input_group_frame = Frame(start_frame)
input_group_frame.pack(side=TOP, pady=4, anchor=E, expand=1)
input_group_text_label = Label(input_group_frame, text='Введите группу:')
input_group_text_label.pack(side=LEFT)
input_group_entry = Entry(input_group_frame, width=30)
input_group_entry.pack(side=RIGHT)
# Подготовка вопросов перед квестом
lines = read_quiz_file('quiz.csv')
questions = convert_lines_to_questions(lines)
# Кнопка начала теста
start_button = Button(start_frame, text='Начать тест', width=30, height=5, command=lambda: run())
start_button.pack(side=BOTTOM, expand=1, anchor=S)


# Заврешение программы при закрытии главного окна
def on_closing():
    root.destroy()
    exit()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Главный цикл
root.mainloop()
