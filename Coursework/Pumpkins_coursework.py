import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tkinter as kin
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


print(r"""
                             _    _       
                            | |  (_)      
 _ __  _   _ _ __ ___  _ __ | | ___ _ __  
| '_ \| | | | '_ ` _ \| '_ \| |/ / | '_ \ 
| |_) | |_| | | | | | | |_) |   <| | | | |
| .__/ \__,_|_| |_| |_| .__/|_|\_\_|_| |_|
| |                   | |                 
|_|                   |_|                 
      """)

#Use tkinter askopenfilename to allow user to select any of the pumpkin datasets. Relative path has also been included commented out for ease of use.
#filepathpumpkin = askopenfilename()
filepathpumpkin = "GIT/LIFE4138_2526_Coursework/Coursework/Pumpkins/pumpkins_datasets/pumpkins_04.csv"
pumpkins = pd.read_csv(filepathpumpkin)

#Print the full row of the heaviest pumpkin, then specifically print the variety and where it was grown.
maxweight = pumpkins.sort_values(by="weight_lbs",ascending=False)
heaviest=maxweight.head(1)
print(heaviest)
print("Variety:",(heaviest.iloc[0,13]),"\nGrown in:",f"{(heaviest.iloc[0,4])}{","}",f"{(heaviest.iloc[0,5])}{","}",(heaviest.iloc[0,6]))

#Convert weight in lbs into kg, then append the newly created dataframe to the end of the pumpkins DF.
weight_kg=pd.DataFrame(pumpkins["weight_lbs"]*0.454)
weight_kg.rename(columns={"weight_lbs":"weight_kg"},inplace=True)
pumpkins = pd.concat([pumpkins,weight_kg],axis=1)

#Use simple lambda function to iterate through pumpkins, appending weight class based on size in kg
pumpkins["weight_class"] = pumpkins["weight_kg"].apply(lambda i: "Light" if i <= 300 else ("Heavy" if i >= 600 else "Medium"))

#Plot estimated weight vs actual weight (both in lbs) for the pumpkins
estvsactualweight = sns.scatterplot(data=pumpkins,x="weight_lbs",y="est_weight",hue="weight_class",hue_order=["Light","Medium","Heavy"])
estvsactualweight.set(xlabel="Weight (lbs)",ylabel="Estimated weight (lbs)",title="Comparison of estimated and actual weight""\n""for individuals from the pumpkins dataset")
plt.legend(title="Weight classes")

#Use tkinter GUI to ask user where plot should output to as a png
wheretosave = askdirectory()
print(wheretosave)
plt.savefig(f"{wheretosave}{"/Pumpkins_Est_Vs_Act.png"}")

#Filters pumpkins to contain individuals from only 3 countries, then saves as a CSV file

