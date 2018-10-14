# INPUT
y0 = 1.0
x0 = 0.0
x_max = 9.3
num_of_steps = 100
MAX_NUM_OF_STEPS = 100000
MAX_NUM_OF_STEPS_ERROR = 1000
show_opt = 0
ALGORITHMS = ['Euler', 'Improved Euler', 'Runge-Kutta']
ALG_CLR = ['g', 'r', 'b']


# Check if all needed modules are installed, if they are not install them.
from pip._internal import main
from importlib import util

module_names = ['PyQt5', 'pyqtgraph', 'numpy']
for m_name in module_names:
    if not util.find_spec(m_name):
        if input('Module not found {}, would you mind to install it?'.format(m_name)).lower() in 'y':
            if main(['install', m_name]):
                print('Installing {}...'.format(m_name))

from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


def f(x, y):
    """
    Calculates function given in task (Variant 11)
    :param x: x values
    :param y: y values
    :return: y values
    """
    return np.exp(-np.sin(x)) - y * np.cos(x)


def exact_sol(y0, x):
    """
    Calculates the exact solution of function given in task (Variant 11)
    :param y0: initial y
    :param x: x values
    :return: y values
    """
    c = y0 / np.exp(-np.sin(x[0])) - x[0]
    y = (x + c) * np.exp(-np.sin(x))
    return y


def error(exact_y, y):
    """
    Calculates error of a function
    :param exact_y: y values of exact function
    :param y: y values of function to compare
    :return: error of given function
    """
    return np.abs(exact_y - y)


def max_error(alg):
    """
    Calculates the max error function (max error to number of steps)
    :param alg: algorithm to calculate
    :return: max error values
    """
    global num_of_steps, x_max, y0, x0
    res = [0]
    for i in range(1, num_of_steps + 1):
        x = np.linspace(x0, x_max, i + 1)
        step = x[1] - x[0]
        exact_sl = exact_sol(y0, x)
        if alg == 0:
            sl = euler(y0, x, step)
        else:
            if alg == 1:
                sl = impr_euler(y0, x, step)
            else:
                sl = runge_kutt(y0, x, step)
        res.append(max(error(exact_sl, sl)))
    return res


def euler(y0, x, step):
    """
        Calculates the euler algorithm for given values
        :param y0: initial y
        :param x: all x values
        :param step: step of x
        :return: calculated y values
        """
    y = [y0]
    for i in range(1, len(x)):
        yi = y[i - 1] + step * f(x[i - 1], y[i - 1])
        y.append(yi)
    return y


def impr_euler(y0, x, step):
    """
    Calculates the improved euler algorithm for given values
    :param y0: initial y
    :param x: all x values
    :param step: step of x
    :return: calculated y values
    """
    y = [y0]
    for i in range(1, len(x)):
        k1 = y[i - 1] + step * f(x[i - 1], y[i - 1])
        yi = y[i - 1] + step * (f(x[i - 1], y[i - 1]) + f(x[i - 1] + step, y[i - 1] + step * k1)) / 2.0
        y.append(yi)
    return y


def runge_kutt(y0, x, step):
    """
    Calculates the runge_kutt algorithm for given values
    :param y0: initial y
    :param x: all x values
    :param step: step of x
    :return: calculated y values
    """
    y = [y0]
    for i in range(1, len(x)):
        k1 = f(x[i - 1], y[i - 1])
        k2 = f(x[i - 1] + step / 2, y[i - 1] + step * k1 / 2)
        k3 = f(x[i - 1] + step / 2, y[i - 1] + step * k2 / 2)
        k4 = f(x[i - 1] + step, y[i - 1] + step * k3)
        yi = y[i - 1] + step / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y.append(yi)
    return y


def solve(y0, x, step, alg):
    if alg == 0:
        return euler(y0, x, step)
    if alg == 1:
        return impr_euler(y0, x, step)
    if alg == 2:
        return runge_kutt(y0, x, step)


def update():
    """
    Updates the values and adds them to the plotWidgets
    """
    global x0, y0, x_max, num_of_steps
    # Clear the plot views
    clear()
    if check_valid():
        x = np.linspace(x0, x_max, num_of_steps + 1)
        step = x[1] - x[0]
        exact_ans = exact_sol(y0, x)
        for i in range(3):
            if ALG_BOX[i].isChecked():
                ans = solve(y0, x, step, i)
                plot1.plot(x, ans, pen=ALG_CLR[i], name=ALGORITHMS[i])
                if show_opt == 0:
                    plot2.plot(x, error(exact_ans, ans), pen=ALG_CLR[i], name=ALGORITHMS[i])
                else:
                    plot2.plot(max_error(i), pen=ALG_CLR[i], name=ALGORITHMS[i])
        if exact_box.isChecked():
            plot1.plot(x, exact_ans, pen='w', name='Exact')


def clear():
    """
    Clears all plotWidgets
    """
    global plot1
    plot1.clear()
    plot1.getViewBox().removeItem(plot1.plotItem.legend)
    plot1.addLegend()
    plot1.enableAutoRange(x=True, y=True)
    plot2.clear()
    plot2.getViewBox().removeItem(plot2.plotItem.legend)
    plot2.addLegend()
    plot2.enableAutoRange(x=True, y=True)


def update_fields():
    """
    Updates fields if they are valid
    """
    global num_of_steps, y0, x0, x_max
    if check_valid():
        num_of_steps = int(num_of_steps_field.text())
        y0 = float(y0_field.text())
        x0 = float(x0_field.text())
        x_max = float(xmax_field.text())


def check_valid():
    """
    Checks if fields are filled with correct values
    :return: True if values of fields are correct, False otherwise
    """

    def check_val_non_zero(a):
        return a.validator().validate(a.text(), 0)[0] == QtGui.QValidator.Acceptable and len(a.text()) > 0 and float(
            a.text()) != 0.0

    def check_val(a):
        return a.validator().validate(a.text(), 0)[0] == QtGui.QValidator.Acceptable and len(a.text()) > 0

    def set_back_color(field, color):
        field.setStyleSheet('QLineEdit { background-color: %s }' % color)

    global num_of_steps_field, y0_field, x0_field, xmax_field
    RED = '#f6989d'
    YELLOW = '#fff79a'
    WHITE = '#ffffff'

    set_back_color(y0_field, WHITE)
    set_back_color(x0_field, WHITE)
    set_back_color(xmax_field, WHITE)
    set_back_color(num_of_steps_field, WHITE)

    if not check_val(y0_field):
        set_back_color(y0_field, RED)
    else:
        if not check_val(x0_field):
            set_back_color(x0_field, RED)
        else:
            if not check_val_non_zero(xmax_field):
                set_back_color(xmax_field, RED)
            else:
                max_num = MAX_NUM_OF_STEPS
                if show_opt == 1:
                    max_num = MAX_NUM_OF_STEPS_ERROR
                if not (check_val_non_zero(num_of_steps_field) and max_num >= int(num_of_steps_field.text()) >= 1):
                    set_back_color(num_of_steps_field, RED)
                else:
                    if float(x0_field.text()) > float(xmax_field.text()):
                        set_back_color(x0_field, RED)
                        set_back_color(xmax_field, YELLOW)
                    return True
    return False


def change_plot2():
    global show_opt
    show_opt = (show_opt + 1) % 2
    if show_opt == 0:
        plot2_label.setText('Error')
        update_show_button.setText('Max Error')
    else:
        plot2_label.setText('Max Error')
        update_show_button.setText('Error')
    update()


# Start by initializing Qt
app = QtGui.QApplication([])

# Define a top-level widget to hold everything
w = QtGui.QWidget(windowTitle='DE Variant 11')

# Create some widgets to be placed inside
# Fonts for labels
big_font = QtGui.QFont('Roboto', 12, True)

font = QtGui.QFont('Roboto light', 10)

# Regular expressions for fields
REG_EXP_DOUBLE = QtGui.QRegExpValidator(QtCore.QRegExp('^(-?)(0|([1-9][0-9]*))(\\.[0-9]+)?$'))
REG_EXP_INTEGER = QtGui.QRegExpValidator(QtCore.QRegExp('^[1-9]\d*$'))

# Fields and labels
y0_field = QtGui.QLineEdit(str(y0))
y0_field.setValidator(REG_EXP_DOUBLE)
y0_field.textChanged.connect(update_fields)
y0_label = QtGui.QLabel('y0:', font=font, alignment=QtCore.Qt.AlignRight)

x0_field = QtGui.QLineEdit(str(x0))
x0_field.setValidator(REG_EXP_DOUBLE)
x0_field.textChanged.connect(update_fields)
x0_label = QtGui.QLabel('x0:', font=font, alignment=QtCore.Qt.AlignRight)

num_of_steps_field = QtGui.QLineEdit(str(num_of_steps))
num_of_steps_field.setValidator(REG_EXP_INTEGER)
num_of_steps_field.textChanged.connect(update_fields)
step_label = QtGui.QLabel('Number of steps:', font=font, alignment=QtCore.Qt.AlignRight)

xmax_field = QtGui.QLineEdit(str(x_max))
xmax_field.setValidator(REG_EXP_DOUBLE)
xmax_field.textChanged.connect(update_fields)
xmax_label = QtGui.QLabel('x max:', font=font, alignment=QtCore.Qt.AlignRight)

var_label = QtGui.QLabel('Variables', font=big_font, alignment=QtCore.Qt.AlignHCenter)

# Check Boxes
box_label = QtGui.QLabel("Graphs", font=big_font, alignment=QtCore.Qt.AlignHCenter)

exact_box = QtGui.QCheckBox("Exact", font=font)
exact_box.nextCheckState()
euler_box = QtGui.QCheckBox("Euler", font=font)
euler_box.nextCheckState()
impr_euler_box = QtGui.QCheckBox("Improved Euler", font=font)
runge_kutt_box = QtGui.QCheckBox("Runge Kutta", font=font)
ALG_BOX = [euler_box, impr_euler_box, runge_kutt_box]

# Buttons
update_button = QtGui.QPushButton('Update')
update_button.clicked.connect(update)
update_show_button = QtGui.QPushButton('Max Error')
update_show_button.clicked.connect(change_plot2)

# Plots
plot1 = pg.PlotWidget(w)
plot1.showGrid(x=True, y=True)
plot1_label = QtGui.QLabel('Solutions', font=big_font, alignment=QtCore.Qt.AlignHCenter)

plot2 = pg.PlotWidget(w)
plot2.showGrid(x=True, y=True)
plot2_label = QtGui.QLabel('Error', font=big_font, alignment=QtCore.Qt.AlignHCenter)

# Add widgets to the layout in their proper positions
layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
w.setLayout(layout)
button_layout = QtGui.QGridLayout()
plot_layout = QtGui.QVBoxLayout()

layout.addLayout(button_layout)
layout.addLayout(plot_layout, 9999)

# Add plots to layout
plot_layout.addWidget(plot1_label)
plot_layout.addWidget(plot1)

plot_layout.addWidget(plot2_label)
plot_layout.addWidget(plot2)

# Add fields and labels
button_layout.addWidget(var_label, 0, 0, 1, 2)

button_layout.addWidget(y0_label, 1, 0)
button_layout.addWidget(y0_field, 1, 1)

button_layout.addWidget(x0_label, 2, 0)
button_layout.addWidget(x0_field, 2, 1)

button_layout.addWidget(step_label, 3, 0)
button_layout.addWidget(num_of_steps_field, 3, 1)

button_layout.addWidget(xmax_label, 4, 0)
button_layout.addWidget(xmax_field, 4, 1)

button_layout.addWidget(box_label, 5, 0, 1, 2)
button_layout.addWidget(exact_box, 6, 0, 1, 2)
button_layout.addWidget(euler_box, 7, 0, 1, 2)
button_layout.addWidget(impr_euler_box, 8, 0, 1, 2)
button_layout.addWidget(runge_kutt_box, 9, 0, 1, 2)

# Add buttons
button_layout.addWidget(update_button, 10, 0, 1, 2)
button_layout.addWidget(update_show_button, 11, 0, 1, 2)
button_layout.addWidget(QtGui.QLabel(''), 12, 0, 100, 2)

# Update the plots, so they wouldn't be empty at launch
update()
# Display the widget Maximized
w.showMaximized()
# Display the widget as a new window
w.show()
# Start the Qt event loop
app.exec_()
