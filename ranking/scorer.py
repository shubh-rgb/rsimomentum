def score(df):

    r = df.iloc[-1]

    print(type(r['Close']))
    print(type(r['DMA30']))
    print(type(r['MACD']))
    print(type(r['MACD_SIG']))
    print(type(r['RSI']))

    s = 0

    if r['Close'] > r['DMA30']:
        s += 30

    if r['MACD'] > r['MACD_SIG']:
        s += 25

    if r['RSI'] > 55:
        s += 20

    if r['Close'] > (r['BB_UP'] + r['BB_DN']) / 2:
        s += 15

    return float(s)