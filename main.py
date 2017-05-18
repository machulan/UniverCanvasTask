from tkinter import *
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter.ttk import *

from constants import *

# from tkinter.filedialog import askopenfilename, askdirectory
# from tkinter.colorchooser import askcolor
# from tkinter.messagebox import askquestion, showerror
# from tkinter.simpledialog import askfloat

canvas = None


def open_image():
    filename = askopenfilename(initialdir=r'C:\Users\User\PycharmProjects\UniverCanvasTask\resourses', initialfile='image.png',
                               title='Открыть изображение', filetypes=[('png files', '.png'), ('jpg files', '.jpg')],
                               defaultextension='.png')

    # print(file.name)
    image = PhotoImage(file=filename)
    # gradient_image = PhotoImage(file='gradient.png')
    global canvas

    canvas.delete(ALL)
    # canvas.create_line(100, 100, 200, 200)  # fromX, fromY, toX, toY
    # canvas.create_line(100, 200, 200, 300)
    canvas.config(scrollregion=(0, 0, image.width(), image.height()))
    canvas.create_image(0, 0, image=image, anchor=NW)
    canvas.image = image
    canvas.focus_set()
    # canvas.config(bg='blue')

    # canvas.create_image(325, 25, image=image, anchor=NW)
    # canvas.create_oval(10, 10, 200, 200, width=2, fill='blue')

    # askopenfilename(initialdir='C:\\wamp64', initialfile='неизвестный ФАЙЛ',
    #                           title='НАЗВАНИЕ ДИАЛОГА', defaultextension='txt'),
    # filetypes = [('sql files', '.sql'), ('all files', '.*')], defaultextension = '.sql


def open_help(root):
    window = Toplevel(root)
    label = Label(window)
    label.pack(expand=YES, fill=BOTH)
    text_data = """    При выборе пункта <Открыть> открывается диалоговое окно
для выбора файла с изображением, после выбора изображение
размещается на виджете Canvas.

    При выборе пункта <Построить график> открывается
вспомогательное окно, где будет возможность выбрать один
из видов функций (sin x, cos x, tg x, ctg x, x^2, x^3) и
диапазон значений x, после введения необходимых данных
строится график функции на виджете Canvas основного окна.

    При выборе пункта <Выход> окно закрывается."""
    label.config(text=text_data, font=HELP_TEXT_FONT, justify=LEFT)

    confirm_button = Button(window, text='ОК')
    confirm_button.pack(expand=YES, fill=Y, padx=10, pady=10)
    confirm_button.config(width=10)
    # confirm_button.config(height=50)
    # confirm_button.config(font=HELP_CONFIRM_BUTTON_FONT)
    confirm_button.config(command=window.destroy)

    window.focus_set()
    window.grab_set()
    window.wait_window()


def draw_chart(root, window, function_name, x_from, x_to):
    window.destroy()
    # print(FUNCTIONS[5](2))
    print('FUNCTION NAME :', function_name)
    # print(help(Combobox))
    pos = FUNCTION_NAMES.index(function_name)
    function = FUNCTIONS[pos]
    print('Trying to draw chart of ' + function_name + '(' + str(x_from) + ', ' + str(x_to) + ')')

    global canvas
    canvas.delete(ALL)
    print('DRAW_CHART :: CANVAS CLEARED')
    # canvas.create_line(100, 100, 101.5, 100)

    # canvas.config(scrollregion=(0, 0, image.width(), image.height()))

    # print('DRAW_CHART :: req', root.winfo_reqwidth(), root.winfo_reqheight())
    # canvas.create_line(100, 100, 382 * 2, 269 * 2)
    print('DRAW_CHART :: [ WIDTH :', root.winfo_width(), 'HEIGHT :', root.winfo_height(), ']')

    width = root.winfo_width()
    height = root.winfo_height()
    center = (width / 2, height / 2)

    coef = (x_to - x_from) / width
    x_middle = -x_from / (x_to - x_from) * width
    y_middle = height / 2

    # drawing axes
    # x
    canvas.create_line(0, y_middle, width, y_middle, dash=(5, 5), fill='black', width=2)
    # y
    canvas.create_line(x_middle, 0, x_middle, height, dash=(5, 5), fill='black', width=2)

    # x_from => 0
    # x_to => width

    def f(x):
        try:
            result = (-1) * function(x)
        except ZeroDivisionError:
            return INFINITY
        return result


    # prev = (0, function(x_from) / coef

    # canvas.create_line(center[0], center[1], center[0] + 100, center[1] - 100)

    prev = (0, f(-x_middle * coef) / coef)
    for x_s in range(1, width):
        x = (x_s - x_middle) * coef
        y = f(x)
        y_s = y / coef
        if 0 <= prev[1] + y_middle < height and 0 <= y_s + y_middle < height:
            line = canvas.create_line(prev[0], prev[1] + y_middle, x_s, y_s + y_middle)
            canvas.itemconfig(line, fill='blue', width=2)
        prev = (x_s, y_s)


def check_values(from_entry, to_entry):
    # x_from = from_entry.getdouble(2)
    # x_to = to_entry.getdouble(2)
    x_from = from_entry.get()
    x_to = to_entry.get()

    print('CHECK_VALUES :: ', x_from, x_to)

    try:
        print(float(x_from), float(x_to))
    except ValueError:
        print('Not numbers')
        return False
    print('Numbers', '<' if x_from < x_to else '>=')
    return float(x_from) < float(x_to)


def draw_chart_dialog(root):
    window = Toplevel(root)
    window.title('Выбор графика')
    window.maxsize(width=250, height=250)
    window.resizable(width=False, height=False)

    combobox = Combobox(window, values=FUNCTION_NAMES)
    combobox.config(width=8, height=4)
    combobox.config(justify=CENTER)
    # combobox.set('sin(x)')
    combobox.set('sin')
    combobox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    combobox.focus_set()

    from_label = Label(window)
    from_label.grid(row=1, column=0, padx=5, pady=5)
    from_label.config(text='От')

    from_entry = Entry(window)
    from_entry.grid(row=1, column=1, padx=5, pady=5)
    from_entry.insert(0, str(DEFAULT_BEGIN_VALUE))

    to_label = Label(window)
    to_label.grid(row=2, column=0, padx=5, pady=5)
    to_label.config(text='До')

    to_entry = Entry(window)
    to_entry.grid(row=2, column=1, padx=5, pady=5)
    to_entry.insert(0, str(DEFAULT_END_VALUE))

    toolbar_frame = Frame(window)
    toolbar_frame.grid(row=3, column=0, columnspan=2)

    confirm_button = Button(toolbar_frame, text='ОК')
    confirm_button.pack(side=LEFT, padx=5, pady=5)
    confirm_button.config(
        command=(
            lambda: check_values(from_entry, to_entry)
                    and draw_chart(root, window, combobox.get(), float(from_entry.get()), float(to_entry.get()))))

    cancel_button = Button(toolbar_frame, text='Отмена')
    cancel_button.pack(side=RIGHT, padx=5, pady=5)
    global canvas
    cancel_button.config(command=(lambda: canvas.delete(ALL) or window.destroy()))

    # window.rowconfigure(i, weight=1)

    window.focus_set()
    window.grab_set()
    window.wait_window()


def make_menu(root):
    root_menu = Menu(root)
    root.config(menu=root_menu)

    file_menu = Menu(root_menu, tearoff=False)
    file_menu.add_command(label='Открыть', command=(lambda: open_image()))
    file_menu.add_command(label='Построить график', command=(lambda: draw_chart_dialog(root)))
    file_menu.add_separator()
    file_menu.add_command(label='Выход', command=root.quit)
    root_menu.add_cascade(label='Файл', menu=file_menu)

    help_menu = Menu(root_menu, tearoff=False)
    # help_menu.add_command(label='Просмотреть справку')
    # help_menu.add_separator()
    help_menu.add_command(label='О программе', command=(lambda: open_help(root)))
    root_menu.add_cascade(label='Справка', menu=help_menu)


def make_canvas(root):
    global canvas
    canvas = Canvas(root, bg='#FFC')
    canvas.config(scrollregion=(0, 0, 800, 500))

    yscrollbar = Scrollbar(root)
    yscrollbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=yscrollbar.set)
    yscrollbar.pack(side=RIGHT, fill=Y)

    xscrollbar = Scrollbar(root, orient=HORIZONTAL)
    xscrollbar.config(command=canvas.xview)
    canvas.config(xscrollcommand=xscrollbar.set)
    xscrollbar.pack(side=BOTTOM, fill=X)

    canvas.pack(expand=YES, fill=BOTH)


root = Tk()
root.title('Canvas')
root.state('zoomed')
# root.minsize(width=800, height=500)
# print(root.winfo_reqwidth())
root.resizable(width=FALSE, height=FALSE)
make_menu(root)
make_canvas(root)
root.mainloop()
