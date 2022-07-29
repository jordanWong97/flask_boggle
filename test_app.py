from unittest import TestCase

from app import app, games
from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board"', html)

            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            json = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(json['board'], list)
            self.assertIsInstance(json['gameId'], str)
            self.assertIsInstance(games[json['gameId']], BoggleGame)
            # write a test for this route

    def test_api_score_word(self):
        """Test checking word on board"""

        with self.client as client:
            new_game_resp = client.post('/api/new-game')

            new_game_json = new_game_resp.get_json()

            gameId = new_game_json['gameId']

            games[gameId].board = [['C', 'A', 'T'],
                                   ['E', 'F', 'G'],
                                   ['H', 'I', 'J']]

            score_resp = client.post('/api/score-word',
                                     json={
                                         'gameId': gameId,
                                         'word': 'CAT'
                                     })
            score_resp_json = score_resp.get_json()
            self.assertEqual(score_resp_json['result'], 'ok')

            score_resp = client.post('/api/score-word',
                                     json={
                                         'gameId': gameId,
                                         'word': 'RAT'
                                     })
            score_resp_json = score_resp.get_json()
            self.assertEqual(score_resp_json['result'], 'not-on-board')

            score_resp = client.post('/api/score-word',
                                     json={
                                         'gameId': gameId,
                                         'word': 'JBLPL'
                                     })
            score_resp_json = score_resp.get_json()
            self.assertEqual(score_resp_json['result'], 'not-word')