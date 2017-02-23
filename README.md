# Youtube Likes Prediction
**A task in feature engineering to predict the number of likes of any given video. The system takes in a range of features using web scraping, youtube api and creativity to predict the range in which the likes will be.**

## Note - A lot of the functions written have been used to store data to mongodb and hence won't be used now and data will directly be accessed from db to reduce computation

## Requirements
* jupyter Notebook
* pandas
* numpy
* sklearn
* mongodb
* pymongo

## steps to run the code
* clone the repo
* import the database (don't change the name of collection)
`mongoimport --db name-of-database --collection precog --file import_this.json`
* run command `jupyter notebook main.ipynb`