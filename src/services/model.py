import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

from npwriter import f_name

model = KNeighborsClassifier(n_neighbors = 5)


def train_model():
    data = pd.read_csv(f_name).values

    X, Y = data[:, 1:-1], data[:, -1]
    
    model.fit(X, Y)

