from flask import Flask, render_template, jsonify, request
import time
import random

app = Flask(__name__)

# ─────────────────────────────────────────────
#  SORTING ALGORITHMS — all implemented from scratch
#  Each yields snapshots so the frontend can animate step-by-step
# ─────────────────────────────────────────────

def bubble_sort_steps(arr):
    """O(n²) — compares adjacent pairs and swaps when out of order."""
    a = arr[:]
    steps = []
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            steps.append({
                "array": a[:],
                "comparing": [j, j + 1],
                "sorted_indices": list(range(n - i, n)),
                "swapped": False,
                "comparisons": comparisons,
                "swaps": swaps,
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                steps.append({
                    "array": a[:],
                    "comparing": [j, j + 1],
                    "sorted_indices": list(range(n - i, n)),
                    "swapped": True,
                    "comparisons": comparisons,
                    "swaps": swaps,
                })
    steps.append({
        "array": a[:],
        "comparing": [],
        "sorted_indices": list(range(n)),
        "swapped": False,
        "comparisons": comparisons,
        "swaps": swaps,
        "done": True,
    })
    return steps


def selection_sort_steps(arr):
    """O(n²) — finds minimum in unsorted portion and places it at front."""
    a = arr[:]
    steps = []
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            steps.append({
                "array": a[:],
                "comparing": [min_idx, j],
                "sorted_indices": list(range(i)),
                "min_index": min_idx,
                "swapped": False,
                "comparisons": comparisons,
                "swaps": swaps,
            })
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            steps.append({
                "array": a[:],
                "comparing": [i, min_idx],
                "sorted_indices": list(range(i + 1)),
                "min_index": min_idx,
                "swapped": True,
                "comparisons": comparisons,
                "swaps": swaps,
            })
    steps.append({
        "array": a[:],
        "comparing": [],
        "sorted_indices": list(range(n)),
        "swapped": False,
        "comparisons": comparisons,
        "swaps": swaps,
        "done": True,
    })
    return steps


def insertion_sort_steps(arr):
    """O(n²) — builds sorted array one element at a time."""
    a = arr[:]
    steps = []
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            steps.append({
                "array": a[:],
                "comparing": [j, j + 1],
                "sorted_indices": list(range(i)),
                "key_index": i,
                "swapped": False,
                "comparisons": comparisons,
                "swaps": swaps,
            })
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
                steps.append({
                    "array": a[:],
                    "comparing": [j + 1, j + 2],
                    "sorted_indices": list(range(i)),
                    "key_index": j + 1,
                    "swapped": True,
                    "comparisons": comparisons,
                    "swaps": swaps,
                })
            else:
                break
        a[j + 1] = key
    steps.append({
        "array": a[:],
        "comparing": [],
        "sorted_indices": list(range(n)),
        "swapped": False,
        "comparisons": comparisons,
        "swaps": swaps,
        "done": True,
    })
    return steps


def merge_sort_steps(arr):
    """O(n log n) — divide and conquer, merges sorted halves."""
    a = arr[:]
    steps = []
    comparisons = [0]
    swaps = [0]

    def merge(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            comparisons[0] += 1
            steps.append({
                "array": arr[:],
                "comparing": [left + i, mid + 1 + j],
                "merge_range": list(range(left, right + 1)),
                "swapped": False,
                "comparisons": comparisons[0],
                "swaps": swaps[0],
            })
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                swaps[0] += 1
                j += 1
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
        steps.append({
            "array": arr[:],
            "comparing": [],
            "merge_range": list(range(left, right + 1)),
            "swapped": True,
            "comparisons": comparisons[0],
            "swaps": swaps[0],
        })

    def merge_sort(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort(arr, left, mid)
            merge_sort(arr, mid + 1, right)
            merge(arr, left, mid, right)

    merge_sort(a, 0, len(a) - 1)
    steps.append({
        "array": a[:],
        "comparing": [],
        "sorted_indices": list(range(len(a))),
        "swapped": False,
        "comparisons": comparisons[0],
        "swaps": swaps[0],
        "done": True,
    })
    return steps


def quick_sort_steps(arr):
    """O(n log n) avg — partitions around a pivot."""
    a = arr[:]
    steps = []
    comparisons = [0]
    swaps = [0]

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparisons[0] += 1
            steps.append({
                "array": arr[:],
                "comparing": [j, high],
                "pivot_index": high,
                "partition_range": list(range(low, high + 1)),
                "swapped": False,
                "comparisons": comparisons[0],
                "swaps": swaps[0],
            })
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps[0] += 1
                steps.append({
                    "array": arr[:],
                    "comparing": [i, j],
                    "pivot_index": high,
                    "partition_range": list(range(low, high + 1)),
                    "swapped": True,
                    "comparisons": comparisons[0],
                    "swaps": swaps[0],
                })
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps[0] += 1
        return i + 1

    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    quick_sort(a, 0, len(a) - 1)
    steps.append({
        "array": a[:],
        "comparing": [],
        "sorted_indices": list(range(len(a))),
        "swapped": False,
        "comparisons": comparisons[0],
        "swaps": swaps[0],
        "done": True,
    })
    return steps


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sort", methods=["POST"])
def sort():
    data = request.get_json()
    algorithm = data.get("algorithm", "bubble")
    array = data.get("array", [])
    size = data.get("size", 20)

    if not array:
        array = random.sample(range(5, 100), min(size, 50))

    algo_map = {
        "bubble": bubble_sort_steps,
        "selection": selection_sort_steps,
        "insertion": insertion_sort_steps,
        "merge": merge_sort_steps,
        "quick": quick_sort_steps,
    }

    func = algo_map.get(algorithm, bubble_sort_steps)

    t0 = time.perf_counter()
    steps = func(array)
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 3)

    return jsonify({
        "steps": steps,
        "total_steps": len(steps),
        "elapsed_ms": elapsed_ms,
        "original_array": array,
    })


@app.route("/generate", methods=["GET"])
def generate():
    size = int(request.args.get("size", 20))
    order = request.args.get("order", "random")
    size = min(size, 60)

    if order == "random":
        arr = random.sample(range(5, 100), size)
    elif order == "sorted":
        arr = sorted(random.sample(range(5, 100), size))
    elif order == "reversed":
        arr = sorted(random.sample(range(5, 100), size), reverse=True)
    elif order == "nearly":
        arr = sorted(random.sample(range(5, 100), size))
        for _ in range(max(1, size // 10)):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
    else:
        arr = random.sample(range(5, 100), size)

    return jsonify({"array": arr})


@app.route("/explore")
def explore():
    return render_template("explore.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
