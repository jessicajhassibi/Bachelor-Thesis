import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler


def text2vec(text, keyed_vectors):
    # takes gensim KeyedVectors object  and pandas series object of preprocessed sentences
    # and maps each word in the sentences to the corrseponding vector
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
    if classifier_type == "Random Forest":
        classifier = RandomForestClassifier()
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
    print('accuracy %s' % accuracy_score(y_pred, y_test))
    print(classification_report(y_test, y_pred,target_names=["persecuted composers", "supported composers"]))