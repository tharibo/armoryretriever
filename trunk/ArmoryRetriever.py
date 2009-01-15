#!/usr/bin/env python

"""Retrieve your WoW character on the Armory"""

import sys
import urllib, urllib2
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

	url = 'http://www.python.org/fish.html'
	#url = urllib.quote( 'http://%s.wowarmory.com/character-sheet.xml?r=%s&n=%s'
	#		% ( prefix, pRealmName.encode('UTF8'), pCharacterName.encode('UTF8') ), '/:&?=' )
	print url

	userAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5";
	headers = { "User-Agent"  : userAgent }

	request = urllib2.Request( url, headers=headers )
	handle = urllib2.urlopen( request )

	return handle.read()

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

		try:
			characterPage = retrieveCharacterPage( unicode( dialog.mCharacterName.text() ),
												   unicode( dialog.mRealmName.text() ),
												   dialog.mContinent.currentText(),
												   proxySettings )
		except urllib2.URLError, e:
			QtGui.QMessageBox.critical( None, "Armory Retriever",
					"Your connection seems broken. Please check your internet/proxy settings.",
					QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton )
		except urllib2.HTTPError, e:
			QtGui.QMessageBox.critical( None, "Armory Retriever",
					"The Armory could'nt fullfill the request. Please try later. Error was %s" % (e.code),
					QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton )

		else:
			displayer = QtGui.QTextEdit()
			displayer.setReadOnly( True )
			displayer.setPlainText( characterPage )
			displayer.show()

			app.setQuitOnLastWindowClosed( True )
			sys.exit( app.exec_() )
