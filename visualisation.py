# importing all nessacary modules
# these include modules made by me too
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
import process_data as pro
from ml_scripts import train_models
from pandas.tools.plotting import radviz
import matplotlib.pyplot as plt
# creating a mongo client object and setting up the db
client = MongoClient()
db = client.precog

# creating a getting a mongo curser with the data we need
# PLEASE REPLACE complete_remove WITH THE NAME OF YOUR MONGO COLLECTION
dic = db.precog.find()

# process the data using preprocess_data in process_data
# this function returns a pandas dataframe
df = pro.preprocess_data(dic)
# now we will normalize the data using mix max scaler
# mms = MinMaxScaler()
# for i in df.columns:
#     df[i] = pd.DataFrame(mms.fit_transform(df[i].values))
# df.describe()

# train_models(df.drop('likes_count', axis=1), df['likes_count'])


def plot_all(df):
    f, axarr = plt.subplots(13, 2)
    for i in range(13):
        axarr[i, 0].scatter(df['likes_count'], df[df.columns[i]])
        axarr[i, 0].set_title(df.columns[i])
        if i == 0:
            axarr[i, 1].scatter(df['likes_count'], df[df.columns[25]])
            axarr[i, 1].set_title(df.columns[25])
        axarr[i, 1].scatter(df['likes_count'], df[df.columns[2*i]])
        axarr[i, 1].set_title(df.columns[2*i])
    plt.show()

plot_all(df)