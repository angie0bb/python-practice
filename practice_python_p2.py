# Practice python, assignment 2
# sorting algorithms - bubble, insertion, merge, quick
  
import random
from time import time as get_time


# recursion limit
import sys
sys.setrecursionlimit(100000)

# Input, input validation
size = input("Size: ")
if (size.isdigit() is False) or (int(size) < 0):
    print("Please enter a positive number for the size of an array.")
    quit()

order = input("Order: ").capitalize()  # just to practice some string methods
if order not in ("Ascending", "Descending", "Random"):
    print("Please enter one of the following orders [Ascending, Descending, Random].")
    quit()

algorithm = input("Algorithm: ").lower()  # just to practice some string methods
if algorithm not in ("bubble", "insertion", "merge", "quick"):
    print("Please enter one of the following algorithms [bubble, insertion, merge, quick].")
    quit()

outputfile = input("Name of the output file: ")
if ".txt" not in outputfile:
    print("Please include .txt at the end of your file name.")
    quit()


# Ref: for bubbleSort, insertionSort, mergeSort, I have copied the codes from the lecture slides - Sorting
def bubbleSort(array):
    while(True):
        swapDetected = False
        for i in range(0, len(array)-1):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                swapDetected = True
        if not swapDetected:
            break


def insertionSort(array):
    for i in range(1, len(array)):
        val, pos = array[i], i
        while pos > 0 and array[pos-1] > val:
            array[pos] = array[pos-1]
            pos = pos-1
        array[pos] = val


def merge(dest, a1, a2):
    i, j, k = 0, 0, 0  # 1
    while i < len(a1) and j < len(a2):
        if a1[i] < a2[j]:
            dest[k]=a1[i]
            i=i+1
        else:
            dest[k]=a2[j]
            j=j+1
        k=k+1
    while i < len(a1):
        dest[k]=a1[i]
        i=i+1
        k=k+1
    while j < len(a2):
        dest[k]=a2[j]
        j=j+1
        k=k+1


def mergeSort(array):
    # base:
    if len(array) < 2:
        return
    # recursion:
    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
    mergeSort(left)
    mergeSort(right)
    merge(array, left, right)


# Reference: https://www.daleseo.com/sort-quick/
def quickSort(array):

    def quicksortHelper(low, high):
        if high <= low:
            return
        mid = partition(low, high)
        quicksortHelper(low, mid - 1)
        quicksortHelper(mid, high)

    def partition(low, high):
        # pivot = array[(low + high) // 2]  # choose middle element as pivot to overcome stack overflowing problem.
        pivot = array[low]  # choose a first element as pivot, it will crash the program with larger size of an array.
        while low <= high:
            while array[low] < pivot:
                low += 1
            while array[high] > pivot:
                high -= 1
            if low <= high:
                array[low], array[high] = array[high], array[low]
                low, high = low + 1, high - 1
        return low
    return quicksortHelper(0, len(array) - 1)


def sortArray(size, order, algorithm, outputfile):
    random_list = []
    # generate a random array with the specific order
    for i in range(int(size)):
        random_list.append(random.randrange(int(size)))
    if order == "Ascending":
        random_list.sort()
    elif order == "Descending":
        random_list.sort(reverse=True)

    # calling algorithm function and print the time
    if algorithm == "bubble":
        start = get_time()
        bubbleSort(random_list)
        end = get_time()
        print(f"{size}-{algorithm}-{order}: ", "{:.10f} s".format(end - start))
    elif algorithm == "insertion":
        start = get_time()
        insertionSort(random_list)
        end = get_time()
        print(f"{size}-{algorithm}-{order}: ", "{:.10f} s".format(end - start))
    elif algorithm == "merge":
        start = get_time()
        mergeSort(random_list)
        end = get_time()
        print(f"{size}-{algorithm}-{order}: ", "{:.10f} s".format(end - start))
    else:
        start = get_time()
        quickSort(random_list)
        end = get_time()
        print(f"{size}-{algorithm}-{order}: ", "{:.10f} s".format(end - start))

    # print(random_list)
    outputFile(outputfile, random_list)


def outputFile(filename, lst):
    with open(filename, 'w') as f:
        for line in lst:
            f.write(str(line))
            f.write('\n')


# calling sortArray function
sortArray(size, order, algorithm, outputfile)



# # Experiments to compare the efficiency
# # just to practice for loops :)
# size = [10, 100, 1000, 10000, 100000, 1000000]
# # size = [10]
# # order = ["Ascending", "Random", "Descending"]
# # algorithm = ["bubble", "insertion", "merge", "quick"]
# # the program stopped when the size of array exceeds 1000 for "quick" algorithm
#
# for i in range(len(size)):
#     for j in range(len(order)):
#         for k in range(len(algorithm)):
#             sortArray(size[i], order[j], algorithm[k], f"{size[i]}_{order[j]}_{algorithm[k]}.txt")

