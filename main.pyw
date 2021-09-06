import tkinter as tk
from tkinter import *
from tkinter import Frame
from tkinter import StringVar
from tkinter import ttk
from tkinter import colorchooser
import requests
import _thread as thread

modes = ("Static","Rainbow","Rainbow Cycle","Christmas blink",) #All different modes that can be chosen

default_ip="70" #Default static ip as in 192.18.1. format
default_bright="50"
window =tk.Tk(className="Room Lights") #Creates Tkinter pop up

subinfo = Frame(window) #Defines the frame where everything will be put in

color = ((0,0,0), '#000000') #Creates tuple used by the colorchoser method of tkinter that can be accessed to set color
colorbtn=None # Sets the default color to a none

ip=None 
GlobalBright=int(default_bright) # Changed to int because default_bright needs to be a string to be put in the text box
def main():
	global window,ip,subinfo,GlobalBright # Brings these global variables into the scope of the function
	window.geometry("300x200") #Sets the size of the window

	ttk.Label(window,text="IP address: 192.168.1.").grid(column=0,row=0) # Creates the first line in the program to be able change the default ip
	uservar = StringVar() # Creates a StringVar so that I can access the contents of the boc later
	user_ip= ttk.Entry(window,textvariable=uservar,width=3) # Creates the actual box
	uservar.set(default_ip) # Sets the contents of the box to the default ip
	user_ip.grid(column=1,row=0,sticky="W") # Puts the box in the grid system and left justifies it

	ttk.Label(window,text="Brightness:").grid(column=0,row=1) # Creates a label for brightness
	brightness= StringVar() #Creates a stringvar so the value can be accessed
	user_Bright = ttk.Entry(window,textvariable=brightness,width=3) # creates the box the user enters the brightness into
	brightness.set(default_bright) # sets default value for the box
	user_Bright.grid(column=1,row=1,sticky="W") # Left justifies the box

	ttk.Label(window,text="Select Mode :").grid(column=0,row=3) # Creates the lable for the selection box

	programvar = StringVar() # Creates variable for the selected item in the selction box
	program = tk.ttk.Combobox(window,textvariable=programvar,justify = "left") # creates the combobox (aka selection box)
	program['values'] = modes # Sets the contents of the combobox as the modes defined at the begining
	program.grid(row=3,column=1) # Places it
	program.state(["readonly"]) # sets the comboBox to read only
	program.bind("<<ComboboxSelected>>",callback) # Links the function Callback to the combobox

	ip=uservar # assignes the value the user gave to the global variable
	GlobalBright=brightness # sets the user defined brightness as the global brightness
	subinfo.grid(column=0,row=4) # places the subInfo box below everything else
	window.mainloop() # starts the window
	input() #Keeps the program from immediatly exiting

def callback(eventObject):
	global window,ip,color,subinfo,colorbtn,GlobalBright # Localizes global variables
	for widget in subinfo.winfo_children(): # This loop removes the contents of the subInfo frame 
		print(widget)
		widget.destroy()
		print("destroyed")

	event = eventObject.widget.get() #Defines as a string what the comboBox selection is
	ip_address = "http://192.168.1.{0}".format(ip.get()) # creates the Ip used in the communication with the server
	threaded_betterget("{0}/bright/{1}".format(ip_address,GlobalBright.get())) # Sets the brightness everytime a selection change occurs
	if (event == "Static"): #Checks and sees if the mode is the static mode
		ttk.Label(subinfo,text="Color: ").grid(column=0,row=0) # Creates a  label for the color button
		colorbtn = tk.StringVar() 
		btn = tk.Button(subinfo, textvariable=colorbtn, command=setColor) # creates the button that activates the color selection window
		btn.grid(column=1,row=0)
		colorbtn.set("R:{0}, G: {1}, B: {2}".format(color[0][0],color[0][1],color[0][2])) #Sets the text of the selection button

		set_btn = tk.Button(subinfo,text="Set Color",command=executeColor) # Button is created that sends the server a commend given the user defined values
		set_btn.grid(column=1,row=1)
	elif (event == "Rainbow"):
		threaded_betterget(ip_address + "/com/rainbows") # Sends a request to the server to set the mode to the rainbow mode, and so forth
		print("Rainbows")
	elif (event == "Christmas blink"):
		threaded_betterget(ip_address + "/com/christmas1")
		print("Christmas")
	elif (event == "Rainbow Cycle"):
		threaded_betterget(ip_address + "/com/improvedrainbow")
		print("RainbowCycle")
def threaded_betterget(command): 
	thread.start_new_thread(betterget,(command, )) #Takes the command, sends it to the get function on its own individual thread so that the program doesnt have to wait for the server to finish executing whatever light mode it is currently on
def setColor():
	global color,colorbtn #Gets global variables
	color = colorchooser.askcolor() # opens the colorchooser window
	try:
		r=round(color[0][0]) #Normalizes the RGB values into integers that the 8 bit microcontroller can use
		g=round(color[0][1])
		b=round(color[0][2])
		if (r >255): r=255 # Puts any out of bounds numbers in bounds
		if (g >255): g=255
		if (b >255): b=255
		colorbtn.set("R:{0},G:{1},B:{2}".format(r,g,b)) #sets the text of the color button to the new RGB Values
		color = ((r,g,b),color[1]) #Re assignes the new normalized values into the color variable, and keeps the hexidecimal value 
	except:
		1
def executeColor():
	global ip #Gets the global variable
	ip_address = "http://192.168.1.{0}".format(ip.get()) #Creates ip of client, new in case it ever changes while the program is running
	threaded_betterget("{0}/bright/{1}".format(ip_address,GlobalBright.get())) # sends command to set the brightness wehn button is pressed
	threaded_betterget(ip_address + "/com/static/{0:0=3d}{1:0=3d}{2:0=3d}".format(color[0][0],color[0][1],color[0][2])) #Takes the RGB values of the Color variable and sends them to the server
def betterget(command):
	for i in range(100): # Tries 100 to send command to the server
		try:
			requests.get(command)
			break # Exits the loop if it is succesful in its attempt to get a command to the server
		except:
			print("command unrecieveable") # IF its unsucesfull after 100 tries it informs the user
if __name__ == "__main__":
	main()
	