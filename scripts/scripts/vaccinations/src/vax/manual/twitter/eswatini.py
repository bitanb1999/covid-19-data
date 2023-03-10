import re

import pandas as pd

from vax.manual.twitter.base import TwitterCollectorBase
from vax.utils.dates import clean_date


class Eswatini(TwitterCollectorBase):
    def __init__(self, api, paths=None, **kwargs):
        super().__init__(
            api=api,
            username="EswatiniGovern1",
            location="Eswatini",
            add_metrics_nan=True,
            paths=paths,
            **kwargs
        )

    def _propose_df(self):
        regex = r"Minister of Health Lizzie Nkosi's #COVID19 update on (\d{1,2} [a-zA-Z]+ 202\d)"
        data = []
        for tweet in self.tweets:
            if match := re.search(regex, tweet.full_text):
                dt = clean_date(match[1], "%d %B %Y")
                if self.stop_search(dt):
                    break
                data.append({
                    "date": dt,
                    "text": tweet.full_text,
                    "source_url": self.build_post_url(tweet.id),
                    "media_url": tweet.extended_entities["media"][0]["media_url_https"],
                })
        return pd.DataFrame(data)


def main(api, paths):
    Eswatini(api, paths).to_csv()
