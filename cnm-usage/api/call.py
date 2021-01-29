import auth
import requests

class Call:
    def __init__(self, host, client_id, client_secret, params):
        self.host = host
        self.token = auth.generate_api_session(host, client_id, client_secret)
        self.params = params

        self.headers = {
            'Authorization': 'Bearer {}'.format(self.token),
        }

        def refreshToken(self):
            self.token = auth.generate_api_session(self.host, self.client_id, self.client_secret)

        def getPerformance(self):
            api_url = 'https://{}/api/v1/devices/performance'.format(self.host)

            r = requests.get(api_url, self.headers, self.params, verify=False)
            auth.check_http_return("API", api_url, r.status_code, r)
            return r.json()



