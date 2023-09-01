import pandas as pd
import yfinance as yf
import datetime
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import os
# ------------------------------------------------------------------
def send_email(sender, password, receiver, smtp_server, 
smtp_port, email_message, subject, attachment=None):  #attachment=None
  #https://zhuanlan.zhihu.com/p/109551738
  message = MIMEMultipart()
  message['To'] = Header(receiver)
  message['From']  = Header(sender)
  message['Subject'] = Header(subject)
  message.attach(MIMEText(email_message,'plain', 'utf-8'))
  if attachment:
    att= MIMEApplication(open(attachment, 'rb').read(), name=os.path.basename(attachment)) #
    #att = MIMEApplication(attachment.read(), _subtype="txt")
    att["Content-Type"] = 'application/octet-stream'
    att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
    message.attach(att)
  server = smtplib.SMTP(smtp_server, smtp_port)
  server.starttls()
  server.ehlo()
  server.login(sender, password)
  text = message.as_string()
  server.sendmail(sender, receiver, text)
  server.quit()
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
def divid_cf_calc(age,income_a,income_g,expense_a,inflation,idir,
          divid_rate,last_close,invest_p,divid_live_p,redempt):
  age_list=[]
  income_list=[]
  expense_list=[]
  shares_list=[]
  shares_list=[]
  shares_list1=[]
  shares_all_list=[]
  shares_value_list=[]
  divid_list=[]
  divid_share_list=[]
  cash_divid_list=[]
  cash_redempt_list=[]
  cash_all_list=[]
  net_income_list=[]
  for i in range(invest_p+divid_live_p):
      age_list.append(age+i)
      if i <=invest_p: # 複利投資期間
          income_list.append(income_a*(1+income_g)**i)
      else:            # 財富自由期間
          income_list.append(0)
      expense_list.append(expense_a*(1+inflation)**i)
      d_income=max(income_list[-1]-expense_list[-1],0)
      shares_list1.append(d_income*idir/last_close) # 年初存入股票
      if i==0:
          shares_list.append(d_income*idir/last_close) #第1期年初存入股票 
          divid_list.append(shares_list[i]*divid_rate) # 通常6月配息 單位:股

      else:
          shares_list.append(d_income*idir/last_close+shares_list[i-1]) # 年初存入股票+累進資產    
          divid_list.append(shares_all_list[-1]*divid_rate) # 通常6月配息 單位:股
      
      if i <=invest_p: # 複利投資期間      
          cash_divid_list.append(0)  # 現金領息為 0
          divid_share_list.append(divid_list[-1]/last_close) # 股息換算股票股數
          shares_all_list.append(shares_list[-1]+divid_share_list[-1])  # 股數轉入累進資產
          cash_redempt_list.append(0)

      else:            # 財富自由期間
          shares_all_list.append(shares_all_list[-1])  # 股數轉入累進資產
          cash_divid_list.append(shares_all_list[i]*divid_rate) # 開始現金領
          divid_share_list.append(0) # 股息領出，就不再換算股票股數
          cash_redempt_list.append(0) # 股票贖回產生的現金
          
          if redempt==1:
            income_shortage=cash_divid_list[-1]-expense_list[-1]
            if income_shortage<0:
              share_redempt=math.ceil(min((income_shortage*-1),shares_value_list[-1])/last_close) # 股票贖回的股數
              cash_redempt_list[-1]=share_redempt*last_close  # 股票贖回產生的現金
              shares_all_list[-1]=shares_all_list[-1]-share_redempt # 股數轉出 累進資產減少
              #cash_divid_list[-1]=shares_all_list[-1]*divid_rate # 開始現金領
              
      cash_all_list.append(cash_divid_list[-1]+cash_redempt_list[-1])
      shares_value_list.append(shares_all_list[-1]*last_close)
      net_income_list.append(income_list[-1]-expense_list[-1]+cash_all_list[-1])
  # initialize data of lists.
  data = {'Age':age_list,'Income':income_list,'Expense':expense_list,'Cash_All':cash_all_list,
          'Cash_Dividends':cash_divid_list,'Cash_Redempt':cash_redempt_list,'Share_Value':shares_value_list,
          'Shares':shares_all_list,'Dividends':divid_list,'Net_Income':net_income_list}
  # Create DataFrame
  df = pd.DataFrame(data)   
  return df
# ------------------------------------------------------------------  
# 前20-->15高現金殖利率股票--> all_list
def get_top_rank_dividend(): #return top_dividend_list
    # https://statementdog.com/screeners/dividend_yield_ranking
    # https://statementdog.com/blog/archives/10896
    # https://tw.stock.yahoo.com/tw-etf/yield
    r = requests.get("https://statementdog.com/screeners/dividend_yield_ranking")
    soup = BeautifulSoup(r.text, 'html.parser')
    id_code=[]
    id_name=[]
    stories1 = soup.find_all("li", {"class":"ranking-item-info ranking-item-ticker-name"})
    for i in range(1,10): #len(stories1)):
            [code,name]=stories1[i].text.split()
            id_code.append(code)    
            id_name.append(name)  
    # 當年現金殖利率
    #stories2 = soup.find_all("li", {"class":"ranking-item-info ranking-item-dividend-yield is-sorted"})
    #rank1y=[]
    #for i in range(1,10): #len(stories2)):
    #       rank1y.append(float(stories2[i].text.replace('%','')))   
    # 平均3年現金殖利率
    stories3 = soup.find_all("li", {"class":"ranking-item-info ranking-item-dividend-yield-3Y"})
    #rank3y=[]
    id_yield=[]
    for i in range(1,10): #len(stories3)):
           #rank3y.append(float(stories3[i].text.replace('%',''))) 
           id_yield.append(float(stories3[i].text.replace('%','')))
    # ------------------------------------------------------------------  
    # 前25->15-->5高現金殖利率ETF--> all_list
    # https://tw.stock.yahoo.com/tw-etf/yield
    r = requests.get("https://tw.stock.yahoo.com/tw-etf/yield")
    soup = BeautifulSoup(r.text, 'html.parser')
    stories0 = soup.find_all("span", {"class":"Fz(14px) C(#979ba7) Ell"})
    for i in range(5): #len(stories0)):
        [id_code0, id_others]=stories0[i].text.split('.')
        id_code.append(id_code0)
        ID_code, ID_name, ID_mkt, ID_type, ID_Inds=Checking_ID(id_code0)
        #print(id_code0,ID_name )
        id_name.append(ID_name[0:9])
    stories2 = soup.find_all("span", {"class":"Jc(fe)"})
    for i in range(5*7): #len(stories2)):
        if (i+1)%7==0: 
            id_yield.append(float(stories2[i].text.replace('%','')))
    #df_etf=pd.DataFrame({'id_code':id_code,'id_name':id_name, 'id_yield':id_yield})        
    df_ranking=pd.DataFrame({'id_code':id_code,'id_name':id_name, 'id_yield':id_yield})    
    df_ranking=df_ranking.sort_values(by='id_yield',ascending=False,ignore_index=True)
    top_dividend_list=[]
    for i in range(len(df_ranking)):
        spaces='  '*(11-len(df_ranking['id_name'][i]))
        top_dividend_list.append(df_ranking['id_code'][i]+'  '+df_ranking['id_name'][i]+spaces+str(df_ranking['id_yield'][i])+'%')
    return top_dividend_list
#st.dataframe(df_ranking)
# ------------------------------------------------------------------  
# 主程式開始
# ------------------------------------------------------------------
st.set_page_config(page_title='財富自由*存股規劃*理財計算機', page_icon=':sparkles:', layout='wide')
st.header(':sparkles: :blue[財富自由*存股規劃]:umbrella_with_rain_drops: :red[理財計算機] :pencil:')
st.markdown('**財富自由 = 被動收入 > 生活支出；  藉由存股的穩定配息，增加被動收入，達成財富自由；  財富自由不是提早退休，而是活出人生命的價值**')
st.info('**_The highest use of capital is not to make more money, but to make money do more for the betterment of life.     ~ Henry Ford_**')
col1, col2 = st.columns([12,30], gap='large')
with col1:
  # Basic Parameters
  # 「Discretionary Income」（可調用所得／可運用所得／可花費所得／可花用所得／可調動所得）
  today = datetime.date.today()
  start='2010-01-01'
  end=today
  st.write('**人生規劃**')
  age = st.slider('開始存股年紀?', 15, 100, 25)
  invest_p = st.slider('投資期間 (年)', 0, 100, 30)  # 複利投資期間
  divid_live_p = st.slider('收成期間 (年)', 0, 100, 30)  # 財富自由期間
  st.write('**薪資收入與生活開銷**')
  income=st.number_input('每月薪資',value=50000,step=5000)
  income_g=st.number_input('薪資年成長率%',value=2.0,step=0.25)
  income_g=income_g/100
  income_bonus=st.number_input('年終獎金 (月)',value=2)
  expense=st.number_input('每月生活開銷',value=20000,step=5000)
  inflation=st.number_input('年通貨膨脹率%',value=3.0,step=0.25)
  inflation=inflation/100
  st.write('**存股規劃**')
  idir = st.slider('投資佔可支配所得率 (%)', 0, 100, 80)  # invest dispo income ratio
  idir = idir/100
  #redempt=st.number_input('可動用存股嗎?',value=1)
  redempt_yn = st.radio("收成期可動用存股嗎?", ('No', 'Yes'))
  if redempt_yn == 'Yes':
    redempt=1
  else:
    redempt=0    
  #ticker
  ID_input=st.text_input('輸入存股標的 :','2330')
  #判斷由使用者輸入，還是由前15高現金殖利率股票+ETF選入
  check_yes=st.checkbox("參考高現金殖利率標的")
  if check_yes:
    top_dividend_list= get_top_rank_dividend() #return top_dividend_list
    ID_select = st.selectbox(  "代號 名稱 殖利率 %",  top_dividend_list, disabled=not check_yes, )
    [id_code,id_name,id_yield]=ID_select.split()
  #if check_yes:
    ID= id_code   
  else:
     ID= ID_input
  ID_code='0'
  ID_name='0'
  ID_mkt='0'
  ID_type='0'
  ID_Inds='0'
  ID_code, ID_name, ID_mkt, ID_type, ID_Inds=Checking_ID(ID) 
  if ID_code=='0':
    stock_ticker=ID
  else:
    stock_ticker=ID_code+'.TW'
  if ID_mkt=='上市 ':
    stock_ticker=ID_code+'.TW'
  if ID_mkt=='上櫃 ':
    stock_ticker=ID_code+'.TWO'
  st.write('**您選擇的存股標的:**')
  st.write(ID_name+' : '+stock_ticker)
# ------------------------------------------------------------------
income_a=income*(12+income_bonus)
expense_a=expense*12

if ID_type=='ETF':
  #myfile='https://github.com/polaryang/streamlit-example/raw/08f2526337ec7dd9ff5e951ffc5c18c543f1f4fc/EFT_Dividend.xlsx'
  myfile='https://github.com/polaryang/streamlit-example/raw/master/EFT_Dividend.xlsx'
  df = pd.read_excel(myfile)
  df1=df[df['代碼']==ID]
  if len(df1) ==0:
    st.header(':red[查無此ETF]')
  years=['2018', '2019', '2020', '2021', '2022']
  divid_list=[]
  for i in range(8,3,-1):
    divid_list.append(df1.iloc[0, i])
  df_etf=pd.DataFrame(divid_list, index = years, columns =['divid'])
  divid_yr=df_etf.dropna()
  #divid_yr0=df_etf.dropna()
  data = yf.Ticker(stock_ticker)
else:
  data = yf.Ticker(stock_ticker)
  divid=data.dividends
  #splits=data.splits
  if len(divid) ==0:
    st.header(':red[查無此股票]')
  years=pd.Series(data.dividends.index.year)
  divid = pd.DataFrame({'divid':divid.values, 'year':years})
  #divid_yr0=divid.groupby('year').sum()
  divid_yr=divid.groupby('year').sum()
  divid_l=len(divid_yr)
  divid_yr=divid_yr[divid_yr.index<today.year]
  divid_yr=divid_yr[divid_yr.index>today.year-min(divid_l,6)]

avg_divid=round(divid_yr['divid'].mean(),2)
max_divid=round(divid_yr['divid'].max(),2)
min_divid=round(divid_yr['divid'].min(),2)

last_close=data.history()['Close'].tail().mean() # 最近5日平均收盤價

with col2:
  if ID_type=='ETF':
    st.subheader(ID_name+' : '+stock_ticker+' : [ETF]')
  else:
    st.subheader(ID_name+' : '+stock_ticker+' : ['+ID_Inds+']')
  tab1, tab2, tab3, tab4, tab5 = st.tabs(["基本資料", ":heart_eyes: 最樂觀", ":neutral_face: 最可能", ":sob: 最悲觀", ":person_in_tuxedo: 自已定義"])
  with tab1:
    st.subheader('歷史配息金額 ($ per share) : ')
    st.bar_chart(divid_yr)
    st.subheader(':vertical_traffic_light: 現金股利情境分析(近五年)')
    st.write('   :heart_eyes: 最樂觀 Max Dividends Rate ($ per share): '+str(max_divid) )
    st.write('   :neutral_face: 最可能 Average Dividends ($ per share): '+str(avg_divid) )
    st.write('   :sob: 最悲觀 Min Dividends ($ per share): '+str(min_divid) )
    st.write(' ')
    st.subheader('歷史股價走勢')
    st.line_chart(data.history()['Close'])
  with tab2:
    divid_rate=max_divid
    st.subheader(':heart_eyes: 最樂觀情境: Max Dividends Rate')
    st.write('Dividends Rate ($ per share): **'+str(max_divid)+ '**.   Dividend Yield (%): **'+str(round(max_divid/last_close*100,2))+'**.')
    df=divid_cf_calc(age,income_a,income_g,expense_a,inflation,idir,
          divid_rate,last_close,invest_p,divid_live_p,redempt)
    df_max=df
    deficit=len(df[df['Net_Income']<0])
    #st.write(deficit)
    #st.dataframe(deficit)
    if deficit>0:
      st.subheader(':fast_forward: 財富自由計畫 :red[失敗] :thumbsdown:')
    else:
      st.subheader(':fast_forward: 財富自由計畫 :violet[成功] :thumbsup:') 
    
    st.write(':large_blue_square: 薪資所得 :large_green_square: 生活支出 :large_red_square:股利所得')
    i = alt.Chart(df, title='未來現金流量模擬分析 :').mark_line(color="steelblue").encode(x='Age', y='Income')
    e = alt.Chart(df).mark_line(color='green').encode(x='Age', y='Expense')
    c = alt.Chart(df).mark_line(color="red").encode(x='Age', y='Cash_All')
    st.altair_chart((i+e+c), use_container_width=True)
    
    c = alt.Chart(df, title='未來淨現金流量 :').mark_line(color="steelblue").encode(x='Age', y='Net_Income')
    st.altair_chart(c, use_container_width=True)
    
    c = alt.Chart(df, title='未來持有股數 :').mark_bar().encode(x='Age', y='Shares')
    st.altair_chart(c, use_container_width=True)
    #st.write('理財計畫底稿')
    #st.dataframe(df)
  with tab3:
    divid_rate=avg_divid
    st.subheader(':neutral_face: 最可能情境: Average Dividends Rate')
    st.write('Dividends Rate ($ per share): **'+str(avg_divid)+ '**   Dividend Yield: **'+str(round(avg_divid/last_close*100,2))+'**')
    df=divid_cf_calc(age,income_a,income_g,expense_a,inflation,idir,
          divid_rate,last_close,invest_p,divid_live_p,redempt)
    df_avg=df
    deficit=len(df[df['Net_Income']<0])
    #st.write(deficit)
    #st.dataframe(deficit)
    if deficit>0:
      st.subheader(':fast_forward: 財富自由計畫 :red[失敗] :thumbsdown:')
    else:
      st.subheader(':fast_forward: 財富自由計畫 :violet[成功] :thumbsup:') 
      
    st.write(':large_blue_square: 薪資所得 :large_green_square: 生活支出 :large_red_square:股利所得')
    i = alt.Chart(df, title='未來現金流量模擬分析 :').mark_line(color="steelblue").encode(x='Age', y='Income')
    e = alt.Chart(df).mark_line(color='green').encode(x='Age', y='Expense')
    c = alt.Chart(df).mark_line(color="red").encode(x='Age', y='Cash_All')
    st.altair_chart((i+e+c), use_container_width=True)
    
    c = alt.Chart(df, title='未來淨現金流量 :').mark_line(color="steelblue").encode(x='Age', y='Net_Income')
    st.altair_chart(c, use_container_width=True)
    
    c = alt.Chart(df, title='未來持有股數 :').mark_bar().encode(x='Age', y='Shares')
    st.altair_chart(c, use_container_width=True)
    #st.write('理財計畫底稿')
    #st.dataframe(df)
  with tab4:
    divid_rate=min_divid
    st.subheader(':sob: 最壞情境: Min Dividends Rate')
    st.write('Dividends Rate ($ per share): **'+str(min_divid)+ '**   Dividend Yield (%): **'+str(round(min_divid/last_close*100,2))+'**')
    df=divid_cf_calc(age,income_a,income_g,expense_a,inflation,idir,
          divid_rate,last_close,invest_p,divid_live_p,redempt)
    df_min=df
    deficit=len(df[df['Net_Income']<0])
    #st.write(deficit)
    #st.dataframe(deficit)
    if deficit>0:
      st.subheader(':fast_forward: 財富自由計畫 :red[失敗] :thumbsdown:')
    else:
      st.subheader(':fast_forward: 財富自由計畫 :violet[成功] :thumbsup:') 
      
    st.write(':large_blue_square: 薪資所得 :large_green_square: 生活支出 :large_red_square:股利所得')
    i = alt.Chart(df, title='未來現金流量模擬分析 :').mark_line(color="steelblue").encode(x='Age', y='Income')
    e = alt.Chart(df).mark_line(color='green').encode(x='Age', y='Expense')
    c = alt.Chart(df).mark_line(color="red").encode(x='Age', y='Cash_All')
    st.altair_chart((i+e+c), use_container_width=True)
    
    c = alt.Chart(df, title='未來淨現金流量 :').mark_line(color="steelblue").encode(x='Age', y='Net_Income')
    st.altair_chart(c, use_container_width=True)
        
    c = alt.Chart(df, title='未來持有股數 :').mark_bar().encode(x='Age', y='Shares')
    st.altair_chart(c, use_container_width=True)
    #st.write('理財計畫底稿')
    #st.dataframe(df)
  
  with tab5:
    st.subheader(':person_in_tuxedo: 自訂情境 Dividends Rate')
    self_divid=st.number_input('Input Dividends Rate  ($ per share):',value=5.0 ,step=0.1)
    divid_rate=self_divid
    st.write('Dividends Rate ($ per share): **'+str(round(self_divid,2))+ '**   Dividend Yield (%): **'+str(round(self_divid/last_close*100,2))+'**')
    #st.write('Max Dividends Rate ($ per share): '+str(max_divid) )
    #st.write('Average Dividends Rate ($ per share): '+str(avg_divid) )
    #st.write('Min Dividends Rate ($ per share): '+str(min_divid) )
    df=divid_cf_calc(age,income_a,income_g,expense_a,inflation,idir,
          divid_rate,last_close,invest_p,divid_live_p,redempt)
    df_self=df
    deficit=len(df[df['Net_Income']<0])
    #st.write(deficit)
    #st.dataframe(deficit)
    if deficit>0:
      st.subheader(':fast_forward: 財富自由計畫 :red[失敗] :thumbsdown:')
    else:
      st.subheader(':fast_forward: 財富自由計畫 :violet[成功] :thumbsup:') 
    
    st.write(':large_blue_square: 薪資所得 :large_green_square: 生活支出 :large_red_square:股利所得')
    i = alt.Chart(df, title='未來現金流量模擬分析 :').mark_line(color="steelblue").encode(x='Age', y='Income')
    e = alt.Chart(df).mark_line(color='green').encode(x='Age', y='Expense')
    c = alt.Chart(df).mark_line(color="red").encode(x='Age', y='Cash_All')
    st.altair_chart((i+e+c), use_container_width=True)
    
    c = alt.Chart(df, title='未來淨現金流量 :').mark_line(color="steelblue").encode(x='Age', y='Net_Income')
    st.altair_chart(c, use_container_width=True)
        
    c = alt.Chart(df, title='未來持有股數 :').mark_bar().encode(x='Age', y='Shares')
    st.altair_chart(c, use_container_width=True)
    #st.write('理財計畫底稿')
    #st.dataframe(df)
st.info('**需要此財富自由-存股-理財計畫，請留下您的電子信箱及需求，有專業理財顧問分析後會盡速跟您聯繫!**')
with st.form("request_form"):
   email_receiver=st.text_input('**請輸入您的電子信箱住址:**')
   email_request=st.text_area('**留言備註:**',value='請理財顧問跟我聯絡。')
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
      #try:
        email_message='感謝您對我們 財富自由-存股-理財計畫 的支持，以下是您的基本資料。我們會依據您的需求盡速提供解決方案給您!'+'\n客戶信箱:'+email_receiver+'\n年紀:'+str(age)+'\n投資期間:'+str(invest_p)+'\n收成期間:'+str(divid_live_p)+'\n每月薪資:'+str(income)+'\n薪資年成長率:'+str(income_g)+'\n年終獎金:'
        email_message=email_message+str(income_bonus)+'\n每月生活開銷:'+str(expense)+'\n年通貨膨脹率:'+str(inflation)+'\n投資佔可支配所得率:'+str(idir)+'\n可動用存股:'+str(redempt)+'\n投資標的:'+ID_name+':'+stock_ticker+'\n您的需求:'+email_request
        #file_out='https:\\github.com\polaryang\streamlit-example\raw\master\output.xlsx'
        url='https://raw.githubusercontent.com/polaryang/streamlit-example/raw/master/EFT_Dividend.xlsx'
        url='https://raw.githubusercontent.com/polaryang/streamlit-example/raw/08f2526337ec7dd9ff5e951ffc5c18c543f1f4fc/output.xlsx'
        url='https://raw.githubusercontent.com/polaryang/streamlit-example/raw/master/output.xlsx'
        file_out = requests.get(url)
        #with pd.ExcelWriter(file_out) as writer:  
        #    df_max.to_excel(writer, sheet_name='max')
        #    df_avg.to_excel(writer, sheet_name='avg')
        #    df_min.to_excel(writer, sheet_name='min')
        #    df_self.to_excel(writer, sheet_name='self')      
        #send_email('polaryang@gmail.com', 'ryxbncdvmgncqepk', email_receiver, 'smtp.gmail.com', 587, email_message, '財富自由客戶需求', attachment=None)
        send_email('polaryang@gmail.com', 'ryxbncdvmgncqepk', email_receiver, 'smtp.gmail.com', 587, email_message, '財富自由客戶需求', attachment=file_out)
        send_email('polaryang@gmail.com', 'ryxbncdvmgncqepk', 'alyssa103076@gmail.com', 'smtp.gmail.com', 587, email_message, '財富自由客戶需求', attachment=file_out)
        send_email('polaryang@gmail.com', 'ryxbncdvmgncqepk', '666666brian@gmail.com', 'smtp.gmail.com', 587, email_message, '財富自由客戶需求', attachment=file_out)
        st.write(':green[資料已寄出!]')
      #except:
        #st.write(':red[信箱住址輸入錯誤!]')
# ------------------------------------------------------------------
#st.write(':gem:*POWERED by* :blue[銘傳大學:dove_of_peace:財務金融學系 金融科技實驗室 楊重任副教授 / 團隊學生: 黃冠斌、姚岱均]')    
# ------------------------------------------------------------------    
plt.bar(df['Age'],df['Shares'])
plt.xlabel('Age')
plt.ylabel('Share(s)')
plt.title('Number of Shares')
plt.grid()
plt.show()
plt.plot(df['Age'],df['Income'], color='blue', linewidth=2, marker='o')
plt.plot(df['Age'],df['Expense'], color='red', linewidth=2, marker='o')
plt.plot(df['Age'],df['Cash_All'], color='green', linewidth=2, marker='o')
plt.legend(['Income','Expense','Cash to Live off'])
plt.xlabel('Age')
plt.ylabel('$')
plt.title('Cash Flow')
plt.grid()
plt.show() 
plt.plot(df['Age'],df['Net_Income'], color='red', linewidth=2, marker='o')
plt.xlabel('Age')
plt.ylabel('$')
plt.grid()
plt.title('Net Wealth')
plt.show() 
plt.plot(df['Age'],df['Share_Value'], color='red', linewidth=2, marker='o')
plt.xlabel('Age')
plt.ylabel('$')
plt.grid()
plt.title('Value of Stocks in Hands')
plt.show()     
