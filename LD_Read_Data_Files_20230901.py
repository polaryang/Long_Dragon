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

st.set_page_config(page_title='長龍股權數據分析儀表板', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[長龍股權數據分析]  :red[儀表板] :pencil:')
st.markdown('**財富自由 = 被動收入 > 生活支出；  藉由存股的穩定配息，增加被動收入，達成財富自由；  財富自由不是提早退休，而是活出人生命的價值**')
st.info('**_The highest use of capital is not to make more money, but to make money do more for the betterment of life.     ~ Henry Ford_**')
today = datetime.date.today()

col1, col2 = st.columns([12,30], gap='large')
with col1:
ID = st.text_input('輸入股票代號', '2330')
id=int(ID)
ID_code, ID_name, ID_mkt, ID_type, ID_Inds=Checking_ID(ID) 
  if ID_code=='0':
    stock_ticker=ID
  else:
    stock_ticker=ID_code+'.TW'
  if ID_mkt=='上市 ':
    stock_ticker=ID_code+'.TW'
  if ID_mkt=='上櫃 ':
    stock_ticker=ID_code+'.TWO'
  #st.write('**您選擇的標的:**')
  st.subheader(ID_name+' : '+stock_ticker+' : ['+ID_Inds+']')

with col2:
    
    file_raw='https://github.com/polaryang/Long_Dragon/raw/main/'
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["重大訊息", "公告查詢", "公司基本資料", "董監事持股餘額明細資料", "年報前十大股東相互間關係表"])
  with tab1:
    # 1.	重大訊息
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
    db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
    db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
    db_news=pd.concat([db_news_L, db_news_O])
    #df_basic['Stock_ID']=str(df_basic['公司代號'])
    df_news=db_news[db_news['公司代號']==id]
    st.dataframe(df_news, use_container_width=True)
    
    # 2.	公告查詢 
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv 不定期更新
    db_announce_L=pd.read_csv(file_raw+'t187ap38_L.csv') #3.	公司基本資料
    db_announce_O=pd.read_csv(file_raw+'t187ap38_O.csv')
    db_announce=pd.concat([db_announce_L, db_announce_O])
    #df_basic['Stock_ID']=str(df_basic['公司代號'])
    df_announce=db_announce[db_announce['公司代號']==id]
    st.dataframe(df_announce, use_container_width=True)
    
    # 3.	公司基本資料 
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
    db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') #3.	公司基本資料
    db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')
    db_basic=pd.concat([db_basic_L, db_basic_O])
    #df_basic['Stock_ID']=str(df_basic['公司代號'])
    df_basic=db_basic[db_basic['公司代號']==id]
    st.dataframe(df_basic, use_container_width=True)
    
    
    # 4.	董監事持股餘額明細資料
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
    db_board_balance_L=pd.read_csv(file_raw+'t187ap11_L.csv') #4.	董監事持股餘額明細資料
    db_board_balance_O=pd.read_csv(file_raw+'t187ap11_O.csv')
    db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
    df_board_balance=db_board_balance[db_board_balance['公司代號']==id]
    st.dataframe(df_board_balance, use_container_width=True)
    
    # 5.	年報前十大股東相互間關係表
    # 先到TEJ執行特殊轉檔 每年一次
    db_control=pd.read_excel(file_raw+'Control.xlsx') #4.	董監事持股餘額明細資料
    df_control=db_control[db_control['公司']==id]
    
    # 6.	股權分散表(公開觀測站)
    # 先到TEJ執行特殊轉檔 每年一次
    db_stock_holder1=pd.read_excel(file_raw+'stock_holder_list.xlsx')
    df_stock_holder1=db_stock_holder1[db_stock_holder1['公司']==id]
    
    # 7.	集保戶股權分散表 TDCC_OD_1-5.csv
    # 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
    db_stock_holder2=pd.read_csv(file_raw+'TDCC_OD_1-5.csv') #4.	董監事持股餘額明細資料
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
    db_share_meeting=pd.read_excel(file_raw+'share_meeting.xlsx')
    df_share_meeting=db_share_meeting[db_share_meeting['公司代號']==id]
