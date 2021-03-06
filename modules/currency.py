import urllib.parse
from bs4 import BeautifulSoup
from decimal import Decimal
import re
import syscmd
import sysErrorLog

def currency( self ):

	if len(self.msg) < 7:
		self.send_chan("Usage: !currency <amount> <from> <to>")
	if len(self.msg) == 7:
		try:
			amount = Decimal(re.sub(",", ".", self.msg[4])).quantize(Decimal("0.00"))
		except Exception as e:
			amount = Decimal(1.00)
		frm = self.msg[5].upper()
		to = self.msg[6].upper()

		## If first value is float and currencies are valid
		if isinstance( amount, Decimal ) and syscmd.checkCurrency( frm, to):
			frm = urllib.parse.quote(frm)
			to = urllib.parse.quote(to)
			url = "https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(amount, frm, to)
			html = syscmd.getHtml(self, url, True)
			try:
				soup = BeautifulSoup(html)
				result = soup.findAll("span", {"class" : "bld"})
				## If there's a result, then send it to the chan
				if result:
					result = "{0} {1} = {2}".format(amount, frm.upper(), result[0])
					trimmed = re.sub('<[^<]+?>', '', result)
					self.send_chan(trimmed)
				else:
					self.send_chan("Google failed to convert your request :(")		
			except Exception as e:
				self.errormsg = "[ERROR]-[Currency] stating: {0}".format(e)
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"]:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			self.send_chan("Usage: !currency <amount> <from> <to>")	

		
