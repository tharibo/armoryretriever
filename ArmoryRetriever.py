#!/usr/bin/env python

"""Retrieve your WoW character on the Armory"""

import sys
import httplib
from PyQt4 import QtCore, QtGui, uic


def retrieveCharacterPage( pCharacterName, pRealmName, pContinentName ):
	"""Opens a connection to the armory and retrieve the given character page"""
	prefix = "www"
	if (pContinentName == "EU") :
		prefix = "eu"
	
	connection = httplib.HTTPConnection( prefix + ".wowarmory.com" )
	# TODO: Transform names to encode special characters
	connection.request( "GET", "/character-sheet.xml?r=%s&n=%s" % ( pRealmName, pCharacterName ) )
	response = connection.getresponse()
	if (response.status == 200 and response.reason == "OK"):
		data = response.read()
		return data

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	dialog = uic.loadUi("ArmoryOptionDialog.ui")

	if (dialog.exec_() == QtGui.QDialog.Accepted):
		characterPage = retrieveCharacterPage( dialog.mCharacterName.text(),
											   dialog.mRealmName.text(),
											   dialog.mContinent.currentText() )

	displayer = QtGui.QTextEdit()
	displayer.setReadOnly( True )
	displayer.setPlainText( characterPage )
	displayer.show()

	app.setQuitOnLastWindowClosed( True );
	sys.exit(app.exec_())
