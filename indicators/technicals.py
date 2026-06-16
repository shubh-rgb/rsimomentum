
import pandas as pd
def rsi(s,n=21):
    d=s.diff()
    up=d.clip(lower=0).rolling(n).mean()
    dn=(-d.clip(upper=0)).rolling(n).mean()
    rs=up/dn
    return 100-(100/(1+rs))
def add(df):
    df['DMA30']=df['Close'].rolling(30).mean()
    m=df['Close'].rolling(20).mean()
    sd=df['Close'].rolling(20).std()
    df['BB_UP']=m+2*sd
    df['BB_DN']=m-2*sd
    df['RSI']=rsi(df['Close'])
    ema7=df['Close'].ewm(span=7,adjust=False).mean()
    ema21=df['Close'].ewm(span=21,adjust=False).mean()
    df['MACD']=ema7-ema21
    df['MACD_SIG']=df['MACD'].ewm(span=9,adjust=False).mean()
    return df
