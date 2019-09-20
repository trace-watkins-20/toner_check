#Project: Toner Status Update
#File: Printer Status Request
#Name: Trace Watkins
#Date: 4/29/2019

import requests
import regex as re
from ast import literal_eval

#declare methods for accessing IP address content
def request_get(ip,access,num_color,loc):
   
    #initializing strings
    new_text = ''
    final_text = ''

   #disable untrusted certificate warnings
    requests.packages.urllib3.disable_warnings()
    
    #explicitly define html address with ip and access method
    if access == 'hp_info':
        try:
            r = requests.get('http://' + ip + '/hp/device/info_deviceStatus.html', verify = False)
        except IOError:
            print("Issue reaching " + ip)
    elif access == 'topPage' or access == 'statbar':
        try:
            r = requests.get('http://' + ip + '/web/guest/en/websys/webArch/topPage.cgi', verify = False)
        except IOError:
            print("Issue reaching " + ip)
    elif access == 'kyocera':
        try:
            r = requests.get('http://' + ip + '/js/jssrc/model/startwlm/Hme_Toner.model.htm', headers = {'connection':'keep-alive','upgrade-insecure-requests': '1','user-agent':'Chrome/74.0.3729.108','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3','referer': 'https://10.54.26.23','accept-encoding':'gzip,deflate,br','accept-language':'en-US,en;q=0.9','cookie':'rtl=0'},verify=False)
        except IOError:
            print("Issue reaching " + ip)
    else:
        try:    
            r = requests.get('http://' + ip, verify = False)
        except IOError:
            print("Issue reaching " + ip)

    #pass relevant info to print_html folder
    if access != 'statbar': 

        #use regex to isolate text and remove whitespace
        html = re.sub(r'(&nbsp|[\n\t\s]|;)','',r.text)
        html = re.findall(r'>[A-Za-z\d\n\* .%&†;<-]+<',html)
        for m in html:
            new_text = new_text + str(m)

        #use regex to isolate desired text
        final_groups = re.findall(r'(Cartridge([\d%*]?)*|Toner|Black)\*?<>([<A-Za-z\d-%†\* ]*)<>([A-Za-z\d-%†\* ]*)',new_text)

        #concatenate groups to create list of text, remove empty strings, make list into string
        for n in final_groups:
            if access is not 'statbar': 
                n = list(n)
                if '' in n: n.remove('')
            final_text = final_text + str(n)    

    #parse html to extract relevant information        
    else:
        final_groups = re.findall(r'src="/images/deviceStTnBarK.gif" width="(\d+)"',r.text)
        final_text = str( int((int(final_groups[0]) / 160) * 100) ) + '%'
    
    if num_color == mono:
        iso = re.search(r'(StatusOK|CartridgeAlmostEmpty|<?(\d|-)+%†?|UNKNOWN)',final_text)
    
    if num_color == color:


    #Create files in C:\Users\watkinst\print_html with dict of ip and status
    f = open("C:\\Users\\watkinst\\AppData\\Local\\Programs\\Python\\Python37-32\\print_html\\html_docs\\" + loc + " " + ip + ".txt","w+", encoding = "utf-8")
    f.write('Display Text:\n' + final_text + '\n\n\n\nToner Text Results: \n' + final_text + '\n\n\n\nHTML Text Regex:\n' + new_text + '\n\n\n\n\nHTML:\n' + r.text) 
    f.close()

    if iso is not None:
        return(display)
        
        


 



                




    