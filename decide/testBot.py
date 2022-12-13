import unittest
import requests
import json
import sys
print(sys.path)

API_DECIDE = 'http://127.0.0.1:8000/'

BOT_TOKEN = '5989598510:AAF2w-xJvPLmgJ3Tz4LsDu72DSBNqDIW1rE'

class TestMethods(unittest.TestCase):

    def test_login(self):
        headers = {"Content-type": "application/json",
        "Accept": "text/plain"}

        credentials = {"username": "admin", "password":"admin123"}
        r = requests.post(API_DECIDE + "authentication/login-bot/", credentials)
        self.assertEqual(r.status_code, 200)

    
    def test_get_voting(self):
        headers = {"Content-type": "application/json",
        "Accept": "text/plain"}      
        id=1
        r = requests.get(API_DECIDE + "voting/?id="+str(id)) 

        self.assertEqual(r.status_code,200)

    def test_vote_invalid_token(self):

        headers = {"Authorization": "Token 7241666026815e02759fde720bb11c40d01edf21"}
        vote = {
                "voting": 1,
                "voter": 1,
                "vote": { "a": "3", "b": "2" }
            }
        r = requests.post(API_DECIDE + "store/store-bot/", json=vote, headers=headers)

        self.assertEqual(r.status_code, 401)

    def test_vote(self):
        payload2={"voting_id":4,"voter_id":23, "a":"97072541147136128328540661818080002218518648328276205975804167680619755313209", "b":"21769321275085393559868179281746092492748370106520199365343124372970487687789"} 
        url = 'http://127.0.0.1:8000/store/store-bot/'
        headers = {"Authorization": "Token e36dd8a072cc071392b8dbecf3be4a5244567f9a"}
        files=[] 
        r = requests.request("POST", url, headers=headers, data=payload2, files=files) 
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()