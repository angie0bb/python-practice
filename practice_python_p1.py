# Practice python, assignment 1
# function, loop
"""
Write python code that accepts a CSV file and summarizes the data within it for each column.
For each numerical column in the file, calculate the follwing:
1. maximum
2. minimum
3. average
4. standard deviation
5. most common value
6. histogram for each numeric column

Do not use "min", "max", "sort", "avg" functions.
Use only "csv", "matplotlib" libraries.
"""


import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def calculation(file_name):

    with open(file_name) as file:
        reader = csv.reader(file)
        header = next(reader)  # it will only read one line and delete this line from the reader
        num_of_column = len(header)
        # print(header)

        data_lst = []
        for i in range(num_of_column):
            data_lst.append([])
        # print(data_lst)

        for line in reader:  # read each column as a list
            # print(line)
            for index in range(len(line)):
                # print(line[index])
                data_lst[index].append(line[index])

        # store each column's results in dictionary (for dataframe)
        value_dict = {}

        for index, criteria in enumerate(data_lst):  # to get header and value in the list
            # print(criteria)

            value_lst = []  # initialize a list to put in a dataframe
            # Finding maximum
            maximum = 0
            try:
                for value in criteria:
                    if float(value) > maximum:
                        maximum = float(value)
                value_lst.append(maximum)

            except:
                value_lst.append("NA")

            # minimum
            minimum = maximum
            try:
                for value in criteria:
                    if float(value) < minimum:
                        minimum = float(value)
                value_lst.append(minimum)

            except:
                value_lst.append("NA")

            # Average
            total = 0
            average = 0
            try:
                for value in criteria:
                    total += float(value)
                    average = round(total / len(criteria), 3)
                value_lst.append(average)

            except:
                value_lst.append("NA")

            # Standard Deviation
            sd = 0
            sum_of_distance = 0
            try:
                for value in criteria:
                    sum_of_distance += (float(value) - average) ** 2
                    sd = round((sum_of_distance/len(criteria))**(1/2), 3)
                value_lst.append(sd)

            except:
                value_lst.append("NA")

            # Most common value
            common_dict = {}
            try:
                # get unique value and counts
                for value in criteria:
                    if value not in common_dict:
                        common_dict[value] = 1
                    else:
                        common_dict[value] += 1

                # find maximum from the dictionary
                max_key = ""
                max_value = 0
                for key, value in common_dict.items():
                    if max_value < value:
                        max_key = key
                        max_value = value

                if max_value >= 1:
                    value_lst.append(max_key)

            except:
                value_lst.append("NA")

            # Histogram
            try:
                # sort values
                for i in range(len(criteria)):
                    for j in range(i + 1, len(criteria)):
                        if criteria[i] > criteria[j]:
                            criteria[i], criteria[j] = criteria[j], criteria[i]

                # put unique value as a key and count as a value in the counts_dict
                counts_dict = {}
                for value in criteria:
                    if value not in counts_dict:
                        counts_dict[value] = 1
                    else:
                        counts_dict[value] += 1

                # get keys and values as a list
                unique_value_lst = list(counts_dict.keys())
                counts_value_lst = list(counts_dict.values())

                # print(unique_value_lst)
                # print(counts_value_lst)

                # graph histogram!
                plt.bar(unique_value_lst, counts_value_lst)
                plt.title(f"{header[index]}'s histogram")
                plt.xlabel(f"Unique values of {header[index]}")
                plt.ylabel(f"Counts")
                plt.show()

            except:
                print(f"{header[index]}'s histogram: NA")

            # print(value_lst)
            value_dict[header[index]] = value_lst

        df = pd.DataFrame(list(zip(*value_dict.values())), index=["max", "min", "average", "sd", "common"], columns=header)
        print(df)


# calculation("Student_Grades.csv")
calculation("Bank_Customers.csv")
# calculation("US_Cities_Population.csv")
# calculation("Office_Supplies.csv")





