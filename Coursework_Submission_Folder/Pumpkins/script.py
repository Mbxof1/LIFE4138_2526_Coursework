import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tkinter as kin
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

#Prints pumpkin ASCII art
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
print("Complete dataset for heaviest pumpkin:")
print("\n",heaviest,"\n")
print("Variety:",(heaviest.iloc[0,13]),"\nGrown in:",f"{(heaviest.iloc[0,4])}{","}",f"{(heaviest.iloc[0,5])}{","}",(heaviest.iloc[0,6]))

#Convert weight in lbs into kg, then append the newly created dataframe to the end of the pumpkins DF.
weight_kg=pd.DataFrame(pumpkins["weight_lbs"]*0.454)
weight_kg.rename(columns={"weight_lbs":"weight_kg"},inplace=True)
pumpkins = pd.concat([pumpkins,weight_kg],axis=1)

#Use simple lambda function to iterate through pumpkins, appending weight class based on size in kg
pumpkins["weight_class"] = pumpkins["weight_kg"].apply(lambda i: "Light" if i <= 300 else ("Heavy" if i >= 600 else "Medium"))

#Plot estimated weight vs actual weight (both in lbs) for the pumpkins
estvsactualweight = sns.scatterplot(data=pumpkins,x="weight_lbs",y="est_weight",hue="weight_class",hue_order=["Light","Medium","Heavy"])
estvsactualweight.set(xlabel="Weight (lbs)",ylabel="Estimated weight (lbs)",title="Comparison of estimated and actual weight\nfor individuals from the pumpkins dataset")
plt.legend(title="Weight classes")

#Use tkinter GUI to ask user where plot should output to as a png
wheretosave = askdirectory(title="Select a directory for the scatterplot output to be saved in")
plt.savefig(f"{wheretosave}{"/Pumpkins_Est_Vs_Act.png"}")

#Filters pumpkins to contain individuals from only 3 countries, then saves as a CSV file in a directory the user chooses.
filteredpumpkins = pumpkins[pumpkins["country"].isin(["Japan","Canada","Italy"])]
wheretosave = askdirectory(title="Select a directory for the filtered .csv to be saved in")
filteredpumpkins.to_csv(f"{wheretosave}{"/pumpkins_filtered.csv"}")

#Summarizes the filtered dataset based on provided requirements.
#Calculates the mean weights of the pumpkins based on the country they came from. Outputs full dataset, then states which country had the highest mean.
meanweights = filteredpumpkins.groupby("country")["weight_kg"].mean().reset_index()
print("Complete dataset, showing mean weights of pumpkins from 3 different countries:","\n",meanweights,"\n")
maxmeanweight = meanweights.sort_values(by="weight_kg",ascending=False)
print("The highest mean weight of the pumpkins from the 3 countries is",f"{maxmeanweight.iloc[0,1]}{"kg"}","from",maxmeanweight.iloc[0,0])

#Does the same as the code above, but also groups by variety within each of the countries.
meanweightsvariety = filteredpumpkins.groupby(["country","variety"])["weight_kg"].mean().reset_index()
print("\n",meanweightsvariety,"\n")
minmeanweight = meanweightsvariety.sort_values(by="weight_kg")
print("The lowest mean weight of pumpkins based on these groups is",f"{minmeanweight.iloc[0,2]}{"kg"}","from the variety",minmeanweight.iloc[0,1],"originating in",minmeanweight.iloc[0,0])

#Closes all open plots to remove aes data, then generates a new box plot from the filtered data based on country of origin and weight.
plt.close()
pumpkinsboxplot = sns.boxplot(data=filteredpumpkins,x="country",y="weight_kg")
pumpkinsboxplot.set(xlabel="Country of origin",ylabel="Pumpkin weight (kg)",title="Boxplot of pumpkin weight in kg\nbased on country of origin.")
#Save graphical output in chosen DIR
wheretosave = askdirectory(title="Select a directory for the boxplot output to be saved in")
plt.savefig(f"{wheretosave}{"/Pumpkin_Boxplot.png"}")

#Close plots again, set up FacetGrid parameters to define how each box plot should be divided (based on variety), generate faceted boxplot, apply aesthetics.
plt.close()
pumpkinsfacetgrid = sns.FacetGrid(filteredpumpkins,col="variety",col_wrap=5)
pumpkinsfacetboxplot = pumpkinsfacetgrid.map(sns.boxplot,"country","weight_kg",order=["Japan","Italy","Canada"])
pumpkinsfacetboxplot.set(xlabel="Country of origin",ylabel="Pumpkin weight (kg)")
plt.subplots_adjust(top=0.9)
pumpkinsfacetboxplot.figure.suptitle("Faceted boxplots, showing data separated by\nboth variety and country of origin")

#Again, save to chosen DIR
wheretosave = askdirectory(title="Select a directory for the faceted boxplot output to be saved in")
plt.savefig(f"{wheretosave}{"/Pumpkin_Faceted_Boxplot.png"}")