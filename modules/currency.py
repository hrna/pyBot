import urllib.parse
from bs4 import BeautifulSoup
import re
import syscmd

def currency( self ):
	
	amount = 1
	frm = "eur"
	to = "usd"
	
	if len(self.msg) < 7:
		self.send_chan("Usage: !currency <amount> <from> <to>")
	else:
		try:
			amount = float(self.msg[4])
		except ValueError:
			pass
		frm = self.msg[5]
		to = self.msg[6]
	if isinstance( amount, float ):
		frm = urllib.parse.quote(frm)
		to = urllib.parse.quote(to)
		url = "https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(amount, frm, to)
		html = syscmd.getHtml(self, url, True)								
		
	try:
		soup = BeautifulSoup(html)
		result = soup.findAll("div", {"id" : "currency_converter_result"})
		result = "{0}".format(result[0])
		trimmed = re.sub('<[^<]+?>', '', result)
		self.send_chan(trimmed)
		
	except:
		pass
		