import tkinter as tk
from tkinter import messagebox
from Model.Try_LogisticRegression import LogisticR
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

def DataProcess(data):#df

    data = data.drop(data[(data["age"]>=0) & (data["age"]<=15)].index, axis=0)
    
    data["reports"] = data.loc[:,"reports"].apply(lambda x: "less than 4" if x < 4 else "equal and greater then 4")
    one_hot_rep = pd.get_dummies(data["reports"], prefix="reports")#---------------------
    
    data['age'] = data['age'].astype(float)
    def age(row):
        if row>=18 and row<30:
            return "18~30"
        elif row>=30 and row<50:
            return "30~50"
        elif row>=50:
            return "50~"
    data['age']=data['age'].apply(age)
    one_hot_age = pd.get_dummies(data["age"], prefix="age")#------------------------
    #----------------------------------------------------------------------------------
    def ceiling_floor(df, col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        max_within_limits = df.loc[(df[col] <= upper_limit) & (df[col] >= lower_limit), col].max()
        min_within_limits = df.loc[(df[col] <= upper_limit) & (df[col] >= lower_limit), col].min()

        df.loc[df[col] < lower_limit, col] = min_within_limits
        df.loc[df[col] > upper_limit, col] = max_within_limits

        return df
    
    data = ceiling_floor(data, 'income')
    data = ceiling_floor(data, 'share')

    def z(row):#極值正規化
        return (row-row.mean())/row.std()
    data["income"] = z(data["income"])
    data["expenditure"] = z(data["expenditure"])
    #----------------------------------------------------------------------------------
    one_hot_owner = pd.get_dummies(data["owner"], prefix="owner")#------------------------
    #----------------------------------------------------------------------------------
    one_hot_selfemp = pd.get_dummies(data["selfemp"], prefix="selfemp")#------------------------
    #----------------------------------------------------------------------------------
    def dep(row):
        if row==0 or row==1:
            return "0~1"
        else:
            return "1~"
    data["dependents"] = data["dependents"].apply(dep)
    one_hot_dep = pd.get_dummies(data["dependents"], prefix="dependents")#------------------------
    #----------------------------------------------------------------------------------
    def mon(row):
        if row<50:
            return "~50"
        elif 50 <= row < 60:
            return "50~60"
        else:
            return "60~"
    data["months"] = data["months"].apply(mon)
    one_hot_mon = pd.get_dummies(data["months"], prefix="months")#------------------------
    #----------------------------------------------------------------------------------
    def mc(row):
        if row>=1:
            return ">=1"
        else:
            return "0"
    data["majorcards"] = data["majorcards"].apply(mc)
    one_hot_mc = pd.get_dummies(data["majorcards"], prefix="majorcards")#------------------------
    #----------------------------------------------------------------------------------
    def active(row):
        if row>=7:
            return ">=7"
        else:
            return "<7"
    data["active"] = data["active"].apply(active)
    one_hot_active = pd.get_dummies(data["majorcards"], prefix="majorcards")#------------------------
    #----------------------------------------------------------------------------------
    feature_df = data.copy()
    feature_df["card"] = feature_df["card"].map({"yes":True, "no":False})
    feature_df = feature_df.drop(["reports", "age", "owner", "selfemp", "dependents", "months", "majorcards", "active"], axis=1)
    feature_df = pd.concat([feature_df, one_hot_rep, one_hot_age, one_hot_owner, one_hot_selfemp, 
                    one_hot_dep, one_hot_mon, one_hot_mc, one_hot_active], axis=1).reset_index(drop=True)
    #-----------------------------------------------------------------------------------
    return feature_df


def tk_ml():#reports,age,income,share,owner,selfemp,dependents,months,majorcards,active
    values = [list(entry.get()) for entry in entries]
    df = pd.DataFrame(values)
    f = pd.concat([X, df], axis=1)
    f = DataProcess(f) 
    feature = f.iloc[-1, :]
    pre = GR.predict(feature)
    
    output1.config(text=f"Result: {pre}")


data_numeric = pd.read_csv("Data/Data2.csv")
X = data_numeric.drop(['card','expenditure'], axis=1)
y = data_numeric['card']
#learning_rate=0.020999999999999998, iter=730
GR = LogisticRegression()
GR.fit(X, y)

root = tk.Tk()
root.geometry("800x500")
root.title("Credit Card Machine Learning")
#[reports,age,income,share,owner,selfemp,dependents,months,majorcards,active]
s = ["reports","age","income","share","owner","selfemp","dependents","months","majorcards","active"]
entries = []

for i in range(len(s)):
    label = tk.Label(root, text=f"{s[i]}:")
    label.grid(row=i, column=0, pady=5, padx=5)

    entry = tk.Entry(root,width=10)
    entry.grid(row=i, column=1, pady=5, padx=5)
    entries.append(entry)

#--------------------------------------------------------------------------
button1 = tk.Button(root, text="Start", command=tk_ml, width=30, height=1)
button1.grid(row=11, column=0, columnspan=2, pady=20)

output1 = tk.Label(root)
output1.grid(row=12, column=0, columnspan=2, pady=10)


root.mainloop()