from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits

# data = load_digits()
# print(f'data : {data}')

digits = load_digits()
data = scale(digits.data)

model = KMeans(n_clusters=10, init='random', n_init=10)
model.fit(data)
