import yfinance as yf
print(yf.__version__)

t = yf.Ticker("VOO")
df = t.history(period="60d", interval="1d")
print(df.shape)
print(df.tail())