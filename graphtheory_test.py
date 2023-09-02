# -*- coding: utf-8 -*-
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
import requests
from bs4 import BeautifulSoup
from PIL import Image
#import graphviz
from graphviz import Digraph
# ------------------------------------------------------------------
def Checking_ID(ID):
  ID_code='0'
  ID_name='0'
  ID_mkt='0'
  ID_type='0'
  ID_Inds='0'
  #證交所 checking ID search => https://isin.twse.com.tw/isin/class_main.jsp?owncode=00632R&stockname=&isincode=&market=&issuetype=&industry_code=&Page=1&chklike=Y
  if ID.encode( 'UTF-8' ).isdigit() :    #input data (all numbers)
    r = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode="+ str(ID) +"&stockname=&isincode=&market=&issuetype=&industry_code=&Page=1&chklike=Y")
  elif ID.encode( 'UTF-8' ).isalnum ():  #input data (English and numbers)
    r = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode="+ str(ID) +"&stockname=&isincode=&market=&issuetype=&industry_code=&Page=1&chklike=Y")
  else:                                  #input data (Chinese)
    ID= ID.encode('UTF-8').decode('UTF-8','strict')
    r = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname="+ str(ID) +"&isincode=&market=&issuetype=&industry_code=&Page=1&chklike=Y")
  try:
    # Whether the download is successful ?
    if r.status_code == requests.codes.ok :
      # using BeautifulSoup parsing HTML code
      soup = BeautifulSoup(r.text, 'html.parser')
      # using CSS td=_FAFAD2 get data 
      stories = soup.find_all('td', bgcolor="#FAFAD2")
      #頁面編號	國際證券編碼	有價證券代號	有價證券名稱	市場別	有價證券別	產業別	公開發行/上市(櫃)/發行日	CFICode	備註
      #1	TW00000632R5	00632R	元大台灣50反1	上市	ETF		2014/10/31	CEOGDU	
      #parsing all td=_FAFAD2 data and reorganization for return string
      for i in range(0 ,len(stories),10) :   
        if ((stories[i+5].text == '股票') or (stories[i+5].text == 'ETF')):  
          ID_code=stories[i+2].text #code
          ID_name=stories[i+3].text #name
          ID_mkt=stories[i+4].text #market
          ID_type=stories[i+5].text #type
          ID_Inds=stories[i+6].text #Inds
          return ID_code, ID_name, ID_mkt, ID_type, ID_Inds
          break
    return ID_code, ID_name, ID_mkt, ID_type, ID_Inds
              #return ID_code,ID_name,ID_type    #return ID number
  except:
    no_found=1
    ID_code='0'
    ID_name='0'
    ID_mkt='0'
    ID_type='0'
    ID_Inds='0'
    return ID_code, ID_name, ID_mkt, ID_type, ID_Inds
    #return '0','0','0','0'
# ------------------------------------------------------------------
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df
# ------------------------------------------------------------------

st.set_page_config(page_title='長龍股權*數據分析儀表板', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[長龍股權*數據分析]  :red[儀表板] :pencil:')
st.markdown('**公司重要事情 : 颱風來襲，請同仁注意安全 !**')
st.info('**_長龍會議顧問 :以「專業委託書徵求機構」，協助各公司順利完成股東會召開，同時兼顧股東行使權益_**')
#today = datetime.date.today()
# ------------------------------------------------------------------
#資料下載 
file_raw='https://github.com/polaryang/Long_Dragon/raw/main/'
# 1.	重大訊息 db_news
url='https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv'
db_news_L = load_data(url)
url='https://mopsfin.twse.com.tw/opendata/t187ap04_O.csv'
db_news_O = load_data(url)
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
#db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
#db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
db_news=pd.concat([db_news_L, db_news_O])
# 2.	公告查詢 db_announce
url='https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv'
db_announce_L = load_data(url)
url='https://mopsfin.twse.com.tw/opendata/t187ap38_O.csv'
db_announce_O = load_data(url)
db_announce=pd.concat([db_announce_L, db_announce_O])
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv 不定期更新
#db_announce_L=pd.read_csv(file_raw+'t187ap38_L.csv') 
#db_announce_O=pd.read_csv(file_raw+'t187ap38_O.csv')
# 3.	公司基本資料 db_basic
url='https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv'
db_basic_L = load_data(url)
url='https://mopsfin.twse.com.tw/opendata/t187ap03_O.csv'
db_basic_O = load_data(url)
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
#db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') 
#db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')
db_basic=pd.concat([db_basic_L, db_basic_O])
# 4.	董監事持股餘額明細資料 db_board_balance
url='https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv'
db_board_balance_L = load_data(url)
url='https://mopsfin.twse.com.tw/opendata/t187ap11_O.csv'
db_board_balance_O = load_data(url)
# 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
#db_board_balance_L=pd.read_csv(file_raw+'t187ap11_L.csv') #4.	董監事持股餘額明細資料
#db_board_balance_O=pd.read_csv(file_raw+'t187ap11_O.csv')
db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
# 5.	年報前十大股東相互間關係表
# 先到TEJ執行特殊轉檔 每年一次
db_control=pd.read_excel(file_raw+'Control.xlsx') 
# 6.	股權分散表(公開觀測站)
# 先到TEJ執行特殊轉檔 每年一次
db_stock_holder1=pd.read_excel(file_raw+'stock_holder_list.xlsx')
# 7.	集保戶股權分散表 TDCC_OD_1-5.csv
url='https://opendata.tdcc.com.tw/getOD.ashx?id=1-5'
db_stock_holder2 = load_data(url)
db_stock_holder2=db_stock_holder2[db_stock_holder2['持股分級']!=16]
# 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
#db_stock_holder2=pd.read_csv(file_raw+'TDCC_OD_1-5.csv') 
#8.	議事錄
#https://mops.twse.com.tw/mops/web/t150sb04 可以出總表 每年一次
db_share_meeting=pd.read_excel(file_raw+'share_meeting.xlsx')

st.write('test')

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge('run', 'intr')
graph.edge('intr', 'runbl')
graph.edge('runbl', 'run')
graph.edge('run', 'kernel')
graph.edge('kernel', 'zombie')
graph.edge('kernel', 'sleep')
graph.edge('kernel', 'runmem')
graph.edge('sleep', 'swap')
graph.edge('swap', 'runswap')
graph.edge('runswap', 'new')
graph.edge('runswap', 'runmem')
graph.edge('new', 'runmem')
graph.edge('sleep', 'runmem')

st.graphviz_chart(graph)
