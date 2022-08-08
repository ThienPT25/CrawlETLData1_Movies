import requests, json, csv
from bs4 import BeautifulSoup

# Hàm dùng để crawl dữ liệu
def crawl(href):
    response = requests.get("https://www.imdb.com" + href)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        NameMovie = soup.find("div", class_="sc-94726ce4-2 khmuXj").h1.text
        EnNameMovie_none = soup.find("div", class_="sc-94726ce4-3 eSKKHi").div.text
        EnNameMovie = EnNameMovie_none.replace("Original title: ", "")
        EnNameMovie = None
        Year = soup.find("span", class_="sc-8c396aa2-2 itZqyK").text
        Rating_Runtime = soup.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt")
        children = Rating_Runtime.find_all("li")
        children1 = Rating_Runtime.find_all("span")
        list_Rating_Runtime = []
        for i in children:
            list_Rating_Runtime.append(i.getText())
        list_Year_Rating = []
        for i in children1:
            list_Year_Rating.append(i.getText())
        IMDbRating = soup.find("div", class_="sc-7ab21ed2-2 kYEdvH").text
        CustomerRating = soup.find("div", class_="sc-7ab21ed2-3 dPVcnq").text
        Populary = soup.find("div", class_="sc-edc76a2-1 gopMqI").text
        Genre = soup.find("span", class_="ipc-chip__text").text
        Decribe = soup.find("span", class_="sc-16ede01-2 gXUyNh").text
        Director = soup.find("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
        Director_Writter_Star = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt")
        children = Director_Writter_Star.find_all("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        list_Director_Writter_Star = []
        for i in children:
            list_Director_Writter_Star.append(i.getText())
        User_reviews_none = soup.find("span", class_="three-Elements").text
        User_reviews = User_reviews_none.replace("User reviews", "")
        UserReviews_CriticReviews_Metascore = soup.find("ul", class_="ipc-inline-list sc-124be030-0 ddUaJu baseAlt").text
        CriticReviews_Metascore = UserReviews_CriticReviews_Metascore.replace(User_reviews_none, "").replace("Critic reviews", " ").replace("Metascore", "")
    except:
        movie_infor = [None, None, None, None, None, None, None, None, None, None, None, None, None]
    if len(list_Year_Rating) >= 2 and len(list_Rating_Runtime) >= 3 and len(list_Director_Writter_Star) >= 4:
        movie_infor = [NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore]
    else:
        list_Year_Rating = ['Null', 'Null', 'Null', 'Null', 'Null']
        list_Rating_Runtime = ['Null', 'Null', 'Null', 'Null', 'Null']
        list_Director_Writter_Star = ['Null', 'Null', 'Null', 'Null', 'Null']        
        movie_infor = [NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore]
    csv_writter.writerow([NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore])
    return movie_infor

# Mở file json để lấy list
json_file = open("./URLMovie.json", "r", encoding="utf-8")
url_movie = json.load(json_file)
url_movie = list(dict.fromkeys(url_movie))
# print(len(url_movie))

# Mở file csv để điền dữ liệu vào
csv_file = open("infor_movie.csv", "w", newline="", encoding="utf-8")
csv_writter = csv.writer(csv_file)
csv_writter.writerow(["NameMovie", "EnNameMovie", "Year", "Rating", "Runtime", "IMDbRating", "CustomerRating", "Populary", "Genre", "Decribe", "Director", "Writter", "Star", "User_reviews", "CriticReviews_Metascore"])

# Lấy infor từng bộ movie trong list
for link in url_movie:
    crawl(link)