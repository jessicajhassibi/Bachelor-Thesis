import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler

from data import get_groups


def text2vec(text, keyed_vectors):
    # takes gensim KeyedVectors object  and pandas series object of preprocessed sentences
    # and maps each word in the sentences to the corresponding vector
    # returns numpy array (for the text) of numpy arrays (sentences) of vectors (words)

    words = set(keyed_vectors.index_to_key)
    text_vect = np.array([np.array([keyed_vectors[i] for i in sentence if i in words])
                          for sentence in text])
    return text_vect


def average_vector(text_vect):
    # Compute sentence vectors by averaging the word vectors for the words contained in the sentence
    avg = []
    for sentence in text_vect:
        if sentence.size:
            avg.append(sentence.mean(axis=0))
        else:
            avg.append(np.zeros(100, dtype=float))
    return avg


def classify_predict(X_train_avg, X_test_avg, y_train_data, classifier_type: str = "Random Forest"):
    print("############################################################################")
    print(f"Processing {classifier_type} Classification\n")
    if classifier_type == "Random Forest":
        classifier = RandomForestClassifier()
    elif classifier_type == "SVM":
        classifier = svm.SVC()
    elif classifier_type == "Multinomial Naive Bayes":
        classifier = MultinomialNB()
        # use MinMaxScaler to remove negative numbers
        scaler = MinMaxScaler()
        X_train_avg = scaler.fit_transform(X_train_avg)
        X_test_avg = scaler.transform(X_test_avg)

    classifier_model = classifier.fit(X_train_avg, y_train_data.values.ravel())
    # Use the trained model to make predictions on the test data
    y_pred_data = classifier_model.predict(X_test_avg)
    return y_pred_data


def print_classification_report(y_pred, y_test):
    group_0, group_1 = get_groups()
    print(classification_report(y_test, y_pred, target_names=[group_0.label, group_1.label]))
    print(f"classes in y_pred: {set(y_pred)} classes in y_test: {set(y_test)}")
    print("############################################################################")
