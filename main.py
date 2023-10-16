import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    def init_main(self):
        # создание панели инструментов
        toolbar = tk.Frame(bg='grey', bd=3)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # создание кнопки добавления сотрудника
        self.img_add = tk.PhotoImage(file = 'img/add.png')
        btn_add = tk.Button(toolbar, bg='grey', bd = 0, image=self.img_add, command=self.open_add)
        btn_add.pack(side=tk.LEFT)

        # создание кнопки редактирования сотрудника
        self.img_edit = tk.PhotoImage(file = 'img/edit.png')
        btn_edit = tk.Button(toolbar, bg='grey', bd=0, image=self.img_edit, command=self.open_edit)
        btn_edit.pack(side=tk.LEFT)

        # создание кнопки удаления сотрудника
        self.img_delete = tk.PhotoImage(file = 'img/delete.png')
        btn_delete = tk.Button(toolbar, bg='grey', bd=0, image=self.img_delete, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # создание кнопки поиска
        self.img_search = tk.PhotoImage(file = 'img/search.png')
        btn_search = tk.Button(toolbar, bg='grey', bd=0, image=self.img_search, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # создание кнопки обновления таблицы
        self.img_refresh = tk.PhotoImage(file = 'img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='grey', bd=0, image=self.img_refresh, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # создание таблицы
        self.tree = ttk.Treeview(root,
                                 columns=('id','name','phone','email','salary'),
                                 height=15,
                                 show='headings')
        # создание колонок
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=70, anchor=tk.CENTER)

        # название для колонок
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        self.tree.heading('salary', text='Зарплата')

        # размещаем таблицу
        self.tree.pack(side=tk.LEFT)

        # создание полосы прокрутки
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # функция вывода данных
    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('''SELECT * FROM employees''')
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # функция добавления данных
    def add_records(self, name, phone, email, salary):
        # проверяем все ли поля заполнены
        if name!='' and phone!='' and email!='' and salary!='':
            self.db.insert_data(name, phone, email, salary)
            self.view_records()
        else:
            # выводим ошибку
            messagebox.showerror('Ошибка','Не все поля заполнены')

    # функция редактирования данных
    def edit_records(self, name, phone, email, salary):
        # проверяем все ли поля заполнены
        if name!='' and phone!='' and email!='' and salary!='':
            # берём id сотрудника
            id = self.tree.set(self.tree.selection()[0], '#1')
            # удаляем по id
            self.db.cur.execute('''
            UPDATE employees SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
            ''', (name, phone, email, salary, id))
            self.db.conn.commit()
            self.view_records()
        else:
            # выводим ошибку
            messagebox.showerror('Ошибка','Не все поля заполнены')

    # функция удаления данных
    def delete_records(self):
        # проверям выделено ли что-то
        if self.tree.selection() == ():
            # окно ошибки, если сотрудник не выделен при удалении
            messagebox.showerror('Ошибка', 'Не выделен сотрудник')
        else:
            # рассматриваем все выделенные строки
            for selected in self.tree.selection():
                    # берем id каждого сотрудника
                    id = self.tree.set(selected, '#1')
                    # удаляем по этому id
                    self.db.cur.execute('''
                        DELETE FROM employees WHERE id = ?
                    ''', (id, ))
            self.db.conn.commit()
            self.view_records()

    # функция поиска данных
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('''SELECT * FROM employees WHERE name LIKE ?''',
                            ('%' + name + '%', ))
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # функция открытия окна добавления
    def open_add(self):
        Add()

    # функция открытия окна редактирования
    def open_edit(self):
        Edit()

    # функция открытия окна поиска
    def open_search(self):
        Search()

# класс окна добавления
class Add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add()
        self.app = app

    def init_add(self):
        # название для окна
        self.title('Добавить сотрудника')
        # размер окна
        self.geometry('400x200')
        # смена цвета окна
        self.configure(bg='#d7d7d7')
        # запрет на изменение окна
        self.resizable(False, False)
        # захватываем все события приложения
        self.grab_set()
        # захватываем фокус
        self.focus_set()

        # создание формы
        label_name = tk.Label(self, text='ФИО', bg='#d7d7d7')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон', bg='#d7d7d7')
        label_phone.place(x=50, y=70)
        label_email = tk.Label(self, text='Email', bg='#d7d7d7')
        label_email.place(x=50, y=90)
        label_salary = tk.Label(self, text='Зарплата', bg='#d7d7d7')
        label_salary.place(x=50, y=110)

        # создание полей ввода
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.place(x=120, y=50)
        self.entry_phone = tk.Entry(self, width=30)
        self.entry_phone.place(x=120, y=70)
        self.entry_email = tk.Entry(self, width=30)
        self.entry_email.place(x=120, y=90)
        self.entry_salary = tk.Entry(self, width=30)
        self.entry_salary.place(x=120, y=110)

        # создание кнопки добавления
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.app.add_records(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            self.entry_salary.get(),
        ))
        self.btn_ok.place(x=120, y=150)

        # создание кнопки закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=190, y=150)

# класс окна редактирования (наследуется от класса добавленя)
class Edit(Add):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_edit()
        self.load_records()

    def init_edit(self):
        # название окна
        self.title('Редактирование данных')
        # убираем кнопку добавления
        self.btn_ok.destroy()
        # добавляем кнопку редактирования
        self.btn_ok = tk.Button(self, text='Редактировать')
        self.btn_ok.bind('<Button-1>', lambda ev: self.app.edit_records(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            self.entry_salary.get(),
        ))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy, add="+")
        self.btn_ok.place(x=120, y=150)
        self.btn_cancel.place(x=220, y=150)

    # функция, загружающая данные в поля для ввода
    def load_records(self):
        try:
            self.db.cur.execute('''SELECT * FROM employees WHERE id = ?''', self.app.tree.set(self.app.tree.selection()[0], '#1'))
            row = self.db.cur.fetchone()
            self.entry_name.insert(0, row[1])
            self.entry_phone.insert(0, row[2])
            self.entry_email.insert(0, row[3])
            self.entry_salary.insert(0, row[4])
        except:
            self.destroy()
            # окно ошибки, если сотрудник не выделен при редактировании
            messagebox.showerror('Ошибка', 'Не выделен сотрудник')

# класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.app = app
        self.init_search()

    def init_search(self):
        # название для окна
        self.title('Добавить сотрудника')
        # размер окна
        self.geometry('300x100')
        # смена цвета окна
        self.configure(bg='#d7d7d7')
        # запрет на изменение окна
        self.resizable(False, False)
        # захватываем все события приложения
        self.grab_set()
        # захватываем фокус
        self.focus_set()

        # создание строки поиска
        label_search = tk.Label(self, text='Введите ФИО', bg='#d7d7d7')
        label_search.place(x=10,y=30)
        self.entry_search = tk.Entry(self, width=30)
        self.entry_search.place(x=100,y=30)

        # создание кнопки добавления
        btn_ok = tk.Button(self, text='Найти')
        btn_ok.bind('<Button-1>', lambda ev: self.app.search_records(self.entry_search.get()))
        btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        btn_ok.place(x = 170, y = 60)

        #создание кнопки закрытия
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=227, y=60)

# класс базы данных
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                salary INTEGER NOT NULL
            )
        ''')

    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
            INSERT INTO employees (name, phone, email, salary)
            VALUES (?,?,?,?)''', (name, phone, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    # создание главного окна
    root = tk.Tk()
    # создание базы данных
    db = Db()
    app = Main(root)
    # название для главного окна
    root.title('Список сотрудников компании')
    # размер главного окна
    root.geometry('735x400')
    # запрет на изменение размера главного окна
    root.resizable(False, False)
    # запуск
    root.mainloop()