import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def business_analytics(conn, cur):
    """Allows user to perform statistical queries and graph data"""
    print("\nChoose an option:")
    print(" a) Sales Statistics")
    print(" b) Sales Graphs")
    print(" c) Go Back")

    # Loop until user inputs valid choice
    choice = "sentinel"
    while (choice != "a" and choice != "b" and choice != "c"):
        choice = input("=> ")

    if (choice == "a"): # a = sales statistics
        sales_statistics(conn, cur)
        
    
    elif (choice == "b"): # b = sales graphs
        sales_graphs(conn, cur)
        
    
    # return to main menu
    else:
        return

def sales_statistics(conn, cur):
    """Tells the user the mean, min, max, median, and standard deviation of how much properties sold for."""
    data = cur.execute("SELECT Sold_For FROM sales;")
    selling_prices = []
    for tup in data:
        sold_for = int(tup[0])
        selling_prices.append(sold_for)
    print(f"Mean selling price: ${np.mean(selling_prices):,.2f}\nMin selling price: ${np.min(selling_prices):,.2f}\nMax selling price: ${np.max(selling_prices):,.2f}")
    print(f"Median selling price: ${np.median(selling_prices):,.2f}\nStandard deviation of selling prices: ${np.std(selling_prices):,.2f}")

def sales_graphs(conn, cur):
    """Shows the user two graphs: A bar plot of # unsold properties vs # of sold properties, and a scatterplot of # of manager sales vs their sum"""
    # Select number of sold properties
    data = cur.execute("SELECT COUNT(Sale_Number) FROM sales;")
    for tup in data:
        num_sold = int(tup[0])
    # Select number of unsold properties
    data = cur.execute("SELECT COUNT(Property_Number) FROM properties WHERE Property_Number NOT IN (SELECT Property_Number FROM sales);")
    for tup in data:
        num_unsold = int(tup[0])
    amount_sold = pd.DataFrame({"Sale Status":["Sold", "Unsold"], "Count":[num_sold, num_unsold]})
    amount_sold_graph = amount_sold.plot.bar(x="Sale Status", y="Count", rot=0)
    plt.show()
    plt.title("# of Unsold Properties vs. # of Sold Properties")
    
    # Select # of sales and their sum per manager
    data = cur.execute("""SELECT COUNT(Sold_For), SUM(Sold_For) FROM sales JOIN properties ON sales.Property_Number = properties.Property_Number
                   JOIN managers ON properties.Manager_ID = managers.Manager_ID GROUP BY properties.Manager_ID""")
    sold_counts = []
    sold_sums = []
    for tup in data:
        sold_counts.append(int(tup[0]))
        sold_sums.append(int(tup[1]))
    sold_counts = np.array(sold_counts)
    sold_sums = np.array(sold_sums)
    plt.scatter(sold_counts, sold_sums)
    plt.title("# of Sales vs. Total Amount Sold per Manager")
    plt.xlabel("# of Sales")
    plt.ylabel("Total Amount Sold ($)")
    plt.show()