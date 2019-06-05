try:
    import tkinter.ttk as ttk
except ImportError:
    import tkinter as ttk
finally:
    import tkinter


class KeyBoard:
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


class ScreenLine:
    def __init__(self, master_frame):
        self.frame = ttk.Frame(master_frame)
        self.text = tkinter.StringVar()
        self.screen_line = ttk.Entry(self.frame, variable=self.text)

