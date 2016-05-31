import requests
from bs4 import BeautifulSoup
from dateutil import parser

# Yahoo
URL = "http://finance.yahoo.com/q?s=QCOM"
res = requests.get(URL)

# print res.text
soup = BeautifulSoup(res.text, "lxml")
# print soup.prettify()
for item in soup.select("#yfi_quote_summary_data"):
    print item.select("th")[1].text, item.select(".yfnc_tabledata1")[1].text


# google

URL = "https://www.google.com/finance/historical?q=NASDAQ%3AQCOM&start=0&num=500"
res = requests.get(URL)

soup = BeautifulSoup(res.text, "lxml")
#print soup.prettify()
price_history = []
for item in soup.select("#prices"):
    print item.select(".rgt")[5].text
#     for price in item.select(".rgt"):
#         price_history.append(price)
# print "price_history: ", price_history



prices = soup.find('table', class_='historical_price')
rows = prices.find_all('tr')
keys = [th.text.strip() for th in rows[0].find_all('th')]

date_list = []
value_list = []

for row in rows[1:]:
    for key, td in zip(keys, row.find_all('td')):
        #print key, td.text.strip()
        if key == "Date":
            print "date", td.text.strip()
            dt = parser.parse(td.text.strip())
            date_list.append(dt)
        if key == "Close":
            value_list.append(float(td.text.strip()))

    # data = {key: td.text.strip() for key, td in zip(keys, row.find_all('td'))}
    # print "data: ", data
    # date_list.append(data.get("Date"))
    # value_list.append(data.get("Close"))

print "date_list: ", date_list
print "value_list: ", value_list

import matplotlib.pyplot as plt
import matplotlib.dates as pdate
import numpy as np

plt.interactive(False)

n = 50
# x = np.random.randn(n)
# y = x * np.random.randn(n)
x = date_list
y = value_list
fig, ax = plt.subplots()
print "date: ", pdate.date2num(x)
#pylab.plot_date(pylab.date2num(dates), values, linestyle='-')
fit = np.polyfit(pdate.date2num(x), y, deg=1)
#fit = np.polyfit(x, y, deg=1)

ax.plot(x, fit[0] * pdate.date2num(x) + fit[1], color='red')
ax.scatter(pdate.date2num(x), y)


plt.show()