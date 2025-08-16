import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import re

BASE_URL = "http://ufcstats.com/statistics/events/completed?page=all"


def get_event_list():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for row in soup.select("tr.b-statistics__table-row")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            text = cols[0].text.strip()
            clean_text = re.sub(r"\s+", " ", text).strip()
            parts = clean_text.rsplit(" ", 3)
            name = parts[0]
            date = " ".join(parts[-3:])
            link = cols[0].find("a")["href"]
            events.append({"event_name": name, "event_date": date, "link": link})

    return pd.DataFrame(events)


if __name__ == "__main__":
    events_df = get_event_list()
    events_df.to_csv(
        "data/raw/events.csv",
        index=False,
    )
    print(f"Salvo {len(events_df)} eventos em data/raw/events.csv")
