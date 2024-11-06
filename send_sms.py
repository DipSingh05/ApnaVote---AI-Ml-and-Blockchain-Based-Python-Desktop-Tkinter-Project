from twilio.rest import Client

class SendSMS:
    def __init__(self):
        self.account_sid = 'paste your sid here'
        self.auth_token = 'paste your auth token here'

        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, body, phone):
        message = self.client.messages.create(
                      from_='paste your twillow mobile number here',
                      body=f"{body}",
                      to=f'+91{phone}'
                    )
        return message

if __name__ == "__main__":
    # sms = SendSMS()
    pass