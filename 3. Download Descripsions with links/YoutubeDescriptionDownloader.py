#Mark O'Dell 21/01/2017 - Youtube description downloader 
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

def DownloadandWrite(yturl):

    #Organise .txts in to folders by User - Change to True/False
    organiseuser = True

    #Open Log file
    filelog=codecs.open("Youtube Description downloader log.txt","a","utf-8")
    
    #Prepare YouTube URL (yturl) and Time
    yturl = yturl.rstrip()
    print ("Started "+str(yturl).rstrip())
    today = datetime.date.today()
    today = str(today)
    localtime = datetime.datetime.now().time()
    localtime = str(localtime)
    
    #Define Webpage
    r = requests.get(yturl)
    #Start BeautifulSouping and downloaded content
    outputdata = BeautifulSoup(r.content, 'html.parser')
    yttitle = str(outputdata.title.string)+" Description.txt"
    justtitle = str(outputdata.title.string)
    #Prevent Errors by stripping out unsuitable characters
    yttitlebeforestrip = yttitle
    yttitle = repr(yttitle).replace("\\","")[1:-1]
    keepcharacters = keepcharacters = (' ','.','_','(',')','-','Ω','[',']','&')
    yttitle = "".join(c for c in yttitle if c.isalnum() or c in keepcharacters).rstrip()
    if yttitlebeforestrip != yttitle:
        print ("File had to be renamed from:\r\n"+yttitlebeforestrip+"\r\nto:\r\n"+yttitle)
        filelog.write (today+" "+localtime+" [RENAME] "+yttitlebeforestrip+" to "+yttitle+" "+yturl+"\r\n")
        print ("A note has been saved to the Log")
        
    #Open and name the file
    #Blank exstiting file, If not there create. Does not delete folder.
    if not os.path.exists(".\\Youtube Description Downloader Output\\"):
        os.makedirs(".\\Youtube Description Downloader Output\\")

    #Find out User
    try:
        for p in outputdata.find('div',attrs={"class" : "yt-user-info"}):
            if p.string == None:
                pass
            elif p.string == "":
                pass
            elif p.string == "\n":
                pass
            else:
                username = p.string
                username = username.replace('\n', '')
    except:
        print ("Error retrieving yt-user-info, Probably because video does not exist.")
        filelog.write (today+" "+localtime+" [ERROR] Error retrieving yt-user-info, Probably because video does not exist. "+yturl+"\r\n")
        print ("A note has been saved to the Log")
        return

    #Prevent Errors by stripping out unsuitable characters out of folder name
    usernamebeforestrip = username
    usernameDIR = repr(username).replace("\\","")[1:-1]
    keepcharacters = keepcharacters = (' ','.','_','(',')','-','Ω','[',']','&')
    usernameDIR = "".join(c for c in usernameDIR if c.isalnum() or c in keepcharacters).rstrip()
    
    #Set output path, If not organise by user blank now as well
    if organiseuser == True:
        if usernamebeforestrip != usernameDIR:
            print ("Folder had to be renamed from:\r\n"+usernamebeforestrip+"\r\nto:\r\n"+usernameDIR)
            filelog.write (today+" "+localtime+" [RENAME] Folder "+usernamebeforestrip+" to "+usernameDIR+" "+yturl+"\r\n")
            print ("A note has been saved to the Log")
            
        txtoutputlocation = ".\\Youtube Description Downloader Output\\"+usernameDIR+"\\"+yttitle
    else:
        txtoutputlocation = ".\\Youtube Description Downloader Output\\"+yttitle
        file=codecs.open(txtoutputlocation,"w","utf-8")
        file.close()


    #Open files
    if organiseuser == True:

        
        
        if not os.path.exists(".\\Youtube Description Downloader Output\\"+usernameDIR+"\\"):
            os.makedirs(".\\Youtube Description Downloader Output\\"+usernameDIR+"\\")
        #Blank if organise by user
        file=codecs.open(txtoutputlocation,"w","utf-8")
        file.close()
        #Now write if organise by user
        file=codecs.open(txtoutputlocation,"a","utf-8")
    else:
        file=codecs.open(txtoutputlocation,"a","utf-8")


    #Output URL
    try:
        file.write (justtitle+"\r\n")
    except:
        print ("Unicode Found in Title or Error, Will output UTF-8")
        file.close()
        file=codecs.open(txtoutputlocation,"a","utf-8")
        file.write (justtitle+"\r\n")
    file.write (yturl.rstrip())
    #Views
    file.write (" - ")

    try:
        for p in outputdata.find("div", { "class" : "watch-view-count" }):
            if p.string == None:
                file.write ("\r\n")
            else:
                file.write(p.string)
        file.write(" as of "+ str(today)+"\r\n\r\n")
    except:
        file.write("0 views as of "+ str(today)+"\r\n\r\n")
        filelog.write (today+" "+localtime+" [ERROR] Error retrieving watch-view-count, Can be caused by livestreams. "+yturl+"\r\n")
        print ("Possable error, Error retrieving watch-view-count, Can be caused by livestreams, A note has been made in the log")

    #Publish date
    for p in outputdata.find(id="watch-uploader-info"):
        if p.string == None:
            file.write ("\r\n")
        else:
            file.write(p.string)


    #If User pressent then write out   
    if username != "" or "\r\n":
        file.write(" by "+username)
    file.write("\r\n\r\n")

    #Body of text
    for p in outputdata.find(id="eow-description"):
        if p.string == None:
            file.write ("\r\n")
        else:
            try:
                file.write(p.string)
            except:
                print ("Unicode Found or Error, Will output UTF-8")
                file.close()
                file=codecs.open(txtoutputlocation,"a","utf-8")
                file.write(p.string)
            

    #List Links at end
    deslinks = outputdata.find(id="eow-description")
    file.write ("\r\n\r\n###End of Description###\r\n\r\nFULL LINKS")
    for link in deslinks.find_all('a'):
        file.write ("\r\n")
        file.write(link.get("href"))

    file.close()
    filelog.close()
    print ("Finished "+str(yturl).rstrip()+"\r\n")


#Load in video list
YoutubeVideoListPath = "YoutubeVideoList.txt"
filepresent = os.path.isfile(YoutubeVideoListPath)
if filepresent == True:
    filelist=open(YoutubeVideoListPath,"r")
else:
    print ("Can't Find input file "+YoutubeVideoListPath+"!\nCreating & Exiting...")
    try:
        filetxt=open(YoutubeVideoListPath,"w")
        filetxt.close()
    except:
        print ("Can't Create file! Check file permissions!")
    sleep(5)
    sys.exit()

#Do until YoutubeVideoListPath is EOF
state = "NOT DONE"
contentfound = False
linesdonecount = 0
while state != "DONE":
    yturl=filelist.readline()
    if yturl != "":
        contentfound = True
        DownloadandWrite(yturl)
        linesdonecount = linesdonecount + 1
    else:
        state = "DONE"
        if contentfound != True:
            print ("No content found in "+YoutubeVideoListPath+"!\nExiting...")

#All finished - Close list
print ("Finished - "+str(linesdonecount)+" lines found")
filelist.close()
sleep(5)
