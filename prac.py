from itertools import permutations

data = list(set(permutations('A' * 8 + 'B' * 2, 10)))
data = sorted(data)
print(data[23])