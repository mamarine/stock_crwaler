import graph
import financecrawler

# target_corp = "yhoo"
target_corp = raw_input("Please enter target corp id: ")

# get data Yahoo finance
yahoo_finance_query = financecrawler.YahooFinanceCrawler(target_corp)
date_list, value_list = yahoo_finance_query.get_history_price(days=500)
stock_graph1 = graph.StockPriceTrend(date_list=date_list, price_list=value_list, target_corp=target_corp.upper())
stock_graph1.draw_with_linear_regression()

# get data from google finance
google_finance_query = financecrawler.GoogleFinanceCrawler(target_corp)
date_list, value_list = google_finance_query.get_history_price(days=350)
stock_graph2 = graph.StockPriceTrend(date_list=date_list, price_list=value_list, target_corp=target_corp.upper())
stock_graph2.draw_with_linear_regression()
