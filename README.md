# Tweets-Database-Manager

## Install

Prerequisite:
mysql installed, or alternative database

```
cd Tweets-Database-Manager/
python3 -m venv venv  
source venv/bin/activate
# upgrade your pip, make sure pip -V is 18.1, otherwise, update
pip install -r requirements.txt
```

## app

1. db_manager: using library sqlalchemy (ORM) to control the connection between the database and *models, (init the table) (I wrap up some functions here as well)

```
# after entering the python CML in virtual environment
import app
from app.db_manager import *
m = Manager()
# m.create_all()  # create the table under tw_test database  # init the table
# m.drop_all() # drop the table under tw_test database # empty the data
# m.reset_all()  # call drop_all then create_all 
```

2. db_models: the setting of tweets storing in database, like user_name = Column(Text, nullable=False)

3. json_handler (testing, not finish): using library ijson (read json in the stream, which should be faster than regular loading) (extract needed data, then assign that info to the tweet *model, then add and commit to the database)

4. fake: used to create fake tweet data, can be used into test function 

## tweets

template.env & tweet_grap.py: grab tweets using official API

super_preprocessor.py: pre-process raw tweets message

The preprocessor supports: 
1. Reading the output path and debug mode from parameters in the command line.  
2. Reformat tweets source file from .dat format to .csv format. (Since eventually we would like the files being in .csv file format) 
3. Emoji/Few-word/Emoticon/Multi-punc filter (These are regular pre-processes on tweets data, for better evaluation later) 
4. Generate n-gram: the final step for pre-processing Tweets data, to prepare for Chonghan’s adjacent metrics evaluation. 
