FROM python:3.11-bookworm
LABEL authors="Akira Otaka"

RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY main.py main.py
COPY requirements.txt requirements.txt
COPY public public
COPY samples samples
RUN pip install -r requirements.txt

# make data
COPY .env .env
COPY make_data.py make_data.py
RUN python -m spacy download ja_core_news_sm
RUN python make_data.py

# startup chainlit
WORKDIR /app
COPY .chainlit .chainlit
COPY chainlit.md chainlit.md

EXPOSE 8000

CMD chainlit run main.py