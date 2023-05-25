# ftp_web

## start server

Usage 

```
python2 ftp.py 8082 
```

you can start a file browser server in 8082 port

## upload by CLI

```
python ./upload.py --file xxxx.py 
```
upload a file named xxxx.py to server.

## vim remote edit

the server we just setting up supports editing by vim. 

```
vim http://you-host/xxxx.py 
```

and when you :w , vim will send a PUT request to ftp.py server, the file will be updated automatically.
