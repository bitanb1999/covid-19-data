import re

import pandas as pd

from vax.manual.twitter.base import TwitterCollectorBase
from vax.utils.dates import clean_date

class Guinea(TwitterCollectorBase):
    def __init__(self, api, paths=None, **kwargs):
        super().__init__(
            api=api,
            username="anss_guinee",
            location="Guinea",
            add_metrics_nan=True,
            paths=paths,
            **kwargs
        )

    def _propose_df(self):
        regex = (
            r"Trouvez ci-bas les données du \d{1,2} [a-zA-Z]+ et la mise à jour globale à la date du (\d{1,2}-\d{1,2}"
            r"-202\d)\."
        )
        data = []
        for tweet in self.tweets:
            if match := re.search(regex, tweet.full_text):
                dt = clean_date(match[1], "%d-%m-%Y")
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
    Guinea(api, paths).to_csv()
