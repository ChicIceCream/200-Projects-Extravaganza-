def sort_by_letter(arr):
    return sorted(arr, key=lambda x: [char for char in x if char.isalpha()])

print(sort_by_letter(["932c", "832u32", "2344b"]) == ["2344b", "932c", "832u32"])

print(sort_by_letter(["99a", "78b", "c2345", "11d"]) == ["99a", "78b", "c2345", "11d"])

print(sort_by_letter(["572z", "5y5", "304q2"]) == ["304q2", "5y5", "572z"])

print(sort_by_letter([]) == [])