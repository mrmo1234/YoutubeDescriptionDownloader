#Mark O'Dell 21/01/2017 - Youtube Link finder and downloader
#Tested to work with Python 3.6.0
#Needs https://www.crummy.com/software/BeautifulSoup/ and http://docs.python-requests.org/en/latest/user/install/ to work
import requests
from time import *
from bs4 import BeautifulSoup, Comment
import datetime
import time
import codecs
import sys
import os

def DownloadandWrite(url):

    #Define Webpage
    r = requests.get(url)
    #Start BeautifulSouping and downloaded content
    outputdata = BeautifulSoup(r.content, 'html.parser')
    yttitle = str(outputdata.title.string)+" - List of Youtube URLs.txt"
    #Prevent Errors by stripping out unsuitable characters
    print (yttitle)
    yttitle = repr(yttitle).replace("\\","")[1:-1]
    keepcharacters = keepcharacters = (' ','.','_','(',')','-','Ω','[',']','&')
    yttitle = "".join(c for c in yttitle if c.isalnum() or c in keepcharacters).rstrip()
    print (yttitle)
    #Open and name the file
    #Blank exstiting file
    #file=open(yttitle,"w")
    #file.close()
    #Write out data
    file=open("YoutubeVideoList.txt","a")

    lastfile = None
    for link in outputdata.find_all('a'):
        linkdec = str(link.get("href"))
        linkdecshort = linkdec[:6]
        linkdeclong = linkdec[:28]
        if linkdecshort == "/watch":
            if lastfile == "https://www.youtube.com"+linkdec:
                print ("Detected Duplicate")
                print ("https://www.youtube.com"+linkdec+" Not Outputed")
            else:
                file.write ("https://www.youtube.com"+linkdec)
                file.write ("\n")
                lastfile = "https://www.youtube.com"+linkdec
        elif linkdeclong == "https://www.youtube.com/watc" or linkdeclong == "http://www.youtube.com/watch":
            file.write (linkdec)
            file.write ("\n")


#Load in URL list
URLlistPath = "URLlist.txt"
filepresent = os.path.isfile(URLlistPath)
if filepresent == True:
    filelist=open(URLlistPath,"r")
else:
    print ("Can't Find input file "+URLlistPath+"!\nCreating & Exiting...")
    try:
        filetxt=open(URLlistPath,"w")
        filetxt.close()
    except:
        print ("Can't Create file! Check file permissions!")
    sleep(5)
    sys.exit()


#Do until urllist.txt is EOF
state = "NOT DONE"
contentfound = False
while state != "DONE":
    url=filelist.readline()
    if url != "":
        contentfound = True
        DownloadandWrite(url)
    else:
        state = "DONE"
        if contentfound != True:
            print ("No content found in "+URLlistPath+"!\nExiting...")

#All finished - Close list
filelist.close()
print ("Done, Exiting...")
sleep(5)
