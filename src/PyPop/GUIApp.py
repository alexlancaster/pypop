#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003. The Regents of the University of California (Regents)
# All Rights Reserved.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

import os

from threading import *
from wxPython.wx import *

ID_ABOUT=101
ID_OPEN_CONFIG=102
ID_OPEN_POP=103
ID_EXIT=110

from Main import Main, getConfigInstance

# Define notification event for thread completion
EVT_RESULT_ID = wxNewId()

def EVT_RESULT(win, func):
  win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wxPyEvent):
  """Simple event to carry arbitrary result data"""

  def __init__(self, data):
    wxPyEvent.__init__(self)
    self.SetEventType(EVT_RESULT_ID)
    self.data = data
    
# Thread class that executes processing
class WorkerThread(Thread):

  def __init__(self, notify_window):
    Thread.__init__(self)

    # if thread doesn't terminate, allows exit to work ?
    self.setDaemon(1)
    self._notify_window = notify_window
    self._want_abort = 0
    # This starts the thread running on creation, but you could
    # also make the GUI thread responsible for calling this
    self.start()

  def run(self):

    # This is the code executing in the new thread, code in the App
    # class periodically peeks at the abort variable

    config = getConfigInstance(self._notify_window.configFilename,
                               altpath = self._notify_window.altpath,
                               usage_message = "none")
    
    application = Main(config=config,
                       debugFlag = self._notify_window.debugFlag,
                       fileName = self._notify_window.popFilename,
                       datapath = self._notify_window.datapath,
                       thread = self)

    self._notify_window.SetStatusText("finished!, please select another file!")

    # Here's where the result would be returned (this is an
    # example fixed result of the number 10, but it could be
    # any Python object)
    wxPostEvent(self._notify_window,ResultEvent("done"))

  def abort(self):
    # Method for use by main thread to signal an abort
    self._want_abort = 1

class MainWindow(wxFrame):
  """Creates the main application window for PyPop.
  """
  def __init__(self,parent,id,title,
               datapath = None,
               altpath = None,
               debugFlag = 0):

    # set data, alt path
    self.datapath = datapath
    self.altpath = altpath
    self.debugFlag = debugFlag
    
    # default directory to start looking in
    self.dirname="."
    
    self.popFilename = None
    self.configFilename = os.path.join(self.dirname, 'config.ini')
    
    wxFrame.__init__(self,parent,-4, title, size = (400,200),
                     style=wxDEFAULT_FRAME_STYLE|
                     wxNO_FULL_REPAINT_ON_RESIZE)
    
    self.control = wxTextCtrl(self, 1, style=wxTE_MULTILINE)
    self.CreateStatusBar() # A Statusbar in the bottom of the window
    
    # Setting up the menu.
    filemenu= wxMenu()
    filemenu.Append(ID_ABOUT, "&About"," Information about this program")
    filemenu.Append(ID_OPEN_CONFIG, "&Config"," Select configuration file")
    filemenu.Append(ID_OPEN_POP, "&Population"," Select population file")
    filemenu.AppendSeparator()
    filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
    
    # Creating the menubar.
    menuBar = wxMenuBar()
    menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
    self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
    
    # attach the menu-event ID_ABOUT to the method self.OnAbout
    EVT_MENU(self, ID_ABOUT, self.OnAbout)
    
    # attach the menu-event ID_OPEN_CONFIG to the method self.OnConfig
    EVT_MENU(self, ID_OPEN_CONFIG, self.OnConfig)
    
    # attach the menu-event ID_OPEN_POP to the method self.OnPop
    EVT_MENU(self, ID_OPEN_POP, self.OnPop)
    
    # attach the menu-event ID_EXIT to the method self.OnExit
    EVT_MENU(self, ID_EXIT, self.OnExit)   
    
    # create "go" button
    b = wxButton(self, 10, "Run population...", wxPoint(20, 20))
    EVT_BUTTON(self, 10, self.OnRun)
    #b.SetBackgroundColour(wxBLUE)
    #b.SetForegroundColour(wxWHITE)
    b.SetDefault()
    
    # create "stop" button
    stop = wxButton(self, 20, 'Stop', wxPoint(20,60))
    EVT_BUTTON(self, 20, self.OnStop)
    
    # Set up event handler for any worker thread results
    EVT_RESULT(self,self.OnResult)
    
    # And indicate we don't have a worker thread yet
    self.worker = None
    
    self.Show(true)
    
  def OnAbout(self, event):
    d= wxMessageDialog(self, "PyPop: "
                       "PYthon for POPulation Genetics",
                       "About PyPop", wxOK)
    # Create a message dialog box
    d.ShowModal() # Shows it
    d.Destroy() # finally destroy it when finished.

  def OnExit(self, event):
    self.Close(true)  # Close the frame.

  def _onOpen(self, event, type="*.*"):
    dlg = wxFileDialog(self, "Choose a file", self.dirname,
                       "", type, wxOPEN)
    fullpath = None
    if dlg.ShowModal() == wxID_OK:
      filename=dlg.GetFilename()
      dirname=dlg.GetDirectory()
      
      fullpath = os.path.join(dirname,filename)
      
      #f=open(os.path.join(self.dirname,self.filename),'r')
      #self.control.SetValue(f.read())
      #f.close()
    dlg.Destroy()
    return fullpath
      
  def OnConfig(self, event):
    """ Select config file"""
    wildcard = "Configuration files (*.ini)|*.ini|" \
               "All files (*.*)|*.*"
    fullpath = self._onOpen(event,type=wildcard)
    
    if fullpath:
      self.configFilename = fullpath
      self.SetStatusText("config file:" + self.configFilename, 0)
          
  def OnPop(self, event):
    """ Select pop file"""
    wildcard = "Population files (*.pop)|*.pop|" \
               "All files (*.*)|*.*"
    fullpath = self._onOpen(event,type=wildcard)

    if fullpath:
      self.popFilename =  fullpath
      self.SetStatusText("pop file: " + self.popFilename, 0)

  def OnRun(self, event):

    if self.popFilename:
      # Trigger the worker thread unless it's already busy
      if not self.worker:
        self.SetStatusText("Running... this could take a while...", 0)
        self.worker = WorkerThread(self)

    else:
      self.SetStatusText("Please select a population, before running")

  def OnStop(self, event):
     # Flag the worker thread to stop if running
     if self.worker:
       self.SetStatusText('Trying to abort computation')
       self.worker.abort()

  def OnResult(self, event):
    if event.data is None:
      # Thread aborted (using our convention of None return)
      self.SetStatusText('Computation aborted')
    else:
      # Process results here
      self.SetStatusText('Computation Result: %s' % event.data)
    # In either event, the worker is done
    self.worker = None
