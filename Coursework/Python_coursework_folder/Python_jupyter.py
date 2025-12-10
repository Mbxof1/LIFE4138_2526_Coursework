import pandas as pd
import random as rand
import matplotlib.pyplot as plt
import array as arr

""" data1={"Name":["Anna","Brian","Chris","Diane","Eric"],"Age":[rand.randint(1,85),rand.randint(1,85),rand.randint(1,85),rand.randint(1,85),rand.randint(1,85)]}
DF1 = pd.DataFrame(data=data1)
print(DF1) """

List1 = [1,2,3,4,5]
print(List1[4])

List2 = tuple(List1)
print(List2)
type(List2)

Dict1 = {"A":123,"G":456,"C":123,"T":723}
print(Dict1)

for i in range(200,301):
    print(i)

i=200
while i<301:
    print(i)
    i=i+1

list2300 = list(range(200,301))
print(list2300)

# Replace elements in this list
animals = ["tiger", "lion", "badger", "fox", "rabbit", "fish", "dog", "octopus"]
animals[5] = "elephant"
animals.append("chicken")
animals[7] = "whale"
print(animals)

mtcars = "https://raw.githubusercontent.com/Apress/mastering-ml-w-python-in-six-steps/refs/heads/master/Chapter_2_Code/Data/mtcars.csv"
cars = pd.read_csv(mtcars)
scatter1 = cars.plot.scatter(x="mpg",y="hp")
plt.show()

starwars_dataset = "https://www.fabricionarcizo.com/post/starwars/updated_starwars.csv"
starwars = pd.read_csv(starwars_dataset)
swtall = starwars.sort_values(by="height",ascending=False)
print(swtall)

import seaborn as sns
life_expectancy = sns.load_dataset('healthexp')
print(life_expectancy["Country"].nunique())
sorted_life_expectancy = life_expectancy.sort_values(by="Life_Expectancy",ascending=False)
print(sorted_life_expectancy.head(1))

life_expectancy_cost = life_expectancy.groupby("Year", as_index=False).sum()
sorted_life_expectancy_cost = life_expectancy_cost.sort_values("Spending_USD")
print(life_expectancy_cost["Year"].tail(1))

listoflists = [[2.4,2.7,2.8],[5.7,5.2,7.8],[5.3,10.7,8.4],[2.1,1.6,7.8],[1.2,3.4,5.6],[9.4,8.3,5.2]]
print(listoflists[5][2])

array1 = arr.array("f",[1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9])
print(array1[0:4])

print(starwars.loc[8,:])
