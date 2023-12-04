FROM python:3.9.18-slim
RUN apt-get update && \
    apt-get install -y firefox-esr wget gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v0.33.0-linux64.tar.gz
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
