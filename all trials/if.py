from sklearn import tree

age = 19

if age < 18:
    print("Not Allwoed")
elif age > 18 and age < 37:
    print("Perfect!")
else:
    print("OLD!!!")
# Sample data
X = [[10], [20], [30], [40], [50], [60], [70], [80]]
y = ["Not Allowed", "Not Allowed", "Perfect!", "Perfect!", "Perfect!", "OLD!!!", "OLD!!!", "OLD!!!"]

# Create decision tree classifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

# Predict the category for the given age
prediction = clf.predict([[age]])
import matplotlib.pyplot as plt

# Visualize the decision tree
plt.figure(figsize=(12,8))
tree.plot_tree(clf, filled=True, feature_names=["age"], class_names=clf.classes_)
plt.show()

print(prediction[0])