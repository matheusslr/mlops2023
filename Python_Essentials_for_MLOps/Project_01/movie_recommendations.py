import re
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_title(title: str):
    """
        Cleans a movie title by removing non-alphanumeric characters and extra spaces.

    Args:
        title (str): The movie title to be cleaned.

    Returns:
        str: The cleaned movie title.
    """
    if not isinstance(title, str):
        raise ValueError("Title argument must be a string.")

    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


def search(title: str, movies: pd.DataFrame, vectorizer: TfidfVectorizer, tfidf: spmatrix):
    """
        Performs a movie search based on a search title.

    Args:
        title (str): The search title.

        movies (pd.DataFrame): A DataFrame containing information about movies.

        vectorizer (TfidfVectorizer): A text vectorization object that transforms the
        search title into a numeric vector.

        tfidf (spmatrix): A set of TF-IDF vectors representing the movies.

    Returns:
        pd.DataFrame: A DataFrame containing the search results, with the
        top 5 most similar movies.

    """
    if not isinstance(movies, pd.DataFrame):
        raise ValueError("The 'movies' argument must be a pandas DataFrame.")
    if not isinstance(vectorizer, TfidfVectorizer):
        raise ValueError("The 'vectorizer' argument must be an instance of TfidfVectorizer.")
    if not isinstance(tfidf, spmatrix):
        raise ValueError("The 'tfidf' argument must be a sparse matrix (spmatrix) of TF-IDF.")

    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]

    return results


def main():
    teste = clean_title("teste")
    print(teste)


if __name__ == '__main__':
    main()
