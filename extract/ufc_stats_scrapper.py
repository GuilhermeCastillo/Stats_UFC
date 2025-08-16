import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re
from tqdm import tqdm

# Garante que a pasta exista
os.makedirs("data/raw", exist_ok=True)


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_fights_from_event(event_url):
    """Extrai dados resumidos de todas as lutas de um evento"""
    resp = requests.get(event_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    fights = []
    rows = soup.select(
        "tr.b-fight-details__table-row.b-fight-details__table-row__hover"
    )

    for row in rows:
        cols = row.find_all("td")

        # Fighters
        raw_text = cols[1].text.strip()
        fighters_split = [f.strip() for f in raw_text.split("\n") if f.strip()]
        fighter_1 = fighters_split[0]
        fighter_2 = fighters_split[1]

        # Resultado (win/lose)
        result = cols[0].text.strip()

        kd = clean_text(cols[2].text.strip()).split(" ")
        sig_str = clean_text(cols[3].text.strip()).split(" ")
        td = clean_text(cols[4].text.strip()).split(" ")
        sub = clean_text(cols[5].text.strip()).split(" ")

        kd_fighter1 = kd[0]
        sig_str_fighter1 = sig_str[0]
        td_fighter1 = td[0]
        sub_fighter1 = sub[0]

        kd_fighter2 = kd[1]
        sig_str_fighter2 = sig_str[1]
        td_fighter2 = td[1]
        sub_fighter2 = sub[1]

        # Evento
        event_name = clean_text(cols[6].text.strip())
        event_name_clean = re.sub(r"\s+", " ", event_name).strip()
        parts = event_name_clean.rsplit(" ", 3)
        event_name = parts[0]
        date = " ".join(parts[-3:])

        # Método e round
        method = clean_text(cols[7].text)
        round_num = cols[8].text.strip()
        fight_time = cols[9].text.strip()

        # Link para estatísticas detalhadas (vem do atributo onclick da <tr>)
        fight_link = None
        onclick = row.get("onclick")
        if onclick:
            match = re.search(r"doNav\('(.*?)'\)", onclick)
            if match:
                fight_link = match.group(1)

        fights.append(
            {
                "fighter_1": fighter_1,
                "fighter_2": fighter_2,
                "result": result,
                "KD_f1": kd_fighter1,
                "SIG_STR_f1": sig_str_fighter1,
                "TD_f1": td_fighter1,
                "SUB_f1": sub_fighter1,
                "KD_f2": kd_fighter2,
                "SIG_STR_f2": sig_str_fighter2,
                "TD_f2": td_fighter2,
                "SUB_f2": sub_fighter2,
                "event": event_name,
                "date": date,
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

    for _, row in tqdm(
        events_df.iterrows(), total=len(events_df), desc="Coletando lutas"
    ):
        event_url = row["link"]
        fights = extract_fights_from_event(event_url)
        all_fights.extend(fights)
        time.sleep(0.7)

    fights_df = pd.DataFrame(all_fights)
    fights_df.to_csv("data/raw/fights.csv", index=False)
    print(f"Salvo {len(fights_df)} lutas em data/raw/fights.csv")
