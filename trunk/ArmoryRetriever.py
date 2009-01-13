#!/usr/bin/env python

"""Retrieve your WoW character on the Armory"""

import sys
import urllib2
from PyQt4 import QtCore, QtGui, uic


def retrieveCharacterPage( pCharacterName, pRealmName, pContinentName, pProxyInfo ):
	"""Opens a connection to the armory and retrieve the given character page"""

	# Proxy info ?
	if len( pProxyInfo ) > 0 :
		# build a new opener that uses a proxy requiring authorization
		proxySupport = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % pProxyInfo})
		opener = urllib2.build_opener(proxySupport, urllib2.HTTPHandler)
		# install opener
		urllib2.install_opener(opener)

	# Check zone
	prefix = "www"
	if (pContinentName == "EU") :
		prefix = "eu"

	f = urllib2.urlopen( "http://%s.wowarmory.com/character-sheet.xml?r=%s&n=%s"
			% ( prefix, pRealmName, pCharacterName ) )

	return f.read()

#	connection = httplib.HTTPConnection(
#			"http://proxycs-toulouse.si.c-s.fr", "8080" )
#	connection.connect()
#	# TODO: Transform names to encode special characters
#	connection.request( "GET", "%s.wowarmory.com/character-sheet.xml?r=%s&n=%s"
#			% ( prefix, pRealmName, pCharacterName ) )
#	response = connection.getresponse()
#	if (response.status == 200 and response.reason == "OK"):
#		data = response.read()
#		return data

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	dialog = uic.loadUi("ArmoryOptionDialog.ui")

	if dialog.exec_() == QtGui.QDialog.Accepted :
		proxySettings = {}
		if dialog.mProxySettings.isChecked() :
			proxySettings = { 'user' : dialog.mProxyUser.text(),
							  'pass' : dialog.mProxyPassword.text(),
							  'host' : dialog.mProxyHost.text(),
							  'port' : dialog.mProxyPort.text().toInt()[0] }
		characterPage = retrieveCharacterPage( dialog.mCharacterName.text(),
											   dialog.mRealmName.text(),
											   dialog.mContinent.currentText(),
											   proxySettings )

	displayer = QtGui.QTextEdit()
	displayer.setReadOnly( True )
	displayer.setPlainText( characterPage )
	displayer.show()

	app.setQuitOnLastWindowClosed( True );
	sys.exit(app.exec_())
