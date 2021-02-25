# AUTOGENERATED! DO NOT EDIT! File to edit: 000_data.ipynb (unless otherwise specified).

__all__ = ['DATA_PATH', 'fetch_dataset', 'pickle_loader', 'data_au_jobs', 'data_wine_reviews', 'data_wiki_movies',
           'data_women_clothing_reviews', 'data_au_election_2019_tweets', 'data_dickens_corpus', 'GUTENBERG_DICKENS']

# Cell
from pathlib import Path
import pickle5 as pickle
import pandas as pd
from urllib.request import urlretrieve
import urllib.parse
from tqdm.auto import tqdm

import typing as T

DATA_PATH = (Path.home() / ".cache") / "mlzero"

# Cell
def fetch_dataset(filename: str, data_path: Path = DATA_PATH, force: bool = False, data_loader=pd.read_csv) -> pd.DataFrame:
    """Loads a stored dataset, with  a progress bar"""
    dest = Path(data_path) / filename
    if force or not dest.exists():
        Path(data_path).mkdir(exist_ok=True, parents=True)
        url = f'https://skeptric.com/datasets/{filename}'
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
            urlretrieve(url, dest, reporthook=t.update_to)
    return data_loader(dest)

# Cell
def pickle_loader(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# Cell
def data_au_jobs(data_path: Path = DATA_PATH, force: bool = False) -> pd.DataFrame:
    """Gets Australian Job Ads

    License: CC BY-NC-SA 4.0
    See https://github.com/EdwardJRoss/job-advert-analysis
    """
    return fetch_dataset('au_jobs.pkl', data_path, force=force, data_loader=pickle_loader)

# Cell
def data_wine_reviews(data_path: Path = DATA_PATH, force: bool = False) -> pd.DataFrame:
    """Retrieves Wine Reivews Data

    License: CC BY-NC-SA 4.0
    See https://www.kaggle.com/zynicide/wine-reviews
    """
    return fetch_dataset('winemag-data-130k-v2.csv.zip', data_path=data_path)

# Cell
def data_wiki_movies(data_path: Path = DATA_PATH, force:bool = False) -> pd.DataFrame:
    """Movie Summaries from Wikipedia

    License: CC BY-SA 4.0
    See https://www.kaggle.com/jrobischon/wikipedia-movie-plots
    """
    return fetch_dataset('wiki_movie_plots_deduped.csv.zip', data_path=data_path, force=force)

# Cell
def data_women_clothing_reviews(data_path: Path = DATA_PATH, force:bool = False) -> pd.DataFrame:
    """Women's E-commerce Clothing Reviews

    License: CC0
    https://www.kaggle.com/nicapotato/womens-ecommerce-clothing-reviews
    """
    return fetch_dataset('Womens%20Clothing%20E-Commerce%20Reviews.csv.zip', data_path, force=force)

# Cell
def data_au_election_2019_tweets(data_path: Path = DATA_PATH, force:bool = False) -> pd.DataFrame:
    """Tweets from the 2019 Australian Elections

    Collected from Twitter API keyword search betwen 2019-05-10 and 2019-05-20.

    License: CC0: Public Domain
    See https://www.kaggle.com/taniaj/australian-election-2019-tweets
    """
    return fetch_dataset('auspol2019.csv.zip', data_path, force=force)

# Cell
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

# Cell
GUTENBERG_DICKENS = {
    98: 'A Tale of Two Cities',
    1400: 'Great Expectations',
    730: 'Oliver Twist',
    766: 'David Copperfield',
    19337: 'A Christmas Carol',
    786: 'Hard Times',
    1023: 'Bleak House',
    580: 'The Pickwick Papers',
    883: 'Out Mutual Friend',
    967: 'Nicholas Nickleby',
    700: 'The Old Curiosity Shop',
    821: 'Domeby and Son',
    963: 'Little Dorrit',
}

def data_dickens_corpus(data_path: Path = DATA_PATH, mirror:str="https://gutenberg.pglaf.org/") -> T.Dict[str, str]:
    """Download a corpus of Charles Dicken's most popular books

    data_path: Where to store the cache
    mirror   : Project Gutenberg mirror to use

    Returns a dictionary of {"title": "full text"}
    """
    dest = data_path / 'dickens.pkl'
    if not dest.exists():
        data = {title: strip_headers(load_etext(idx, mirror=mirror)).strip() for idx, title in GUTENBERG_DICKENS.items()}
        with open(dest, 'wb') as f:
            pickle.dump(data, f)
    with open(dest, 'rb') as f:
        data = pickle.load(f)
    return data