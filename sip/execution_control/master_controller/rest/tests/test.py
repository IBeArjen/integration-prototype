# -*- coding: utf-8 -*-
"""Unit tests for the Master Controller (REST variant).

Run with (from the rest directory):

    $ nose2

see <http://flask.pocoo.org/docs/0.12/testing/>

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import unittest
import json

from app import APP as app
from app import MC_STATES as states



class MasterControllerTests(unittest.TestCase):
    """Test of the Master Controller"""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        """Executed after each test."""
        pass

    def test_default(self):
        """Test of the default route"""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.mimetype,
                         'application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['module'], 'Master Controller')
        self.assertTrue(data['state'] in states)
