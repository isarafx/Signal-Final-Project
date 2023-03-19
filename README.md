![special](https://user-images.githubusercontent.com/32303293/98947774-31d69c80-2528-11eb-99df-6889b4209775.png)

# Signal Final Project

This is a group final project for the 010123106 Signal and System class at KMUTNB.<br>
The project involves a GUI program to control DS1054Z using Tkinter and DS1054Z class.

The program only works for Python >= 3.x.  <br>
Before running the program, please use the package manager pip to install dependencies.<br>

The wave_sample folder contains a list of various signals that can be used to plot,<br>
in case you don't have access to the equipment for convenient coding.

##How to use<br>
Create new enviroment or using the exist one and git pull this file
```bash
git init
git remote origin https://github.com/isarafx/Signal-Final-Project.git
git pull origin main
```
or just using
```bash
git pull https://github.com/isarafx/Signal-Final-Project.git
```
Then install the required dependency first
```bash
pip install -r requirements.txt
```
and you could run our program using IDE of your choice or through command line
```bash
python signal_work.py
```

### Dependency

* [ds1054z](https://github.com/pklaus/ds1054z) - for doing most things with ds1054z
* [NumPY](https://github.com/numpy/numpy) - not crucial but useful tools for create ploting list
* Tkinter - gui
* [Matplotlib](https://github.com/matplotlib/matplotlib) - for plotting graph

Our group consists of three members:

  - Mr.Isara Kunudomchhaiwat, 6001012610097
  - Mr.Phichet Eaktrakul, 6001012630071
  - Mr.Saksit Wilainuch, 6001012630144


