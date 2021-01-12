# coding=utf-8


class OkexAPIException(Exception):

    def __init__(self, response):
        print(response.text + ', ' + str(response.status_code))
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Okex: {}'.format(response.text)
        else:
            if "code" in json_res.keys() and "msg" in json_res.keys():
                self