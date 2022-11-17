from collections import Counter
import pandas as pd 
import matplotlib.pyplot as plt

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





