import sys
import pandas as pd
from sqlalchemy import create_engine


def encode_categories(categories):
    '''
    Function where we will clean some data and give category numeric value.
    Args: categories data frame.
    Returns: encoded categories.
    '''

    # spiting the categories to get the separate categories name and values.
    categories = categories['categories'].str.split(';', expand=True)
    row = categories.iloc[[1]].values[0]
    categories.columns = [x.split("-")[0] for x in row]
    # giving the numerical value (0,1) to the categories
    for col in categories:
        categories[col] = categories[col].map(
            lambda x: 1 if int(x.split("-")[1]) > 0 else 0)
    return categories


def load_data(messages_filepath, categories_filepath):
    '''
    Function where we will merge the two dataset into one.
    Args:   messages_filepath: The file path to the messages.csv file.
            categories_filepath: The file path to the categories.csv file.
    Returns: A pandas DataFrame containing both files.
    '''

    # loading the messages csv file
    messages = pd.read_csv(messages_filepath)
    # getting the encoded categories from the function
    categories = encode_categories(pd.read_csv(categories_filepath))
    # combining the message and categories data to single datafarme
    return pd.concat([messages, categories], join="inner", axis=1)


def clean_data(df):
    '''
    Function to remove the duplicate from data frame
    Args: pandas DataFrame gross.
    Returns: pandas DataFrame after removing duplicate
    '''
    # removing the duplicate
    return df.drop_duplicates()


def save_data(df, database_filename):
    '''
    Function for saving the database in an sql file
    Args:   df: The pandas DataFrame which shall be saved
            database_filename: The path where the sql database shall be saved
    Returns: Nothing. The function saves the database in an sql file
    '''

    # saving the data to given filename.
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('messages_table', engine, if_exists='replace', index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories ' \
              'datasets as the first and second argument respectively, as ' \
              'well as the filepath of the database to save the cleaned data ' \
              'to as the third argument. \n\nExample: python process_data.py ' \
              'disaster_messages.csv disaster_categories.csv ' \
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
