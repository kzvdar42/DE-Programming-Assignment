# Differential Equations Programming Assignment
This is a solution to the assignment given during the Differential Equations course in Innopolis University.\
Author : Kuleykin Vladislav.\
Variant 11.

## General information
In this task we've been asked to implement the different approximation methods (Euler, improved Euler and Runge-Kutta) for solving Initial value problem with data visualization and possibility of changing input.\
Given equation:
 ### y' = e<sup>(-sin⁡(x))</sup> - y * cos(x);  x<sub>0</sub> = 0, y<sub>0</sub> = 1, x<sub>max</sub> = 9.3

So I was lucky because this equation does not have any breakpoints and continuous on all interval.

## Implementation
I implemented all in Python using next libraries:\
**NumPy** – computation (sin(), cos(), etc.),\
**PyQtGraph** – visualization of graphs,\
**PyQt5** – UI of the program.

## How to run
For the ease of installation of needed libraries you can launch the ```init.bat``` file from the main folder, or directly```main.py``` with administrative rights.

If you already have all needed libraries installed, you can just run the ```main.py```.

## Limits of input
**Logic** - only real numbers (except the field ‘Number of steps’), x_max>x_0 and Number of steps in greater than or equal to 1.\
**Computational limitations** - Number of steps is limited by 1000 then computing Max error function and limited by 100000 otherwise due the time and memory consumption.

