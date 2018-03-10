# Tkinter_4chan_crawler

A 4chan thread crawler with simple GUI.<br/>
Tested on windows 10 and Mac with Python 3, and it works.

### Preparement
```
pip install -r requirements.txt
```
```
python /path/to/main.py
```

![image](https://raw.githubusercontent.com/hohh0115/Tkinter_4chan_crawler/master/1.PNG)

Target URL: the url of the thread<br/>
Save Path: the path where you want to save the files<br/>
Maximum Size: the maximum size of a file you allowed to download<br/>

Each time you press "Submit", it will save your preference of Save Path and Maximum Size in file "user_info.pickle".
Also, you can press cancel button to stop the download process.

It will create a folder under your Save Path, and the regulation of the folder name is:
```
"the first post number" + "the titile"(if none, use "No Title" instead) + "the current timestamp"
```
The reason why I choose "the first post number" as the prefix is that once you sort the folder by file name, you would know which 4chan thread you had downloaded before, and it is up to you to decide which stays.

I hope it meet meet your needs.
