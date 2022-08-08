from bs4 import BeautifulSoup
import requests
import json

# Request pars ra HTML để lấy link trang 2
json_file = open("./URLGenre.json", "r", encoding="utf-8")
url_genre = json.load(json_file)
next_links = []
for url in url_genre:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    next_button = soup.find("div", class_="desc")
    next_link = next_button.find("a").attrs["href"]
    next_links.append("https://www.imdb.com" + next_link)

# In ra file json URLGenre_page2
with open('URLGenre_page2.json', 'w', encoding="utf-8") as json_file:
    json.dump(next_links, json_file)