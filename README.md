## Initial Setup:
This repo currently contains the starter files.

Clone repo and create a virtual environment
```
$ cd chat_borobudur_NLP
$ python3 -m venv venv
$ .\venv\Scripts\activate
```
Install dependencies
```
$ (venv) pip install Flask torch torchvision scikit-learn nltk
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('punkt_tab')
```
Modify `intents.json` with different intents and responses for your Chatbot

Run
```
$ (venv) python train.py
```
This will dump data.pth file. And then run
the following command to test it in the console.
```
$ (venv) python chat.py
```

LINK SHEET DATA "https://docs.google.com/spreadsheets/d/1OCU3lXY5LWUoTXK1qcLnb3O8ENCbL4gY7y1i6QBA8_I/edit?gid=0#gid=0"

untuk update
```
pip install pandas requests
```