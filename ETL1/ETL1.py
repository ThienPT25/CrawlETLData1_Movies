from numpy import NaN
import pandas as pd

# Mở file csv
infor_movie1 = pd.read_csv('./infor_movie1.csv')
infor_movie2 = pd.read_csv('./infor_movie2.csv')

# Sửa infor_movie1
infor_movie1.pop('Released') # Giảm cột
# Chỉ lấy năm 2012 --> 2019
infor_movie1 = infor_movie1.loc[infor_movie1["Year"] < 2020].loc[infor_movie1["Year"] > 2011]
infor_movie1.to_csv('./infor_movie1_fix.csv', index=False)

# Sửa infor_movie2
# Lấy EnName (Null thì lấy từ cột NameMovie sang) xóa cột NameMovie --> Name
infor_movie2.loc[infor_movie2['EnNameMovie'].isnull(), 'EnNameMovie'] = infor_movie2['NameMovie']
infor_movie2.pop('NameMovie') # Giảm cột
infor_movie2.rename(columns = {'EnNameMovie':'Name'}, inplace = True)
# Rating --> Rating # Genre --> Genre # Year --> Year # IMDbRating xóa /10 --> Score
infor_movie2["IMDbRating"].replace('/10','',regex=True, inplace = True)
infor_movie2.rename(columns = {'IMDbRating':'Score'}, inplace = True)
infor_movie2.rename(columns = {'CustomerRating':'Votes'}, inplace = True)
# Director --> Director # Writer --> Writer # Star --> Star # Country --> Null # Budget --> Null # Gross --> Null # Company --> Null
# Xóa --> Populary Decribe User_reviews CriticReviews_Metascore 2020 - 2022
infor_movie2 = infor_movie2.drop(["Populary", "Decribe", "User_reviews", "CriticReviews_Metascore"], axis=1)
infor_movie2.replace('Null', NaN, regex=True, inplace = True)
infor_movie2 = infor_movie2.loc[infor_movie2["Year"] < '2023'].loc[infor_movie2["Year"] > '2019']
# Director --> Director # Writer --> Writer # Star --> Star # Country --> Null # Budget --> Null # Gross --> Null # Company --> Null
new_cols = ["Name", "Rating", "Genre", "Year", "Score", "Votes", "Director", "Writter", "Star", "Runtime",]
infor_movie2 = infor_movie2[new_cols]
infor_movie2.insert(9, "Country", NaN, True)
infor_movie2.insert(10, "Budget", NaN, True)
infor_movie2.insert(11, "Gross", NaN, True)
infor_movie2.insert(12, "Company", NaN, True)
infor_movie2.to_csv('./infor_movie2_fix.csv', index=False)  