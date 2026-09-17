import pandas as pd
import numpy as np
import json

#MATCH SUMMARY

with open("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\t20_wc_match_results.json") as f:
    data=json.load(f)

dataframe_matchresult=pd.DataFrame(data[0]["matchSummary"])#list ke liye data[0]dala,fir dic ke liye key dala
dataframe_matchresult.rename(columns={"scorecard":"match_id"},inplace=True)#score board ko match id ka name de dia 
""" 
for checking purpose
print(dataframe_matchresult.head())#starting eke 5 value
"""

#maine yeh socha hai yaha ki , index banane ke liye csv se krke jana hoga , usme index_col use krte hai 

dataframe_matchresult.to_csv("matchresult.csv",index=False)
match_result=pd.read_csv("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\datafilter\\matchresult.csv",index_col="match_id")
"""print(match_result.head())#for checking 
"""

##batting summary
battinginfo=[]
with open("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\t20_wc_batting_summary.json") as f:
    data=json.load(f)
    for i in data:
        battinginfo.extend(i["battingSummary"])
#append() → Puri list ko ek single element ki tarah add karta hai.
#extend() → List ke har element ko alag-alag add karta hai.
""" for checking pp
print(battinginfo)
"""

dataframe_battingresult=pd.DataFrame(battinginfo)
#isme ek dismissal ka option hai , agrrrrr  uske jagah nan hai toh not out (orelse out)
#                                     df name                 coulmn,pure coumn pe apply,lambd matlb check (x)
dataframe_battingresult["out/notout"]=dataframe_battingresult.dismissal.apply(lambda x:"out"if len(x)>0 else"notout")

#hata do coulmn:dismissal  name ka 
dataframe_battingresult.drop(columns=["dismissal"],inplace=True)


#name players ke correct karo , jahaa khrb ho 
dataframe_battingresult["batsmanName"] = (
    dataframe_battingresult["batsmanName"]
    .str.replace("â€\xa0", "", regex=False)
    .str.strip()
)
"""check"
print(dataframe_battingresult.head(10))
"""

#NOW MERGE OF  MATCHRESULT AND BATTING
"""abhi Apne batting aur match summary ka donon ka nikala hai ,
to usse Hamen Koi common chij dhundhni Hai,
 To Maine yah Ek chij dhundha Hai match Ek colum batting wale colum match mein suppose aisa hai ki Namibia vs Sri Lanka to Vahi upar wale table Mein team bus team Van versis team bhi Karen To Hamen sem result mil sakta hai aur ham vah chij se Ham combine combine kar Payenge so Hamen donon possibility team ka dekhna padega ki teamA versus Team B &team b versus team A exists krsakta hai"""

#common chiz 
"""
match_ids_dic={
    Namibia Vs Sri Lanka:T20I # 1823
    Netherlands Vs U.A.E.:T20I # 1823
}
"""

#try to make above thing 
match_ids_dic={}
for index,row in dataframe_matchresult.iterrows():
    key1=row["team1"]+" Vs "+row["team2"]
    key2=row["team2"]+" Vs "+row["team1"]

    match_ids_dic[key1]=row["match_id"]
    match_ids_dic[key2]=row["match_id"]
#checkk
#print(match_ids_dic)    

#ab batting wale mai match id dlna hai 
#match column mai jo likha hai woh compare kr naye dic mai , agr hua toh uska match id de
dataframe_battingresult["match_id"]=dataframe_battingresult["match"].map(match_ids_dic)#match wale column mai nikla toh uska match id added usme


#export this things in csv files 
dataframe_battingresult.to_csv("battingresult.csv",index=False)
batting_result=pd.read_csv("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\datafilter\\battingresult.csv",index_col="match_id")


#BOWLING
with open("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\t20_wc_bowling_summary.json") as f:
    data=json.load(f)
    bowlingdata=[]
    for i in data:
        bowlingdata.extend(i["bowlingSummary"])


dataframe_bowling=pd.DataFrame(bowlingdata)

dataframe_bowling["match_id"]=dataframe_bowling["match"].map(match_ids_dic)#match wale column mai nikla toh uska match id added usme

dataframe_bowling.to_csv("bowling_result.csv",index=False)


#players infooooo

with open("C:\\Users\\Bhavik\\OneDrive\\Desktop\\cricket data analy\\t20_json_files\\t20_wc_player_info.json")as f:
    data=json.load(f)


players_info=pd.DataFrame(data)
players_info['name'] = players_info['name'].apply(lambda x: x.replace('â€', ''))
players_info['name'] = players_info['name'].apply(lambda x: x.replace('†', ''))
players_info['name'] = players_info['name'].apply(lambda x: x.replace('\xa0', ''))

print(players_info[players_info["team"]=="India"])
players_info.to_csv("playersinfo_no_img.csv",index=False)