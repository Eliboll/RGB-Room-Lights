#https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#This guide helped navigate creating the API key and using the cell commmands

import gspread,time,requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def betterget(command): #Sometimes individual commands fail. This tries 100 times to send the command before failing.
	for i in range(100):
		try:
			requests.get(command) #sends command
			break
		except: #Catches for the device being unreachable or other common errors with sending a command
			print("command unrecieveable")

def Tprint(message): #Prints to the console message with a time stamp added
	now = datetime.now()
	print("[{0}] ".format(now.strftime("%H:%M:%S")) + message)


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('monitary-224103-08aa40d6212d.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1QpCyhEw_BaMp4GApFhQItKvO0WCoLcikXKggYy6rNaE/edit#gid=0").sheet1

ip_address = "http://192.168.1.70" # adress has a DHCP reservation.

sheet.update_cell(1,1,'') # Clears spreadsheet's maininformation cell

text_to_color = open("lookup.txt","r") #txt file containing names of colors and translates them into RGB values. This is done to make it easier to add colors and speach to text translation
text_to_color_list_raw = text_to_color.read().split("\n") 
text_to_color.close()

errors =0
lasterror=0

text_to_color_list = [] # initalizes the list of text translated colors
for line in text_to_color_list_raw: #goes through the contents of lookup.txt  and creates a list full of color values usable by the code
	line = line.split(",")
	if line == [""] or line == [" "] or line ==[]: #accounts for by bad habit of leaving an enter at the end of the file 
		continue
	text_to_color_list.append(line)

bright_scale =5 #Creates variable used to describe the brightness level
wait = 5 #defines how long the program should wait between checking the spreadsheet

def main():
	while True:
		try:
			time.sleep(wait)
			client.login()  # Sometimes google no longer accepts the token so this makes sure that a valid token is being used
			command = sheet.cell(1,1).value.lower() #Gets the contents of the spreadsheet 
			if command =="": #jumps back to the time.sleep at the top avoiding the rest of the program
				continue
			Tprint("RECIEVED COMMAND: "+ command) 
			for color in text_to_color_list: #checks list of colors for the command
				if command.find(color[0]) >=0 and len(color) >=0: #find is used because if the string (make it green) is given, it can see to make it green rather than looking for command==green
					Tprint("SET COLOR TO " + str(color[0])) #color [0] is the name of the color, color[1] would be the r value, etc
					betterget(ip_address + "/com/static/{0}{1}{2}".format(color[1],color[2],color[3])) # sends command to esp8266 to set the color
					sheet.update_cell(1,1,"") #clears the sheet of the command so it doesn't try and do it again
					continue #goes back to the time.sleep()
			if command.find("brighter") >=0: 
				if bright_scale ==10:#refuses to make it any brighter
					Tprint("AT MAX BIRGHTNESS")
				else:
					bright_scale +=1 #increases brightness counter
					betterget(ip_address + "/bright/{0:0=3d}".format(bright_scale*10)) #sends command to make the change the brightness and formats it in a way the server will accept
					Tprint("RAISED BRIGHTNESS TO " + str(bright_scale))
				sheet.update_cell(1,1,"") #goes back to the time.sleep() function
				continue
			if command.find("darker") >=0: #basically same as the above section for brighter
				if bright_scale ==0:
					print("AT MINIMUM BIRGHTNESS")
				else:
					bright_scale -=1
					betterget(ip_address + "/bright/{0:0=3d}".format(bright_scale*10))
					Tprint("LOWERED BIRGHTNESS TO " + str(bright_scale))
				sheet.update_cell(1,1,"")
				continue
			if command.find("rainbow cycle") >=0: # translates text to command
				betterget(ip_address + "/com/improvedrainbow")
				Tprint("SET MODE TO RAINBOW CYCLE")
				sheet.update_cell(1,1,"")
				continue
			elif command.find("rainbow") >=0: #translates text to command
				betterget(ip_address + "/com/rainbows")
				Tprint("SET MODE TO RAINBOW")
				sheet.update_cell(1,1,"")
				continue
		except KeyboardInterrupt: # allows ctrl C to be used with the except
			Tprint("User has exiting program. Shutting down")
			
		except: # keeps program from continuing after it has clearly stopped functioning and continously runs into errors
			Tprint("A Fatal Error has occured!")
			errors +=1 # incriments error counter
			if lasterror==0:
				Tprint("Recovering in 1 minute")
				lasterror = time.time()
				time.sleep(60)  #alllows time to see if the problem fixes itself
			else:
				if (time.time()-lasterror < 100):
					Tprint("2 errors have occured within 100 seconds. Exiting program.")
					exit()
				else:
					lasterror = time.time()
					time.sleep(60)


if __name__ == "__main__":
	main()