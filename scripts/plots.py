import matplotlib.pyplot as plt
import pandas as pd
# the complement cumulative distribution function


def CCDF(df):
    ccdf = df.sort_values(by = "k", ascending = False)
    ccdf["cumsum"] = ccdf["count"].cumsum()
    ccdf["ccdf"] = ccdf["cumsum"] / ccdf["count"].sum()
    ccdf = ccdf[["k", "ccdf"]].sort_values(by = "k")



    # Plot as usual and save it for later, since it's very pretty.
    ccdf.plot(kind = "line", x = "k", y = "ccdf", color = "#e41a1c", loglog = True)
    plt.title("CCDF of the Degree Distribution")
    plt.savefig("degree_distribution_ccdf.png")

