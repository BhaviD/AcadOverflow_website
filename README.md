# SE_Project: AcadOverFlow
### AcadOverFlow is a platform for professional and enthusiast programmers of IIIT-H where technical questions can be posted/queried by any student, so that fellow peers can post responses to it or previously asked similar questions can be listed along with the answers.

#### There are some system requirements:
```
The dataset for the required problem statement is quite big. So it need to be run on ada servers or the machines which have RAM > 12GB. Otherwise MemoryError would be shown.
```

#### Before running the flask server, there are some ML files that are need to be downloaded and kept in their specific folders and also some modules need to be installed:

(i) For downloading the ML related files, go to ML_Module/models and download the data shown upon clicking the links mentioned in the following files(and save at the same location with the same name):
```
(a) SO_word2vec_embeddings.bin
(b) Tag_predictor.h5
(c) title_embeddings.csv.zip, unzip it in the same location.
(d) tokenizer.pickle

Also download csv_files.zip, unzip it in SE_Project/AcadOverflow/app/session_data. After unzipping it, do the following:
$ cd csv_files
$ git checkout Preprocessed_users.csv
```

(ii) Install the following modules:
```
pip3 install -U gensim
pip3 uninstall zipp => Do this only if shows some error, no need to uninstall if zipp is not installed.
pip3 install inflect
pip3 install nltk
pip3 install -U spacy
pip3 install smart-open
python3 -m spacy download en_core_web_sm
```

To run the module, Go to AcadOverflow folder and run the following command:
```
python3 run.py
```

Webserver will run on http://127.0.0.1:8889/ . The website can be accessed using this address.
The user can register and then login into the AcadOverFlow Webapp. :)
