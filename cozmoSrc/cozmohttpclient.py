import requests

GET_URL = "https://ou5p106hw5.execute-api.us-east-1.amazonaws.com/dev/RivalrySkillFunction"

class CozmoHttpClient:
    
    def __init__(self):
        # TODO: debug here
        # self._conn = http.client.HTTPConnection(HOST_URL)
        pass

    def __del__(self):
        # self._conn.close()
        pass
        
    
    def getMessage(self):
        payload = {"action": "PROVOKE"}
        r = requests.get(GET_URL, params=payload)
        return r.text 

if __name__ == "__main__":
    client = CozmoHttpClient()
    print(client.getMessage())
    
