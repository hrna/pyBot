##Logger daemon version 2

from time import gmtime, strftime
import time
import os
import re
import sys_error_log

def logger_daemon ( self ):

	if os.path.exists(self.config["log-path"]) == True:	#Checking if log-path in config is valid and exists
	
		if len(self.msg) >= 4:

			if self.msg[1] in self.irc_codes:		#No logging if matching code received from the server
				return
			else:
				brackets = self.config["TimestampBrackets"].split(",") #Looking brackets from the config file
				usertxt = ""
				chan = self.msg[2]

				for i in range(3, len(self.msg)):	#Creating the string of text starting from the user output in console
					usertxt += self.msg[i]+" "

				if chan[0] == "#":
					log = self.config["log-path"]+chan+".log"
					logline = "{0}{1}{2} {3} @ {4} >> {5}".format( #1-3 timestamp with brackets, 3 nick, 4 channel, 5 the message
						brackets[0], strftime(self.config["timeformat"]), brackets[1], self.get_nick(), chan, usertxt.rstrip(" ")[1:])

					with open(log, "a") as log: #Opening the log and appending the latest result
						log.write(logline)
						log.flush()


	else:
		try:
			self.errormsg = "[NOTICE]-[logger_daemon] Cannot find existing folder for logs, creating: {0}".format(self.config["log-path"])
			sys_error_log.log( self )
			if self.config["debug"] == "true": #If the path set in config doesn't exist, create one
				print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
			os.mkdir(self.config["log-path"])
		except Exception as e:
			self.errormsg = "[ERROR]-[logger_daemon] logger_daemon() stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

		
	

