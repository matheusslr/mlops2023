import re
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from exceptions.ResourceNotFound import ResourceNotFound


def clean_title(title: str):
    """
    Cleans a movie title by removing non-alphanumeric characters and extra spaces.

    Returns:
        str: The cleaned movie title.
    """
    if not isinstance(title, str):
        raise TypeError("Title argument must be a string.")

    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


def search(
        title: str,
        movies: pd.DataFrame,
        vectorizer: TfidfVectorizer,
        tfidf: spmatrix
):
    """
    Performs a movie search based on a search title.

    Returns:
        pd.DataFrame: A DataFrame containing the search results, with the
        top 5 most similar movies.
    """
    if not isinstance(movies, pd.DataFrame):
        raise TypeError("The 'movies' argument must be a pandas DataFrame.")
    if not isinstance(vectorizer, TfidfVectorizer):
        raise TypeError(
            "The 'vectorizer' argument must be an instance of TfidfVectorizer.")
    if not isinstance(tfidf, spmatrix):
        raise TypeError(
            "The 'tfidf' argument must be a sparse matrix (spmatrix) of TF-IDF.")

    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]

    return results


def find_movie_by_id(movie_id: int, movies: pd.DataFrame):
    """
    Searches for a movie by its ID in a DataFrame of movies.

    Returns:
        pd.DataFrame: A DataFrame containing the information of the found movie.
    """
    movie = movies[movies["movieId"] == movie_id]
    if len(movie) == 0:
        raise ResourceNotFound("There's no movie found for this ID")
    return movie


def main():
    movies = pd.read_csv('dataset/movies.csv')
    movies["clean_title"] = movies["title"].apply(clean_title)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(movies["clean_title"])
    print(search("The", movies, vectorizer, tfidf))


if __name__ == '__main__':
    main()
