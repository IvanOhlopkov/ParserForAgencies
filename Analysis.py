import csv
import pandas as pd
from matplotlib import pyplot as plt

with open("all.csv", "r") as file:
     reader = csv.reader(file, delimiter= " ")
     row_count = len(list(reader))
print("Количество рекламных агенств/дизайн-студий всего: " +  str(row_count))

analys_read = pd.read_csv("all.csv", delimiter=";", encoding="windows-1251",
            names=["Агенство: ", "Телефон: ", "Страна: ", "Город: "])
analys_read = analys_read.fillna("Отсутствует страна")

countries = pd.unique(analys_read["Страна: "])

df = pd.DataFrame({"Страна": [countries[0], countries[1], countries[2],
                               countries[3]],
                    "Количество агенств": [analys_read["Страна: "].value_counts()[countries[0]],
                                           analys_read["Страна: "].value_counts()[countries[1]],
                                           analys_read["Страна: "].value_counts()[countries[2]],
                                           analys_read["Страна: "].value_counts()[countries[3]]]
                    })

df.groupby(["Страна"]).sum().plot(kind="pie", y="Количество агенств")

plt.show()

print(analys_read["Страна: "].value_counts().to_frame("Количество агенств: "))

print(analys_read["Город: "].value_counts().to_frame("Количество агенств: "))

