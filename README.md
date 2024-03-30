# Re.Quest

**Re.Quest - A simple resource catcher**

A small, simple, docker-hosted http request sink with a basic web UI.

## Features
- Captures HTTP requests directed at any path.
- Displays requests in an easy-to-read format.


## Getting Started

### Prerequisites
- Python 3.9+
- Docker (for Dockerized setup)

### Local Setup
    pip install -r requirements.txt
    flask run

### Docker Setup
    docker build -t re.quest .
    docker run -p 5000:5000 re.quest

### Docker Compose Usage
Minimal docker compose file:

    version: '3.8'
    services:
        request:
            image: ymekesser/re.quest
            ports:
            - "8083:5000"

## Configuration
Use environment variables to configure the application:

- `REFRESH_INTERVAL`: Auto-refresh interval for the UI (in milliseconds).
- `FLASK_PORT`: Flask server port.
- `FLASK_DEBUG`: Enable (true) or disable (false) Flask debug mode.
