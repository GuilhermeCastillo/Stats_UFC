import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import os
import re

os.makedirs("data/raw", exist_ok=True)


def get_fights_from_event(event_url):
    """Extrai todas as lutas de um evento pelo link do evento"""
    resp = requests.get(event_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    fights = []
    rows = soup.select(
        "tr.b-fight-details__table-row.b-fight-details__table-row__hover"
    )

    for row in rows:
        cols = row.find_all("td")

        raw_text = cols[1].text.strip()
        fighters_split = [f.strip() for f in raw_text.split("\n") if f.strip()]
        fighter_1 = fighters_split[0]
        fighter_2 = fighters_split[1]
        result = cols[0].text.strip()
        weight_class = cols[6].text.strip()
        method = re.sub(r"\s+", " ", cols[7].text.strip())
        round_num = cols[8].text.strip()
        fight_time = cols[9].text.strip()

        # Link para estatísticas detalhadas
        fight_link = cols[0].find("a")["href"] if cols[0].find("a") else None

        fights.append(
            {
                "fighter_1": fighter_1,
                "fighter_2": fighter_2,
                "result": result,
                "weight_class": weight_class,
                "method": method,
                "round": round_num,
                "time": fight_time,
                "fight_link": fight_link,
                "event_url": event_url,
            }
        )

    return fights


if __name__ == "__main__":
    events_df = pd.read_csv("data/raw/events.csv")

    all_fights = []

    for _, event in tqdm(
        events_df.iterrows(), total=len(events_df), desc="Coletando lutas"
    ):
        fights = get_fights_from_event(event["link"])
        all_fights.extend(fights)
        time.sleep(0.7)  # respeitar o servidor

    fights_df = pd.DataFrame(all_fights)
    fights_df.to_csv(
        "data/raw/fights.csv",
        index=False,
    )
    print(f"Salvo {len(fights_df)} lutas em data/raw/fights.csv")
