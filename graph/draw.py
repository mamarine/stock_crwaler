import matplotlib.pyplot as plt
import matplotlib.dates as pdate
import numpy as np


class StockPriceTrend:
    def __init__(self, date_list, price_list, target_corp):
        self.date_list = date_list
        self.price_list = price_list
        self.target_corp = target_corp

    def draw_with_linear_regression(self):
        plt.interactive(False)
        x = self.date_list
        y = self.price_list
        fig, ax = plt.subplots(figsize=(15, 8))
        # print "date: ", pdate.date2num(x)
        fit = np.polyfit(pdate.date2num(x), y, deg=1)
        plt.title(self.target_corp + " Stock Price")
        plt.xlabel("Time(day)")
        plt.ylabel("Price")

        ax.plot(x, fit[0] * pdate.date2num(x) + fit[1], color='red', linewidth=2)
        ax.scatter(pdate.date2num(x), y)

        plt.show()