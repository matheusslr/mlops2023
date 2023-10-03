import zipfile
import os
import shutil
import urllib.request
import pandas as pd


def read_csv(path: str):
    """
    Reads a CSV file into a pandas DataFrame.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.
    """

    try:
        df_data = pd.read_csv(path)
        return df_data
    except FileNotFoundError as error:
        raise error
    except pd.errors.EmptyDataError as error:
        raise error


def extract_zip_file(zip_file_name='dataset/ml-25m.zip', dest_folder='dataset'):
    """ Extracts files from a ZIP archive and removes the ZIP file. """

    try:
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)

        print(f'ZIP file "{zip_file_name}" extracted to "{dest_folder}" successfully.')

        os.remove(zip_file_name)
        os.rename('dataset/ml-25m/movies.csv', f'{dest_folder}/movies.csv')
        os.rename('dataset/ml-25m/ratings.csv', f'{dest_folder}/ratings.csv')
        shutil.rmtree('dataset/ml-25m')

    except zipfile.BadZipFile as error:
        raise error
    except FileNotFoundError as error:
        raise error


def download_data(extract_path: str):
    """
    Downloads a ZIP archive from a specified URL, extracts its contents, and removes the ZIP file.
    """

    url = 'https://files.grouplens.org/datasets/movielens/ml-25m.zip'

    local_file_name = 'dataset/ml-25m.zip'

    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                print(f'Starting The ZIP file download')
                with open(local_file_name, 'wb') as local_file:
                    local_file.write(response.read())

                print(f'The ZIP file was successfully downloaded as {local_file_name}')

                extract_zip_file(local_file_name, extract_path)
            else:
                print(f'Download failed. Status code: {response.getcode()}')

    except urllib.error.URLError as error:
        raise error
