import pickle
import os.path

import tkinter.messagebox
from tkinter import *
from tkinter import simpledialog

import numpy as np
import PIL
import cv2 as cv

# Importing different types of models
# Your choice which ones you want to import 
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


class DrawingClassifier:
    
    def __init__(self):
        self.class1, self.class2, self.class3 = None, None, None
        self.class1_counter, self.class2_counter, self.class3_counter = None, None, None
        self.clf = None
        self.proj_name = None
        self.root = None
        self.image1 = None
        
        self.status_label = None
        self.canvas = None
        self.draw = None
        
        self.brush_width = 15
        
        self.classes_prompt()
        self.init_gui()
        
    def classes_prompt(self):
        msg = Tk()
        msg.withdraw()
        
        self.proj_name = simpledialog.askstring('Project Name', "Please enter your project name down below!", parent=msg)
        if os.path.exists(self.proj_name):
            with open(f"{self.proj_name}/{self.proj_name}_data.pikle", "rb") as f:
                data = pickle.load(f)
    def init_gui(self) -> None:
        pass