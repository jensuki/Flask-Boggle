from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def setUp(self):
        """Set up test client & session data"""
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session['board'] = [['R', 'S', 'L', 'P', 'A'],
                                ['T', 'E', 'P', 'L', 'S'],
                                ['A', 'A', 'O', 'O', 'B'],
                                ['E', 'D', 'A', 'P', 'F'],
                                ['A', 'B', 'C', 'D', 'E']]

    def test_homepage(self):
        """Test home page"""
        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form class="add-word">', html)
            self.assertIn('<div class="letter">', html)
            self.assertTrue(session.get('board'))

    def test_valid_word(self):
        """Test if the word is valid"""
        with self.client:
            response = self.client.get('/check-word?word=apple')
            self.assertEqual(response.json['result'],'ok')
            self.assertIn('ok', response.json.values())

    def test_invalid_word(self):
        """Test is word is valid but not on board"""
        with self.client as client:
            response = client.get('/check-word?word=dictionary')
            self.assertEqual(response.json['result'], 'not-on-board')
            self.assertIn('not-on-board', response.json.values())

    def test_non_english_word(self):
        """Test if word is not an English word"""
        with self.client as client:
            response = client.get('/check-word?word=xhaskgh')
            self.assertEqual(response.json['result'], 'not-word')
            self.assertIn('not-word', response.json.values())

    def test_gameboard(self):
        with self.client.session_transaction() as session:
            board = session['board']
            self.assertEqual(len(board), 5)
            self.assertEqual(len(board[0]), 5)

    