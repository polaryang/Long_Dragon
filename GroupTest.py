# -*- coding: utf-8 -*-
import datetime
import json
import pandas as pd
from datetime import datetime
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from streamlit_agraph import agraph, Node, Edge, Config

# ------------------------------------------------------------------
#@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df
# ------------------------------------------------------------------
def Dateform(datestring):
    if type(datestring)!=str:
        datestring=str(datestring)
    if len(datestring)==8:
        year_s=datestring[0:4]
        month_s=datestring[4:6]
        day_s=datestring[6:8]
    if len(datestring)==7:
        year_s=int(datestring[0:3])
        year_s=str(year_s+1911)
        month_s=datestring[3:5]
        day_s=datestring[5:7]
    dated_string=year_s+'/'+month_s+'/'+day_s
    return dated_string     
# ------------------------------------------------------------------
# DB資料下載 與 處理 [開始] 
@st.cache_data
def load_data_process():
    file_raw='https://github.com/polaryang/Long_Dragon/raw/main/'
    file_raw='https://github.com/polaryang/Long_Dragon/raw/main/' 
    st.markdown('** 資料更新狀態 : **')
    # 1.	重大訊息 db_news
    st.text('重大訊息...')
    try:      
        url='https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv'
        db_news_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap04_O.csv'
        db_news_O = load_data(url)
        db_news=pd.concat([db_news_L, db_news_O])
    except:
        db_news=pd.read_excel(file_raw+"db_news.xlsx")
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
        #db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
        #db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
        st.text('local db')
    db_news['發言日期'] = db_news['發言日期'].astype(str)
    db_news['發言時間'] = db_news['發言時間'].astype(str)
    db_news['公司代號'] = db_news['公司代號'].astype(str)
    db_news['事實發生日'] = db_news['事實發生日'].astype(str)
    collect_date=db_news.iloc[0,0]
    st.text('   '+ Dateform(collect_date))
        
    # 2.	公告查詢 db_announce
    st.text("公告查詢...")
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv'
        db_announce_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap38_O.csv'
        db_announce_O = load_data(url)
        db_announce=pd.concat([db_announce_L, db_announce_O])
    except:
        db_announce=pd.read_excel(file_raw+"db_announce.xlsx")
        st.text('local db...')
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv 不定期更新
        #db_announce_L=pd.read_csv(file_raw+'t187ap38_L.csv') 
        #db_announce_O=pd.read_csv(file_raw+'t187ap38_O.csv')
    db_announce=db_announce.rename(columns={'股東常(臨時)會日期-常或臨時':'股東常(臨時)會'})
    db_announce=db_announce.rename(columns={'股東常(臨時)會日期-日期':'開會日期'})
    db_announce=db_announce.rename(columns={'停止過戶起訖日期-起':'停止過戶-起期'})
    db_announce=db_announce.rename(columns={'停止過戶起訖日期-訖':'停止過戶-訖期'})
    db_announce['公司代號'] = db_announce['公司代號'].astype(str)
    db_announce['開會日期'] = db_announce['開會日期'].astype(str)
    db_announce['停止過戶-起期'] = db_announce['停止過戶-起期'].astype(str)
    db_announce['停止過戶-訖期'] = db_announce['停止過戶-訖期'].astype(str)
    collect_date=db_announce.iloc[0,0]
    st.text('   '+ Dateform(collect_date))
        
    # 3.	公司基本資料 db_basic
    st.text('公司基本資料...')
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv'
        db_basic_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap03_O.csv'
        db_basic_O = load_data(url)
        db_basic=pd.concat([db_basic_L, db_basic_O])
    except:
        db_basic=pd.read_excel(file_raw+"db_basic.xlsx")
        st.text('read local...')    
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
        #db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') 
        #db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')  
    collect_date=db_basic.iloc[0,0]
    st.text('   '+ Dateform(collect_date))
        
    # 4.	董監事持股餘額明細資料 db_board_balance
    st.text('董監事持股明細...')
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv'
        db_board_balance_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap11_O.csv'
        db_board_balance_O = load_data(url)
        db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
    except:
        db_board_balance=pd.read_excel(file_raw+"db_board_balance.xlsx")
        st.text('local db...')   
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
        #db_board_balance_L=pd.read_csv(file_raw+'t187ap11_L.csv') #4.	董監事持股餘額明細資料
        #db_board_balance_O=pd.read_csv(file_raw+'t187ap11_O.csv')
    db_board_balance['資料年月'] = db_board_balance['資料年月'].astype(str)
    collect_date=db_board_balance.iloc[0,0]
    st.text('   '+ Dateform(collect_date))
    
    # 5.	年報前十大股東相互間關係表
    # 先到TEJ執行特殊轉檔 TEJ 公司治理 TCGI 1 股權結構 控制持股與董監結構明細 每年一次
    st.text('十大股東資訊...')
    try:
        db_control_L=pd.read_excel(file_raw+'Control_L.xlsx') 
        db_control_O=pd.read_excel(file_raw+'Control_O.xlsx') 
        db_control=pd.concat([db_control_L, db_control_O])
        collect_date=db_control.iloc[0,2]
    except:
        st.text('error local...')  
    st.text('   '+ str(collect_date)[0:4] +'/'+str(collect_date)[4:6])
    
    # 6.	股權分散表(公開觀測站)
    # 先到TEJ執行特殊轉檔 TEJ Company DB 股權結構 每年一次
    try:
        db_stock_holder1_L=pd.read_excel(file_raw+'stock_holder_list_L.xlsx')
        db_stock_holder1_O=pd.read_excel(file_raw+'stock_holder_list_O.xlsx')
        db_stock_holder1=pd.concat([db_stock_holder1_L, db_stock_holder1_O])
    except:
        st.text('error local...')
    db_stock_holder1['公司'] = db_stock_holder1['公司'].astype(str)
        
    # 7.	集保戶股權分散表 TDCC_OD_1-5.csv
    st.text("股權分散表-集保...")
    try:
        url='https://opendata.tdcc.com.tw/getOD.ashx?id=1-5'
        db_stock_holder2 = load_data(url)
    except:
        db_stock_holder2=pd.read_excel(file_raw+"db_stock_holder2.xlsx")
        st.text('read local...')  
        # 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
        #db_stock_holder2=pd.read_csv(file_raw+'TDCC_OD_1-5.csv') 
    db_stock_holder2=db_stock_holder2[db_stock_holder2['持股分級']!=16]
    collect_date=db_stock_holder2.iloc[0,0]
    st.text('   '+ Dateform(collect_date))
    
    #8.	議事錄
    #https://mops.twse.com.tw/mops/web/t150sb04 可以出總表 每年一次
    try:
        db_share_meeting_L=pd.read_excel(file_raw+'share_meeting_L.xlsx')
        db_share_meeting_O=pd.read_excel(file_raw+'share_meeting_O.xlsx')
        db_share_meeting=pd.concat([db_share_meeting_L, db_share_meeting_O])
    except:
        st.write('error local...')
    db_share_meeting=db_share_meeting.dropna()
    db_share_meeting['公司代號'] = db_share_meeting['公司代號'].astype(int)
    # DB資料下載 與 處理 [結束] 
    return db_news, db_announce, db_basic, db_board_balance, db_control, db_stock_holder1, db_stock_holder2, db_share_meeting
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
def K_bar(stock_data):
    #fig = go.Figure(data=[go.Candlestick(x=stock_data['Date'], open=stock_data['Open'], high=stock_data['High'],low=stock_data['Low'], close=stock_data['Close'])])
    #fig.update_layout(xaxis_rangeslider_visible=False)  
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                   vertical_spacing=0.03, subplot_titles=('股價', '成交量'), row_width=[0.2, 0.7])
    # 繪製 股價 線圖
    fig.add_trace(go.Candlestick(x=stock_data["Date"], open=stock_data["Open"], high=stock_data["High"],
                    low=stock_data["Low"], close=stock_data["Close"], showlegend=False , name="", increasing_line_color= 'red', decreasing_line_color= 'green'), 
                    row=1, col=1 )
    # 繪製 成交量 線圖
    fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['Volume'], showlegend=False), row=2, col=1)
    fig.update_xaxes( rangeselector = dict(
        # 增加固定范围选择
        buttons = list([
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(count = 3, label = '3Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig
# ------------------------------------------------------------------
# 程式開始
# ------------------------------------------------------------------
st.set_page_config(page_title='長龍股權*數據分析儀表板', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[長龍股權*數據分析]  :red[儀表板] :pencil:')
st.markdown('**公司重要事情 : 颱風來襲，請同仁注意安全 !**')
st.info('**_長龍會議顧問 : 為一家「專業委託書徵求機構」，透過徵求委託書出席的方式，協助各公司順利完成股東會，並兼顧股東權益_**')
today_s =datetime.today().strftime('%Y-%m-%d')

col1, col2 = st.columns([1,3], gap='small')
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
      st.markdown('**'+ID_name+' : '+ID_code+'**')
      st.write(ID_mkt+' '+ID_Inds)
      id=int(ID_code)
  db_news, db_announce, db_basic, db_board_balance, db_control, db_stock_holder1, db_stock_holder2, db_share_meeting=load_data_process() 

    
with col2:
  nodes = []
  edges = []
  df_control=db_control[db_control['公司']==id]
  nodes.append( Node(id=ID_code, label=ID_name, size=20, color='blue') )   
  for i in range(len(db_control)):
      investor=df_control['持股人集團名'][i]
      st.write(investor)
      nodes.append( Node(id=investor, size=10, color='red') ) 

  edges.append( Edge(source="Captain_Marvel", label="friend_of", target="Spiderman", type="CURVE_SMOOTH" ) )  
  edges.append( Edge(source="1101", label="friend_of", target="Spiderman", type="CURVE_SMOOTH" ) )   
  edges.append( Edge(source="Captain_Marvel", label="friend_of", target="Spiderman", type="CURVE_SMOOTH" ) ) 
  edges.append( Edge(source="Captain_Marvel", label="friend_of", target="2330", type="CURVE_SMOOTH" ) ) 
  edges.append( Edge(source="2330", label="friend_of", target="Spiderman", type="CURVE_SMOOTH" ) ) 
  edges.append( Edge(source="2330", label="investment", target="Spiderman", type="CURVE_SMOOTH" ) )   
    
  config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

  return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
                  
  from streamlit_agraph.config import Config, ConfigBuilder

  # 1. Build the config (with sidebar to play with options) .
  config_builder = ConfigBuilder(nodes)
  config = config_builder.build()

  # 2. If your done, save the config to a file.
  config.save("config.json")

  # 3. Simple reload from json file (you can bump the builder at this point.)
  config = Config(from_json="config.json")   
  
# ------------------------------------------------------------------

st.info(':copyright: 2023 長龍會議顧問股份有限公司  :school: 100 台北市中正區博愛路80號10樓 ​ :vibration_mode: Line搜尋:長龍(@110qfcpf)')
st.write(':gem: *POWERED by*  :dragon_face: :red[長龍會議顧問  X  銘傳大學] :dove_of_peace: :blue[財務金融學系 金融科技實驗室 團隊學生: 黃冠斌、姚岱均] :mailbox_with_mail:')

