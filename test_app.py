from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test client."""
        cls.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage."""
        res = self.client.get('/')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<form class="add-word">', html)

    def test_valid_word(self):
        """Test if a valid word is recognized."""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['R', 'S', 'L', 'P', 'A'],
                                           ['T', 'E', 'P', 'L', 'S'],
                                           ['A', 'A', 'O', 'O', 'B'],
                                           ['E', 'D', 'A', 'P', 'F'],
                                           ['A', 'B', 'C', 'D', 'E']]

            res = client.get('/check-word?word=apple')
            self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if an invalid word is recognized as not on the board."""
        with self.client as client:
            res = client.get('/check-word?word=impossible')
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if a non-English word is recognized as invalid."""
        res = self.client.get('/check-word?word=xyzyz')
        self.assertEqual(res.json['result'], 'not-word')