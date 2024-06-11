import cv2
import numpy as np
import pandas as pd
from npwriter import f_name
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors = 5)


def train_model():
    data = pd.read_csv(f_name).values

    X, Y = data[:, 1:-1], data[:, -1]
    
    model.fit(X, Y)
    print(X, Y)

