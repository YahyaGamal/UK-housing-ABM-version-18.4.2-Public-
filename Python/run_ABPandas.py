from Housing_Model_ABPandas import HousingModel
from statistics import median, mean
import geopandas as gpd
import pandas as pd
import abpandas as abp
import matplotlib.pyplot as plt
import os
import multiprocessing as mp
import random

# define python directory
python_directory = os.path.dirname(os.path.realpath(__file__))

# load space .shp file
## option to modify the input values (64, 64, ...) to modify the grid space size of the model
## note that this function will save by default to the directory \Space\64x64_grid.shp
grid = abp.create_patches(64, 64, rf"{python_directory}\Space\64x64_grid.shp")
## load space edited shape file
grid = gpd.read_file(rf"{python_directory}\Space\64x64_grid.shp")
grid["i"] = [int(row) for row in list(grid["i"])]
grid["j"] = [int(row) for row in list(grid["j"])]
abm = HousingModel(space=grid)

# initialise the model
abm.initialise()

ones = list()

for i in abm.indices_in_radius(centre= abm.space.at[100, "geometry"], radius=10, outline_only=True):
    abm.space.at[i, "n_agents"] = 4

count_realtors = list()
for house in abm.houses:
    count_realtors.append(len(house.props["local_realtors"]))

abm.space["monitor"] = [0 for i in abm.space.index]
for h_list in abm.space["houses"]:
    monitor_dict = {"mortgage": -1, "rent": 1}
    if len(h_list) > 0:
        house = h_list[0]
        #abm.space.at[house.location_index, "monitor"] = house.props["sale_price"]
        abm.space.at[house.location_index, "monitor"] = monitor_dict[house.props["my_type"]]


visualise = True
if visualise == True:
    # create plot figure space with interactive mode on
    plt.ion()
    ## plot two rows of plots
    ## ax[0] represents the first plot
    ## if you use subplots(2, 2), the ax list becomes two-dimensional i.e., ax[2, 2]
    fig, ax = plt.subplots(2, 3)

steps = 1000
x_ticks = list()
counts = {"households": list(), "houses": list()}
n_discouraged = {"discouraged": list()}
median_prices = {"prices": list()}
median_rents = {"rents": list()}
houses = {"mortgage": list(), "rent": list()}
households = {"mortgage": list(), "rent": list()}



for s in range(steps):
    abm.step()
    # Visualisation

    ## plot the ABM space
    if visualise == True:
        monitor_dict = {"mortgage": -1, "rent": 1}
        for h_list in abm.space["houses"]:
            if len(h_list) > 0:
                house = h_list[0]
                #abm.space.at[house.location_index, "monitor"] = house.props["sale_price"]
                abm.space.at[house.location_index, "monitor"] = monitor_dict[house.props["my_type"]]
            else:
                abm.space.at[house.location_index, "monitor"] = 0
        ax[0, 0].clear()
        myplot = abm.space.plot(ax= ax[0, 0], cmap = 'coolwarm', column ='monitor', legend=False, figsize = (8, 10))
        ## create the plot for the agents
        #x = [abm.space.at[a.location_index, "i"] - 0.5 for a in abm.households if a.location_index is not None]
        #y = [abm.space.at[a.location_index, "j"] - 0.5 for a in abm.households if a.location_index is not None]
        x = [abm.space.at[a.location_index, "geometry"].centroid.x for a in abm.households if a.location_index is not None]
        y = [abm.space.at[a.location_index, "geometry"].centroid.y for a in abm.households if a.location_index is not None]
        ax[0, 0].scatter(x , y, s=0.5, color="yellow")
        ## create a plot for the number of households
        ax[0, 1].clear()
        x_ticks.append(abm.ticks)
        counts["households"].append(len(abm.households))
        counts["houses"].append(len(abm.houses))
        df = pd.DataFrame(counts)
        lines = ax[0, 1].plot(df)
        lines[0].set_color('red')
        lines[1].set_color('blue')
        ax[0, 1].legend(["Households", "Houses"])
        ## create a plot for the n of discouraged households
        # n_discouraged["discouraged"].append(abm.monitors["nDiscouraged"])
        # df = pd.DataFrame(n_discouraged)
        # ax[2].clear()
        # ax[2].plot(df)
        ## create a plot for prices
        median_prices["prices"].append(abm.monitors["medianPriceForSale"])
        df = pd.DataFrame(median_prices)
        lines = ax[0, 2].plot(df)
        lines[0].set_color('green')
        ax[0, 2].legend(["Median prices of houses for-sale"])
        ## create a plot for prices
        median_rents["rents"].append(abm.monitors["medianPriceForRent"])
        df = pd.DataFrame(median_rents)
        lines = ax[1, 2].plot(df)
        lines[0].set_color('green')
        ax[1, 2].legend(["Median rents of houses for-rent"])
        ## create an income histogram
        incomes = [hh.props["income"] for hh in abm.households]
        ax[1, 0].clear()
        ax[1, 0].hist(incomes)
        ax[1, 0].set_title("Income histogram")
        ## create a histogram for the number of houses and agents by type
        houses["mortgage"].append(len([h for h in abm.houses if h.props["my_type"] == "mortgage"])) 
        houses["rent"].append(len([h for h in abm.houses if h.props["my_type"] == "rent"])) 
        households["mortgage"].append(len([hh for hh in abm.households if hh.props["my_type"] == "mortgage" and hh.props["my_house"] is not None]))
        households["rent"].append(len([hh for hh in abm.households if hh.props["my_type"] == "rent" and hh.props["my_house"] is not None]))
        df_h = pd.DataFrame(houses)
        df_hh = pd.DataFrame(households)
        ax[1, 1].clear()
        lines = ax[1, 1].plot(df_h)
        lines[0].set_color("mediumblue")
        lines[1].set_color("brown")
        lines = ax[1, 1].plot(df_hh)
        lines[0].set_color("lightseagreen")
        lines[1].set_color("darkgoldenrod")
        ax[1, 1].legend(["Mortgage houses", "Rent houses", "Mortgage households", "Rent households"])
        ## create a plot for the n of households and n of houses
        ## draw the plot
        plt.draw()
        plt.pause(0.2)

switch = False
if switch == True:
    for r in range(len(abm.realtors[0].props["records"])):
        record = abm.realtors[0].props['records'][r]
        print(f"{record['house'].props['my_type']} house | sale_price = {record['sale_price']} | rent_price = {record['rent_price']} | for_sale? = {record['house'].props['for_sale?']}")

incomes = [hh.props["income"] for hh in abm.households]




# plot an ABM run interface
# turn interactive model on
#plt.ion()
# create figure and axes (2 axes here for elaboration)
fig, ax = plt.subplots(1, 2)
# create the plot for the patches
myplot = abm.space.plot(ax= ax[0], cmap = 'coolwarm', column ='monitor', legend=True, figsize = (8, 10))
# create the plot for the agents
x = [abm.space.at[a.location_index, "i"] - 0.5 for a in abm.households if a.location_index is not None]
y = [abm.space.at[a.location_index, "j"] - 0.5 for a in abm.households if a.location_index is not None]
ax[0].scatter(x , y, s=0.5, color="yellow")
# create a histogram
ax[1].hist(incomes)
ax[1].set_title("Income histogram")
plt.show()


