import re
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from exceptions.ResourceNotFound import ResourceNotFound
from util.data_util import read_csv, download_data

def clean_title(title: str) -> str:
    """
    Cleans a movie title by removing non-alphanumeric characters and extra spaces.

    Returns:
        str: The cleaned movie title.
    """
    if not isinstance(title, str):
        raise TypeError("Title argument must be a string.")

    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


def search(title: str, movies: pd.DataFrame) -> pd.DataFrame:
    """
    Performs a movie search based on a search title.

    Returns:
        pd.DataFrame: A DataFrame containing the search results, with the
        top 5 most similar movies.
    """
    if not isinstance(movies, pd.DataFrame):
        raise TypeError("The 'movies' argument must be a pandas DataFrame.")

    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies["clean_title"])

    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]

    return results


def find_movie_by_id(movie_id: int, movies: pd.DataFrame) -> pd.DataFrame:
    """
    Searches for a movie by its ID in a DataFrame of movies.

    Returns:
        pd.DataFrame: A DataFrame containing the information of the found movie.
    """
    movie = movies[movies["movieId"] == movie_id]
    if len(movie) == 0:
        raise ResourceNotFound("There's no movie found for this ID")
    return movie


def find_similar_movies_by_id(movie_id: int, movies: pd.DataFrame, ratings: pd.DataFrame):
    """
    Find and return a list of similar movies based on a given movie ID.

    Returns:
        pd.DataFrame: A DataFrame containing a list of similar movies based on user ratings.
    """
    similar_users = ratings[(ratings["movieId"] == movie_id)
                             & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users))
                                 & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index))
                        & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]

    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10) \
        .merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]


def display_search_results(data: widgets.Text, movie_list: widgets.Output()):
    """Event handler function that responds to user input events."""
    with movie_list:
        movie_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            display(search(title, data))

def display_movie_recommendations(data: widgets.Text, recommendation_list: widgets.Output,
                                   movies: pd.DataFrame, ratings: pd.DataFrame):
    """
    Event handler function that responds to user input events and displays movie recommendations
    """
    with recommendation_list:
        print(data)
        recommendation_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            results = search(title, movies)
            movie_id = results.iloc[0]["movieId"]
            display(find_similar_movies_by_id(movie_id, movies, ratings))


def main():
    """Main code"""
    download_data('dataset')
    movies = read_csv('dataset/movies.csv')

    movies["clean_title"] = movies["title"].apply(clean_title)

    movie_input = widgets.Text(
        value='Toy Story',
        description='Movie Title:',
        disabled=False
    )
    movie_list = widgets.Output()
    movie_input.observe(display_search_results, names='value')
    display(movie_input, movie_list)

    movie_id = 89745
    movie = movies[movies["movieId"] == movie_id]
    display(movie)

    ratings = read_csv('dataset/ratings.csv')
    display(find_similar_movies_by_id(movie_id, movies=movies, ratings=ratings))

    movie_name_input = widgets.Text(
        value='Toy Story',
        description='Movie Title:',
        disabled=False
    )
    recommendation_list = widgets.Output()
    movie_name_input.observe(display_movie_recommendations, names='value')
    display(movie_name_input, recommendation_list)


if __name__ == '__main__':
    main()
