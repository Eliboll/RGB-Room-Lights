import gspread,time,requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
def betterget(command):
	for i in range(100):
		try:
			requests.get(command)
			break
		except:
			print("command unrecieveable")

def Tprint(message):
	now = datetime.now()
	print("[{0}] ".format(now.strftime("%H:%M:%S")) + message)


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('monitary-224103-08aa40d6212d.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1QpCyhEw_BaMp4GApFhQItKvO0WCoLcikXKggYy6rNaE/edit#gid=0").sheet1

ip_address = "http://192.168.1.70"

sheet.update_cell(1,1,'')

text_to_color = open("lookup.txt","r")
text_to_color_list_raw = text_to_color.read().split("\n")
text_to_color.close()

errors =0
lasterror=0

text_to_color_list = []
for line in text_to_color_list_raw:
	line = line.split(",")
	if line == [""] or line == [" "] or line ==[]:
		continue
	text_to_color_list.append(line)

bright_scale =5
wait = 5

while True:
	try:
		time.sleep(wait)
		client.login()
		command = sheet.cell(1,1).value.lower()
		if command =="":
			continue
		Tprint("RECIEVED COMMAND: "+ command)
		for color in text_to_color_list:
			if command.find(color[0]) >=0 and len(color) >=0:
				Tprint("SET COLOR TO " + str(color[0]))
				betterget(ip_address + "/com/static/{0}{1}{2}".format(color[1],color[2],color[3]))
				sheet.update_cell(1,1,"")
				continue
		if command.find("brighter") >=0:
			if bright_scale ==10:
				Tprint("AT MAX BIRGHTNESS")
			else:
				bright_scale +=1
				betterget(ip_address + "/bright/{0:0=3d}".format(bright_scale*10))
				Tprint("RAISED BRIGHTNESS TO " + str(bright_scale))
			sheet.update_cell(1,1,"")
		if command.find("darker") >=0:
			if bright_scale ==0:
				print("AT MINIMUM BIRGHTNESS")
			else:
				bright_scale -=1
				betterget(ip_address + "/bright/{0:0=3d}".format(bright_scale*10))
				Tprint("LOWERED BIRGHTNESS TO " + str(bright_scale))
			sheet.update_cell(1,1,"")
		if command.find("rainbow cycle") >=0:
			betterget(ip_address + "/com/improvedrainbow")
			Tprint("SET MODE TO RAINBOW CYCLE")
			sheet.update_cell(1,1,"")
		elif command.find("rainbow") >=0:
			betterget(ip_address + "/com/rainbows")
			Tprint("SET MODE TO RAINBOW")
			sheet.update_cell(1,1,"")
	except KeyboardInterrupt:
		Tprint("User has exiting program. Shutting down")
		
	except:
		Tprint("A Fatal Error has occured!")
		errors +=1
		if lasterror==0:
			Tprint("Recovering in 1 minute")
			time.sleep(60)
		else:
			if (time.time()-lasterror < 100):
				Tprint("2 errors have occured within 100 seconds. Exiting program.")
				exit()
			else:
				lasterror = time.time()
				time.sleep(60)