# TODO : calls in database
import json
from twilio.rest import Client


class CallProvider:
    path_configurations = "configurations/configurations.json"
    account_sid = authentication_token = client_numbers = url_voice = provider_number = None

    def __init__(self):
        self.setConfigurations()

    # permit to alert the client
    def doCall(self):
        client = Client(self.account_sid, self.authentication_token)

        for client_number in self.client_numbers:
            client.calls.create(
                url=self.url_voice,
                to=client_number,
                from_=self.provider_number
            )

    def setConfigurations(self):
        configs = self.getConfigurations()
        self.client_numbers = configs[0]
        self.provider_number = configs[1]
        self.url_voice = configs[2]
        self.account_sid = configs[3]
        self.authentication_token = configs[4]

    def getConfigurations(self):
        with open(self.path_configurations, "r") as read_file:
            return list(json.load(read_file).values())
