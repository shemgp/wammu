# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Wammu - Phone manager
Locales initialisation and gettext wrapper
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2003 - 2010 Michal Čihař

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 2 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os
import gettext
import locale
import codecs
import __builtin__
import wx
import sys


LOCAL_LOCALE_PATH = os.path.join('build', 'share', 'locale')
LOCALE_PATH = None

FALLBACK_LOCALE_CHARSET = 'iso-8859-1'

# Determine "correct" character set
try:
    # works only in python > 2.3
    LOCALE_CHARSET = locale.getpreferredencoding()
except:
    try:
        LOCALE_CHARSET = locale.getdefaultlocale()[1]
    except:
        try:
            LOCALE_CHARSET = sys.getdefaultencoding()
        except:
            LOCALE_CHARSET = FALLBACK_LOCALE_CHARSET
if LOCALE_CHARSET in [None, 'ANSI_X3.4-1968']:
    LOCALE_CHARSET = FALLBACK_LOCALE_CHARSET

try:
    CONSOLE_CHARSET = sys.stdout.encoding
except AttributeError:
    CONSOLE_CHARSET = None
if CONSOLE_CHARSET is None:
    CONSOLE_CHARSET = LOCALE_CHARSET
CONSOLE_ENCODER = codecs.getencoder(CONSOLE_CHARSET)

def ConsoleStrConv(txt):
    """
    This function coverts something (txt) to string form usable on console.
    """
    try:
        if type(txt) == type(''):
            return txt
        if type(txt) == type(u''):
            return str(CONSOLE_ENCODER(txt, 'replace')[0])
        return str(txt)
    except UnicodeEncodeError:
        return '???'

def StrConv(txt):
    """
    This function coverts something (txt) to string form usable by wxPython. There
    is problem that in default configuration in most distros (maybe all) default
    encoding for unicode objects is ascii. This leads to exception when converting
    something different than ascii. And this exception is not catched inside
    wxPython and leads to segfault.

    So if wxPython supports unicode, we give it unicode, otherwise locale
    dependant text.
    """
    try:
        if type(txt) == type(u''):
            return txt
        if type(txt) == type(''):
            return unicode(txt, LOCALE_CHARSET)
        return str(txt)
    except UnicodeEncodeError:
        return '???'

# detect html charset
HTML_CHARSET = LOCALE_CHARSET

# prepare html encoder
HTML_ENCODER = codecs.getencoder(HTML_CHARSET)

def HtmlStrConv(txt):
    """
    This function coverts something (txt) to string form usable by wxPython
    html widget. There is problem that in default configuration in most distros
    (maybe all) default encoding for unicode objects is ascii. This leads to
    exception when converting something different than ascii. And this
    exception is not catched inside wxPython and leads to segfault.

    So if wxPython supports unicode, we give it unicode, otherwise locale
    dependant text.
    """
    try:
        if type(txt) == type(u''):
            return txt
        if type(txt) == type(''):
            return unicode(txt, LOCALE_CHARSET)
        return str(txt)
    except UnicodeEncodeError:
        return '???'

def UnicodeConv(txt):
    """
    This function coverts something (txt) to string form usable by wxPython. There
    is problem that in default configuration in most distros (maybe all) default
    encoding for unicode objects is ascii. This leads to exception when converting
    something different than ascii. And this exception is not catched inside
    wxPython and leads to segfault.

    So if wxPython supports unicode, we give it unicode, otherwise locale
    dependant text.
    """
    try:
        if type(txt) == type(u''):
            return txt
        if type(txt) == type(''):
            return unicode(txt, LOCALE_CHARSET)
        return unicode(str(txt), LOCALE_CHARSET)
    except UnicodeEncodeError:
        return unicode('???')

class WammuTranslations(gettext.GNUTranslations):
    '''
    Wrapper for gettext returning always "correct" charset.
    '''
    def ngettext(self, msgid1, msgid2, n):
        result = gettext.GNUTranslations.ngettext(self, msgid1, msgid2, n)
        if type(result) == type(''):
            return unicode(result, 'utf-8')
        else:
            return result

    def ugettext(self, message):
        result = gettext.GNUTranslations.gettext(self, message)
        if type(result) == type(''):
            return unicode(result, 'utf-8')
        else:
            return result

    def gettext(self, message):
        return self.ugettext(message)

    def hgettext(self, message):
        return self.ugettext(message)

def Init():
    '''
    Initialises gettext for wammu domain and installs global function _,
    which handles translations.
    '''
    global LOCALE_PATH
    switch = False
    if (os.path.exists('setup.py') and
        os.path.exists(LOCAL_LOCALE_PATH) and
        os.path.exists(
            os.path.join('Wammu', '__init__.py')
            )):
        LOCALE_PATH = LOCAL_LOCALE_PATH
        switch = True
    Install()
    if switch:
        print ConsoleStrConv(_('Automatically switched to local locales.'))

def UseLocal():
    '''
    Use locales from current build dir.
    '''
    global LOCALE_PATH
    LOCALE_PATH = LOCAL_LOCALE_PATH
    Install()

def ngettext(msgid1, msgid2, n):
    if n == 1:
        return msgid1
    else:
        return msgid2

def ugettext(message):
    return message

def lgettext(message):
    return message

def hgettext(message):
    return message

def Install():
    global LOCALE_PATH, ngettext, ugettext, lgettext, hgettext
    try:
        trans = gettext.translation('wammu',
            class_ = WammuTranslations,
            localedir = LOCALE_PATH)
        __builtin__.__dict__['_'] = trans.gettext
        ngettext = trans.ngettext
        ugettext = trans.ugettext
        lgettext = trans.lgettext
        hgettext = trans.hgettext
    except IOError:
        # No translation found for current locale
        __builtin__.__dict__['_'] = ugettext
        pass
