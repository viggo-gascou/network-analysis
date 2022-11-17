num_degrees = Counter(node_list_degrees["Degree"]) 

# Normalising y with the total number of nodes in the network. 

degrees = num_degrees.keys()
counts = num_degrees.values()


pw = pd.DataFrame()
pw["k"] = degrees
pw["count"] = counts

num_degrees_normalised = {key: value / len(G.nodes) for key, value in num_degrees.items()} 
pw['p(k)'] = num_degrees_normalised.values() 


# plot the degrees against the number of nodes 

# With log-scale

pw.plot(x = "k", y = "p(k)", kind = "scatter", loglog= True)

# without log-scale

pw.plot(x = "k", y = "p(k)", kind = "scatter" )



