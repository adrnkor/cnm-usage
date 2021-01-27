import auth

class Call:
    def __init__(self, host, client_id, client_secret, params):
        self.host = host
        self.token = auth.generate_api_session(host, client_id, client_secret)
        self.params = params

        def refreshToken(self):
            self.token = auth.generate_api_session(self.host, self.client_id, self.client_secret)

#def getPerformance


