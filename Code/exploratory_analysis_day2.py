#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#%%
# Load the data
data = pd.read_csv("/Users/gracelee/Documents/computational BME/Module-2-Epidemics-SIR-Modeling_lee_abed/Data/mystery_virus_daily_active_counts_RELEASE#1.csv", parse_dates=['date'], header=0, index_col=None)
#%%
# We have day number, date, and active cases. We can use the day number and active cases to fit an exponential growth curve to estimate R0.
# Let's define the exponential growth function
def exponential_growth(t, r):
    return np.exp(r * t)


# Fit the exponential growth model to the data. 
# We'll use a handy function from scipy called CURVE_FIT that allows us to fit any given function to our data. 
# We will fit the exponential growth function to the active cases data. HINT: Look up the documentation for curve_fit to see how to use it.

x = data["day"]
y = data["active reported daily cases"]

param, covariance = curve_fit(exponential_growth, x, y)

plt.scatter(data["day"], data["active reported daily cases"])
plt.xlabel("Day")
plt.ylabel("Active Reported Daily Cases")
plt.title("Day vs. Active Reported Daily Cases")

# Approximate R0 using this fit
r0 = 1+ param[0] * 2 # The infectious period is 2 days. Use 1 + r * D to estimate R0
print ("Estimated R0:", r0)
print (param)
# Add the fit as a line on top of your scatterplot.
plt.plot(x, exponential_growth(x, *param), label='Fitted Exponential Growth Curve')
plt.legend()
plt.show() 