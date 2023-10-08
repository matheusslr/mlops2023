import time
import requests
import pandas as pd

from bs4 import BeautifulSoup


def get_html_from_url(url: str) -> requests.Response:
    """
    Fetches HTML content from the specified URL and returns it as a response object.

    Args:
        url (str): The URL to retrieve HTML content from.

    Returns:
        requests.Response: A response object containing the HTML content.

    Raises:
        ValueError: If the URL is empty or None.
        requests.exceptions.HTTPError: If an HTTP error response is received.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.ConnectionError: If a connection error occurs during the request.
    """
    if not url:
        raise ValueError("URL cannot be empty or None.")

    try:
        response = requests.get(url, timeout=10)
        return response
    except requests.exceptions.HTTPError as err:
        raise err
    except requests.exceptions.Timeout as err:
        raise err
    except requests.exceptions.ConnectionError as err:
        raise err


def extract_match_stats(data: requests.Response) -> requests.Response:
    """
    Extracts match statistics data from a Premier League web page and returns it as a response object.

    Args:
        data (requests.Response): A response object containing HTML content.

    Returns:
        requests.Response: A response object containing match statistics data.

    This function scrapes match statistics data from a web page using BeautifulSoup
    and returns it as a response object. The input 'data' should be a response object
    obtained from a previous HTTP request to a web page containing match statistics.
    """
    soup = BeautifulSoup(data.text)
    standings_table = soup.select('table.stats_table')[0]
    links = standings_table.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]

    team_urls = [f"https://fbref.com{l}" for l in links]

    result = get_html_from_url(team_urls[0])
    return result


def get_match_shooting_stats(data: requests.Response) -> requests.Response:
    """
    Retrieves match shooting statistics from a Premier League web page and returns
    them as a response object.

    Args:
        data (requests.Response): A response object containing HTML content.

    Returns:
        requests.Response: A response object containing match shooting statistics.

    This function scrapes shooting statistics data from a web page using BeautifulSoup
    and returns it as a response object. The input 'data' should be a response object
    obtained from a previous HTTP request to a web page containing shooting statistics.
    """
    soup = BeautifulSoup(data.text)
    links = soup.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if l and 'all_comps/shooting/' in l]

    result = get_html_from_url(f"https://fbref.com{links[0]}")
    return result


def get_all_matches_from_interval_season(initial_year: int, final_year: int) -> list:
    """
    Retrieves match and shooting statistics for Premier League teams for a given season interval.

    Args:
        initial_year (int): The initial year of the season interval.
        final_year (int): The final year of the season interval.

    Returns:
        list of pd.DataFrame: A list of DataFrames containing match and shooting statistics data.

    This function scrapes match and shooting statistics for Premier League teams for a specified
    season interval using BeautifulSoup. It returns a list of DataFrames, each containing match
    and shooting statistics for a particular team in a specific season.
    """
    url = f'https://fbref.com/en/comps/9/{initial_year}-{final_year}/{initial_year}-{final_year}-Premier-League-Stats'
    years = list(range(final_year, initial_year, -1))
    all_matches = []

    for year in years:
        data = get_html_from_url(url)
        soup = BeautifulSoup(data.text)
        standings_table = soup.select('table.stats_table')[0]

        links = [l.get("href") for l in standings_table.find_all('a')]
        links = [l for l in links if '/squads/' in l]
        team_urls = [f"https://fbref.com{l}" for l in links]
        
        previous_season = soup.select("a.prev")[0].get("href")
        standings_url = f"https://fbref.com{previous_season}"
        
        for team_url in team_urls:
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
            data = get_html_from_url(team_url)
            matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            soup = BeautifulSoup(data.text)
            links = [l.get("href") for l in soup.find_all('a')]
            links = [l for l in links if l and 'all_comps/shooting/' in l]
            data = get_html_from_url(f"https://fbref.com{links[0]}")
            shooting = pd.read_html(data.text, match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()
            try:
                team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
            except ValueError:
                continue
            team_data = team_data[team_data["Comp"] == "Premier League"]
            
            team_data["Season"] = year
            team_data["Team"] = team_name
            all_matches.append(team_data)
            time.sleep(1)
    
    return all_matches


def main():
    """ Main code """
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    data = get_html_from_url(standings_url)
    
    raw_html_matches = extract_match_stats(data)
    matches = pd.read_html(raw_html_matches.text, match="Scores & Fixtures")[0]

    raw_html_shooting = get_match_shooting_stats(raw_html_matches)
    shooting = pd.read_html(raw_html_shooting.text, match="Shooting")[0]

    all_matches = get_all_matches_from_interval_season(2023, 2024)
    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]

    match_df.to_csv("matches.csv")

if __name__ == '__main__':
    main()
