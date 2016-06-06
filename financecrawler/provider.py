
class ContainProvider:
    URL = ""

    def __init__(self, company_id="", parameter_string=""):
        self.__parameter = parameter_string
        self.__company = company_id
        self.request_url = self.URL + self.__company + self.__parameter
        self.date_list = []
        self.value_list = []

    def get_history_price(self, days=200):
        raise NotImplementedError()