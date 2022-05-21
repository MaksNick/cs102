from math import log

import numpy as np


class NaiveBayesClassifier:
    def __init__(self):
        self.dict = {}
        self.classes = {}
        self.points = 0

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to x, y."""
        values, counts = np.unique(np.array(y), return_counts=True)
        count = {value: 0 for value in values}
        self.classes = {values[i]: counts[i] / len(y) for i in range(len(values))}
        for i, text in enumerate(X):
            for item in text:
                if item not in self.dict:
                    self.dict[item] = {value: 0 for value in values}
                self.dict[item][y[i]] += 1
                count[y[i]] += 1

        for item, counter in self.dict.items():
            probabilities = {
                key: (counter[key] + 1) / (count[key] + 1 * len(self.dict))
                for key in counter.keys()
            }
            self.dict[item] = probabilities

    def predict(self, X):
        """Perform classification on an array of test vectors x."""
        prediction = []
        for text in X:
            predict = {key: log(value) for key, value in self.classes.items()}
            for item in text:
                if item in self.dict:
                    for key in predict.keys():
                        predict[key] += log(self.dict[item][key])
            prediction.append(list(dict(sorted(predict.items(), key=lambda x: x[1])))[-1])
        return prediction

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        for i, label in enumerate(y_test):
            if self.predict(X_test)[i] == label:
                self.points += 1
        return self.points / len(y_test)
