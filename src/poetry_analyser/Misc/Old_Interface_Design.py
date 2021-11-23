from tkinter import *

root = Tk()
root.title("Poetry Reader")

root.rowconfigure(0, minsize=300, weight=1)
root.columnconfigure(0, minsize=150, weight=1)
root.rowconfigure(1, minsize=200, weight=1)
root.columnconfigure(1, minsize=350, weight=1)
root.columnconfigure(2, minsize=350, weight=1)

# Frames for delineation
fr_input = Frame(root, width=250, height=350)
fr_display = Frame(root, width=250, height=350)
fr_dashboard = Frame(root)
fr_buttons = Frame(root)

fr_input.grid(row=0, column=1, sticky="n", ipady=5)
fr_display.grid(row=0, column=2, sticky="n", ipady=5)
fr_dashboard.grid(row=1, column=1, columnspan=2, sticky="new")
fr_buttons.grid(row=0, column=0, sticky="ns")

# Text input/output boxes
# inp_scrollbar = Scrollbar(fr_input)
# inp_scrollbar.pack(side=RIGHT, fill=Y)
# disp_scrollbar = Scrollbar(fr_display)
# disp_scrollbar.pack(side=RIGHT, fill=Y)

txt_input = Text(fr_input)
txt_display = Text(fr_display)
txt_input.pack(side=RIGHT, padx=10, pady=50)
txt_display.pack(padx=150, pady=50)

# File/System Buttons
btn_open = Button(fr_buttons, text="Open")
btn_save = Button(fr_buttons, text="Save As")

dash_scroll = Scrollbar(fr_dashboard, orient="horizontal")
dash_scroll.pack(side=BOTTOM, fill=X)

# Analytical buttons
# Structural analysis
btn_metre = Button(fr_dashboard, text="Metre")
btn_rhyme_scheme = Button(fr_dashboard, text="Rhyme Scheme")
btn_form = Button(fr_dashboard, text="Form")

# Phonetic analysis
btn_alliteration = Button(fr_dashboard, text="Alliteration")
btn_assonance = Button(fr_dashboard, text="Assonance")
btn_consonance = Button(fr_dashboard, text="Consonance")
btn_sibilance = Button(fr_dashboard, text="Sibilance")
btn_internal_rhyme = Button(fr_dashboard, text="Internal Rhyme")
btn_end_rhyme = Button(fr_dashboard, text="End Rhyme")

# Linguistic Analysis
btn_repetition = Button(fr_dashboard, text="Repetition")
btn_anaphora = Button(fr_dashboard, text="Anaphora")
btn_simile = Button(fr_dashboard, text="Simile")
btn_enjambment = Button(fr_dashboard, text="Enjambment")
btn_caesura = Button(fr_dashboard, text="Caesura")
# more buttons...

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

btn_metre.pack(side=LEFT, padx=20, pady=5)
btn_rhyme_scheme.pack(side=LEFT, padx=20, pady=5)
btn_form.pack(side=LEFT, padx=20, pady=5)
btn_alliteration.pack(side=LEFT, padx=20, pady=5)
btn_assonance.pack(side=LEFT, padx=20, pady=5)
btn_consonance.pack(side=LEFT, padx=20, pady=5)
btn_sibilance.pack(side=LEFT, padx=20, pady=5)
btn_internal_rhyme.pack(side=LEFT, padx=20, pady=5)
btn_end_rhyme.pack(side=LEFT, padx=20, pady=5)
btn_repetition.pack(side=LEFT, padx=20, pady=5)
btn_anaphora.pack(side=LEFT, padx=20, pady=5)
btn_simile.pack(side=LEFT, padx=20, pady=5)
btn_enjambment.pack(side=LEFT, padx=20, pady=5)
btn_caesura.pack(side=LEFT, padx=20, pady=5)
# btn_metre.grid(row=0, column=0, sticky="ns", padx=20, pady=5)
# btn_rhyme_scheme.grid(row=0, column=1, sticky="ns", padx=20, pady=5)
# btn_form.grid(row=0, column=2, sticky="ns", padx=20, pady=5)
# btn_alliteration.grid(row=0, column=3, sticky="ns", padx=20, pady=5)
# btn_assonance.grid(row=0, column=4, sticky="ns", padx=20, pady=5)
# btn_consonance.grid(row=0, column=5, sticky="ns", padx=20, pady=5)
# btn_sibilance.grid(row=0, column=6, sticky="ns", padx=20, pady=5)
# btn_internal_rhyme.grid(row=0, column=7, sticky="ns", padx=20, pady=5)
# btn_end_rhyme.grid(row=0, column=8, sticky="ns", padx=20, pady=5)
# btn_repetition.grid(row=0, column=9, sticky="ns", padx=20, pady=5)
# btn_anaphora.grid(row=0, column=10, sticky="ns", padx=20, pady=5)
# btn_simile.grid(row=0, column=11, sticky="ns", padx=20, pady=5)
# btn_enjambment.grid(row=0, column=12, sticky="ns", padx=20, pady=5)
# btn_caesura.grid(row=0, column=13, sticky="ns", padx=20, pady=5)

root.mainloop()

