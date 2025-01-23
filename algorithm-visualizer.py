#inmport the libraries 

import streamlit as st
import matplotlib.pyplot as plt
import time

# Set the page configuration

st.set_page_config(page_title="Sorting and Searching Visualizer", layout="wide")

# CSS injection

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #1e1e1e; /* Dark background */
        color: white; /* Default text color */
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2e2e2e; /* Dark sidebar background */
        color: black; /* Set sidebar text color to black */
    }

    /* Sidebar header styling */
    .css-1d391kg h1 {
        color: black; /* Set the header text color to white */
    }

    /* Heading styling - ensure the title stays white */
    h1 {
        color: white !important; /* Force title color to white */
    }

    /* Button styling */
    div.stButton > button {
        background-color: #6a0dad; /* Purple button */
        color: white; /* Button text color */
    }

    /* Text input field styling */
    div.stTextInput > div > input {
        background-color: #2e2e2e; /* Dark input field */
        color: black; /* Text color in input field */
    }

    /* Text area styling */
    div.stTextArea > div > textarea {
        background-color: #2e2e2e; /* Dark text area */
        color: black; /* Text color in text area */
    }

    /* General text styling */
    .css-16huue1 {
        color: black; /* White text for markdown */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header

st.title("Sorting and Searching Visualizer")

# Visualization function for sorting

def visualize_sort(array, sort_function):
    st.write("Sorting Visualization:")
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the size of the figure
    bars = ax.bar(range(len(array)), array, color="purple", width=0.3)  # Adjusted bar width

    # Display array elements above the bars
    for i, v in enumerate(array):
        ax.text(i, v + 0.1, str(v), ha="center", color="black", fontsize=10)

    # Create a placeholder for the plot that can be updated
    plot_placeholder = st.empty()
    plot_placeholder.pyplot(fig)

    for state in sort_function(array):
        ax.clear()  # Clear previous bars
        bars = ax.bar(range(len(state)), state, color="purple", width=0.3)  # Adjusted bar width

        # Re-add the text annotations for updated state
        for i, v in enumerate(state):
            ax.text(i, v + 0.1, str(v), ha="center", color="black", fontsize=10)

        plot_placeholder.pyplot(fig)  # Update the plot with the new state
        time.sleep(0.1)  # Add a small delay to make the visualization visible

# Sorting Algorithms 

def bubble_sort(array):
    array = array.copy()
    for i in range(len(array) - 1):
        for j in range(len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            yield array

def selection_sort(array):
    array = array.copy()
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        yield array

def insertion_sort(array):
    array = array.copy()
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        yield array

def merge_sort(array):
    array = array.copy()
    def merge_sort_recursive(array, start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from merge_sort_recursive(array, start, mid)
            yield from merge_sort_recursive(array, mid, end)
            left, right = array[start:mid], array[mid:end]
            i, j, k = 0, 0, start
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                array[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                array[k] = right[j]
                j += 1
                k += 1
            yield array
    yield from merge_sort_recursive(array, 0, len(array))

def quick_sort(array):
    array = array.copy()
    def quick_sort_recursive(array, start, end):
        if start < end:
            pivot = array[end]
            i = start - 1
            for j in range(start, end):
                if array[j] < pivot:
                    i += 1
                    array[i], array[j] = array[j], array[i]
                yield array
            array[i + 1], array[end] = array[end], array[i + 1]
            yield array
            yield from quick_sort_recursive(array, start, i)
            yield from quick_sort_recursive(array, i + 2, end)
    yield from quick_sort_recursive(array, 0, len(array) - 1)

def heap_sort(array):
    array = array.copy()
    def heapify(array, n, i):
        largest = i
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and array[largest] < array[left]:
            largest = left
        if right < n and array[largest] < array[right]:
            largest = right
        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            yield from heapify(array, n, largest)
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(array, n, i)
    for i in range(n - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        yield array
        yield from heapify(array, i, 0)

def shell_sort(array):
    array = array.copy()
    gap = len(array) // 2
    while gap > 0:
        for i in range(gap, len(array)):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
            yield array
        gap //= 2

# Linear Search Algorithm 

def linear_search(arr, target):
    steps = []
    for idx, value in enumerate(arr):
        if value == target:
            reason = f"Found {target} at index {idx}."
            steps.append((arr[:], idx, target, reason))
            break
        else:
            reason = f"{value} is not equal to {target}."
            steps.append((arr[:], idx, target, reason))
    if not any(step[2] == target for step in steps):  # If target was not found
        steps.append((arr[:], -1, target, "Target not found."))
    return steps

# Binary Search Algorithm 

def binary_search(arr, target):
    steps = []
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            reason = f"Found {target} at index {mid}."
            steps.append((arr[:], mid, target, reason))
            break
        elif arr[mid] < target:
            reason = f"{arr[mid]} is less than {target}, searching the right half."
            left = mid + 1
        else:
            reason = f"{arr[mid]} is greater than {target}, searching the left half."
            right = mid - 1
        steps.append((arr[:], mid, target, reason))
    if left > right:
        steps.append((arr[:], -1, target, "Target not found."))
    return steps

# Visualization function for search steps

def visualize_steps(steps, algorithm):
    placeholder = st.empty()
    for step in steps:
        arr, idx, target, reason = step
        colors = [
            'blue' if i == idx and arr[i] == target else 'red' if i == idx else 'skyblue'
            for i in range(len(arr))
        ]
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(arr)), arr, color=colors, width=0.3)
        for i, v in enumerate(arr):
            ax.text(i, v + 0.1, str(v), ha="center", color="black", fontsize=10)

        ax.set_title(f"Step: {reason}")
        placeholder.pyplot(fig)
        time.sleep(0.5)

# Sidebar Controls 

st.sidebar.header("User Input")
array_size = st.sidebar.number_input("Enter Array Size", min_value=1, value=10, step=1)
array = st.sidebar.text_area("Enter Array Elements (comma-separated)", value=",".join([str(i) for i in range(1, array_size + 1)]))
target = st.sidebar.number_input("Enter Target Value", value=5)

# Convert array input to list of integers

array = [int(x) for x in array.split(",")]

# Select Sorting Algorithm

selected_sort = st.sidebar.selectbox("Select Sorting Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort"])

# Sort visualization

if st.sidebar.button("Visualize Sort"):
    if selected_sort == "Bubble Sort":
        visualize_sort(array, bubble_sort)
    elif selected_sort == "Selection Sort":
        visualize_sort(array, selection_sort)
    elif selected_sort == "Insertion Sort":
        visualize_sort(array, insertion_sort)
    elif selected_sort == "Merge Sort":
        visualize_sort(array, merge_sort)
    elif selected_sort == "Quick Sort":
        visualize_sort(array, quick_sort)
    elif selected_sort == "Heap Sort":
        visualize_sort(array, heap_sort)
    elif selected_sort == "Shell Sort":
        visualize_sort(array, shell_sort)

# Select Search Algorithm

selected_search = st.sidebar.selectbox("Select Search Algorithm", ["Linear Search", "Binary Search"])

# Search visualization

if st.sidebar.button("Visualize Search"):
    if selected_search == "Linear Search":
        steps = linear_search(array, target)
    elif selected_search == "Binary Search":
        array.sort()  # Sort array for binary search
        steps = binary_search(array, target)

    visualize_steps(steps, selected_search)
