from numpy import NaN
import pandas as pd
import re

informovie2 = pd.read_csv("./infor_movie2_fix.csv")
# Lấy cột Votes đổi 'K' thành '000' đổi 'M' thành '000000' --> Votes
votes_list = []
for i in informovie2["Votes"]:
    if type(i) == str:
        if i.isnumeric() == False:
            a = re.sub("K", "", i)
            if a.isnumeric() == False:
                z = float(a) * 1000
                votes_list.append(int(z))
            else:
                z = int(a) * 1000
                votes_list.append(z)
        else:
            votes_list.append(i)
    else:
        z = i * 1000
        votes_list.append(z)
informovie2["Votes"] = votes_list

# Cột Runtime chuyển định dạng sang 'phút' --> Runtime
informovie2[["Runtime_1", "Runtime_2"]]  = informovie2['Runtime'].str.split(' ', expand=True)
informovie2["Runtime_1"] = informovie2["Runtime_1"].replace(['TV-MATV-MA'],NaN)
informovie2["Runtime_1"] = informovie2["Runtime_1"].replace(['TV-Y7TV-Y7'],NaN)
Runtime_list_hours = []
for i in informovie2["Runtime_1"]:
    if type(i) == str:
        a = re.sub("h", "", i)
        if a.isnumeric() == True:
            z = int(a) * 60
            Runtime_list_hours.append(z)
        else:
            a = re.sub("m", "", i)
            Runtime_list_hours.append(a)
    else:
        Runtime_list_hours.append(i)
Runtime_list_minutes = []
for i in informovie2["Runtime_2"]:
    if type(i) == str:
        a = re.sub("m", "", i)
        Runtime_list_minutes.append(int(a))
    elif type(i) == float:
        Runtime_list_minutes.append(i)
    else:
        Runtime_list_minutes.append(NaN)
Runtime_list_done = []
for a, b in zip(Runtime_list_hours, Runtime_list_minutes):
    if type(a) == int and type(b) == int:
        z = a + b
        Runtime_list_done.append(z)
    elif type(a) == int and type(b) == float:
        b = 0
        z = a + b
        Runtime_list_done.append(z)
    else:
        Runtime_list_done.append(a)
informovie2.drop(['Runtime', 'Runtime_1', 'Runtime_2'], axis=1, inplace = True)
informovie2["Runtime"] = Runtime_list_done
informovie2.to_csv("infor_movie2_1_fix.csv")

