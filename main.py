import csv

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("/Users/zain/Documents/GitHub/Module-2-Epidemics-SIR-Modeling_lee_abed/Data/mystery_virus_daily_active_counts_RELEASE#1.csv")

plt.plot(data["day"], data["active reported daily cases"])
plt.xlabel("Day")
plt.ylabel("Active Reported Daily Cases")
plt.title("Day vs. Active Reported Daily Cases")
plt.show() 

# 1. The initial infections increase exponentially
# 2. By finding our R0 value, R0>1 means its spreading, R0<1 means it could be dying out
# 3. Recovery time, transmission methods, and how contagious the virus is 
