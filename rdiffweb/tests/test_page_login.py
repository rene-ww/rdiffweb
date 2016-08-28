#!/usr/bin/python
# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2015 Patrik Dufresne Service Logiciel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Dec 26, 2015

@author: Patrik Dufresne
"""

from __future__ import unicode_literals

import logging
import unittest

from rdiffweb.test import WebCase


class LoginPageTest(WebCase):

    def test_getpage(self):
        """
        Make sure the login page can be rendered without error.
        """
        self.getPage('/')
        self.assertStatus('200 OK')
        self.assertInBody('login')

    def test_getpage_with_plaintext(self):
        """
        Requesting plain text without being authenticated should return a 403
        error instead of login form.
        """
        self.getPage('/', headers=[("Accept", "text/plain")])
        self.assertStatus('403 Forbidden')

    def test_getpage_with_redirect_get(self):
        """
        Check encoding of redirect url when send using GET method.
        """
        #  Query the page without login-in
        self.getPage('/browse/' + self.REPO + '/DIR%EF%BF%BD/')
        self.assertStatus('200 OK')
        self.assertInBody(self.baseurl + '/browse/' + self.REPO + '/DIR%EF%BF%BD/')

    def test_getpage_with_broken_encoding(self):
        """
        Check encoding of redirect url when send using GET method.
        """
        #  Query the page without login-in
        self.getPage('/restore/' + self.REPO + '/Fichier%20avec%20non%20asci%20char%20%C9velyne%20M%E8re.txt?date=1454448640')
        self.assertStatus('200 OK')
        self.assertInBody(self.baseurl + '/restore/' + self.REPO + '/Fichier%20avec%20non%20asci%20char%20%C9velyne%20M%E8re.txt?date=1454448640')

    def test_getpage_with_redirect_post(self):
        """
        Check encoding of redirect url when send using POST method.
        """
        b = {'login': 'admin',
             'password': 'invalid',
             'redirect': self.baseurl + '/browse/' + self.REPO + '/DIR%EF%BF%BD/'}
        self.getPage('/login/', method='POST', body=b)
        self.assertStatus('200 OK')
        self.assertInBody('id="form-login"')
        self.assertInBody(self.baseurl + '/browse/' + self.REPO + '/DIR%EF%BF%BD/"')

    def test_getpage_with_querystring_redirect_get(self):
        """
        Check if unauthenticated users are redirect properly to login page.
        """
        self.getPage('/browse/' + self.REPO + '/?restore=T')
        self.assertStatus('200 OK')
        self.assertInBody(self.baseurl + '/browse/' + self.REPO + '/?restore=T')

        self.getPage('/restore/' + self.REPO + '?date=1414871387&usetar=T')
        self.assertStatus('200 OK')
        self.assertInBody(self.baseurl + '/restore/' + self.REPO + '?date=1414871387&amp;usetar=T')

    def test_getpage_with_redirection(self):
        """
        Check if redirect url is properly rendered in HTML.
        """
        b = {'login': 'admin',
             'password': 'admin123',
             'redirect': '/restore/' + self.REPO + '?date=1414871387&usetar=T'}
        self.getPage('/login/', method='POST', body=b)
        self.assertStatus('303 See Other')
        self.assertHeaderItemValue('Location', self.baseurl + '/restore/' + self.REPO + '?date=1414871387&usetar=T')

    def test_getpage_without_username(self):
        """
        Check if error 405 is raised when requesting /login without a username.
        """
        self.getPage('/login/', method='GET')
        self.assertStatus('303 See Other')
        self.assertHeaderItemValue('Location', self.baseurl + '/')

    def test_getpage_with_empty_password(self):
        """
        Check if authentication is failing without a password.
        """
        b = {'login': 'admin',
             'password': ''}
        self.getPage('/login/', method='POST', body=b)
        self.assertStatus('200 OK')
        self.assertInBody('Invalid username or password.')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
