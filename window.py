try:
    import tkinter.ttk as ttk
except ImportError:
    import tkinter as ttk
finally:
    import tkinter
    from functools import reduce
    import console
    import ops
    import pics
    import pic2py


__keyboard_img = None


def _get_keyboard_img():
    global __keyboard_img
    if __keyboard_img is None:
        pic2py.generate_pic(pics.kbs_gif, 'kbs.gif')
        __keyboard_img = tkinter.PhotoImage(file='kbs.gif')
    return __keyboard_img


class ButtonBoard:
    class KeyButton:
        def __init__(self, master_frame, modes: list):
            self.modes = modes
            self.status = tkinter.IntVar(master=master_frame, value=0)
            self.button = tkinter.Button(master_frame, font=(('consolas', 13) if modes[0][0].find('\n') == -1
                                                             else ('consolas', 8)),
                                         background='#CCE', foreground='#333',
                                         borderwidth=0, text=modes[0][0],
                                         width=(7 if modes[0][0].find('\n') == -1 else 10),
                                         command=modes[0][1])

        def switch(self, num):
            if 0 <= self.status.get() + num < len(self.modes):
                self.status.set(self.status.get() + num)
                self.button.config(text=self.modes[self.status.get()][0], command=self.modes[self.status.get()][1],
                                   font=(('consolas', 13) if self.modes[self.status.get()][0].find('\n') == -1
                                         else ('consolas', '8')))

    class SwitchButton:
        def __init__(self, master_frame, text, command):
            self.button_on = tkinter.BooleanVar(master=master_frame, value=False)
            self.button = tkinter.Button(master_frame, font=('consolas', 13), background='#CCE', foreground='#333',
                                         borderwidth=0, text=text, width=7,
                                         command=lambda: (self.button_on.set(not self.button_on.get()),
                                                          self.button.config(background='#EEE')
                                                          if self.button_on.get()
                                                          else self.button.config(background='#CCE'),
                                                          command(self.button_on.get())))

        def switch(self, _):
            pass

    def __init__(self, master):
        def __switch(li):
            if isinstance(li, tuple):
                return [li]
            else:
                return [(e[0], (lambda y: lambda: self.master.input.insert(y))(e[1])) for e in li]

        self.master = master
        self.frame = tkinter.Frame(master.frame, background='#DDD')
        self.chunks = [tkinter.Frame(self.frame, background='#DDD'),
                       tkinter.Frame(self.frame, background='#DDD'),
                       tkinter.Frame(self.frame, background='#DDD'),
                       tkinter.Frame(self.frame, background='#DDD')]
        self.key_buttons = list()
        self.key_buttons.append(ButtonBoard.SwitchButton(self.chunks[0], '↑',
                                                         lambda b: [k.switch(1 if b else -1)
                                                                    for k in self.key_buttons]))
        self.key_buttons.append(ButtonBoard.SwitchButton(self.chunks[0], 'hyp',
                                                         lambda b: [k.switch(2 if b else -2)
                                                                    for k in self.key_buttons]))
        for m in [[('⌈0 0⌉\n⌊0 0⌋', 'O(')],
                  [('sin', 'sin '), ('sin⁻¹', 'asin '), ('sinh', 'sinh '), ('sinh⁻¹', 'asinh ')],
                  [('sec', 'sec '), ('sec⁻¹', 'asec '), ('sech', 'sech '), ('sech⁻¹', 'asech ')],
                  [('⌈1 1⌉\n⌊1 1⌋', 'I(')],
                  [('cos', 'cos '), ('cos⁻¹', 'acos '), ('cosh', 'cosh '), ('cosh⁻¹', 'acosh ')],
                  [('csc', 'csc '), ('csc⁻¹', 'acsc '), ('csch', 'csch '), ('csch⁻¹', 'acsch ')],
                  [('⌈1 0⌉\n⌊0 1⌋', 'E(')],
                  [('tan', 'tan '), ('tan⁻¹', 'atan '), ('tanh', 'tanh '), ('tanh⁻¹', 'atanh ')],
                  [('cot', 'cot '), ('cot⁻¹', 'acot '), ('coth', 'coth '), ('coth⁻¹', 'acoth ')],
                  [('⌈dᵢ O⌉\n⌊O ᵃg⌋', 'diag(')]]:
            self.key_buttons.append(ButtonBoard.KeyButton(self.chunks[0], __switch(m)))
        len_chunk1 = len(self.key_buttons)
        i = 0
        for kb in self.key_buttons:
            kb.button.grid(row=i % (len_chunk1//4), column=i // (len_chunk1//4), padx=1, pady=1, sticky='nswe')
            i += 1
        for m in [[('var A', '$A ')],
                  [('var B', '$B ')],
                  [('var C', '$C ')],
                  [('var+=', '+= '), ('var-=', '-= ')],
                  [('var D', '$D ')],
                  [('var E', '$E ')],
                  [('var F', '$F ')],
                  [('var=', '= ')],
                  [('°', '°')],
                  [("’", "'")],
                  [('”', '"')],
                  [('Answer', '@')]]:
            self.key_buttons.append(ButtonBoard.KeyButton(self.chunks[1], __switch(m)))
        len_chunk2 = len(self.key_buttons) - len_chunk1
        i = 0
        for kb in self.key_buttons[len_chunk1:]:
            kb.button.grid(row=i // 4, column=i % 4, padx=1, pady=1, sticky='nswe')
            i += 1
        for m in [[('xʸ', '^')],
                  [('ʸ√x', '√')],
                  [('log(b,A)', 'log(')],
                  [('log₁₀', 'lg '), ('ln', 'ln ')],
                  [('|a|', 'abs '), ('|⌈x x⌉|\n|⌊x x⌋|', 'det ')],
                  [('⌊a⌋', 'floor '), ('⌈a⌉', 'ceil ')],
                  [('eˣ', 'exp ')],
                  [('⌈x x⌉T\n⌊x x⌋ ', 'T')],
                  [(' n!', '! ')],
                  [('nPr', 'P ')],
                  [('nCr', 'C ')],
                  [('mod', 'mod ')],
                  [('i', 'i ')],
                  [('π', 'π')],
                  [('e', 'e ')],
                  [('×10ʸ', 'E')],
                  [('ā', '~')],
                  [(',', ','), (' [A];\n [B] ', ';')],
                  [('(', '(')],
                  [(')', ')')]]:
            self.key_buttons.append(ButtonBoard.KeyButton(self.chunks[2], __switch(m)))
        len_chunk3 = len(self.key_buttons) - len_chunk1 - len_chunk2
        i = 0
        for kb in self.key_buttons[len_chunk1 + len_chunk2:]:
            kb.button.grid(row=i // 4, column=i % 4, padx=1, pady=1, sticky='nswe')
            i += 1
        for m in [[('%', '% ')],
                  [('/', '/')],
                  ('C', self.master.input.clear),
                  ('DEL', self.master.input.delete),
                  [('7', '7')],
                  [('8', '8')],
                  [('9', '9')],
                  [('×', '×'), ('·', '*')],
                  [('4', '4')],
                  [('5', '5')],
                  [('6', '6')],
                  [('-', '-')],
                  [('1', '1')],
                  [('2', '2')],
                  [('3', '3')],
                  [('+', '+')],
                  [('±', '-')],
                  [('0', '0')],
                  [('.', '.')],
                  ('=', self.master.submit)]:
            self.key_buttons.append(ButtonBoard.KeyButton(self.chunks[3], __switch(m)))
        len_chunk4 = len(self.key_buttons) - len_chunk1 - len_chunk2 - len_chunk3
        i = 0
        for kb in self.key_buttons[len_chunk1 + len_chunk2 + len_chunk3:]:
            kb.button.grid(row=i // 4, column=i % 4, padx=1, pady=1, sticky='nswe')
            i += 1
        for i in range(len(self.chunks)):
            self.chunks[i].grid(row=i % 2, column=i // 2, padx=0, pady=0, sticky='nwe')
        self.logo_frame = tkinter.Frame(self.frame, background='#DDD', height=180)

    def mode1(self):
        for f in self.chunks:
            f.grid_forget()
        self.logo_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nswe')
        for i in range(len(self.chunks)):
            self.chunks[i].grid(row=i + 1, column=0, padx=0, pady=0, sticky='s')

    def mode2(self):
        self.logo_frame.grid_forget()
        for f in self.chunks:
            f.grid_forget()
        for i in range(len(self.chunks)):
            self.chunks[i].grid(row=i // 2, column=i % 2, padx=0, pady=0, sticky='nwe')


class OutputScreen:
    def __init__(self, master):
        self.frame = ttk.Frame(master.frame)
        self.master = master
        self.screen = tkinter.Text(self.frame, width=55, height=3, state=tkinter.DISABLED,
                                   font=('consolas', 14), background='#DDF', foreground='#000',
                                   highlightthickness=0, borderwidth=0)
        self.scroll = tkinter.ttk.Scrollbar(self.frame, command=self.screen.yview, orient=tkinter.VERTICAL)
        self.screen.config(yscrollcommand=self.scroll.set)
        self.screen.grid(row=0, column=0)
        self.scroll.grid(row=0, column=1, sticky='ns')

    def __print(self, text, prompt):
        self.screen.config(state=tkinter.NORMAL)
        lines = text.splitlines()
        for l in lines[:1]:
            self.screen.insert(tkinter.END, prompt + l + '\n')
        for l in lines[1:]:
            self.screen.insert(tkinter.END, ' ' * len(prompt) + l + '\n')
        self.screen.config(state=tkinter.DISABLED)
        self.screen.yview_scroll(len(lines) + reduce(lambda x, y: x+y,
                                                     [0, *[len(l) // 50 for l in lines]]
                                                     ), 'units')

    def print_out(self, text):
        self.__print(text, '= ')

    def print_err(self, text):
        self.__print(text, 'E ')

    def print_echo(self, text):
        self.__print(text, '  ')

    def set_height(self, height):
        self.screen.config(height=height)


class InputScreen:
    def __init__(self, master):
        self.frame = tkinter.Frame(master.frame, background='#CCC')
        self.master = master
        self.histories = list()
        self.history_at = 0
        self.text = tkinter.StringVar()
        self.screen = tkinter.Entry(self.frame, width=55, textvariable=self.text,
                                    font=('consolas', 14), background='#CCC', foreground='#000',
                                    insertbackground='#000', highlightthickness=0, borderwidth=0)
        self.screen.grid(row=0, column=0)

        self.screen.bind('<Return>', self.master.submit)
        self.screen.bind('<Up>', self.last)
        self.screen.bind('<Down>', self.next)

    def input(self):
        string = self.text.get()
        self.history_at = len(self.histories)
        self.histories.append(string)
        self.text.set('')
        return string

    def last(self, _):
        if 0 <= self.history_at < len(self.histories):
            if self.text.get() != self.histories[self.history_at]:
                self.history_at = len(self.histories)
            if self.history_at > 0:
                self.history_at -= 1
            self.text.set(self.histories[self.history_at])

    def next(self, _):
        if 0 <= self.history_at < len(self.histories):
            if self.text.get() != self.histories[self.history_at]:
                self.history_at = len(self.histories) - 1
            if self.history_at < len(self.histories) - 1:
                self.history_at += 1
            self.text.set(self.histories[self.history_at])

    def insert(self, text):
        self.screen.insert(tkinter.INSERT, text)

    def delete(self):
        self.screen.delete(self.screen.index(tkinter.INSERT) - 1, tkinter.INSERT)

    def clear(self):
        self.screen.delete(0, tkinter.END)


class StatusBoard:
    def __init__(self, master):
        self.master = master
        self.frame = tkinter.Frame(self.master.frame, background='#DDF')
        self.drg_mode = tkinter.StringVar()
        self.drg_mode.set('DEG')
        self.dms_mode = tkinter.StringVar()
        self.dms_mode.set('POINT')
        self.drg_button = tkinter.Button(self.frame, font=('consolas', 12, 'bold'), width=5, background='#CCE',
                                         foreground='#000', borderwidth=0, highlightthickness=1,
                                         textvariable=self.drg_mode,
                                         command=lambda: (console.main({'DEG': 'rad',
                                                                        'RAD': 'grad',
                                                                        'GRAD': 'deg'}[self.drg_mode.get()],
                                                                       self.master.output.print_err,
                                                                       self.read_err,
                                                                       self.master.op_list))
                                         )
        self.dms_button = tkinter.Button(self.frame, font=('consolas', 12, 'bold'), width=5, background='#CCE',
                                         foreground='#000', borderwidth=0, highlightthickness=1,
                                         textvariable=self.dms_mode,
                                         command=lambda: (console.main('dms', self.master.output.print_err,
                                                                       self.read_err,
                                                                       self.master.op_list))
                                         )
        self.prec_text = tkinter.StringVar(value='PRECISION 50')
        self.prec_button = tkinter.Button(self.frame, font=('consolas', 12, 'bold'), width=13, background='#CCE',
                                          foreground='#000', borderwidth=0, highlightthickness=1,
                                          textvariable=self.prec_text,
                                          command=lambda: (console.main('prec %d' %
                                                                        ((int(self.prec_text.get()[10:]) + 4) % 50 + 1),
                                                                        self.master.output.print_err,
                                                                        self.read_err, self.master.op_list))
                                          )
        self.center_label = tkinter.Label(self.frame, background='#CCE', highlightthickness=0, width=23)
        self.output_height = tkinter.StringVar()
        self.output_height.set('NARROW CONSOLE')
        self.output_height_button = tkinter.Button(self.frame, font=('consolas', 12, 'bold'), width=15,
                                                   background='#CCE', foreground='#000', borderwidth=0,
                                                   highlightthickness=1,
                                                   textvariable=self.output_height,
                                                   command=lambda: (
                                                       self.output_height.set(
                                                           {'MEDIUM CONSOLE': 'LARGE CONSOLE',
                                                            'LARGE CONSOLE': 'NARROW CONSOLE',
                                                            'NARROW CONSOLE': 'MEDIUM CONSOLE'
                                                            }[self.output_height.get()]),
                                                       self.master.output.set_height(
                                                           {'MEDIUM CONSOLE': 10,
                                                            'LARGE CONSOLE': 30,
                                                            'NARROW CONSOLE': 3,
                                                            }[self.output_height.get()]),
                                                       self.master.refresh_keyboard()),
                                                   )
        self.keyboard_open = tkinter.BooleanVar()
        self.keyboard_open.set(False)
        self.keyboard_button = tkinter.Button(self.frame, image=_get_keyboard_img(), height=27, foreground='#000',
                                              background='#EEE', borderwidth=0, highlightthickness=1,
                                              command=lambda: (
                                              self.keyboard_open.set(not self.keyboard_open.get()),
                                              self.keyboard_button.config(background=(
                                                  '#CCE' if self.keyboard_open.get() else '#EEE')),
                                              self.master.close_keyboard() if self.keyboard_open.get()
                                              else self.master.open_keyboard()))
        self.drg_button.grid(row=0, column=0, padx=0, sticky='w')
        self.dms_button.grid(row=0, column=1, padx=0, sticky='w')
        self.prec_button.grid(row=0, column=2, padx=0, sticky='w')
        self.center_label.grid(row=0, column=3, padx=0, sticky='wens')
        self.output_height_button.grid(row=0, column=4, padx=0, sticky='e')
        self.keyboard_button.grid(row=0, column=5, padx=0, sticky='e')

    def read_err(self, text):
        if text == 'deg':
            self.drg_mode.set('DEG')
        elif text == 'rad':
            self.drg_mode.set('RAD')
        elif text == 'grad':
            self.drg_mode.set('GRAD')
        elif text == 'dms':
            self.dms_mode.set('DMS')
        elif text == 'point':
            self.dms_mode.set('POINT')
        elif text.startswith('prec'):
            self.prec_text.set('PRECISION %02d' % int(text[5:]))


class Window:
    def __init__(self, master_frame):
        self.op_list = ops.OpList()
        self.frame = ttk.Frame(master_frame)
        self.status = StatusBoard(self)
        self.status.frame.grid(row=0, column=0, sticky='we')
        self.output = OutputScreen(self)
        self.output.frame.grid(row=1, column=0)
        self.input = InputScreen(self)
        self.input.frame.grid(row=2, column=0, sticky='we')
        self.keyboard = ButtonBoard(self)
        self.open_keyboard()

    def submit(self, *_):
        line = self.input.input()
        self.output.print_echo(line)
        console.main(line, self.output.print_out,
                     lambda x: (self.output.print_err(x), self.status.read_err(x)),
                     self.op_list)

    def open_keyboard(self):
        if self.status.output_height.get() == 'LARGE CONSOLE':
            self.keyboard.mode1()
            self.keyboard.frame.grid(row=0, column=1, rowspan=3, sticky='swn')
        else:
            self.keyboard.mode2()
            self.keyboard.frame.grid(row=3, column=0, sticky='nwe')

    def close_keyboard(self):
        self.keyboard.frame.grid_forget()

    def refresh_keyboard(self):
        if not self.status.keyboard_open.get():
            self.close_keyboard()
            self.open_keyboard()


def main():
    root = tkinter.Tk()
    pic2py.generate_pic(pics.avatar_ico, 'avatar.ico')
    root.wm_iconbitmap('avatar.ico')
    root.wm_title('F91 said the Calculator.')
    root.resizable(0, 0)
    window = Window(root)
    window.frame.grid()
    pic2py.delete_pic('avatar.ico')
    pic2py.delete_pic('kbs.gif')
    root.mainloop()


if __name__ == '__main__':
    main()
