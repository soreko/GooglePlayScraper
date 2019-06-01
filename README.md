# GooglePlayScraper
Google Play App Store scraper 

## Intro
This application runs a service thats gets a package id and retrieves its email, title and icon, and outputs it to an output.txt file.
You can send a list of app IDs by running app_sender.exe.

## Installation
Make sure Python 2.7 is installed and Install requirements:
```
pip install -r requirements.txt
```

## Usage
1. Load up the service
```
python app.py
```

2. Send apps ids
```
app_sender/app_sender.exe
```

3. Tail output.txt for app details

## Architecture
2 main threads are running:
1. Web application 
2. Scraper Launcher

### Web application thread
A thread that runs a simple flask application, listens on localhost:5000.
Support one method - GET /ScrapApp?id=ABC.
For each app id, this thread insert the id to a simple thread-safe ids-queue (python Queue).

### Scraper Launcher thread







