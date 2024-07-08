import tkinter as tk
import random
import time

# Constants
WIDTH, HEIGHT = 1000, 700
BAR_WIDTH = 10

# Initialize Tkinter
root = tk.Tk()
root.title("Sorting Visualizer")

# Canvas for drawing bars
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Global variables
array_size = WIDTH // BAR_WIDTH
sorting_algorithm_generator = None
sorting = False
start_time = 0

# Function to draw bars with colors
def draw_bars(array, colors={}):
    canvas.delete("all")
    for i, val in enumerate(array):
        color = "sky blue" if i not in colors else colors[i]
        canvas.create_rectangle(i * BAR_WIDTH, HEIGHT, (i + 1) * BAR_WIDTH, HEIGHT - val, fill=color)
    root.update()

# Function to generate random array
def generate_random_array(size):
    return [random.randint(10, HEIGHT - 50) for _ in range(size)]

# Function to start sorting based on selected algorithm
def start_sorting(selected_algorithm, array):
    global sorting_algorithm_generator, sorting, start_time
    sorting = True
    start_time = time.time()  # Start time for stopwatch
    if selected_algorithm == 'Bubble Sort':
        sorting_algorithm_generator = bubble_sort(array)
    elif selected_algorithm == 'Selection Sort':
        sorting_algorithm_generator = selection_sort(array)
    elif selected_algorithm == 'Insertion Sort':
        sorting_algorithm_generator = insertion_sort(array)
    elif selected_algorithm == 'Merge Sort':
        sorting_algorithm_generator = merge_sort(array, 0, len(array))
    elif selected_algorithm == 'Heap Sort':
        sorting_algorithm_generator = heap_sort(array)
    elif selected_algorithm == 'Quick Sort':
        sorting_algorithm_generator = quick_sort(array, 0, len(array) - 1)
    else:
        sorting_algorithm_generator = None

    # Start sorting in a separate thread to avoid freezing the GUI
    root.after(100, perform_sorting)

# Function to perform sorting
def perform_sorting():
    global sorting_algorithm_generator, sorting
    if sorting:
        try:
            next(sorting_algorithm_generator)
            root.after(50, perform_sorting)  # Continue sorting after a delay
        except StopIteration:
            sorting = False
            show_time_taken()

# Function to display time taken after sorting completes
def show_time_taken():
    global start_time
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_label.config(text=f"Time taken: {elapsed_time:.2f} seconds")

# Bubble sort algorithm
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_bars(array, {j: "red", j + 1: "blue"})
                yield True

# Selection sort algorithm
def selection_sort(array):
    n = len(array)
    for s in range(n):
        min_idx = s
        for i in range(s + 1, n):
            if array[i] < array[min_idx]:
                min_idx = i
        array[s], array[min_idx] = array[min_idx], array[s]
        draw_bars(array, {s: "red", min_idx: "blue"})
        yield True

# Insertion sort algorithm
def insertion_sort(array):
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        draw_bars(array, {i: "red", j + 1: "blue"})
        yield True

# Merge sort algorithm
def merge_sort(array, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(array, start, mid)
        yield from merge_sort(array, mid, end)
        left = array[start:mid]
        right = array[mid:end]
        k = start
        i = j = 0
        while start + i < mid and mid + j < end:
            if left[i] <= right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1
            draw_bars(array, {k: "green"})
            yield True
        while start + i < mid:
            array[k] = left[i]
            i += 1
            k += 1
            draw_bars(array, {k: "green"})
            yield True
        while mid + j < end:
            array[k] = right[j]
            j += 1
            k += 1
            draw_bars(array, {k: "green"})
            yield True

# Heapify function for heap sort
def heapify(array, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and array[l] > array[largest]:
        largest = l
    if r < n and array[r] > array[largest]:
        largest = r

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        draw_bars(array, {i: "red", largest: "blue"})
        yield True
        yield from heapify(array, n, largest)

# Heap sort algorithm
def heap_sort(array):
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(array, n, i)
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        draw_bars(array, {i: "red", 0: "blue"})
        yield True
        yield from heapify(array, i, 0)

# Partition function for quick sort
def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            draw_bars(array, {i: "red", j: "blue"})
            yield True
    array[i + 1], array[high] = array[high], array[i + 1]
    draw_bars(array, {i + 1: "red", high: "blue"})
    yield True
    return i + 1

# Quick sort algorithm
def quick_sort(array, low, high):
    if low < high:
        pi = yield from partition(array, low, high)
        yield from quick_sort(array, low, pi - 1)
        yield from quick_sort(array, pi + 1, high)

# Function to handle start sorting button click
def start_button_click():
    selected_algorithm = algorithm_selector.get()
    if random_var.get() == 1:  # Random array generation selected
        array = generate_random_array(array_size)
    else:  # Manual array input selected
        array = [int(num) for num in manual_entry.get().split() if num.isdigit()]
    start_sorting(selected_algorithm, array)

# GUI elements
top_frame = tk.Frame(root)
top_frame.pack()

time_label = tk.Label(top_frame, text="Time taken: ")
time_label.pack()

algorithm_label = tk.Label(root, text="Select Sorting Algorithm:")
algorithm_label.pack()

algorithm_selector = tk.StringVar(root)
algorithm_selector.set('Bubble Sort')
algorithm_menu = tk.OptionMenu(root, algorithm_selector, 'Bubble Sort', 'Selection Sort', 'Insertion Sort',
                               'Merge Sort', 'Heap Sort', 'Quick Sort')
algorithm_menu.pack()

random_var = tk.IntVar()
random_checkbox = tk.Checkbutton(root, text="Random Array", variable=random_var)
random_checkbox.pack()

manual_label = tk.Label(root, text="Enter Array Elements (space-separated):")
manual_label.pack()

manual_entry = tk.Entry(root, width=50)
manual_entry.pack()

start_button = tk.Button(root, text="Start Sorting", command=start_button_click)
start_button.pack()

quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.pack()

# Main loop
root.mainloop()
