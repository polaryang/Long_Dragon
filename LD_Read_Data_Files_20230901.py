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
        collect_date=db_news.iloc[0,0]
    except:
        db_news=pd.read_excel(file_raw+"db_news.xlsx")
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap04_L.csv 每日更新
        #db_news_L=pd.read_csv(file_raw+'t187ap04_L.csv') 
        #db_news_O=pd.read_csv(file_raw+'t187ap04_O.csv')
        collect_date=db_news['出表日期'][0]
        st.text('local db')
    db_news['發言日期'] = db_news['發言日期'].astype(str)
    db_news['發言時間'] = db_news['發言時間'].astype(str)
    db_news['公司代號'] = db_news['公司代號'].astype(str)
    db_news['事實發生日'] = db_news['事實發生日'].astype(str)
    
    st.text('   '+ Dateform(collect_date))
        
    # 2.	公告查詢 db_announce
    st.text("公告查詢...")
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap38_L.csv'
        db_announce_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap38_O.csv'
        db_announce_O = load_data(url)
        db_announce=pd.concat([db_announce_L, db_announce_O])
        collect_date=db_announce.iloc[0,0]
    except:
        db_announce=pd.read_excel(file_raw+"db_announce.xlsx")
        collect_date=db_announce['出表日期'][0]
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
    st.text('   '+ Dateform(collect_date))
        
    # 3.	公司基本資料 db_basic
    st.text('公司基本資料...')
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv'
        db_basic_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap03_O.csv'
        db_basic_O = load_data(url)
        db_basic=pd.concat([db_basic_L, db_basic_O])
        collect_date=db_basic.iloc[0,0]
    except:
        db_basic=pd.read_excel(file_raw+"db_basic.xlsx")
        collect_date=db_basic['出表日期'][0]
        st.text('read local...')    
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv 不定期更新
        #db_basic_L=pd.read_csv(file_raw+'t187ap03_L.csv') 
        #db_basic_O=pd.read_csv(file_raw+'t187ap03_O.csv')  
    st.text('   '+ Dateform(collect_date))
        
    # 4.	董監事持股餘額明細資料 db_board_balance
    st.text('董監事持股明細...')
    try:
        url='https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv'
        db_board_balance_L = load_data(url)
        url='https://mopsfin.twse.com.tw/opendata/t187ap11_O.csv'
        db_board_balance_O = load_data(url)
        db_board_balance=pd.concat([db_board_balance_L, db_board_balance_O])
        collect_date=db_board_balance.iloc[0,0]
    except:
        db_board_balance=pd.read_excel(file_raw+"db_board_balance.xlsx")
        collect_date=db_board_balance['出表日期'][0]
        st.text('local db...')   
        # 先執行 https://mopsfin.twse.com.tw/opendata/t187ap11_L.csv 不定期更新
        #db_board_balance_L=pd.read_csv(file_raw+'t187ap11_L.csv') #4.	董監事持股餘額明細資料
        #db_board_balance_O=pd.read_csv(file_raw+'t187ap11_O.csv')
    db_board_balance['資料年月'] = db_board_balance['資料年月'].astype(str)
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
        collect_date=db_stock_holder2.iloc[0,0]
    except:
        db_stock_holder2=pd.read_excel(file_raw+"db_stock_holder2.xlsx")
        collect_date=db_stock_holder2['資料日期'][0]
        st.text('read local...')  
        # 先執行 https://opendata.tdcc.com.tw/getOD.ashx?id=1-5  每周更新
        #db_stock_holder2=pd.read_csv(file_raw+'TDCC_OD_1-5.csv') 
    db_stock_holder2=db_stock_holder2[db_stock_holder2['持股分級']!=16]
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

    #9.	委託書
    try:
        db_entrust=pd.read_excel(file_raw+"entrust_pdf_all.xlsx")
    except:
        st.write('error local...')
    db_entrust['證券代號'] = db_entrust['證券代號'].astype(int)
    #9.	委託書
    #try:
    #    #https://webline.sfi.org.tw/download/lib_ftp/opendata/eFileFreeData.csv 每年一次
    #    url='https://webline.sfi.org.tw/download/lib_ftp/opendata/eFileFreeData.csv'
    #    db_entrust = load_data(url)
    #except:
    #    db_entrust=pd.read_excel(file_raw+"db_entrust.xlsx")
    #    st.write('Local ...')
    #db_entrust['股東會日期'] = db_entrust['股東會日期'].astype(str)
    #collect_date=datetime.today()
    #st.write(collect_date)
    
    # DB資料下載 與 處理 [結束] 
    return db_news, db_announce, db_basic, db_board_balance, db_control, db_stock_holder1, db_stock_holder2, db_share_meeting, db_entrust
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
def group_graphy(id,ID_name ):
  df_control=db_control[db_control['公司']==id]
  df_control=df_control.drop(['公司'], axis=1)
  df_control=df_control.drop(['年月'], axis=1)
  share_holded_all=df_control['最終控制者個人持股%']+df_control['集團未上市公司持股%']+df_control['集團基金會持股%']+df_control['集團上市公司持股%']+df_control['經理人持股%']+df_control['外部個人持股%']+df_control['外部未上市公司持股%']+df_control['外部基金會持股%']+df_control['外部上市公司持股%']
  total_share_ratio=sum(share_holded_all)
  df_control.insert(5,"持股占比",share_holded_all,True)
  df_control=df_control[df_control['持股人集團名']!="                     "]  
  df_control_investor = df_control.groupby('持股人集團名').sum()
  df_control_investor=df_control_investor.sort_values(by='持股占比', ascending=False)
  nodes = []
  edges = []
  nodes_keep=[]
  nodes.append( Node(id=str(id), label=ID_name, size=45, color='blue') )   
  nodes_keep.append(str(id))  
  if  len(df_control_investor) > 0: 
      for i in range(len(df_control_investor)): # control_investor 持股人集團名 len(df_control_investor)
          control_investor=df_control_investor.index[i]
          if control_investor not in nodes_keep:
              nodes.append( Node(id=control_investor, label=control_investor, size=5+int(df_control_investor['持股占比'][i]/total_share_ratio*40), color='red') )
              edges.append( Edge(source=control_investor, target=str(id), label=str(round(df_control_investor['持股占比'][i],2)), type="CURVE_SMOOTH" ) )
              nodes_keep.append(control_investor)
          df_control_invested=db_control[db_control['持股人集團名']==control_investor]
          df_control_invested=df_control_invested[df_control_invested['公司']!=id]
          df_control_invested_id=df_control_invested['公司'] #被控制者 投資的 公司代號
          df_control_invested_name=df_control_invested['簡稱'] #被控制者 投資的 公司名稱
          df_control_invested_id=pd.unique(pd.Series(df_control_invested_id))
          df_control_invested_name=pd.unique(pd.Series(df_control_invested_name))
          if len(df_control_invested_name) > 0:
              for j in range(len(df_control_invested_name)): #len(df_control_invested_name)
                  investee_id= pd.DataFrame(df_control_invested_id).iloc[j,0]
                  investee_name= pd.DataFrame(df_control_invested_name).iloc[j,0]
                  if str(investee_id) not in nodes_keep:
                      nodes.append( Node(id=str(investee_id), label=investee_name, size=20, color='green') )
                      nodes_keep.append(str(investee_id))
                  edges.append( Edge(source=control_investor, target=str(investee_id), type="CURVE_SMOOTH" ) )
  config = Config(width=1000, height=700, directed=True, physics=True, hierarchical=False,
                nodeHighlightBehavior=True,  )  #nodeHighlightBehavior=True,   highlightColor="#F7A7A6",   directed=True,   collapsible=True 
  return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# 程式開始
# ------------------------------------------------------------------
st.set_page_config(page_title='長龍股權*數據分析儀表板', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[長龍股權*數據分析]  :red[儀表板] :pencil:')
st.markdown('**公司重要公布 : '目前此系統為測試資料，請小心使用 !**')
st.info('**_長龍會議顧問 : 為一家「專業委託書徵求機構」，透過徵求委託書出席的方式，協助各公司順利完成股東會，並兼顧股東權益_**')
today_s =datetime.today().strftime('%Y-%m-%d')

col1, col2 = st.columns([4,28], gap='small')
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
  db_news, db_announce, db_basic, db_board_balance, db_control, db_stock_holder1, db_stock_holder2, db_share_meeting, db_entrust=load_data_process() 
  try:
      stock_data=yf.download(stock_ticker, period='5y')
      st.text('股價線圖...')
      st.text('   '+ stock_data.index[-1].strftime("%Y-%m-%d"))
  except:
      st.text('yfinance download error')
      
with col2:
  tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(["重大訊息", "公告查詢", "公司基本資料", "董監事持股餘額", "十大股東", "集團控制關聯圖", "股權分散表", "議事錄", "委託書徵求", "股價趨勢圖", "徵求作業流程圖", "系統維護"])
  #tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["重大訊息", "公告查詢", "公司基本資料", "董監事持股餘額", "十大股東*", "股權分散表-", "議事錄*"])
  with tab1:
    # 1.	重大訊息 db_news
    #collect_date=db_news.iloc[0,0]
    st.subheader('重大訊息')
    db_news=db_news.drop(['出表日期'], axis=1)
    df_news=db_news[db_news['公司代號']==str(id)]
    if len(df_news)>0:
      seq=range(1,len(df_news)+1)
      df_news.insert(0,"序號",seq,True)
      st.dataframe(df_news, use_container_width=True,hide_index=True)
    else:
      st.dataframe(df_news, use_container_width=True,hide_index=True)
    st.write('今日全部重大訊息')
    if len(db_news)>0:
      seq=range(1,len(db_news)+1)
      db_news.insert(0,"序號",seq,True)
      st.dataframe(db_news, use_container_width=True,hide_index=True)
    else:
      st.dataframe(db_news, use_container_width=True,hide_index=True)
    #st.write('資料收集日期: '+str(collect_date))
    
  with tab2:    
    # 2.	公告查詢 db_announce 
    #collect_date=db_announce.iloc[0,0]
    st.subheader('股東會公告查詢')
    db_announce=db_announce.drop(['出表日期'], axis=1)
    df_announce=db_announce[db_announce['公司代號']==str(id)]
    #df_announce=df_announce.reset_index(drop=True)
    if len(df_announce)>0:
      seq=range(1,len(df_announce)+1)
      df_announce.insert(0,"序號",seq,True)
      st.dataframe(df_announce, use_container_width=True,hide_index=True)
    else:
      st.dataframe(df_announce, use_container_width=True,hide_index=True)
    st.write('今年全部公告')
    if len(db_announce)>0:
      seq=range(1,len(db_announce)+1)
      db_announce.insert(0,"序號",seq,True)
      st.dataframe(db_announce, use_container_width=True,hide_index=True)
    else:
      st.dataframe(db_announce, use_container_width=True,hide_index=True)
    #st.write('資料收集日期: '+str(collect_date))
    
  with tab3:    
    # 3.	公司基本資料 db_basic
    #collect_date=db_basic.iloc[0,0]
    st.subheader('公司基本資料')
    db_basic=db_basic.drop(['出表日期'], axis=1)
    df_basic=db_basic[db_basic['公司代號']==id]
    df_basic=df_basic.reset_index(drop=True)
    df_basic_T=df_basic.T
    st.dataframe(df_basic_T, use_container_width=True)
    #st.write('資料收集日期: '+str(collect_date))
    
  with tab4:
    # 4.	董監事持股餘額明細資料 db_board_balance
    #collect_date=db_board_balance.iloc[0,0]
    st.subheader('董監事持股餘額明細資料')
    db_board_balance=db_board_balance.drop(['出表日期'], axis=1)
    df_board_balance=db_board_balance[db_board_balance['公司代號']==id]
    df_board_balance=df_board_balance.drop(['公司代號'], axis=1)
    if len(df_board_balance)>0:
      seq=range(1,len(df_board_balance)+1)
      df_board_balance.insert(0,"序號",seq,True)
      st.dataframe(df_board_balance, use_container_width=True,hide_index=True)
    else:
      st.dataframe(df_board_balance, use_container_width=True,hide_index=True)
    #st.write('資料收集日期: '+str(collect_date))
    
  with tab5:    
    # 5.	年報前十大股東相互間關係表
    #collect_date=db_control.iloc[0,2]
    st.subheader('年報前十大股東相互間關係表')
    df_control=db_control[db_control['公司']==id]
    df_control=df_control.drop(['公司'], axis=1)
    df_control=df_control.drop(['年月'], axis=1)
    #df_control['持股占比']=df_control['最終控制者個人持股%']+df_control['集團未上市公司持股%']+df_control['集團基金會持股%']+df_control['集團上市公司持股%']+df_control['經理人持股%']+df_control['外部個人持股%']+df_control['外部未上市公司持股%']+df_control['外部基金會持股%']+df_control['外部上市公司持股%']
    share_holded_all=df_control['最終控制者個人持股%']+df_control['集團未上市公司持股%']+df_control['集團基金會持股%']+df_control['集團上市公司持股%']+df_control['經理人持股%']+df_control['外部個人持股%']+df_control['外部未上市公司持股%']+df_control['外部基金會持股%']+df_control['外部上市公司持股%']
    df_control.insert(5,"持股占比",share_holded_all,True)
    if len(df_control)>0:
      seq=range(1,len(df_control)+1)
      df_control.insert(0,"序號",seq,True)
      st.dataframe(df_control, use_container_width=True,hide_index=True)
    else:
      st.dataframe(df_control, use_container_width=True,hide_index=True)
    st.write('持股人之控制別說明 : :red[A=最終控制者、B=經理人、C=集團經理人、L=友好集團、X=外部人]')
    T5col1, T5col2 = st.columns([1,3], gap='small')
    with T5col1:
        option = st.radio('控制分析依據角度 : ', ['持股人控制別', '持股人集團別', '持股人身分別'])
    with T5col2:  
        if option=='持股人控制別':
          df_control_class = df_control.groupby('控制別').sum()
          df_control_class=df_control_class.sort_values(by='持股占比', ascending=False)
          df_control_results=df_control_class['持股占比']
          df_control_results.rename(index={'A':'最終控制者A', 'B':'經理人B', 'C':'集團經理人C', 'L':'友好集團L', 'X':'外部人X'}, inplace=True)
        if option=='持股人集團別':
          df_control_class = df_control.groupby('持股人集團名').sum()
          df_control_class=df_control_class.sort_values(by='持股占比', ascending=False)
          df_control_results=df_control_class['持股占比']
          df_control_results.rename(index={'                     ':'其他'}, inplace=True)
        if option=='持股人身分別':
          df_control_class = df_control.groupby('身份別').sum()
          df_control_class=df_control_class.sort_values(by='持股占比', ascending=False)
          df_control_results=df_control_class['持股占比']  
        st.dataframe(df_control_results, use_container_width=True)  
        st.bar_chart(df_control_results, use_container_width=True)
        #st.write('資料截止日期: '+str(collect_date))
    
  with tab6:      
    # 集團控制之關聯圖
    st.subheader('集團控制之關聯圖')   
    group_graphy(id,ID_name )
      
  with tab7:  
    # 6.	股權分散表(公開觀測站)
    st.subheader('股權分散表')
    df_stock_holder1=db_stock_holder1[db_stock_holder1['公司']==str(id)]  
    # 7.	集保戶股權分散表 TDCC_OD_1-5.csv
    #collect_date=db_stock_holder2.iloc[0,0]
    df_stock_holder2=db_stock_holder2[db_stock_holder2['證券代號']==str(id)]
    #30~40 40~50 合併
    df_stock_holder2.iloc[6,3:5]=df_stock_holder2.iloc[6,3:5]+df_stock_holder2.iloc[7,3:5]
    df_stock_holder2=df_stock_holder2[df_stock_holder2['持股分級']!=8]
    df_stock_holder2['持股分級']=range(1,16)
    df_stock_holder2['股數']=round(df_stock_holder2['股數']/1000,0)
    df_stock_holder2=df_stock_holder2.rename(columns={'股數':'張數'})
    df_stock_holder2=df_stock_holder2.rename(columns={'占集保庫存數比例%':'比率'})
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
    df_stock_holder3=df_stock_holder3.drop(['資料日期','證券代號'], axis=1)
    #df_stock_holder3=df_stock_holder3.reset_index(drop=True)
    st.dataframe(df_stock_holder3, width=5, hide_index=True , use_container_width=True)
    df_stock_holder3=df_stock_holder3[df_stock_holder3['持股分級']!=15]
    st.line_chart(df_stock_holder3, x='持股分級', y=['股東會時_比率', '比率'], color = ['#00008B', '#8B0000'], use_container_width=True) 
    #st.write('資料收集日期: '+str(collect_date))

  with tab8: 
    #8.	議事錄
    st.subheader('議事錄')
    df_share_meeting=db_share_meeting[db_share_meeting['公司代號']==id]
    #df_share_meeting=df_share_meeting.reset_index(drop=True)    
    df_share_meeting=df_share_meeting.drop(['公司代號'], axis=1)
    st.dataframe(df_share_meeting, use_container_width=True,hide_index=True)
    st.write('全部公司議事錄')
    db_share_meeting=db_share_meeting.sort_values(by='公司代號', ascending=True)
    seq=range(1,len(db_share_meeting)+1)
    db_share_meeting.insert(0,"序號",seq,True)  
    db_share_meeting['公司代號'] = db_share_meeting['公司代號'].astype(str)
    st.dataframe(db_share_meeting, use_container_width=True,hide_index=True)

  with tab9: 
    #9.	委託書徵求
    st.subheader('委託書徵求(歷年)')
    st.write('status=1 : 可以從委託書公告網站自動抓下pdf資料；status=0 : 無法自動抓下pdf資料，不代表沒有委託徵求')
    db_entrust['證券代號'] = db_entrust['證券代號'].astype(str)
    db_entrust['股東常會日期'] = db_entrust['股東常會日期'].astype(str)
    df_entrust=db_entrust[db_entrust['證券代號']==str(id)] 
    df_entrust=df_entrust.drop(['證券代號'], axis=1)
    df_entrust=df_entrust.sort_values(by='股東常會日期', ascending=False)  
    st.dataframe(df_entrust, use_container_width=True,hide_index=True)
    st.caption('此資料僅供參考，必要時請自行修正 委託書徵求資料庫')  
    st.write(' ')
    st.write('全部公司委託書徵求')
    db_entrust=db_entrust.sort_values(by=['證券代號','股東常會日期'], ascending=True) 
    seq=range(1,len(db_entrust)+1)
    db_entrust.insert(0,"序號",seq,True)  
    #db_entrust['證券代號'] = db_entrust['證券代號'].astype(str)
    st.dataframe(db_entrust, use_container_width=True,hide_index=True)
      
  with tab10:   
    # 繪製 k 線圖
    st.subheader('近五年股價走勢圖')
    Date_s=stock_data.index.strftime("%Y-%m-%d")
    stock_data.insert(0,"Date",Date_s,True)
    fig=K_bar(stock_data)
    st.plotly_chart(fig, use_container_width=True)  
    st.dataframe(stock_data,hide_index=True)
      
  with tab11:
    st.subheader('股東常會徵求作業日程表')
    image = Image.open('./workflow_常會.png')
    st.image(image)  
    st.subheader('股東臨時會徵求作業日程表')
    image = Image.open('./workflow_臨時會.png')
    st.image(image)  
      
  with tab12:
    st.subheader('系統維護說明')
    st.write(':one: 資料更新後首次使用，系統會先把所需要的資料下載')
    st.write(':two: 因此系統會較慢，等資料全部下載完成後速度就恢復正常')
    st.write(':three: 更新中如有錯誤訊息，通常是資料抓取時連線中斷造成的')
    st.write(':four: 請執行 :blue[重新載入此頁] 或 :blue[離開系統重新執行] !')
    st.write(':question: 有問題請 :envelope_with_arrow: 楊老師 cjyang@mail.mail.mcu.edu.tw')
    st.write('')
    st.write('')
    st.write(':fire: 如確認進行資料更新，請按以下 :red[清除Caches並資料更新] 鍵')
    if st.button("清除Caches並資料更新"):
        st.cache_data.clear()
  
# ------------------------------------------------------------------

st.info(':copyright: 2023 長龍會議顧問股份有限公司  :school: 100 台北市中正區博愛路80號10樓 ​ :vibration_mode: Line搜尋:長龍(@110qfcpf)')
st.write(':gem: *POWERED by*  :dragon_face: :red[長龍會議顧問  X  銘傳大學] :dove_of_peace: :blue[財務金融學系 金融科技實驗室 團隊學生: 黃冠斌、姚岱均] :mailbox_with_mail:')


