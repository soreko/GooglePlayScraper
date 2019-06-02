# GooglePlayScraper
Google Play App Store python scraper 

## Intro
This python application runs a service thats gets a package id and retrieves its email, title and icon as Json format  <br />
and outputs it to output.txt file.

You can send a list of app IDs by running app_sender.



## Installation
1. Make sure Python 2.7 is installed and Install requirements:
```
pip install -r requirements.txt
```

2. Make sure golang is installed and build app_sender.  <br />
In app_sender folder, run:
```
go build
```


## Usage
1. Start the service (runs on localhost:5000)
```
python app.py
```

2. Send apps ids (sends to localhost:5000) <br />
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
1. Flask web application should be wrapped with Nginx or Apache or any other web server in production.
2. I used a ProcessPool and not a ThreadPool, because of python GIL (no real parallelism).
3. The ProcessPool is initialized to number of cores size, it can be increased in order to use more CPU. 
4. In real world I would use a permenent Queue (e.g. RabbitMQ), to support crash recovering - lost data. 
5. In real world I would use a permenent Cache (e.g. Redis), to support crash recovering - all cache flushed.






