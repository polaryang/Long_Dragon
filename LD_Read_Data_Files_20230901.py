# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 00:48:11 2023

@author: user
"""
import datetime
import json
import pandas as pd
from datetime import datetime
import datetime as dt
import yfinance as yf
# Import matplotlib and set the style for plotting
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
file_raw='https://github.com/polaryang/Long_Dragon/raw/main/'
id=2330
# 1.	重大訊息
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
db_news=pd.concat([db_news_L, db_news_O])
#df_basic['Stock_ID']=str(df_basic['公司代號'])
df_news=db_news[db_news['公司代號']==id]

# 2.	公告查詢 
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv 不定期更新
db_announce_L=pd.read_csv(file_raw+'t187ap38_L.csv') #3.	公司基本資料
db_announce_O=pd.read_csv(file_raw+'t187ap38_O.csv')
db_announce=pd.concat([db_announce_L, db_announce_O])
#df_basic['Stock_ID']=str(df_basic['公司代號'])
df_announce=db_announce[db_announce['公司代號']==id]

# 3.	公司基本資料 
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') #3.	公司基本資料
db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')
db_basic=pd.concat([db_basic_L, db_basic_O])
#df_basic['Stock_ID']=str(df_basic['公司代號'])
df_basic=db_basic[db_basic['公司代號']==id]



# 4.	董監事持股餘額明細資料
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
db_board_balance_L=pd.read_csv('C:/Users/user/Desktop/Long_dragon/t187ap11_L.csv') #4.	董監事持股餘額明細資料
db_board_balance_O=pd.read_csv('C:/Users/user/Desktop/Long_dragon/t187ap11_O.csv')
db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
df_board_balance=db_board_balance[db_board_balance['公司代號']==id]

# 5.	年報前十大股東相互間關係表
# 先到TEJ執行特殊轉檔 每年一次
db_control=pd.read_excel('C:/Users/user/Desktop/Long_dragon/Control.xlsx') #4.	董監事持股餘額明細資料
df_control=db_control[db_control['公司']==id]

# 6.	股權分散表(公開觀測站)
# 先到TEJ執行特殊轉檔 每年一次
db_stock_holder1=pd.read_excel('C:/Users/user/Desktop/Long_dragon/stock_holder_list.xlsx')
df_stock_holder1=db_stock_holder1[db_stock_holder1['公司']==id]

# 7.	集保戶股權分散表 TDCC_OD_1-5.csv
# 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
db_stock_holder2=pd.read_csv('C:/Users/user/Desktop/Long_dragon/TDCC_OD_1-5.csv') #4.	董監事持股餘額明細資料
db_stock_holder2=db_stock_holder2[db_stock_holder2['持股分級']!=16]
df_stock_holder2=db_stock_holder2[db_stock_holder2['證券代號']==str(id)]
#30~40 40~50 合併
df_stock_holder2.iloc[6,3:5]=df_stock_holder2.iloc[6,3:5]+df_stock_holder2.iloc[7,3:5]
df_stock_holder2=df_stock_holder2[df_stock_holder2['持股分級']!=8]
df_stock_holder2['持股分級']=range(1,16)
df_stock_holder2['股數']=round(df_stock_holder2['股數']/1000,0)
df_stock_holder2=df_stock_holder2.rename(columns={'股數':'張數'})
stock_holder_class=['1張以下','1~5張','5~10張','10~15張','15~20張','20~30張','30~50張','50~100張','100~200張','200~400張','400~600張','600~800張','800~1000張','1000以上張','合計']
df_stock_holder2.insert(3,"持股分級_說明",stock_holder_class,True)

temp_person=[]
for i in range(14):
    temp_person.append(df_stock_holder1.iloc[0,54+i*3])
temp_person.append(sum(temp_person))
temp_share=[]
for i in range(14):
    temp_share.append(df_stock_holder1.iloc[0,55+i*3])
temp_share.append(sum(temp_share))
temp_ratio=[]
for i in range(14):
    temp_ratio.append(df_stock_holder1.iloc[0,56+i*3])
temp_ratio.append(sum(temp_ratio))
df_stock_holder2.insert(4,"股東會時_比率",temp_ratio,True)
df_stock_holder2.insert(4,"股東會時_張數",temp_share,True)
df_stock_holder2.insert(4,"股東會時_人數",temp_person,True)

#8.	議事錄
#https://mops.twse.com.tw/mops/web/t150sb04 可以出總表 每年一次
db_share_meeting=pd.read_excel('C:/Users/user/Desktop/Long_dragon/share_meeting.xlsx')
df_share_meeting=db_share_meeting[db_share_meeting['公司代號']==id]
