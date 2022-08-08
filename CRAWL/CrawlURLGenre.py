from bs4 import BeautifulSoup
import requests
import json

# Request parser ra HTML để lấy link đăng nhập vào từng thể loại phim
response = requests.get("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")
soup = BeautifulSoup(response.content, "html.parser")
titles = soup.find_all("div", class_="table-cell primary")
links = [link.find("a").attrs["href"] for link in titles]
list_url = []
for i in range(24):
    list_url.append("https://www.imdb.com" + links[i])
    
# In ra file json URLGenre
with open('URLGenre.json', 'w', encoding="utf-8") as json_file:
    json.dump(list_url, json_file)