# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

class ViewTests(TestCase):

    def test_paths(self):
        c = Client()
        r = c.get('http://localhost:8000/')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/faq')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/contact')
        self.assertEqual(r.status_code, 200)

