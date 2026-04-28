def choice():
    # формирует текст меню и возвращает его
    return '1. Добавить задачу\n2. Посмотреть список задач\n3. Изменить задачу\n4. Удалить задачу\n5. Остановить программу'

def add_tasks():
    # режим добавления задач (работает в цикле до 'exit')
    while True:
        text_tasks = input('Введите Вашу задачу или exit для выхода из режима добавления задачи: ')
        if text_tasks.lower() == 'exit':
            return 'Вы вышли из режима добавления задач'  # выход из режима
        else:
            with open('tasks.txt', 'a', encoding='utf-8') as f:
                if not text_tasks.strip():
                    print('Пустой ввод')  # защита от пустых строк
                else:
                    f.write(text_tasks + '\n')  # добавление задачи в файл
                    print('Задача добавлена')

def format_tasks():
    # преобразует список задач в строку с нумерацией
    with open('tasks.txt', 'r', encoding='utf-8') as f:
        return '\n'.join(f'{i}: {task_.strip()}' for i, task_ in enumerate(f, start=1))

def list_task():
    # возвращает список задач или сообщение, если список пуст
    with open('tasks.txt', 'r', encoding='utf-8') as f:
        if not f.readline():
            return 'Список задач пуст'
    return format_tasks()

def edit_task():
    # режим редактирования задач
    while True:
        with open('tasks.txt', 'r', encoding='utf-8') as f:
            tasks_list = f.readlines()
            if not tasks_list:
                return 'Список задач пуст'  # нет задач для редактирования

        # вывод текущего списка
        print('Ваш текущий список задач: ', format_tasks(), sep ='\n')

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
                    tasks_list[index] = text + '\n'  # обновление задачи
                    with open('tasks.txt', 'w', encoding='utf-8') as f:
                        f.writelines(tasks_list)
                    print('Задача обновлена')
            else:
                print('Такой задачи нет в списке')
        except ValueError:
            print('Вводить нужно номер задачи')  # защита от нечислового ввода

def delete_task():
    while True:
        with open('tasks.txt', 'r', encoding='utf-8') as f:
            tasks_list = f.readlines()
            if not tasks_list:
                return 'Список задач пуст'  # нечего удалять

        # вывод списка задач
        print('Ваш список задач: ', format_tasks(), sep ='\n')

        # возможность удалить все задачи сразу
        number = input('''Удалить все задачи - введите "y";, 
Выйти из режима удаления - "exit";
Или выберите задачу для удаления: ''')
        if number.lower() == 'y':
            with open('tasks.txt', 'w', encoding='utf-8'):
                pass
            return 'Все задачи удалены'

        if number.lower() == 'exit':
            return 'Вы вышли из режима удаления'

        try:
            index = int(number) - 1  # перевод номера в индекс
            if 0 <= index < len(tasks_list):
                del tasks_list[index]  # удаление задачи по индексу
                with open('tasks.txt', 'w', encoding='utf-8') as f:
                    f.writelines(tasks_list)
                print('Задача удалена')
            else:
                print('Такой задачи нет в списке')
        except ValueError:
            print('Вводить нужно номер задачи')

def start(user_choice):
    with open('tasks.txt', 'a', encoding='utf-8'):
        pass

    # словарь: выбор пользователя -> функция
    choice_dict = {'1': add_tasks, '2': list_task, '3': edit_task, '4': delete_task}

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

    if task == '5':
        print('Всего хорошего!')
        break
    else:
        # вызов функции через start и вывод результата (если есть return)
        print(start(task))

        # повторный вывод меню
        print('\n', '''------------------------------------------------------------------------------------------------------
Продолжайте выбирать''')
        print(choice())