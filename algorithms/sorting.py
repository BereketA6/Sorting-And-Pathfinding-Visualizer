"""
Each sorting function is a generator: instead of sorting the array and
returning, it `yield`s the current state of the array after every
meaningful step (a comparison or a swap). The visualizer's main loop
pulls one step at a time and redraws, which is what creates the
animation — the algorithm itself doesn't know or care that it's being
animated.

Yielded value: (array_snapshot, comparing_indices, swapped_indices, sorted_indices)
- comparing_indices: indices currently being compared (highlighted yellow)
- swapped_indices: indices just swapped (highlighted red)
- sorted_indices: indices confirmed in final sorted position (highlighted green)
"""


def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    sorted_idx = set()
    for i in range(n):
        for j in range(0, n - i - 1):
            yield arr[:], (j, j + 1), (), sorted_idx.copy()
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr[:], (), (j, j + 1), sorted_idx.copy()
        sorted_idx.add(n - i - 1)
    yield arr[:], (), (), set(range(n))


def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    sorted_idx = set()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr[:], (min_idx, j), (), sorted_idx.copy()
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr[:], (), (i, min_idx), sorted_idx.copy()
        sorted_idx.add(i)
    yield arr[:], (), (), set(range(n))


def insertion_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            yield arr[:], (j, j + 1), (), set(range(i))
            arr[j + 1] = arr[j]
            j -= 1
            yield arr[:], (), (j + 1, j + 2), set(range(i))
        arr[j + 1] = key
        yield arr[:], (), (), set(range(i + 1))
    yield arr[:], (), (), set(range(n))


def merge_sort(arr):
    arr = arr[:]
    n = len(arr)

    def merge_sort_helper(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        yield from merge_sort_helper(lo, mid)
        yield from merge_sort_helper(mid, hi)

        left = arr[lo:mid]
        right = arr[mid:hi]
        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            yield arr[:], (lo + i, mid + j), (), set()
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            yield arr[:], (), (k,), set()
            k += 1
        while i < len(left):
            arr[k] = left[i]
            yield arr[:], (), (k,), set()
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            yield arr[:], (), (k,), set()
            j += 1
            k += 1

    yield from merge_sort_helper(0, n)
    yield arr[:], (), (), set(range(n))


def quick_sort(arr):
    arr = arr[:]
    n = len(arr)

    def quick_sort_helper(lo, hi):
        if lo >= hi:
            return
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            yield arr[:], (j, hi), (), set()
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr[:], (), (i, j), set()
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        yield arr[:], (), (i + 1, hi), set()
        yield from quick_sort_helper(lo, i)
        yield from quick_sort_helper(i + 2, hi)

    yield from quick_sort_helper(0, n - 1)
    yield arr[:], (), (), set(range(n))


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}
