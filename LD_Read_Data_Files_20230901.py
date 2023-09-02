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

st.set_page_config(page_title='長龍股權*數據分析儀表板', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[長龍股權*數據分析]  :red[儀表板] :pencil:')
st.markdown('**公司重要事情 : 颱風來襲，請同仁注意安全 !**')
st.info('**_長龍會議顧問 :以「專業委託書徵求機構」，協助各公司順利完成股東會召開，同時兼顧股東行使權益_**')
#today = datetime.date.today()

col1, col2 = st.columns([4,27], gap='small')
with col1:
  ID = st.text_input('輸入股票代號(代號或名稱皆可)', '2330')
  ID_code, ID_name, ID_mkt, ID_type, ID_Inds=Checking_ID(ID) 
  if ID_code=='0':
      st.write('查無此股票')
  else:  
      if ID_mkt=='上市 ':
        stock_ticker=ID_code+'.TW'
      if ID_mkt=='上櫃 ':
        stock_ticker=ID_code+'.TWO'
      st.write(ID_name+' : '+stock_ticker)
      st.write(ID_mkt+' '+ID_Inds)
      id=int(ID_code)
    
with col2:
 
  file_raw='https://github.com/polaryang/Long_Dragon/raw/main/'
  #tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["重大訊息", "公告查詢", "公司基本資料", "董監事持股餘額", "十大股東", "股權分散表", "議事錄","徵求作業日程表"])
  tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["重大訊息", "公告查詢", "公司基本資料", "董監事持股餘額", "十大股東*", "股權分散表-", "議事錄*"])
  with tab1:
    # 1.	重大訊息
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
    #db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
    #db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
    url='https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv'
    db_news_L = load_data(url)
    #db_news_L=pd.read_csv('C:/Users/user/Desktop/Long_dragon/t187ap04_L.csv') 
    url='https://mopsfin.twse.com.tw/opendata/t187ap04_O.csv'
    db_news_O = load_data(url)
    db_news=pd.concat([db_news_L, db_news_O])
    collect_date=db_news.iloc[0,0]
    db_news['發言日期'] = db_news['發言日期'].astype(str)
    db_news['發言時間'] = db_news['發言時間'].astype(str)
    db_news['公司代號'] = db_news['公司代號'].astype(str)
    db_news['事實發生日'] = db_news['事實發生日'].astype(str)
    df_news=db_news[db_news['公司代號']==str(id)]
    df_news=df_news.drop(['出表日期'], axis=1)
    df_news=df_news.reset_index(drop=True)
    st.dataframe(df_news, use_container_width=True)
    st.write('今日全部重大訊息')
    db_news1=db_news
    db_news1=db_news1.drop(['出表日期'], axis=1)
    st.dataframe(db_news1, use_container_width=True)
    st.write('資料收集日期: '+str(collect_date))
    
  with tab2:    
    # 2.	公告查詢 
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv 不定期更新
    url='https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv'
    db_announce_L = load_data(url)
    #db_announce_L=pd.read_csv(file_raw+'t187ap38_L.csv') #3.	公司基本資料
    url='https://mopsfin.twse.com.tw/opendata/t187ap38_O.csv'
    db_announce_O = load_data(url)
    #db_announce_O=pd.read_csv(file_raw+'t187ap38_O.csv')
    db_announce=pd.concat([db_announce_L, db_announce_O])
    collect_date=db_announce.iloc[0,0]
    db_announce=db_announce.rename(columns={'股東常(臨時)會日期-常或臨時':'股東常(臨時)會'})
    db_announce=db_announce.rename(columns={'股東常(臨時)會日期-日期':'開會日期'})
    db_announce=db_announce.rename(columns={'停止過戶起訖日期-起':'停止過戶-起期'})
    db_announce=db_announce.rename(columns={'停止過戶起訖日期-訖':'停止過戶-訖期'})
    db_announce['公司代號'] = db_announce['公司代號'].astype(str)
    db_announce['開會日期'] = db_announce['開會日期'].astype(str)
    db_announce['停止過戶-起期'] = db_announce['停止過戶-起期'].astype(str)
    db_announce['停止過戶-訖期'] = db_announce['停止過戶-訖期'].astype(str)
    df_announce=db_announce[db_announce['公司代號']==str(id)]
    df_announce=df_announce.drop(['出表日期'], axis=1)
    df_announce=df_announce.reset_index(drop=True)
    st.dataframe(df_announce, use_container_width=True)
    st.write('今日全部重大訊息')
    db_announce1=db_announce
    db_announce1=db_announce1.drop(['出表日期'], axis=1)
    st.dataframe(db_announce1, use_container_width=True)
    st.write('資料收集日期: '+str(collect_date))
    
  with tab3:    
    # 3.	公司基本資料 
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
    #db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') #3.	公司基本資料
    #db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')
    url='https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv'
    db_basic_L = load_data(url)
    url='https://mopsfin.twse.com.tw/opendata/t187ap03_O.csv'
    db_basic_O = load_data(url)
    db_basic=pd.concat([db_basic_L, db_basic_O])
    collect_date=db_basic.iloc[0,0]
    df_basic=db_basic[db_basic['公司代號']==id]
    df_basic=df_basic.drop(['出表日期'], axis=1)
    df_basic=df_basic.reset_index(drop=True)
    df_basic_T=df_basic.T
    st.dataframe(df_basic_T, use_container_width=True)
    st.write('資料收集日期: '+str(collect_date))
    
  with tab4:
    # 4.	董監事持股餘額明細資料
    # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
    #db_board_balance_L=pd.read_csv(file_raw+'t187ap11_L.csv') #4.	董監事持股餘額明細資料
    #db_board_balance_O=pd.read_csv(file_raw+'t187ap11_O.csv')
    url='https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv'
    db_board_balance_L = load_data(url)
    url='https://mopsfin.twse.com.tw/opendata/t187ap11_O.csv'
    db_board_balance_O = load_data(url)
    db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
    db_board_balance['資料年月'] = db_board_balance['資料年月'].astype(str)
    collect_date=db_board_balance.iloc[0,0]
    df_board_balance=db_board_balance[db_board_balance['公司代號']==id]
    df_board_balance=df_board_balance.drop(['公司代號'], axis=1)
    df_board_balance=df_board_balance.drop(['出表日期'], axis=1)
    df_board_balance=df_board_balance.reset_index(drop=True)
    st.dataframe(df_board_balance, use_container_width=True)
    st.write('資料收集日期: '+str(collect_date))
    
  with tab5:    
    # 5.	年報前十大股東相互間關係表
    # 先到TEJ執行特殊轉檔 每年一次
    db_control=pd.read_excel(file_raw+'Control.xlsx') #4.	董監事持股餘額明細資料
    collect_date=db_control.iloc[0,2]
    db_control=db_control.drop(['年月'], axis=1)
    df_control=db_control[db_control['公司']==id]
    df_control=df_control.drop(['公司'], axis=1)
    df_control=df_control.reset_index(drop=True)
    st.dataframe(df_control, use_container_width=True)
    st.write('持股人之控制別 : A=最終控制者、B=經理人、C=集團經理人、L=友好集團、X=外部人')
    df_control['Control_ratio']=df_control['最終控制者個人持股%']+df_control['集團未上市公司持股%']+df_control['集團基金會持股%']+df_control['集團上市公司持股%']+df_control['經理人持股%']+df_control['外部個人持股%']+df_control['外部未上市公司持股%']+df_control['外部基金會持股%']+df_control['外部上市公司持股%']
    df_control_class = df_control.groupby('控制別').sum()
    df_control_results=df_control_class['Control_ratio']
    df_control_results.rename(index={'A':'最終控制者', 'B':'經理人', 'C':'集團經理人', 'L':'友好集團', 'X':'外部人'}, inplace=True)
    st.table(df_control_results)
    st.bar_chart(df_control_results, use_container_width=True)
    st.write('資料截止日期: '+str(collect_date))
    
  with tab6:  
    # 6.	股權分散表(公開觀測站)
    # 先到TEJ執行特殊轉檔 每年一次
    db_stock_holder1=pd.read_excel(file_raw+'stock_holder_list.xlsx')
    df_stock_holder1=db_stock_holder1[db_stock_holder1['公司']==id]
     
    # 7.	集保戶股權分散表 TDCC_OD_1-5.csv
    # 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
    #db_stock_holder2=pd.read_csv(file_raw+'TDCC_OD_1-5.csv') #4.	董監事持股餘額明細資料
    url='https://opendata.tdcc.com.tw/getOD.ashx?id=1-5'
    db_stock_holder2 = load_data(url)
    db_stock_holder2=db_stock_holder2[db_stock_holder2['持股分級']!=16]
    df_stock_holder2=db_stock_holder2[db_stock_holder2['證券代號']==str(id)]
    #30~40 40~50 合併
    df_stock_holder2.iloc[6,3:5]=df_stock_holder2.iloc[6,3:5]+df_stock_holder2.iloc[7,3:5]
    df_stock_holder2=df_stock_holder2[df_stock_holder2['持股分級']!=8]
    df_stock_holder2['持股分級']=range(1,16)
    df_stock_holder2['股數']=round(df_stock_holder2['股數']/1000,0)
    df_stock_holder2=df_stock_holder2.rename(columns={'股數':'張數'})
    df_stock_holder2=df_stock_holder2.rename(columns={'占集保庫存數比例%':'比例'})
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
    df_stock_holder3=df_stock_holder2
    df_stock_holder3.insert(4,"股東會時_比率",temp_ratio,True)
    df_stock_holder3.insert(4,"股東會時_張數",temp_share,True)
    df_stock_holder3.insert(4,"股東會時_人數",temp_person,True)
    collect_date=df_stock_holder3.iloc[0,0]
    df_stock_holder3=df_stock_holder3.drop(['資料日期','證券代號'], axis=1)
    df_stock_holder3=df_stock_holder3.reset_index(drop=True)
    st.dataframe(df_stock_holder3, width=5 , use_container_width=True)
    st.write('資料收集日期: '+str(collect_date))
    
  with tab7:   
    #8.	議事錄
    #https://mops.twse.com.tw/mops/web/t150sb04 可以出總表 每年一次
    db_share_meeting=pd.read_excel(file_raw+'share_meeting.xlsx')
    df_share_meeting=db_share_meeting[db_share_meeting['公司代號']==id]
    df_share_meeting=df_share_meeting.reset_index(drop=True)    
    df_share_meeting=df_share_meeting.drop(['公司代號'], axis=1)
    st.dataframe(df_share_meeting, use_container_width=True)
  #with tab8:   
    #image = Image.open('https://raw.githubusercontent.com/polaryang/Long_Dragon/main/workflow')
    image = Image.open('https://static.wixstatic.com/media/d89a3a_578b9900f19c44bba75a961ad436dfcc~mv2.png/v1/fill/w_940,h_503,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/%E8%82%A1%E6%9D%B1%E8%87%A8%E6%9C%83%E6%97%A5%E7%A8%8B%E8%A1%A8.png')
    st.image(image, caption='股東常會徵求作業日程表')    
st.info('© 2023 長龍會議顧問股份有限公司  100 台北市中正區博愛路80號10樓')
st.write(':gem: *POWERED by*  :dragon_face: :red[長龍會議顧問  X  銘傳大學] :dove_of_peace: :blue[財務金融學系 金融科技實驗室 團隊學生: 黃冠斌、姚岱均] :mailbox_with_mail:')


