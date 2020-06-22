import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_file():
    df = pd.read_csv("person2.csv", sep=';')
    return df


file = read_file()
print(file)

first_3 = file[16:45]


print(first_3['latitude'].min())

print(first_3['latitude'].max())

print(first_3['longitude'].min())

print(first_3['longitude'].max())

BBox = (first_3['latitude'].min(),   first_3['longitude'].max(),
         first_3['longitude'].min(), first_3['latitude'].max())

#ruh_m = plt.imread('map-2.png')















