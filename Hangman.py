import time
import os
import csv
import sys
from random import choice
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout, QGroupBox, QDialog, QButtonGroup, QStackedWidget
import string


class GameMainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_main_window()

    # Initialize parameters of the window.
    def init_main_window(self):
        left, top, width, height = 400, 75, 300, 400
        window_icon = "/home/strovosky/MyProjects/Hangman/windowicon.png"
        self.setWindowTitle("Strovosky's Hangman")
        self.setWindowIcon(QtGui.QIcon(window_icon))
        self.setGeometry(left, top, width, height)
        self.setFont(QtGui.QFont("Cooper Black", 12))
        self.create_layout_main_window()

        # First, a happy picture on top.
        v_layout = QVBoxLayout()
        label_image = QLabel()
        pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/Nervous.png")
        label_image.setPixmap(pixmap)
        label_image.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(label_image)

        # Now, let's add the option radio buttons we created.
        v_layout.addWidget(self.groupbox_categories)
        self.setLayout(v_layout)

        self.show()

    def page_opener(self):
        self.category_import = ""
        for categ in self.category_radiobutton_dic:
            if self.category_radiobutton_dic[categ].isChecked():
                self.category_import = categ

        # Creates base window without parameters.
        self.second_window = GameWindow()

        # Creates the secret word and available words.
        self.second_window.variables_preparator(self.category_import)

        # Creates layout and the x_word
        self.second_window.create_layout()

        # Creates the alphabet and other buttons.
        self.second_window.init_window()
        self.second_window.exec()

    def create_layout_main_window(self):
        # This one will contain the two columns of radiobutton options.
        self.groupbox_categories = QGroupBox("Choose the category:")
        h_layout_for_categories = QHBoxLayout()

        # Left row.
        self.groupbox_categories_colum1 = QGroupBox()
        v_layout_column1 = QVBoxLayout()

        # Right row
        self.groupbox_categories_colum2 = QGroupBox()
        v_layout_column2 = QVBoxLayout()

        # Lets create a list with the categories in the csv file.
        categories = []
        self.category_radiobutton_dic = {}
        with open("/home/strovosky/MyProjects/Hangman/hangman_vocab.csv") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for field in csv_reader.fieldnames:
                if "Hint" not in field:
                    categories.append(field)

        # Let's create a categories dictionary and add the radiobuttons there.
        for category in categories:
            radio_button = QRadioButton(category)
            self.category_radiobutton_dic[category] = radio_button
            self.category_radiobutton_dic[category].toggled.connect(self.page_opener)

        # Let's add them to the layout and Buttongroup
        self.buttongroup_options = QButtonGroup()

        for ind, category in enumerate(categories):
            if ind < len(self.category_radiobutton_dic)//2:
                v_layout_column1.addWidget(self.category_radiobutton_dic[category])
                self.buttongroup_options.addButton(self.category_radiobutton_dic[category])
            else:
                v_layout_column2.addWidget(self.category_radiobutton_dic[category])
                self.buttongroup_options.addButton(self.category_radiobutton_dic[category])

        self.groupbox_categories_colum1.setLayout(v_layout_column1)
        self.groupbox_categories_colum2.setLayout(v_layout_column2)
        h_layout_for_categories.addWidget(self.groupbox_categories_colum1)
        h_layout_for_categories.addWidget(self.groupbox_categories_colum2)
        self.groupbox_categories.setLayout(h_layout_for_categories)


class GameWindow(QDialog):
    def __init__(self):
        super().__init__()

    # Here I'll return the random word and the starting values of Available Letters.
    def variables_preparator(self, category_input):
        category_words = []
        with open("/home/strovosky/MyProjects/Hangman/hangman_vocab.csv") as hangman_csv:
            csv_reader = csv.DictReader(hangman_csv)
            for line in csv_reader:
                if line[category_input.title()] != '' and line[category_input.title()] != None:
                    category_words.append(line[category_input.title()].upper())

        random_word = choice(category_words)

        self.word = random_word

        self.guessed_letters = 0
        self.strikes = 0
        self.max_num_strikes = 10

        self.rob_pics_dict = {}
        os.chdir("/home/strovosky/MyProjects/Hangman/Body 1")
        for direct in os.listdir():
            if direct[0].isdigit() and direct[1].isdigit():
                num = str(direct[0]) + str(direct[1])
                self.rob_pics_dict[int(num)] = os.path.join("/home/strovosky/MyProjects/Hangman/Body 1", str(direct))
            elif direct[0].isdigit():
                self.rob_pics_dict[int(direct[0])] = os.path.join("/home/strovosky/MyProjects/Hangman/Body 1", str(direct))

    def init_window(self):
        left, top, width, height = 30, 30, 1000, 700
        window_icon = "/home/strovosky/MyProjects/Hangman/windowicon.png"
        self.setWindowTitle("Strovosky's Hangman")
        self.setWindowIcon(QtGui.QIcon(window_icon))
        self.setGeometry(left, top, width, height)

        v_layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        groupbox_left = QGroupBox()
        v_layout.addWidget(self.groupbox_buttons)

        self.button_creator()
        v_layout.addWidget(self.button_set_1)
        v_layout.addWidget(self.button_set_2)
        v_layout.addWidget(self.button_set_3)
        v_layout.addWidget(self.button_set_4)
        v_layout.addWidget(self.button_set_5)

        v_layout.addWidget(self.groupbox_i_know_the_word)

        groupbox_left.setLayout(v_layout)
        hlayout.addWidget(groupbox_left)
        hlayout.addWidget(self.groupbox_pic_label)

        self.setLayout(hlayout)

        self.show()


    def create_layout(self):
        self.groupbox_buttons = QGroupBox()
        self.groupbox_pic_label = QGroupBox()
        self.groupbox_pic_label.setStyleSheet("background-color:white")
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.pic_label = QLabel()
        #self.pic_label.setMinimumSize(50,50)
        pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/0.png")
        self.pic_label.setPixmap(pixmap)
        self.pic_label.setAlignment(QtCore.Qt.AlignCenter)
        h_layout.addWidget(self.pic_label)
        self.groupbox_pic_label.setLayout(h_layout)

        # Let's create a function which will generate the x_word.
        def x_word_generator(w):
            x_word = ""
            for ind, x in enumerate(w):
                if w[ind] == " ":
                    x_word += " "
                if w[ind] == "-":
                    x_word += "-"
                else:
                    x_word += "#"

            return x_word

        self.secret_word = x_word_generator(self.word)

        self.secret_word_label = QLabel(self.secret_word)
        self.secret_word_label.setFont(QtGui.QFont("Cooper Black", 24))
        self.secret_word_label.setStyleSheet("background-color: #0BA99A")
        self.secret_word_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.secret_word_label)

        self.groupbox_buttons.setLayout(v_layout)

    def button_creator(self):
        # I will automatically create the buttons with the letters of the alphabet in 5 different rows.
        self.buttongroup_alphabet = QButtonGroup()
        self.index_alph = 1

        self.button_set_1 = QGroupBox()
        self.button_set_2 = QGroupBox()
        self.button_set_3 = QGroupBox()
        self.button_set_4 = QGroupBox()
        self.button_set_5 = QGroupBox()
        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()
        h_layout4 = QHBoxLayout()
        h_layout5 = QHBoxLayout()

        # To access each button. I did this before I knew about buttongroup.
        button_dic = {}
        letters = [letter for letter in string.ascii_uppercase]

        def button_set_creator(groupbox, hlayout):
            # This one creates the six rows of letters.
            for iteration in range(6):
                if len(letters) > 0:
                    button = QPushButton(letters[0])
                    button_dic[letters[0]] = button
                    hlayout.addWidget(button_dic[letters[0]])
                    self.buttongroup_alphabet.addButton(button_dic[letters[0]], self.index_alph)
                    self.index_alph += 1
                    del letters[0]
                else:
                    break
            groupbox.setLayout(hlayout)

        button_set_creator(self.button_set_1, h_layout1)
        button_set_creator(self.button_set_2, h_layout2)
        button_set_creator(self.button_set_3, h_layout3)
        button_set_creator(self.button_set_4, h_layout4)
        button_set_creator(self.button_set_5, h_layout5)

        self.groupbox_i_know_the_word = QGroupBox()
        self.buttongroup_i_k_t_w = QButtonGroup()
        self.h_layout_i_know_the_word = QHBoxLayout()

        button_i_k_t_w = QPushButton("I Know\nThe Word")
        button_i_k_t_w.setFont(QtGui.QFont("Arial Nova", 8))
        button_i_k_t_w.setStyleSheet("background-color: #141EEC")

        #The button has been added to the alphabet button group and id is 27 (because it's 26 letters in the English dictionary).
        self.buttongroup_i_k_t_w.addButton(button_i_k_t_w, 1)
        self.h_layout_i_know_the_word.addWidget(button_i_k_t_w)

        self.full_word = QLineEdit()
        self.full_word.setStyleSheet("color:blue")
        self.full_word.setDisabled(True)
        self.full_word.returnPressed.connect(self.i_k_t_w_game_runner)
        self.h_layout_i_know_the_word.addWidget(self.full_word)

        # Here we enable the line_edit when we press the button I know the word.
        def line_edit_i_k_t_w_enabler():
            self.full_word.setDisabled(False)
        self.buttongroup_i_k_t_w.buttonClicked[int].connect(line_edit_i_k_t_w_enabler)

        # To connect to the method.
        self.buttongroup_alphabet.buttonClicked[int].connect(self.game_runner)

        self.groupbox_i_know_the_word.setLayout(self.h_layout_i_know_the_word)

    def game_runner(self, id):

        # If we guessed a letter or got the full word.
        if self.buttongroup_alphabet.button(id).text() in self.word:

            word = self.word
            xword = self.secret_word_label.text()
            letter = self.buttongroup_alphabet.button(id).text()

            def word_changer(w, x, l):
                new_x = [let for let in x]
                new_w = [let for let in w]
                for iteration in range(w.count(l)):
                    if l in new_w:
                        ind = new_w.index(l)
                    for num, letter in enumerate(new_w):
                        if num == ind:
                            new_x[ind] = letter
                            new_w[ind] = "#" # So that it can search for the nex letter index and doesn't repeat it.
                new_x = "".join(new_x)
                return new_x

            self.secret_word_label.setText(word_changer(word, xword, letter))

            # If we got the full word we win
            if self.secret_word_label.text() == self.word:
                pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/Winner.png")
                self.pic_label.setPixmap(pixmap)
                self.secret_word_label.setText(self.word)
                for button in self.buttongroup_alphabet.buttons():
                    button.setDisabled(True)

                self.next_button_creator()

            # If we got the letter we procceed accordingly.
            elif self.secret_word_label.text() != self.word:
                #pixmap = QtGui.QPixmap("C:/Users/Lenovo/Desktop/Python-Programs/Hangman/Body 1/Good Job.png")
                #self.pic_label.setPixmap(pixmap)
                #time.sleep(2)
                self.buttongroup_alphabet.button(id).setDisabled(True)
                pixmap = QtGui.QPixmap(self.rob_pics_dict[self.strikes])
                self.pic_label.setPixmap(pixmap)

        # If you don't guess the letter.
        elif not self.buttongroup_alphabet.button(id).text() in self.word:
            self.strikes += 1
            if self.strikes == self.max_num_strikes:
                pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/Sad.png")
                self.pic_label.setPixmap(pixmap)
                self.secret_word_label.setText(self.word)
                for button in self.buttongroup_alphabet.buttons():
                    button.setDisabled(True)

                self.next_button_creator()

            elif  self.strikes < self.max_num_strikes:
                pixmap = QtGui.QPixmap(self.rob_pics_dict[self.strikes])
                self.pic_label.setPixmap(pixmap)
                self.buttongroup_alphabet.button(id).setDisabled(True)

    def i_k_t_w_game_runner(self):
        if self.full_word.text().upper() == self.word:
            pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/Winner.png")
            self.pic_label.setPixmap(pixmap)
            self.secret_word_label.setText(self.word)
            for button in self.buttongroup_alphabet.buttons():
                button.setDisabled(True)

            self.next_button_creator()

        else:
            pixmap = QtGui.QPixmap("/home/strovosky/MyProjects/Hangman/Body 1/Sad.png")
            self.pic_label.setPixmap(pixmap)
            self.secret_word_label.setText(self.word)
            for button in self.buttongroup_alphabet.buttons():
                button.setDisabled(True)

            self.next_button_creator()

    def next_button_creator(self):
        # Let's create the button
        next_button = QPushButton("Next")
        next_button.setIcon(QtGui.QIcon("/home/strovosky/MyProjects/Hangman/Here You Go.png"))
        next_button.setIconSize(QtCore.QSize(50, 50))
        next_button.setStyleSheet("background-color: #248AAE")

        # It's next to the line edit (I hope,hehe)
        self.h_layout_i_know_the_word.addWidget(next_button)


app = QApplication(sys.argv)
game = GameMainWindow()
sys.exit(app.exec())
