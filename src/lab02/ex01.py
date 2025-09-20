def min_max(nums: list[float | int]):
    if not nums:
        print("Value Error")
    min_val = min(nums)
    max_val = max(nums)
    return (min_val,max_val)
def unique_sorted(nums: list[float | int]):
    return (list(sorted(set(nums))))
def flatten(mat: list[list | tuple]):
    flattened_list = []
    for row in mat:
        if isinstance(row, (list, tuple)):
            flattened_list.extend(row)
        else:
            raise TypeError
    return (flattened_list)
print(min_max([42]))
print(unique_sorted([2.4,1,2,1,3]))
print(flatten([[1, 2], "ab"]))