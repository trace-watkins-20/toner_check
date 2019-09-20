#Project: Toner Status Update
#File: Printer Ink Cartridge Inquiry
#Name: Trace Watkins
#Date: 4/22/2019

from print_loc import INTPRO
import print_loc
from req_get import request_get
import regex as re

final_dict = {}

#loop through database
for loc,entry in INTPRO.ipdict.items():         #get key:value pairs from database
    for access,ip,num_color in entry:                 #get access method and ip address from list of values
        
        #access online resources and grab data
        final_text = request_get(ip,access,num_color,loc)
        print('Information retrieved for ' + ip)
        final_dict[ip] = final_text

#Create files in C:\Users\watkinst\print_html with dict of ip and status
f = open("C:\\ip_dict.txt","w+", encoding = "utf-8")
f.write(str(final_dict))
f.close() 
