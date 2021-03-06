import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import fbeta_score, make_scorer, accuracy_score
from typing import Tuple, List
import nltk

nltk.download('punkt')
nltk.download('wordnet')
import pickle


def load_data(database_filepath):
    '''
    Function to load the database and table to panda dataframe
    Args: database_filepath: the path of the database
    Returns:    X: features (messages)
                y: categories (numeric)
                categories: An ordered list of categories name
    '''
    # loading the data from the db
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql("SELECT * FROM messages_table", engine)
    # creating a dataframe with only message feature.
    X = df['message']
    # creating dataframe with relevant categories.
    y = df.drop(['id', 'message', 'original', 'genre'], axis=1).astype(float)
    # storing the categories name list
    categories = y.columns.values
    return X, y, categories


def tokenize(text):
    '''
    Function for tokenizing string
    Args: Text string
    Returns: List of tokens
    '''
    tokens = nltk.word_tokenize(text)
    lemmatizer = nltk.WordNetLemmatizer()
    return [lemmatizer.lemmatize(x).lower().strip() for x in tokens]


def build_model():
    '''
    Function for building pipeline and GridSearch
    Args: None
    Returns: Model
    '''
    # creating pipeline with RandomForestClassifier to fit the model
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier())])
    # parameters grid search.
    parameters = {
        'clf__min_samples_split': [5, 10, 15],
        'clf__n_estimators': [50, 100, 150]}

    cv = GridSearchCV(pipeline, param_grid=parameters,
                      scoring='accuracy', verbose=1, n_jobs=-1)
    # for now retuning only pipeline for faster processing.
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Function for evaluating model by printing a classification report
    Args:   Model, features, labels to evaluate, and a list of categories
    Returns: Classification report
    '''
    y_pred = model.predict(X_test)
    print(classification_report(Y_test, y_pred, target_names=category_names))
    for idx, cat in enumerate(Y_test.columns.values):
        print("{} -- {}".format(cat, accuracy_score(Y_test.values[:, idx], y_pred[:, idx])))
    print("accuracy = {}".format(accuracy_score(Y_test, y_pred)))


def save_model(model, model_filepath):
    '''
    Function for saving the model as picklefile
    Args: Model, filepath
    Returns: Nothing.
    '''
    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database ' \
              'as the first argument and the filepath of the pickle file to ' \
              'save the model to as the second argument. \n\nExample: python ' \
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
