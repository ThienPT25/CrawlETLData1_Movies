import requests, json
from bs4 import BeautifulSoup

# Lấy link movie
def movies_page(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h3", class_="lister-item-header")
        for movie_link in titles:
            check_year = movie_link.find("span", class_="lister-item-year text-muted unbold").text.replace('(', "").replace(")", "").replace("I", "").strip()      
            if check_year == '2018':
                movies_links_2018.append(movie_link.find("a").attrs["href"])
            elif check_year == '2019':
                movies_links_2019.append(movie_link.find("a").attrs["href"])
            if check_year == '2020':
                movies_links_2020.append(movie_link.find("a").attrs["href"])
            elif check_year == '2021':
                movies_links_2021.append(movie_link.find("a").attrs["href"])
            elif check_year == '2022':
                movies_links_2022.append(movie_link.find("a").attrs["href"])
            elif check_year == '2023':
                movies_links_2022.append(movie_link.find("a").attrs["href"])
    except:
        None
    return movies_links_2018, movies_links_2019, movies_links_2020, movies_links_2021, movies_links_2022, movies_links_2023

# Lấy link movie chi tiết
def get_links_movie(url, number):
    # Tìm link đến trang start = 9951
    links_101_9951 = []
    for i in range(51, 9951, 50):
        url_change = url.replace(str(i), str(i + 50))
        links_101_9951.append(url_change)

    # URL trang 1, 2 --> start = 101 --> 9951
    links = [url_genre[number], url] + links_101_9951
    for link in links:
        movies_page(link)
    return movies_links_2018, movies_links_2019, movies_links_2020, movies_links_2021, movies_links_2022, movies_links_2023

# Lấy Url Genre từ file URLGenre.json
json_file = open("./URLGenre.json", "r", encoding="utf-8")
url_genre = json.load(json_file)
url_genre.remove(url_genre[20])

# Lấy Url Genre từ file URLGenre_page2.json
json_file = open("./URLGenre_page2.json", "r", encoding="utf-8")
url_genre_page2 = json.load(json_file)
url_genre_page2.remove(url_genre_page2[20])

# Khai báo list
movies_links_2018 = []
movies_links_2019 = []
movies_links_2020 = []
movies_links_2021 = []
movies_links_2022 = []
movies_links_2023 = []
list_b = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

i = 0
# Lấy URL movie từng thể loại
for a, b in zip(url_genre_page2, list_b):
    i = i + 1
    get_links_movie(a, b)
    print(i)
    
# In ra file json URLMovie
movies_links = movies_links_2018 + movies_links_2019 + movies_links_2020 + movies_links_2021 + movies_links_2022 + movies_links_2023
with open('URLMovie.json', 'w', encoding="utf-8") as json_file:
    json.dump(movies_links, json_file)