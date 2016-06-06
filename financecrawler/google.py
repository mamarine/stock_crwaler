from provider import ContainProvider
import requests
from bs4 import BeautifulSoup
from dateutil import parser


class GoogleFinanceCrawler(ContainProvider):
    URL = "https://www.google.com/finance/historical?q=NASDAQ%3A"

    def __init__(self, company_id="", parameter_string=""):
        ContainProvider.__init__(self, company_id, parameter_string)

    def get_history_price(self, days=200):
        if days <= 200:
            self.request_url += ("&start=0&num=" + str(days))
            self.__fetch_data(self.request_url)
        else:
            i = 0
            while days > 0:
                url = self.request_url + "&num=200&start=" + str(i)
                days -= 200
                i += 200
                self.__fetch_data(url)

        return self.date_list, self.value_list

    def __fetch_data(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        try:
            prices = soup.find('table', class_='historical_price')
            rows = prices.find_all('tr')
        except AttributeError:
            print "no more data from server"
            return
        keys = [th.text.strip() for th in rows[0].find_all('th')]

        for row in rows[1:]:
            for key, td in zip(keys, row.find_all('td')):
                if key == "Date":
                    dt = parser.parse(td.text.strip())
                    self.date_list.append(dt)
                if key == "Close":
                    self.value_list.append(float(td.text.strip()))