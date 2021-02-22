from tkinter import *
import time
from tkinter import messagebox
import pyodbc
from pynput import mouse

conn_str = ("Driver={SQL Server Native Client 11.0};" 
                          "Server=DESKTOP\SQLEXPRESS;" 
                          "Database=DB_Keyboard_Writing;" 
                          "Trusted_Connection=yes")

connection = pyodbc.connect(conn_str, autocommit=True)
dbCursor = connection.cursor()


key = Tk()  # key window name
key.geometry('700x325')  # normal size
key.configure(bg='#FFA07A')  # add background color
key.title("Identification")

# key.iconbitmap('add icon link And Directory name')    # icon add

# function coding start 
password = ""  # global variable
# showing all data in display
speed_print = 0
input_dynamics = 0
count_but = 0
start_time = 0
number_input = 0

def press(num):
    global start_time
    global count_but
    global login
    login = Login_entry.get()
    cursor = connection.cursor()
    request = "SELECT COUNT(*) FROM Користувачі WHERE Ім_яКористувача = '" + login + "'"
    cursor.execute(request)
    count = cursor.fetchall()
    if count[0][0] == 0:
        warning = messagebox.showerror('Увага!', 'Такого користувача не існує!')
    else:
        request_max = "SELECT MAX(Номер_входу) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'"
        cursor.execute(request_max)
        number_input = cursor.fetchall()
        if number_input[0][0] == None:
            number_input[0][0] = 0
        st_time_but = time.perf_counter()
        if count_but == 0:
            start_time = time.perf_counter()
        global password
        password += num
        equation.set(password)
        cursor = connection.cursor()
        request = "INSERT INTO Таймери(Ім_яКористувача, Номер_входу, Клавіша, Час_утримання, Квадратичне_відхилення)" \
                  " VALUES (?, ?, ?, ?, ?);"
        fin_time_but = time.perf_counter()
        if count_but == 0:
            cursor.execute(request, (login, int(number_input[0][0]+1), num, fin_time_but - st_time_but, 0))
        else:
            cursor.execute(request, (login, int(number_input[0][0]+1), num, fin_time_but - st_time_but, 0))
        connection.commit()
        count_but += 1
# end
# function clear button

def clear():
    global password
    password = " "
    equation.set(password)
# end



def action(cursor):
    global start_time
    global password
    global speed_print
    global number_input
    i = 0.5
    input = 0
    end_time = time.perf_counter()
    length_pass = len(password)
    if len(password)!=0:
        speed_print = (end_time - start_time) / length_pass
    login = Login_entry.get()
    cursor = connection.cursor()
    request = "SELECT COUNT(*) FROM Користувачі WHERE Ім_яКористувача = '" + login + "'"
    cursor.execute(request)
    count = cursor.fetchall()
    if count[0][0] == 0:
        warning = messagebox.showerror('Увага!', 'Такого користувача не існує!')
    request_p = "SELECT COUNT(*) FROM Користувачі WHERE Пароль = '" + password + "' AND Ім_яКористувача = '" + login + "'"
    cursor.execute(request_p)
    count_p = cursor.fetchall()
    if count_p[0][0] == 0:
        warning = messagebox.showerror('Увага!', 'Не коректно введено пароль!')
    if count[0][0] == 1 and count_p[0][0] == 1:
        request_max = "SELECT MAX(Номер_входу) FROM Швидкість_час WHERE Ім_яКористувача='"+ login + "'"
        cursor.execute(request_max)
        number_input = cursor.fetchall()
        if number_input[0][0] == None:
            number_input[0][0] = 0
        insert = "INSERT INTO Швидкість_час(Ім_яКористувача, Номер_входу, Швидкість_набору, Загальний_час_набору)" \
                 " VALUES (?, ?, ?, ?);"
        cursor.execute(insert, (login, int(number_input[0][0]+1), speed_print, end_time - start_time))
        connection.commit()
        for i in range(len(password)):
            select = "SELECT AVG(Час_утримання) FROM Таймери WHERE Клавіша='" + password[i] + "' AND Ім_яКористувача='" \
                     + login + "'AND Номер_входу<6"
            sel_stdev = "SELECT STDEV(Час_утримання) FROM Таймери WHERE Клавіша='" + password[i] + "' AND Ім_яКористувача='" \
                     + login + "'AND Номер_входу<6"
            sel_numder = "SELECT COUNT(*) FROM Таймери WHERE Клавіша='" + password[i] + "' AND Ім_яКористувача = '" + login + \
                         "'AND Номер_входу<6"
            insert = "INSERT INTO Налаштування(Ім_яКористувача, Клавіша, Середнє_значення, Квадратичне_відхилення, Кількість)" \
                     " VALUES (?, ?, ?, ?, ?)"
            sel_avg_speed= "SELECT AVG(Швидкість_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу<6"
            sel_time = "SELECT AVG(Загальний_час_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу<6"
            sel_stdev_time = "SELECT STDEV(Загальний_час_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу<6"
            sel_stdev_speed = "SELECT STDEV(Швидкість_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу<6"

            cursor.execute(sel_avg_speed)
            avg_speed = cursor.fetchall()
            cursor.execute(sel_time)
            time1 = cursor.fetchall()
            cursor.execute(sel_stdev_time)
            stdev_time = cursor.fetchall()
            cursor.execute(sel_stdev_speed)
            stdev_speed = cursor.fetchall()

            if number_input[0][0] > 5:
                select2 = "SELECT AVG(Час_утримання) FROM Таймери WHERE Клавіша='" + password[
                    i] + "' AND Ім_яКористувача='" \
                         + login + "' AND Номер_входу>5"
                sel_stdev2 = "SELECT STDEV(Час_утримання) FROM Таймери WHERE Клавіша='" + password[
                    i] + "' AND Ім_яКористувача='" \
                            + login + "'AND Номер_входу>5"
                sel_numder2 = "SELECT COUNT(*) FROM Таймери WHERE Клавіша='" + password[
                    i] + "' AND Ім_яКористувача = '" + login + "'AND Номер_входу>5"
                insert2 = "INSERT INTO Ідентифікація(Ім_яКористувача, Клавіша, Середнє_значення, Квадратичне_відхилення, Кількість)" \
                         " VALUES (?, ?, ?, ?, ?)"
                sel_n = "SELECT COUNT(*) FROM Налаштування WHERE Клавіша = '" + password[i] + "'"
                sel_avg_speed2 = "SELECT AVG(Швидкість_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу>5"
                sel_time2 = "SELECT AVG(Загальний_час_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу>5"
                sel_stdev_time2 = "SELECT STDEV(Загальний_час_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу>5"
                sel_stdev_speed2 = "SELECT STDEV(Швидкість_набору) FROM Швидкість_час WHERE Ім_яКористувача='" + login + "'AND Номер_входу>5"

                cursor.execute(sel_n)
                n = cursor.fetchall()

                cursor.execute(select2)
                avg2 = cursor.fetchall()

                cursor.execute(sel_stdev2)
                sel_stdev2 = cursor.fetchall()

                cursor.execute(sel_numder2)
                sel_numder2 = cursor.fetchall()

                cursor.execute(sel_avg_speed2)
                avg_speed2 = cursor.fetchall()

                cursor.execute(sel_time2)
                time2 = cursor.fetchall()

                cursor.execute(sel_stdev_time2)
                stdev_time2 = cursor.fetchall()

                cursor.execute(sel_stdev_speed2)
                stdev_speed2 = cursor.fetchall()

                if sel_stdev2[0][0] == None:
                    sel_stdev2[0][0] = 0
                cursor.execute(insert2, (login, password[i], avg2[0][0], sel_stdev2[0][0], sel_numder2[0][0]))
                cursor.execute(select)
                avg = cursor.fetchall()
                cursor.execute(sel_stdev)
                sel_stdev = cursor.fetchall()
                cursor.execute(sel_numder)
                sel_numder = cursor.fetchall()
                t = (avg[0][0] - avg2[0][0])/((((sel_stdev[0][0]**2)/n[0][0])+(sel_stdev2[0][0]**2)/n[0][0])**0.5)
                f = sel_stdev[0][0]**2/sel_stdev2[0][0]**2

                t_s = (avg_speed[0][0] - avg_speed2[0][0])/((((stdev_speed[0][0]**2)/number_input[0][0])+(stdev_speed2[0][0]**2)/number_input[0][0])**0.5)
                f_s = (stdev_speed[0][0]**2)/(stdev_speed2[0][0]**2)

                t_t = (time1[0][0] - time2[0][0])/((((stdev_time[0][0]**2)/number_input[0][0])+(stdev_time2[0][0]**2)/number_input[0][0])**0.5)
                f_t = (stdev_time[0][0]**2)/(stdev_time2[0][0]**2)

                if t>1:
                    input+=1
                connection.commit()
            else:
                cursor.execute(select)
                avg = cursor.fetchall()
                cursor.execute(sel_stdev)
                sel_stdev = cursor.fetchall()
                cursor.execute(sel_numder)
                sel_numder = cursor.fetchall()
                if sel_stdev[0][0] == None:
                    sel_stdev[0][0] = 0
                cursor.execute(insert, (login, password[i], avg[0][0], sel_stdev[0][0], sel_numder[0][0]))
                connection.commit()
        if speed_print==0:
            result = messagebox.showerror('Увага!', 'Несанкціонований доступ!')
        if number_input[0][0] < 6:
            info = "Для завершення налаштувань необхідно вийти з програми і зайти знову для ведення паролю ще " +\
                   str((5-number_input[0][0])) + ' разів'
            result = messagebox.showinfo('Увага!', info)
        else:
            if (input / len(password) > 0.6) or (f > 2) or (t_s > 2.9) or (f_s > 161) or (t_t > 2.9) or (f_t > 161):
                result = messagebox.showerror('Увага!', 'Несанкціонований доступ!')
            else:
                result = messagebox.showinfo('Вітаємо!', 'Ви увійшли до системи')


app = Frame(key)
app.grid()
lb = Label(text="Введіть, будь ласка, ім_я користувача та логін, яку були видані адміністратором", background='#555', foreground='#ccc', font="Arial 14")
lb.grid(row=0, columnspan=16)
equation = StringVar()
Login_entry = Entry(key)
Login_entry.grid(row=1, columnspan=100, ipadx=999, ipady=10)
Dis_entry = Entry(key, state='readonly', textvariable=equation)
Dis_entry.grid(row=2, columnspan=100, ipadx=999, ipady=10)
# end entry box
# add all button line wise 

# 1-3 Line Button
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '1', '2', '3'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '@', '4', '5', '6'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '*', '+', '_', '7', '8', '9']]
buttons = []
for i in range(3):
    for j in range(13):
        buttons.append(Button(key, text=keys[i][j], background='#555', foreground='#ccc', font="Arial 14"))
count_line = 3
for i, x in enumerate(buttons):
    if i % 13 == 0:
        count_line += 1
    x.grid(row=count_line, column=i % 13 + 1, padx=1, pady=5)

buttons[0].config(command=lambda: press(keys[0][0]))
buttons[1].config(command=lambda: press(keys[0][1]))
buttons[2].config(command=lambda: press(keys[0][2]))
buttons[3].config(command=lambda: press(keys[0][3]))
buttons[4].config(command=lambda: press(keys[0][4]))
buttons[5].config(command=lambda: press(keys[0][5]))
buttons[6].config(command=lambda: press(keys[0][6]))
buttons[7].config(command=lambda: press(keys[0][7]))
buttons[8].config(command=lambda: press(keys[0][8]))
buttons[9].config(command=lambda: press(keys[0][9]))
buttons[10].config(command=lambda: press(keys[0][10]))
buttons[11].config(command=lambda: press(keys[0][11]))
buttons[12].config(command=lambda: press(keys[0][12]))
buttons[13].config(command=lambda: press(keys[1][0]))
buttons[14].config(command=lambda: press(keys[1][1]))
buttons[15].config(command=lambda: press(keys[1][2]))
buttons[16].config(command=lambda: press(keys[1][3]))
buttons[17].config(command=lambda: press(keys[1][4]))
buttons[18].config(command=lambda: press(keys[1][5]))
buttons[19].config(command=lambda: press(keys[1][6]))
buttons[20].config(command=lambda: press(keys[1][7]))
buttons[21].config(command=lambda: press(keys[1][8]))
buttons[22].config(command=lambda: press(keys[1][9]))
buttons[23].config(command=lambda: press(keys[1][10]))
buttons[24].config(command=lambda: press(keys[1][11]))
buttons[25].config(command=lambda: press(keys[1][12]))
buttons[26].config(command=lambda: press(keys[2][0]))
buttons[27].config(command=lambda: press(keys[2][1]))
buttons[28].config(command=lambda: press(keys[2][2]))
buttons[29].config(command=lambda: press(keys[2][3]))
buttons[30].config(command=lambda: press(keys[2][4]))
buttons[31].config(command=lambda: press(keys[2][5]))
buttons[32].config(command=lambda: press(keys[2][6]))
buttons[33].config(command=lambda: press(keys[2][7]))
buttons[34].config(command=lambda: press(keys[2][8]))
buttons[35].config(command=lambda: press(keys[2][9]))
buttons[36].config(command=lambda: press(keys[2][10]))
buttons[37].config(command=lambda: press(keys[2][11]))
buttons[38].config(command=lambda: press(keys[2][12]))

# Fourth Line Button
space = Button(key, text='Space', width=6, background='#555', foreground='#ccc', font="Arial 14", command=lambda: press(' '))
space.grid(row=7, columnspan=7, ipadx=100, pady=5)

enter = Button(key, text='Enter', width=6, background='#555', foreground='#ccc', font="Arial 14", command=lambda: action(connection))
enter.grid(row=7, columnspan=16, padx=20, pady=5)

clear = Button(key, text='Clear', width=6, background='#555', foreground='#ccc', font="Arial 14", command=clear)
clear.grid(row=7, columnspan=26, padx=20, pady=5)




key.mainloop()  # using ending point


