# -*- coding: UTF-8 -*-
# Wammu - Phone manager
# Copyright (c) 2003 - 2006 Michal Čihař
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
Main Wammu application
'''

import wx
import sys
import Wammu.Main
import Wammu.Error
from Wammu.Paths import *
from Wammu.Utils import Str_ as _, StrConv

class WammuApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        self.SetAppName('Wammu')
        vendor = StrConv(u'Michal Čihař')
        if vendor.find('?') != -1:
            vendor = 'Michal Čihař'
        self.SetVendorName(vendor)

        wx.InitAllImageHandlers()

        frame = Wammu.Main.WammuFrame(None, -1)
        Wammu.Error.handlerparent = frame

        frame.Show(True)
        frame.PostInit()
        self.SetTopWindow(frame)

        # Return a success flag
        return True

def Run():
    try:
        sys.excepthook = Wammu.Error.Handler
    except:
        print _('Failed to set exception handler.')
    app = WammuApp()
    app.MainLoop()

