
##Simple stats version 1
import readline

def stats( self ):
	
	if len(self.msg) == 4:
		self.send_chan("Usage: !stats <nick>")
	else:
		
		counter = 0

		try:
			chan = self.msg[2]	#trying if the 2nd parameter is given in stream data, if yes set it as a channel

		except IndexError:
			print("Error, something is wrong :(\r\n")

		logfile = "logs/"+chan+".log"

		try:
			with open(logfile): pass	#trying if such logfile exists or not
		except IOError:
			self.send_chan("I think i have not been on that channel yet")

		else:	
		
			LookingNick = self.msg[4].rstrip("\r\n")
		
			log = open(logfile, "r")
			line = log.readlines()
			log.close()

			for x in line:
				line2 = x.split(" ")
				if LookingNick in line2:
					counter += 1
			
			if counter is not False:
				self.send_chan(LookingNick + " has written " + str(counter) + " lines on this channel ("+ chan +")")
			else:
				self.send_chan("I don't remember seeing "+ LookingNick +" on this channel before ("+ chan +")")
		
			return
		
