import pandas as pd
import numpy as np
import random
import sys

# Reading the datasets

bidder = pd.read_csv("bidder_dataset.csv")
#print(bidder)
queries = pd.read_csv("queries.txt",header = None, names = ['q'])
#print(queries)

# Dictionary to map advertisers with budget.
bidder =  bidder_dataset.loc[(bidder_dataset.Budget > 0), ['Advertiser', 'Budget']]
budget_dictionary = bidder.set_index('Advertiser')['Budget'].to_dict()
# Total budget.
total_budget = sum(budget_dictionary.values())

#Collating queries for advertisers placing the bid
queries_dictionary = {}
for q in queries['q'].values:
    if q not in queries_dictionary.keys():
        x = bidder_dataset.loc[(bidder_dataset.Keyword == q)]
        y = x.sort_values(by = 'Bid Value', ascending = False)
        queries_dictionary[q] = y.values
#print(queries_dictionary)    

# Greedy Algorithm
def greedy(bidder_dataset, queries, budget_dictionary):
    total_revenue = 0
    for i in range(100):
        revenue = 0
        budget = budget_dictionary.copy()
        quer = queries['q'].sample(frac = 1).values
        for q in quer:
            for b in queries_dictionary[q]:
                if budget[b[0]] - b[2] >= 0:
                    budget[b[0]] -= b[2]
                    revenue += b[2]
                    break
        total_revenue += revenue
    return total_revenue /100

#print(greedy(bidder_dataset, queries, budget_dictionary))

# MSVV Algorithm
def msvv(bidder_dataset, queries, budget_dictionary):
    queries_dictionary = {}
    for q in queries['q'].values:
        if q not in queries_dictionary.keys():
            x = bidder_dataset.loc[(bidder_dataset.Keyword == q)]
            #y = x.sort_values(by = 'Bid Value', ascending = False)
            queries_dictionary[q] = x.values
    total_revenue = 0
    for i in range(100):
        spent_budget = dict.fromkeys(budget_dictionary, 0)
        revenue = 0	
        quer = queries['q'].sample(frac = 1).values
        for q in quer:
            bid, advert = 0, 0
            msvv = 0
            for b in queries_dictionary[q]:
                new_msvv = (b[2] * (1 - np.exp((spent_budget[b[0]] / budget_dictionary[b[0]]) - 1)))
                if (msvv < new_msvv) and ((spent_budget[b[0]] + b[2]) <= budget_dictionary[b[0]]):
                    msvv = new_msvv
                    bid = b[2]
                    advert = b[0]
            spent_budget[advert] += bid
            revenue += bid
        total_revenue += revenue
    return(total_revenue/100)
#print(msvv(bidder_dataset, queries, budget_dictionary))

# Balance Method
def balance(bidder_dataset, queries, budget_dictionary):
    total_revenue = 0
    for i in range(100):
        revenue = 0
        budget = budget_dictionary.copy()
        quer = queries['q'].sample(frac = 1).values
        for q in quer:
            bal, bid, advert = 0, 0, 0
            for b in queries_dictionary[q]:
                if bal < budget[b[0]] and budget[b[0]] >= b[2]:
                    bal = budget[b[0]]
                    advert = b[0]
                    bid = b[2]
            budget[advert] -= bid
            revenue += bid
        total_revenue += revenue
    return(total_revenue/100)
#print(balance(bidder_dataset, queries, budget_dictionary)/total_budget)


# Reading Input
algo = sys.argv[1]
# Setting random seed
random.seed(0)
if algo == "greedy":
    revenue = greedy(bidder_dataset, queries, budget_dictionary)
    print("Revenue Collected - Greedy : ", revenue)
    print("Competitive Ratio - Greedy : ", (revenue/total_budget))
elif algo == "msvv":
    revenue = msvv(bidder_dataset, queries, budget_dictionary)
    print("Revenue Collected - MSVV : ", revenue)
    print("Competitive Ratio - MSVV : ", (revenue/total_budget))
elif algo == "balance":
    revenue = balance(bidder_dataset, queries, budget_dictionary)
    print("Revenue Collected - Balance : ", revenue)
    print("Competitive Ratio - Balance : ", (revenue/total_budget))
else:
    print("Wrong method chosen!")