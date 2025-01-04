import requests
from bs4 import BeautifulSoup
import re

# Headers pour éviter d'être bloqué
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Fonction pour extraire les données d'une URL
def extract_data(url):
    response = requests.get(url, headers=headers,timeout=10)
    # session = requests.Session()
    # response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {
            "Title": soup.find("h1").text.strip() if soup.find("h1") else "N/A",
        }  
        # extraction de runtime
    runtime_section = soup.find_all("div", class_="title-detail-hero-details__item")
    runtime_text = next((div.text.strip() for div in runtime_section if "min" in div.text), "N/A")
    data["Runtime"] = runtime_text
    
    # Extraction du pourcentage JustWatch
    jw_rating_section = soup.find_all("div", class_="title-detail-hero-details__item")
    jw_rating = next((div.text.strip() for div in jw_rating_section if "%" in div.text), "N/A")
    data["pourcentage_section"] = jw_rating
    
    # extraire le nombre de season
    seasons_section = soup.find("h2", class_="title-detail__title")
    if seasons_section:
        seasons_text = seasons_section.text.strip()
        # Extraction du nombre avec une expression régulière
        match = re.search(r'(\d+)\s+Seasons?', seasons_text)
        number_of_seasons = int(match.group(1)) if match else "N/A"
    else:
        number_of_seasons = "N/A"
    data["number_of_seasons"] = number_of_seasons
    #

    # Popularité des interactions (Votes positifs et négatifs)
    quick_action_bar = soup.find("div", class_="quick-action-bar title-sidebar__quick-action-bar")
    if quick_action_bar:
        buttons = quick_action_bar.find_all("button", class_="quick-action-bar__button")
        
        if buttons and len(buttons) >= 2:  # Vérifier qu'il y a au moins deux boutons
            # Vote positif
            positive_button = buttons[0]
            positive_votes = positive_button.find("span", class_="quick-action-bar_button_text")
            data["Positive Votes"] = positive_votes.text.strip() if positive_votes else "N/A"

            # Vote négatif
            negative_button = buttons[1]
            negative_votes = negative_button.find("span", class_="quick-action-bar_button_text")
            data["Negative Votes"] = negative_votes.text.strip() if negative_votes else "N/A"
    

    
    # Classement JustWatch
    ranking_section = soup.find("div", class_="title-chart-info")
    if ranking_section:
        # Extraire les valeurs du classement
        current_ranking = ranking_section.find("p", class_="title-ranking-list__rank")
        highest_ranking = ranking_section.find("p", class_="title-chart-info_item_value")
        top_10_days = ranking_section.find_all("p", class_="title-chart-info_itemvalue")[1] if len(ranking_section.find_all("p", class="title-chart-info_item_value")) > 1 else "N/A"
        top_100_days = ranking_section.find_all("p", class_="title-chart-info_itemvalue")[2] if len(ranking_section.find_all("p", class="title-chart-info_item_value")) > 2 else "N/A"
        top_1000_days = ranking_section.find_all("p", class_="title-chart-info_itemvalue")[3] if len(ranking_section.find_all("p", class="title-chart-info_item_value")) > 3 else "N/A"
        
        data["Current Ranking"] = current_ranking.text.strip() if current_ranking else "N/A"
        data["Highest Ranking"] = highest_ranking.text.strip() if highest_ranking else "N/A"
        data["Days in Top 10"] = top_10_days.text.strip() if top_10_days else "N/A"
        data["Days in Top 100"] = top_100_days.text.strip() if top_100_days else "N/A"
        data["Days in Top 1000"] = top_1000_days.text.strip() if top_1000_days else "N/A"

        return data
    else:
        print(f"Erreur: {response.status_code} pour l'URL {url}")
        return None