# People Detection using HOG + Linear SVM

## Install requirements

```bash
poetry install

# or with pip
pip install -r requirements.txt
```

## Credentials

Create file .env in _people_detection/config/_

```bash
CHAT_ID=<YOUR ID HERE>
TELEGRAM_TOKEN=<YOUR TOKEN HERE>
RTSP_URL=<YOUR URL HERE>
```

## Running with Docker

```bash
sudo docker build -t peopledetection .
sudo docker run -v /logs/:/app/logs -d --name people-detection --restart=always peopledetection
```

