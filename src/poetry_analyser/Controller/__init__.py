from poetry_analyser.Model import Model
from poetry_analyser.View import View


class Controller:
    def __init__(self):
        """
        Initialises the Controller. Uses composition to give access to Model and View.
        """
        self.model = Model()
        self.view = View(self)
        self.disp_result = ""  # the result string to be displayed in the View

    def on_button_click(self, name):
        """
        Factory pattern for assigning functionality to each button.
        Cleans the output of each algorithm so that it can be clearly displayed in the View's results box.
        Updates global variable `disp_result` with the appropriate algorithmic output for each button.
        :param name: string name of the button
        :return: None
        """
        print(f"Button {name} clicked")  # Logs button clicks in terminal for dev reference

        if self.model.poem == "":
            self.disp_result = "Please enter a poem"
            self.display_result()
            return

        if name == "Rhyme Scheme":
            self.disp_result += "Rhyme Scheme: " + "".join(chr(s + 64) for s in self.model.get_rhyme_scheme()) + "\n\n\n"
        elif name == "Alliteration":
            self.disp_result += "Alliteration:\n"
            l_no = 1
            for l in self.model.get_alliteration():
                if len(l) > 0:
                    self.disp_result += "Line " + str(l_no) + ": " + str(l) + "\n"
                l_no += 1
            self.disp_result += "\n\n"
        elif name == "Sibilance":
            self.disp_result += "Sibilance: \n" + "\n".join(str(line) for line in self.model.get_sibilance()) + "\n\n"
        elif name == "Enjambment":
            self.disp_result += "Enjambing lines: " + " ".join(str(l) for l in self.model.get_enjambment()) + "\n\n\n"
        elif name == "Caesura":
            self.disp_result += "Caesuras: \n" + "\n".join(str(line) for line in self.model.get_caesura()) + "\n\n"
        elif name == "Assonance":
            self.disp_result += "Assonance: \n" + "\n".join(str(line) for line in self.model.get_assonance()) + "\n\n"

        self.display_result()

    def display_result(self):
        """
        Updates the View's result box with the algorithm results and then locks it.
        :return: None
        """
        self.view.txt_disp.config(state="normal")  # Unlocks display textbox for text input
        self.view.txt_disp.delete("1.0", "end")  # Removes any previous text
        self.view.txt_disp.insert("1.0", self.disp_result)  # Inserts new results
        self.view.txt_disp.config(state="disabled")  # Locks textbox

    def on_click_enter(self, text):
        """
        Executes the function of the 'Enter' button. Loads the user-input text from the GUI into the Model component
        for manipulation. Displays the entered text with line numbers in the input box and displays original input
        in the disp_txt view box.
        :param text: the poem entered by the user into the view input_txt box.
        :return: None
        """
        self.model.poem_injection(text)
        self.view.txt_inp.config(state="normal")
        self.view.txt_inp.delete("1.0", "end")
        self.view.txt_inp.insert("1.0", self.clean_display())

        self.view.txt_disp.config(state="normal")
        self.view.txt_disp.delete("1.0", "end")
        self.view.txt_disp.insert("1.0", text)
        self.view.txt_disp.config(state="disabled")
        self.disp_result = ""

    def clean_display(self):
        """
        Cleans input text for display in the input box. Iterates through each line and compiles a sequence of
        'Line :line_number: :line:' strings, separated by new lines to restore poem's structure.
        :return: a string of all lines in the poem along with line numbers.
        """
        cleaned = ""
        l_no = 1
        for stanza in self.model.stanzas:
            lines = self.model.stanzas[stanza].split("\n")
            for l in range(len(lines)):
                if l == len(lines)-1:
                    cleaned += "Line " + str(l_no) + ":\t\t" + lines[l] + "\n\n"
                else:
                    cleaned += "Line " + str(l_no) + ":\t\t" + lines[l] + "\n"
                l_no += 1
        return cleaned


