import pandas as pd

informovie1 = pd.read_csv("./infor_movie1_fix.csv")
informovie2 = pd.read_csv("./infor_movie2_1_fix.csv")
informovie2.drop(['Unnamed: 0'], axis=1, inplace = True)
informovie2.rename({'Writter':'Writer'}, axis=1, inplace = True)
informovie3 = pd.concat([informovie1, informovie2])
informovie3 = informovie3.loc[informovie3['Genre'] != "Short"]
informovie3.to_csv("infor_movie.csv", index=False)