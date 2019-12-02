import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#Data cleaning and preprocessing 
train = pd.read_csv("pc_spark.csv")
#train.info()

#drop entries with missing value in ls_price_pc
train.dropna(subset = ["ls_price_pc"], inplace = True)
#only keep price above 1000
train = train[train["ls_price_pc"] > 1000]
train.fillna(0, inplace = True)
#compute y = log($/ha)
train["log_price_per_ha"] = np.log(train["ls_price_pc"]/train["ha"])
#extract year from ls_date_pc, drop any entry with ~
# train = train[train["ls_date_pc"] != "~"]
#print(train[.iloc[700,])
#print(train.ls_date_pc.unique())
train["ls_date_pc"] = train["ls_date_pc"].apply(str)
train = train[~train.ls_date_pc.str.contains("~")]
#train.drop([28862,28863,28866, 28868, 28869], inplace = True)

#train.drop(train.ls_date_pc.str.contains("~"), inplace = True)
year = []
#print(train["ls_date_pc"].dtypes)
for idx, row in train.iterrows():
    #print(row["ls_date_pc"], idx)
    if row["ls_date_pc"] == 0:
        year.append("0")
    elif "/" in row["ls_date_pc"]:
        #print(row["ls_date_pc"], "0")
        row["ls_date_pc"] = pd.to_datetime(row["ls_date_pc"],errors = "coerce")
        #pd.DatetimeIndex(row['ls_date_pc']).year  
        year.append(row['ls_date_pc'].year)
    elif "-" in row["ls_date_pc"]:
        #print(row["ls_date_pc"])
        year.append(pd.to_datetime(row["ls_date_pc"],errors = "coerce",yearfirst = True).year)
    else:
        year.append(row["ls_date_pc"])
train["year"] = year

#train["year"] = pd.to_datetime(train["ls_date_pc"]).dt.year
#e_sold: 0: no easement when the land was sold, binary variable
train["e_sold"] = np.where(train["e_year"].le(train["year"].astype(float)), 1, 0)

#split to train and test set ratio 7:3
y = train["log_price_per_ha"]
X = train.drop(columns = ["log_price_per_ha"])
X_train, X_test, y_train, y_test  = train_test_split(X,y,test_size=0.3)
X_train.to_csv("X_train.csv")
X_test.to_csv("X_test.csv")
y_train.to_csv("y_train.csv", header = True)
y_test.to_csv("y_test.csv", header = True)