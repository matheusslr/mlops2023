import os
import requests
import xmltodict

from airflow.providers.sqlite.hooks.sqlite import SqliteHook

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
EPISODE_FOLDER = "episodes"

def get_episodes():
    try:
        data = requests.get(PODCAST_URL, timeout=10)
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes
    except requests.exceptions.HTTPError as error:
        raise error
    except requests.exceptions.Timeout as error:
        raise error
    except requests.exceptions.ConnectionError as error:
        raise error

def load_episodes(episodes):
    hook = SqliteHook(sqlite_conn_id="podcasts")
    stored_episodes = hook.get_pandas_df("SELECT * from episodes;")
    new_episodes = []
    for episode in episodes:
        if episode["link"] not in stored_episodes["link"].values:
            filename = f"{episode['link'].split('/')[-1]}.mp3"
            new_episodes.append(
                [episode["link"], episode["title"], episode["pubDate"],
                    episode["description"], filename])

    hook.insert_rows(
        table='episodes',
        rows=new_episodes,
        target_fields=["link", "title", "published", "description", "filename"]
        )
    return new_episodes

def download_episodes(episodes):
    audio_files = []
    for episode in episodes:
        name_end = episode["link"].split('/')[-1]
        filename = f"{name_end}.mp3"
        audio_path = os.path.join(EPISODE_FOLDER, filename)
        if not os.path.exists(audio_path):
            print(f"Downloading {filename}")
            try:
                audio = requests.get(episode["enclosure"]["@url"], timeout=10)
                with open(audio_path, "wb+") as file:
                    file.write(audio.content)
            except requests.exceptions.HTTPError as error:
                raise error
            except requests.exceptions.Timeout as error:
                raise error
            except requests.exceptions.ConnectionError as error:
                raise error
            except requests.exceptions.RequestException as error:
                raise error
            except (IOError, FileNotFoundError) as error:
                raise error
        audio_files.append({
            "link": episode["link"],
            "filename": filename
        })
    return audio_files
