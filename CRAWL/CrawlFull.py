from bs4 import BeautifulSoup
import requests
import csv


# Request parser ra HTML để lấy link đăng nhập vào từng thể loại phim
def crawlUrl(x):
    response = requests.get(x)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("div", class_="table-cell primary")
    links_Url = [link.find("a").attrs["href"] for link in titles]
    return links_Url

# Crawl link để di chuyển sang trang 2
def crawl_next_links(x):
    response = requests.get(x)
    soup = BeautifulSoup(response.content, "html.parser")
    next_button = soup.find("div", class_="desc")
    next_link = next_button.find("a").attrs["href"]
    return next_link

# Lấy link movies
def movies_page(x):
    try:
        response = requests.get(x)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h3", class_="lister-item-header")
        for movie_link in titles:
            check_year = movie_link.find("span", class_="lister-item-year text-muted unbold").text.replace('(', "").replace(")", "").replace("I", "").strip()      
            if check_year == '2020':
                movies_links_2020.append(movie_link.find("a").attrs["href"])
            elif check_year == '2021':
                movies_links_2021.append(movie_link.find("a").attrs["href"])
            elif check_year == '2022':
                movies_links_2022.append(movie_link.find("a").attrs["href"])
    except:
        None
    return movies_links_2020, movies_links_2021, movies_links_2022

# Lấy link movie chi tiết
def get_links_movie(url, number):
    # Tìm link đến trang start = 9951
    links_101_9951 = []
    for i in range(51, 9951, 50):
        url_change = url.replace(str(i), str(i + 50))
        links_101_9951.append(url_change)
    # URL trang 1, 2 --> start = 101 --> 9951
    links = [list_url[number], url] + links_101_9951
    for link in links:
        movies_page(link)
    return movies_links_2020, movies_links_2021, movies_links_2022

# Hàm dùng để crawl dữ liệu
def crawl(href):
    response = requests.get("https://www.imdb.com" + href)
    soup = BeautifulSoup(response.content, "html.parser")
    NameMovie = soup.find("div", class_="sc-94726ce4-2 khmuXj").h1.text
    Year = soup.find("span", class_="sc-8c396aa2-2 itZqyK").text
    try:
        EnNameMovie_none = soup.find("div", class_="sc-94726ce4-3 eSKKHi").div.text
        EnNameMovie = EnNameMovie_none.replace("Original title: ", "")
    except:
        EnNameMovie = None
    try:
        Rating_Runtime = soup.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt")
        children = Rating_Runtime.find_all("li")
        children1 = Rating_Runtime.find_all("span")
        list_Rating_Runtime = []
        for i in children:
            list_Rating_Runtime.append(i.getText())
        list_Year_Rating = []
        for i in children1:
            list_Year_Rating.append(i.getText())
    except:
        list_Rating_Runtime = None
        list_Year_Rating = None
    try:
        IMDbRating = soup.find("div", class_="sc-7ab21ed2-2 kYEdvH").text
    except:
        IMDbRating = None
    try:
        CustomerRating = soup.find("div", class_="sc-7ab21ed2-3 dPVcnq").text
    except:
        CustomerRating = None
    try:
        Populary = soup.find("div", class_="sc-edc76a2-1 gopMqI").text
    except:
        Populary = None
    try:
        Genre = soup.find("span", class_="ipc-chip__text").text
    except:
        Genre = None
    try:
        Decribe = soup.find("span", class_="sc-16ede01-2 gXUyNh").text
    except:
        Decribe = None
    try:
        Director = soup.find("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
    except:
        Director = None
    try:
        Director_Writter_Star = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt")
        children = Director_Writter_Star.find_all("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        list_Director_Writter_Star = []
        for i in children:
            list_Director_Writter_Star.append(i.getText())
    except:
        list_Director_Writter_Star = None
    try:
        User_reviews_none = soup.find("span", class_="three-Elements").text
        User_reviews = User_reviews_none.replace("User reviews", "")
    except:
        User_reviews = None
    try:
        UserReviews_CriticReviews_Metascore = soup.find("ul", class_="ipc-inline-list sc-124be030-0 ddUaJu baseAlt").text
        CriticReviews_Metascore = UserReviews_CriticReviews_Metascore.replace(User_reviews_none, "").replace("Critic reviews", " ").replace("Metascore", "")
    except:
        CriticReviews_Metascore = None
    if len(list_Year_Rating) >= 2 and len(list_Rating_Runtime) >= 3 and len(list_Director_Writter_Star) >= 4:
        movie_infor = [NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore]
    else:
        list_Year_Rating = ['Null', 'Null', 'Null', 'Null', 'Null']
        list_Rating_Runtime = ['Null', 'Null', 'Null', 'Null', 'Null']
        list_Director_Writter_Star = ['Null', 'Null', 'Null', 'Null', 'Null']        
        movie_infor = [NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore]
    csv_writter.writerow([NameMovie, EnNameMovie, Year, list_Year_Rating[1], list_Rating_Runtime[2], IMDbRating, CustomerRating, Populary, Genre, Decribe, Director, list_Director_Writter_Star[1], list_Director_Writter_Star[3], User_reviews, CriticReviews_Metascore])
    return movie_infor

# Khai báo list
list_url = []
next_links = []
movies_links_2020 = []
movies_links_2021 = []
movies_links_2022 = []
list_b = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

# Crawl list_url từ 24 thể loại movies
for i in range(24):
    list_url.append("https://www.imdb.com" + crawlUrl("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")[i])

# Crawl next_links để chuyển sang trang sau
for url in list_url:
    next_links.append("https://www.imdb.com" + crawl_next_links(url))

# Lấy URL movie từng thể loại
for a, b in zip(next_links, list_b):
    get_links_movie(a, b)

# Lấy ra list movies
movies_links = movies_links_2020 + movies_links_2021 + movies_links_2022
url_movie = list(dict.fromkeys(movies_links))

# Mở file csv để điền dữ liệu vào
csv_file = open("infor_movie_full.csv", "w", newline="", encoding="utf-8")
csv_writter = csv.writer(csv_file)
csv_writter.writerow(["NameMovie", "EnNameMovie", "Year", "Rating", "Runtime", "IMDbRating", "CustomerRating", "Populary", "Genre", "Decribe", "Director", "Writter", "Star", "User_reviews", "CriticReviews_Metascore"])

# Lấy infor từng bộ movie trong list
for link in url_movie:
    crawl(link)