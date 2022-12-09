import urllib.request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

file_name = 'dataR2.csv'
def download_file(file_name):
    print('Descargando el dataset')
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00451/dataR2.csv'
    urllib.request.urlretrieve(url, file_name)
download_file(file_name)

data = pd.read_csv(file_name)
y = data["Classification"]
X = data.drop(["Classification"], axis=1)
(X_train, X_test,
 y_train, y_test) = train_test_split(X,
                                     y,
                                     stratify=y,
                                     test_size=0.33,
                                     random_state=11)
                                     
tree = DecisionTreeClassifier(random_state=11)
tree.fit(X_train, y_train)
print(f"Tree Accuracy: {tree.score(X_test, y_test)}")
  
model = RandomForestClassifier(random_state=11, n_estimators=200,
                               class_weight="balanced", max_features="log2")
model.fit(X_train, y_train)
print(f"RF Accuracy: {model.score(X_test, y_test)}")
