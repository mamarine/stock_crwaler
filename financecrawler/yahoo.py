from provider import ContainProvider
import requests
from bs4 import BeautifulSoup
from dateutil import parser
import datetime


class YahooFinanceCrawler(ContainProvider):
    URL = "http://finance.yahoo.com/q/hp?s="

    def __init__(self, company_id="", parameter_string=""):
        ContainProvider.__init__(self, company_id.upper(), parameter_string)

    def get_history_price(self, days=66):
        today_date = datetime.date.today()
        if days <= 66:
            start_date = datetime.date.today() - datetime.timedelta(days=days)
            url = self.request_url + "&a=" + str(start_date.month - 1) + "&b=" + str(start_date.day) + "&c=" + str(
                start_date.year) + "&d=" + str(today_date.month - 1) + "&e=" + str(today_date.day - 1) + "&f=" + str(
                today_date.year) + "&g=d"
            self.__fetch_data(url)
        else:
            i = 0
            start_date = datetime.date.today() - datetime.timedelta(days=66)
            end_date = today_date
            while days > 0:
                url = self.request_url + "&a=" + str(start_date.month - 1) + "&b=" + str(start_date.day) + "&c=" + str(
                    start_date.year) + "&d=" + str(end_date.month - 1) + "&e=" + str(
                    end_date.day - 1) + "&f=" + str(end_date.year) + "&g=d"
                days -= 66
                end_date = start_date - datetime.timedelta(days=1)
                start_date = start_date - datetime.timedelta(days=66)
                i += 66
                self.__fetch_data(url)
        # self.__fetch_data("http://finance.yahoo.com/q/hp?s=QCOM&a=11&b=16&c=1991&d=05&e=3&f=2016&g=d")
        return self.date_list, self.value_list

    def __fetch_data(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        prices = soup.find('table', class_='yfnc_datamodoutline1')
        rows = prices.find_all("tr")
        keys = [th.text.strip() for th in rows[0].find_all('th')]
        previous_date = ""
        for row in rows[1:]:
            for key, td in zip(keys, row.find_all('td')):
                try:
                    if key == "Date":
                        dt = parser.parse(td.text.strip())
                        current_date = dt
                        if current_date != previous_date:

                            previous_date = dt
                            self.date_list.append(dt)
                        else:
                            # print "invalid data"
                            pass
                    if key == "Close":
                        self.value_list.append(float(td.text.strip()))
                except ValueError:
                    pass
