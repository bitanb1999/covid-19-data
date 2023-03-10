import os
import requests
import tempfile
import re
from urllib.error import HTTPError

from bs4 import BeautifulSoup
import pandas as pd


VAX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def read_xlsx_from_url(url: str, as_series: bool = False, **kwargs) -> pd.DataFrame:
    """Download and load xls file from URL.

    Args:
        url (str): File url.
        as_series (bol): Set to True to return a pandas.Series object. Source file must be of shape 1xN (1 row, N
                            columns). Defaults to False.
        kwargs: Arguments for pandas.read_excel.

    Returns:
        pandas.DataFrame: Data loaded.
    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686)"}
    response = requests.get(url, headers=headers)
    with tempfile.NamedTemporaryFile() as tmp:
        with open(tmp.name, 'wb') as f:
            f.write(response.content)
        df = pd.read_excel(tmp.name, **kwargs)
    return df.T.squeeze() if as_series else df


def get_headers() -> dict:
    """Get generic header for requests.

    Returns:
        dict: Header.
    """
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }


def get_soup(source: str, headers: dict = None, verify: bool = True, from_encoding: str = None) -> BeautifulSoup:
    """Get soup from website.

    Args:
        source (str): Website url.
        headers (dict, optional): Headers to be used for request. Defaults to general one.
        verify (bool, optional): Verify source URL. Defaults to True.
        from_encoding (str, optional): Encoding to use. Defaults to None.
    Returns:
        BeautifulSoup: Website soup.
    """
    if headers is None:
        headers = get_headers()
    try:
        response = requests.get(source, headers=headers, verify=verify)
    except Exception as err:
        raise err
    if not response.ok:
        raise HTTPError("Web {} not found! {response.content}")
    content = response.content
    return BeautifulSoup(
        content,
        "html.parser",
        from_encoding=from_encoding
    )


def url_request_broken(url):
    url_base, url_params = url.split('query?')
    x = filter(lambda x: x[0] != 'where', [p.split('=') for p in url_params.split('&')])
    params = dict(x)
    return f"{url_base}/query", params


def clean_count(count):
    count = re.sub(r"[^0-9]", "", count)
    count = int(count)
    return count
