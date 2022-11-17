from collections import Counter
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import powerlaw as pl
from scipy.stats import powerlaw
import networkx as nx
#Here we make a data frame with a count of the degrees. "k" is the number of degrees, and 
#"count" is how many nodes have that corresponding degree. We make this data frame to help us with the degree distribution

def make_df(node_list_degrees):
    num_degrees = Counter(node_list_degrees["Degree"]) 

    # Normalising y with the total number of nodes in the network. 

    degrees = num_degrees.keys()
    counts = num_degrees.values()

    pw = pd.DataFrame()
    pw["k"] = degrees
    pw["count"] = counts

    num_degrees_normalised = {key: value / len(degrees) for key, value in num_degrees.items()} 
    pw['p(k)'] = num_degrees_normalised.values() 
    return pw


# plot the degrees against the number of nodes 
# With log-scale
def plot_degree_log(df):
    df.plot(x = "k", y = "p(k)", kind = "scatter", loglog= True)
    plt.title("Log-log plot of the Degree Distribution")

def plot_degree(df):
    df.plot(x = "k", y = "p(k)", kind = "scatter" )
    plt.title("Plot of the Degree Distribution")




def check_power_law(G):
    # define ccdf like in the plot function.
    dd = Counter(dict(G.degree).values()) # dict(degree of node: how many nodes have this degree)
    dd = pd.DataFrame(list(dd.items()), columns = ("k", "count")).sort_values(by = "k")  # make df and sort values by degree, ascending
    ccdf = dd.sort_values(by = "k", ascending = False) 
    #^ sort degree from high to low. 

    # Now we calculate the cumulative sum of the degrees, in descending order.
    # So the 100% "chance" is in the beginning of the plot, as opposite the CDF
    ccdf["cumsum"] = ccdf["count"].cumsum()  # cumsum= cumsum of the count of degrees
    ccdf["ccdf"] = ccdf["cumsum"] / ccdf["count"].sum() # normalise the cumsum
    # sort the values again by ascentding order, since k is ascending in the x-axis
    # the lowest value of k is the most likely 
    ccdf = ccdf[["k", "ccdf"]].sort_values(by = "k") 

    # We take the logarithm in base 10 of both degree and CCDF. Then we simply do a linear regression. 
    # The slope is  the exponent. The intercept needs to be the power of 10, to undo the logarithm operation. 
    # Look at that r-squared!
    logcdf = np.log10(ccdf[["k", "ccdf"]])
    slope, log10intercept, r_value, p_value, std_err = linregress(logcdf["k"], logcdf["ccdf"])
    print("CCDF Fit: %1.4f x ^ %1.4f (R2 = %1.4f, p = %1.4f)" % (10 ** log10intercept, slope, r_value ** 2, p_value))
    plt.plot(np.log10(ccdf['k']), np.log10(ccdf['ccdf']))
    plt.show()


    results = pl.Fit(ccdf["ccdf"])
    k_min = ccdf[ccdf["ccdf"] == results.power_law.xmin]["k"]
    print("Powerlaw CCDF Fit: %1.4f x ^ -%1.4f (k_min = %d)" % (10 ** results.power_law.Kappa, results.power_law.alpha, k_min))

    print(powerlaw.fit(ccdf['ccdf']))
    print(results.power_law.alpha)
    # Let's plot the best fit.
    ccdf["fit"] = (10 ** results.power_law.Kappa) * (ccdf["k"] ** -results.power_law.alpha)
    ax = plt.gca()
    ax.set_xlim(min(ccdf['k']), max(ccdf['k']))
    ccdf.plot(kind = "line", x = "k", y = "ccdf", color = "#e41a1c", loglog = True, ax = ax)
    ccdf.plot(kind = "line", x = "k", y = "fit", color = "#377eb8", loglog = True, ax = ax)
    plt.savefig("ccdf_fit.png")


