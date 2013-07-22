import time
import datetime
import dateutil.relativedelta
from time import gmtime, strftime
import re

def seen ( self ):
	
	if self.config["logging"] == True:
		if len(self.msg) >= 5:
			try:
				seendb = self.config["log-path"]+"seen.db"
				with open(seendb): pass
			except Exception as e:
				if self.config["debug"] == "true":
					print(e)
			else:
				nick 		= self.msg[4].rstrip("\r\n")
				nick_in_line 	= 0
				
				
				with open(seendb, "r", encoding="UTF-8") as db:
					for line in db:
						if re.search("\\b"+nick+":\\b", line, flags=re.IGNORECASE):
							spl = line.split(":")
							name = spl[0]
							dbtime = spl[1].rstrip("\r\n")
							dbconvert = datetime.datetime.fromtimestamp(int(dbtime)).strftime('[%d.%m.%Y // %H:%M:%S]')
							past = datetime.datetime.fromtimestamp(int(dbtime))
							current = datetime.datetime.fromtimestamp(int(time.time()))
							diff = dateutil.relativedelta.relativedelta(current, past)
							output = ""
							if diff.hours == False:
								#empty... ideas?
							else:
								hours = str(diff.hours)+" hours "
								output += hours

							if diff.minutes == False:
								#empty... ideas?
							else:
								minutes = str(diff.minutes)+" minutes "
								output += minutes

							if diff.seconds == False:
								seconds = "0 seconds "
								output += seconds
							else:
								seconds = str(diff.seconds)+" seconds "
								output += seconds
							nick_in_line = 1
							
				if nick_in_line == 1:
					self.send_chan(name+" spoke last time: "+dbconvert+
						" which is exactly "+output+"ago.")
				else:
					self.send_chan("I have never logged "+nick+" while being on any channel")

		else:
			self.send_chan("Usage: !seen <nick>")
	else:
		self.send_chan("Logging must be enabled from config in order to use this module")
					
