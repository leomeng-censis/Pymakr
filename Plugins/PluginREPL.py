import os
from PyQt5.QtCore import QObject, QCoreApplication

import UI
from E5Gui.E5Application import e5App
import Preferences
from REPL.Shell import ShellAssembly
from PluginPycomDevice import PycomDeviceServer

# Start-Of-Header
name = "REPL Console"
author = "Pycom"
autoactivate = True
deactivateable = False
version = "1.0.0"
className = "PluginREPL"
packageName = "PluginREPL"
shortDescription = "Implement the MicroPython console"
longDescription = "Allow users to use the MicroPython console from within Pymakr"


pyqtApi = 2
python2Compatible = True


class PluginREPL(QObject):
    def __init__(self,  ui):
        super(PluginREPL, self).__init__(ui)
        self.__ui = ui
        self.__oldShowEvent = self.__ui.showEvent
        self.__ui.showEvent = self.__onWindowLoad
        self.__windowLoaded = False

    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of None and activation status (boolean)
        """
        self.__active = True
        if self.__windowLoaded == True:
            self.__initializeShell()
        return None, True

    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        #todo: add won't use channel call
        pass

    def __onWindowLoad(self, event):
        # I must run only once
        self.__ui.showEvent = self.__oldShowEvent
        self.__ui.showEvent(event)

        if self.__active == True:
            self.__initializeShell()
        self.__windowLoaded = True

    def __initializeShell(self):
        self.__pds = PycomDeviceServer()

        self.__shell = ShellAssembly(self.__pds,
            e5App().getObject("ViewManager"))

        self.__ui.bottomSidebar.insertTab(0, self.__shell,
            UI.PixmapCache.getIcon("chip.png"), "Pycom Console")

        self.__ui.bottomSidebar.setTabText(1, self.tr("Local Shell"))

        self.__ui.bottomSidebar.setCurrentIndex(0)
