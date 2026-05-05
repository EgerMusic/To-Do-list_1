def choice():
    # формирует текст меню и возвращает его
    return '1. Добавить задачу\n2. Посмотреть список задач\n3. Изменить задачу\n4. Удалить задачу\n5. Изменить статус задачи\n6. Остановить программу'

def load_tasks():
    try:
        with open('tasks.txt', 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def save_tasks(tasks_list):
    with open('tasks.txt', 'w', encoding='utf-8') as f:
        f.writelines(tasks_list)

def dict_task_and_status(list_tasks):
    dict_tasks = {}
    for t in list_tasks:
        t, s = t.split('|')
        dict_tasks[t.strip()] = s.strip()
    return dict_tasks

def add_tasks():
    # режим добавления задач (работает в цикле до 'exit')
    while True:
        text_tasks = input('Введите Вашу задачу или exit для выхода из режима добавления задачи: ')
        if text_tasks.lower() == 'exit':
            return 'Вы вышли из режима добавления задач'  # выход из режима
        elif not text_tasks.strip():
            print('Пустой ввод')  # защита от пустых строк
        else:
            tasks = load_tasks()
            tasks.append(text_tasks + ' | False\n')
            print('Задача добавлена')
            save_tasks(tasks)

def format_tasks(tasks):
    # преобразует список задач в строку с нумерацией
    return '\n'.join(f'{i}: {task_.strip()}' for i, task_ in enumerate(tasks, start=1))

def list_task():
    # возвращает список задач или сообщение, если список пуст
    tasks = load_tasks()
    if not tasks:
        return 'Список задач пуст'
    return format_tasks(tasks)

def edit_task():
    # режим редактирования задач
    while True:
        tasks_list = load_tasks()
        if not tasks_list:
            return 'Список задач пуст'  # нет задач для редактирования

        # вывод текущего списка
        print('Ваш текущий список задач: ', format_tasks(tasks_list), sep ='\n')

        number = input('Выберите задачу для редактирования или введите exit для выхода из этого режима: ')
        if number.lower() == 'exit':
            return 'Вы вышли из режима редактирования'
        try:
            index = int(number) - 1  # перевод номера в индекс списка
            if 0 <= index < len(tasks_list):
                text = input('Введите обновление в задачу: ')
                if not text.strip():
                    print('Пустой ввод')  # защита от пустого редактирования
                else:
                    temp = tasks_list[index]
                    tasks_list[index] = text + temp[temp.index('|') - 1:]   # Обновление задачи с учетом нового введенного текста плюс статус задачи (т.е. то, что идет после '|')
                    save_tasks(tasks_list)
                    print('Задача обновлена')
            else:
                print('Такой задачи нет в списке')
        except ValueError:
            print('Вводить нужно номер задачи')  # защита от нечислового ввода

def delete_task():
    while True:
        tasks_list = load_tasks()
        if not tasks_list:
            return 'Список задач пуст'  # нечего удалять

        # вывод списка задач
        print('Ваш список задач: ', format_tasks(tasks_list), sep ='\n')

        # возможность удалить все задачи сразу
        number = input('''Удалить все задачи - введите "y";
Выйти из режима удаления - "exit";
Или выберите задачу для удаления: ''')
        if number.lower() == 'y':
            save_tasks([])
            return 'Все задачи удалены'

        if number.lower() == 'exit':
            return 'Вы вышли из режима удаления'

        try:
            index = int(number) - 1  # перевод номера в индекс
            if 0 <= index < len(tasks_list):
                del tasks_list[index]  # удаление задачи по индексу
                save_tasks(tasks_list)
                print('Задача удалена')
            else:
                print('Такой задачи нет в списке')
        except ValueError:
            print('Вводить нужно номер задачи')

def task_status():
    while True:
        tasks_list = load_tasks()
        temp_dict = dict_task_and_status(tasks_list)
        if not temp_dict:
            return 'Список задач пуст'

        print('Ваш список задач: ', format_tasks(tasks_list), sep='\n')

        number = input('''Изменить статусы всех задач все задачи на "Не выполнено" (f) или "Выполнено" (t). Введите "f" или "t"
Выйти из режима удаления - "exit";
Или выберите задачу для изменения ее статуса: ''')
        if number.lower() == 't':
            temp_dict = temp_dict.fromkeys(temp_dict.keys(), 'Выполнено\n')
            return_list = [f'{k} | {v}' for k, v in temp_dict.items()]
            save_tasks(return_list)
        elif number.lower() == 'f':
            temp_dict = temp_dict.fromkeys(temp_dict.keys(), 'Не выполнено\n')
            return_list = [f'{k} | {v}' for k, v in temp_dict.items()]
            save_tasks(return_list)
        elif number.lower() == 'exit':
            return 'Вы вышли из режима изменения статуса'
        else:
            try:
                index = int(number)  # перевод номера в индекс
                if 0 <= index - 1 < len(tasks_list):
                    temp_dict[number] = input('Введите обновленный статус задачи: ')
                    return_list = [f'{k} | {v + "\n"}' for k, v in temp_dict.items()]
                    save_tasks(return_list)
                    print('Статус задачи изменен')
                else:
                    print('Такой задачи нет в списке')
            except ValueError:
                print('Вводить нужно номер задачи')


def start(user_choice):
    # словарь: выбор пользователя -> функция
    choice_dict = {'1': add_tasks, '2': list_task, '3': edit_task, '4': delete_task, '5': task_status}

    # получение функции по ключу
    func = choice_dict.get(user_choice)

    # если введён неверный вариант
    if func is None:
        return 'Такого варианта нет, выберите другое действие'

    # вызов выбранной функции с передачей списка задач
    return func()

print('''------------------------------------------------------------------------------------------------------
Добро пожаловать в задачник!
Ниже представлен основной функционал программы (просьба выбрать действие по соответствующему ему номеру):''')

print(choice())  # вывод меню

while True:
    task = input('Введите номер действия: ')

    if task == '6':
        print('Всего хорошего!')
        break
    else:
        # вызов функции через start и вывод результата (если есть return)
        print(start(task))

        # повторный вывод меню
        print('\n', '''------------------------------------------------------------------------------------------------------
Продолжайте выбирать''')
        print(choice())