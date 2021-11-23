import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    PAD = 10  # Global padding variable

    # Button naming list for easy initialisation of buttons
    button_names = ["Rhyme Scheme", "Alliteration",
                    "Assonance", "Sibilance", "Enjambment",
                    "Caesura"]

    def __init__(self, controller):
        """
        Initialises the View with all the components assembled individually using different methods.
        :param controller: Controller parameter allows View to pass feedback to the Controller
        """
        super().__init__()
        self.title("PoetryAnalyser")
        self.geometry("1000x525")

        self.inp_value = tk.StringVar()
        self._create_main_frame()
        self._create_txt_frame()
        self._create_disp_frame()
        self._make_text_input()
        self._add_enter_button()
        self._make_text_display()
        self._make_dashboard()
        self.controller = controller

    def main(self):
        self.mainloop()

    def _create_main_frame(self):
        self.main_fr = ttk.Frame(self)
        self.main_fr.pack(padx=self.PAD, pady=self.PAD)

    def _create_txt_frame(self):
        self.txt_fr = ttk.Frame(self.main_fr)
        self.txt_fr.pack(side="left", padx=self.PAD, pady=self.PAD)

    def _create_disp_frame(self):
        self.disp_fr = ttk.Frame(self.main_fr)
        self.disp_fr.pack(side="right", padx=self.PAD, pady=self.PAD)

    def click(self, event):
        self.txt_inp.configure(state="normal")
        self.txt_inp.delete("1.0", "end")
        self.txt_inp.unbind('<Button-1>', self.clicked)

    def _make_text_input(self):
        self.txt_inp = tk.Text(self.txt_fr, relief="solid", wrap="none")
        self.txt_inp.config(width=50)
        self.txt_inp.pack(padx=self.PAD, pady=self.PAD)
        self.txt_inp.insert("1.0", "Enter poem here...")
        self.clicked = self.txt_inp.bind('<Button-1>', self.click)

        scroll_x = tk.Scrollbar(self.txt_fr, orient="horizontal", command=self.txt_inp.xview)
        scroll_x.pack(fill='x')
        self.txt_inp['xscrollcommand'] = scroll_x.set

    def _add_enter_button(self):
        btn_enter = ttk.Button(self.main_fr, text="Enter",
                               command=lambda: self.controller.on_click_enter(self.txt_inp.get("1.0", "end-1c"))
                               )
        btn_enter.pack(side="left", padx=self.PAD, pady=self.PAD)

    def _make_text_display(self):
        # State needs to be updated when inserting/deleting text from window
        self.txt_disp = tk.Text(self.disp_fr, relief="solid", wrap="none", state="disabled")
        self.txt_disp.config(width=50)
        self.txt_disp.pack(padx=self.PAD, pady=self.PAD)

        scroll_x = tk.Scrollbar(self.disp_fr, orient="horizontal", command=self.txt_disp.xview)
        scroll_x.pack(fill='x')
        self.txt_disp['xscrollcommand'] = scroll_x.set

    def _make_dashboard(self):
        dash_fr = ttk.Frame(self)
        dash_fr.pack(padx=self.PAD, pady=self.PAD)

        for name in self.button_names:
            btn = ttk.Button(dash_fr, text=name,
                             command=lambda button=name: self.controller.on_button_click(button)
                             )
            btn.pack(side="left", padx=self.PAD)
