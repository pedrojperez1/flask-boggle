import json
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_root_route(self):
        with app.test_client() as client:

            res = client.get('/')
            html = res.get_data(as_text=True)

            # check status code
            self.assertEqual(res.status_code, 200)
            # check HTML response
            self.assertIn('<h3>Time left: <span id="timer-msg"></span></h3>', html)
            self.assertIn('<h4 id="scoreboard-msg"></h4>', html)
            # check session vars
            self.assertEqual(len(session['board']), 5)


    def test_guess_route(self):
        with app.test_client() as client:
            client.get('/') # make req to root first to imitate user landing at root first
            result_list = {'not-on-board', 'not-word', 'ok'}

            res_1 = client.post('/guess', data='{"guess": "word"}')
            res_2 = client.post('/guess', data='{"guess": "1234"}')
            res_3 = client.post('/guess', data='{"guess": ""}')
            
            self.assertEqual(res_1.status_code, 200)
            self.assertIn(json.loads(res_1.get_data())['result'] , result_list)
            self.assertEqual(res_2.status_code, 200)
            self.assertIn(json.loads(res_2.get_data())['result'] , result_list)
            self.assertEqual(res_3.status_code, 200)
            self.assertIn(json.loads(res_3.get_data())['result'] , result_list)

    
    def test_send_score_route(self):
        with app.test_client() as client:
            client.get('/')
            session['hiscore'] = 20

            # check user gets redirected and new hiscore is updated in session
            res_1 = client.post('/send-score', data='{"score": 30}')
            self.assertEqual(res_1.status_code, 302)
            self.assertEqual(session['hiscore'], 30)
            # check user gets redirected and hiscore remains the same
            res_2 = client.post('/send-score', data='{"score": -10}')
            self.assertEqual(res_2.status_code, 302)
            self.assertEqual(session['hiscore'], 30)
            # check we get bad request response for passing a string
            res_3 = client.post('/send-score', data='{"score": "hamster"}')
            self.assertEqual(res_3.status_code, 400)


            

