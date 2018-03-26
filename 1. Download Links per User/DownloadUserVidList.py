#Need to fix download using ID


import requests
from time import *
from bs4 import BeautifulSoup, Comment
import datetime
import time
import codecs
import sys
import os
import json
import math

def DownloadUserandWrite(ytUserURL,myYTapiKey):
    onefile = False #Needs to be made

    filelog=open("User Vid get log.txt","a")

    #Deside how to qurry the line
    
    ytUserURLlong = ytUserURL[:28]
    if ytUserURLlong == "https://www.youtube.com/chan" or ytUserURLlong == "http://www.youtube.com/chann":
        inputmodeusername = False
        print ("www.youtube.com/channel/ Found")
        print (ytUserURL)
    elif ytUserURLlong == "https://www.youtube.com/user" or ytUserURLlong == "http://www.youtube.com/user/":
        inputmodeusername = True
        print ("www.youtube.com/user/ Found")
        print (ytUserURL)
    else:
        print ("Invalad line")
        print (ytUserURL)
        filelog.write (today+" "+localtime+" [ERROR] Error, Invalad line. "+ytUserURL+"\n")
        return
        
    if inputmodeusername == True:
        ytusername = ytUserURL
        ytUserURLHTTP = ytUserURL[:5]
        if ytUserURLHTTP == "http:":
            ytusername = ytUserURL[28:]
            print (ytusername)
            ytusername = ytusername.split("/")[0]
            print (ytusername)
        elif ytUserURLHTTP == "https":
            ytusername = ytUserURL[29:]
            print (ytusername)
            ytusername = ytusername.split("/")[0]
            print (ytusername)
        else:
            print ("Can't tell if line is http or https!")
            filelog.write (today+" "+localtime+" [ERROR] Can't tell if line is http or https. Identified as /user/. "+ytUserURL+"\n")
            return
        
        #Find Uploads list from Username
        r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername="+ytusername+"&key="+myYTapiKey)
        filelog.write("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername="+ytusername+"&key="+myYTapiKey+"\n")
        jdata = r.json()
        uploadsID = jdata["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        print(uploadsID)
        filelog.write (uploadsID+"\n")
    else:
        ytuserID = ytUserURL
        ytUserURLHTTP = ytUserURL[:5]
        if ytUserURLHTTP == "http:":
            ytuserID = ytUserURL[31:]
        elif ytUserURLHTTP == "https":
            ytuserID = ytUserURL[32:]
        else:
            print ("Can't tell if line is http or https!")
            filelog.write (today+" "+localtime+" [ERROR] Can't tell if line is http or https Identified as /channel/. "+ytUserURL+"\n")
            return
        
        #Find Uploads list from ID
        r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id="+ytuserID+"&key="+myYTapiKey)
        filelog.write("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id="+ytuserID+"&key="+myYTapiKey+"\n")
        jdata = r.json()
        uploadsID = jdata["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        print(uploadsID)
        filelog.write (uploadsID+"\n")

    #Download playlistItems
    pageToken = ""
    r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"+pageToken+"maxResults=50&playlistId="+uploadsID+"&key="+myYTapiKey)
    jdata = r.json()
    filelog.write ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"+pageToken+"maxResults=50&playlistId="+uploadsID+"&key="+myYTapiKey+"\n")

    #Get totalResults from playlistItems
    totalResults = jdata["pageInfo"]["totalResults"]
    print(totalResults)
    filelog.write (str(totalResults)+"\n")

    #Get resultsPerPage from playlistItems
    resultsPerPage = jdata["pageInfo"]["resultsPerPage"]
    print(resultsPerPage)
    filelog.write (str(resultsPerPage)+"\n")

##    #Blank file
##    file=open("User Uploads.txt","w")
##    file.close()
    
    file=open("YoutubeVideoList.txt","a")

    #Calculate how many pages there are
    noofpages = math.ceil(float(totalResults)/resultsPerPage)
    noofpages = noofpages
    print ("Number of pages: ",noofpages)

    filelog.write ("Number of pages: "+str(noofpages)+"\n")
                 
    nextPageToken = ""
    currentpage=1
    while currentpage <= noofpages:
        print ("Current page: ",currentpage)
        filelog.write ("Current page: "+str(currentpage)+"\n")
        currentresult=0
        while currentresult <= resultsPerPage-1:
            print ("Current result: ",currentresult)
            filelog.write ("Current result: "+str(currentresult)+"\n")
            try:
                videoId = jdata["items"][currentresult]["snippet"]["resourceId"]["videoId"]
                print (videoId)
                filelog.write ("videoId: "+videoId+"\n")
                file.write ("https://www.youtube.com/watch?v="+videoId+"\n")
            except:
                print("No videoId in this result.")
                filelog.write ("No videoId in this result."+"\n")
            currentresult = currentresult+1

        try:
            if currentpage <= noofpages:
                #Get nextPageToken from playlistItems
                nextPageToken = jdata["nextPageToken"]
                print(nextPageToken)
                filelog.write (str(nextPageToken)+"\n")
                
                pageToken= "pageToken="+nextPageToken+"&"
                currentpage=1+currentpage
                r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"+pageToken+"maxResults=50&playlistId="+uploadsID+"&key="+myYTapiKey)
                print ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"+pageToken+"maxResults=50&playlistId="+uploadsID+"&key="+myYTapiKey)
                filelog.write ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"+pageToken+"maxResults=50&playlistId="+uploadsID+"&key="+myYTapiKey+"\n")
                jdata = r.json()
            else:
                break
        except:
            print("Error getting next page")
            break
    file.close()


#Load in API key
YTAPIkeyPath = "YoutubeAPIkey.txt"
APIfilepresent = os.path.isfile(YTAPIkeyPath)
if APIfilepresent == True:
    APIfile=open(YTAPIkeyPath,"r")
    myYTapiKey=APIfile.readline()
else:
    print ("Can't Find API key file "+YTAPIkeyPath+"!\nCreating empty file\nYou need to request an API key if you don't have one already.\nhttps://developers.google.com/youtube/v3/getting-started")
    try:
        APIfiletxt=open(YTAPIkeyPath,"w")
        APIfiletxt.close()
    except:
        print ("Can't Create file! Check file permissions!")
    input("Press Enter to Exit...")
    sys.exit()


#Load in video list
YTuserIDlistPath = "Youtube User ID list.txt"
filepresent = os.path.isfile(YTuserIDlistPath)
if filepresent == True:
    filelist=open(YTuserIDlistPath,"r")
else:
    print ("Can't Find input file "+YTuserIDlistPath+"!\nCreating empty file & Exiting...")
    try:
        filetxt=open(YTuserIDlistPath,"w")
        filetxt.close()
    except:
        print ("Can't Create file! Check file permissions!")
    sleep(5)
    sys.exit()

#Do until Youtube list.txt is EOF
state = "NOT DONE"
contentfound = False
linesdonecount = 0
while state != "DONE":
    ytuserID=filelist.readline()
    if ytuserID != "":
        contentfound = True
        DownloadUserandWrite(ytuserID,myYTapiKey)
        linesdonecount = linesdonecount + 1
    else:
        state = "DONE"
        if contentfound != True:
            print ("No content found in "+YTuserIDlistPath+"!\nExiting...")

#All finished - Close list
print ("Finished - "+str(linesdonecount)+" lines found")
filelist.close()
sleep(5)


