try:
    import tkinter.ttk as ttk
except ImportError:
    import tkinter as ttk
finally:
    import tkinter
    import console


class ButtonBoard:
    def __init__(self, master_frame, keys):
        """

        :param master_frame:
        :param keys: [{'grid_args': {...},
                       'button_args': {...},
                       }]
        """
        self.frame = ttk.Frame(master_frame)
        for key in keys:
            ttk.Button(self.frame, **key['button_args']).grid(**key['grid_args'])


class OutputScreen:
    def __init__(self, master):
        self.frame = ttk.Frame(master.frame)
        self.master = master
        self.screen = tkinter.Text(self.frame, width=55, height=10, state=tkinter.DISABLED,
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
        self.screen.yview_scroll(len(lines), 'units')

    def print_out(self, text):
        self.__print(text, '= ')

    def print_err(self, text):
        self.__print(text, 'E ')

    def print_echo(self, text):
        self.__print(text, '  ')


class InputScreen:
    def __init__(self, master):
        self.frame = ttk.Frame(master.frame)
        self.master = master
        self.histories = list()
        self.history_at = 0
        self.text = tkinter.StringVar()
        self.screen = tkinter.Entry(self.frame, width=55, textvariable=self.text,
                                    font=('consolas', 14), background='#DDD', foreground='#333',
                                    insertbackground='#333', highlightthickness=0, borderwidth=0)
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


class Window:
    def __init__(self, master_frame):
        self.frame = ttk.Frame(master_frame)
        self.output = OutputScreen(self)
        self.output.frame.grid(row=0, column=0)
        self.input = InputScreen(self)
        self.input.frame.grid(row=1, column=0, sticky='w')

    def submit(self, e):
        line = self.input.input()
        self.output.print_echo(line)
        console.main(line, self.output.print_out, self.output.print_err)


def main():
    root = tkinter.Tk()
    window = Window(root)
    window.frame.grid()
    root.mainloop()


if __name__ == '__main__':
    main()
