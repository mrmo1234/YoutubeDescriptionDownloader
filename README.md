YoutubeDescriptionDownloader
==============

What is it?
--------------
YoutubeDescriptionDownloader is a small python project to fulfill a need I had to archive Youtube Descriptions in bulk.

What do I need to run it?
--------------

- Python 3 (Known to work on Python 3.6.0)
- BeautifulSoup https://www.crummy.com/software/BeautifulSoup/
- Requests http://docs.python-requests.org/en/latest/user/install/

How do I use it?
--------------
Its usage is pretty basic, there are no command line arguments and it’s paths for the input and output files are hard coded.
When you first run the python file, it will create blank versions of the input files it needs.
You can then populate this file with your own URLs or copy the list from another program.

An exsample use would be 

How long will it work for?
--------------
"1. Download Links per User" Is probably the most robust as it uses the Youtube API, Will will work as long as the YouTube Data API v3 is available.

“2. Download Links on a page” Searches for strings like“https://www.youtube.com/watc” and “/watch”. New domains like http://youtu.be not work until fixed.

“3. Download Descripsions with links” Unfortunately is not based on the API and is vulnerable to the minor layout changes that YouTube has every 6 months.

It won't work what can I do?
--------------
The most commnon issue I had python libarys not installed properly or my internet connection beeing funny.
I don't really expect anyone to take any interrest in this so I don't plan to update it regulay but open issue on github with any URLs that don't work and I/Someone may be able to sugest a fix.
