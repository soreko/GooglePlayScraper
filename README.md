# GooglePlayScraper
Google Play App Store scraper 

## Intro
This application runs a service thats gets a package id and retrieves its email, title and icon, and outputs it to an output.txt file.

You can send a list of app IDs by running app_sender.exe.



## Installation
1. Make sure Python 2.7 is installed and Install requirements:
```
pip install -r requirements.txt
```

2. Make sure golang is installed and build app_sender. In app_sender folder, run:
```
go build
```


## Usage
1. Load up the service
```
python app.py
```

2. Send apps ids
Windows:
```
app_sender/app_sender.exe
```

Linux:
```
./app_sender/app_sender
```

3. Tail output.txt for apps details



## Architecture
2 main threads are running:
1. Web application 
2. Scraper Launcher

### Web application thread
A thread that runs a simple flask application, listens on localhost:5000.

Support one method - GET /ScrapApp?id=ABC.

For each app id, it inserts the id to a simple thread-safe ids-queue (python Queue).

### Scraper Launcher thread
A thread that loops on the ids-queue, waiting for new id.

For each id it gets from the queue:
1. Checks in its cache if we already scraped this id, if so it outputs the data, else it continue:
2. Asks from Proxy manager for an available proxy. In case no proxy is avaiable it waits for 2 seconds and asks again.
3. Spawns a new process with a GoogleScrapper, and the given app id and proxy.
4. When a process successfully returns, it saves the result to the cache.





## Notes on architecture
1. I used a ProcessPool and not a ThreadPool, because of python GIL (no real parallelism).
2. The ProcessPool is initialized to number of cores size, it can be increased in order to use more CPU. 
3. In real world I would use a permenent Queue (saves data to disk), to support crash recovering - lost data. 
4. In real world I would use a permenent Cache (like redis), to support crash recovering - all cache flushed.






