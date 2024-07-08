import random

def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                yield True

def selection_sort(array):
    n = len(array)
    for s in range(n):
        min_idx = s
        for i in range(s + 1, n):
            if array[i] < array[min_idx]:
                min_idx = i
        array[s], array[min_idx] = array[min_idx], array[s]
        yield True

def insertion_sort(array):
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        yield True

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
            yield True
        while start + i < mid:
            array[k] = left[i]
            i += 1
            k += 1
            yield True
        while mid + j < end:
            array[k] = right[j]
            j += 1
            k += 1
            yield True

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
        yield True
        yield from heapify(array, n, largest)

def heap_sort(array):
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(array, n, i)
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        yield True
        yield from heapify(array, i, 0)

def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            yield True
    array[i + 1], array[high] = array[high], array[i + 1]
    yield True
    return i + 1

def quick_sort(array, low, high):
    if low < high:
        pi = yield from partition(array, low, high)
        yield from quick_sort(array, low, pi - 1)
        yield from quick_sort(array, pi + 1, high)
