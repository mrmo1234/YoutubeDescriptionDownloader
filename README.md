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

An example use would be that you want to pull all the descriptions from this Wiki page https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos

First you download YoutubeDescriptionDownloader, You will have 3 Folders. In this case we need to extract the youtube links from the wiki page "2. Download Links on a page" will do this for us. Running LinkDownloader.py will prompt it to create URLlist.txt this you can add https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos

If you would like to do more than page you can add more URLs on new lines. Don't add blank lines before URLs, this will make it think it has reached the end of the list.

YoutubeVideoList.txt will be created with a list of all found YouTube Links. "2. Download Links on a page" is not capable of detecting duplicates, This is not an issue for "3. Download Descripsions with links" however it is something to be aware of if you plan to use this list in another program.

We can now copy YoutubeVideoList.txt and place it in the folder "3. Download Descripsions with links", Now when we run YoutubeDescriptionDownloader.py an output folder named "Youtube Description Downloader Output" will be created.
By default the output will be organised by YouTube channel. This can be disabled by editing into YoutubeDescriptionDownloader.py and changing organiseuser = True on line 17 to False.


How long into the foreseeable future will this project work for?
--------------
"1. Download Links per User" Is probably the most robust as it uses the Youtube API, This will work as long as the YouTube Data API v3 is available.

“2. Download Links on a page” Searches for strings like “https://www.youtube.com/watc” and “/watch” in the HTML of pages. Any new domains that youtube adds will not work.

“3. Download Descripsions with links” Unfortunately is not based on the API and is vulnerable to the minor layout changes that YouTube has every 6 months.

It won't work what can I do?
--------------
The most common issue I had was python libarys not installed properly or my internet connection beeing funny.
I don't really expect anyone to take any interrest in this but you can open issue on github with any URLs that don't work and I/Someone may be able to suggest a fix.
