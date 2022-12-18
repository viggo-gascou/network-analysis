import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
# the complement cumulative distribution function


def CCDF(df):
    ccdf = df.sort_values(by = "k", ascending = False)
    ccdf["cumsum"] = ccdf["count"].cumsum()
    ccdf["ccdf"] = ccdf["cumsum"] / ccdf["count"].sum()
    ccdf = ccdf[["k", "ccdf"]].sort_values(by = "k")

    ax = plt.gca()
    # Plot as usual and save it for later, since it's very pretty.
    ccdf.plot(kind = "line", x = "k", y = "ccdf", color = "#e41a1c", loglog = True, ax=ax)
    ax.set_xlim(min(ccdf['k']), max(ccdf['k']))
    ax.set_ylabel('p(k>=x)')
    ax.set_xlabel('x')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plt.title("CCDF of the Degree Distribution")
    plt.savefig("degree_distribution_ccdf.png")

