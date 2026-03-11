import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


# Generative AI tools were used in assistance of writing some portions of code and identifying bugs when they occured

data2 = pd.read_csv('/Users/gracelee/Documents/computational BME/Module-2-Epidemics-SIR-Modeling_lee_abed/Data/mystery_virus_daily_active_counts_RELEASE#2.csv')

# Total population size
N = 17900

#Creating an array to hold the timepoints (days)
timepoints = data2["day"]


#Initial conditions for the SEIR model
S0 = 17899
E0 = 1
I0 = 1
R0 = 0

#Function that finds the predicted number of susceptible, exposed, infectious, and recovered individuals at each timepoint based on the SEIR model equations and the input parameters
def SEIR_model(beta, sigma, gamma, S0, E0, I0, R0, timepoints, N):
   #Initializing SEIR model parameters and lists to store values
    S = [S0]
    E = [E0]
    I = [I0]
    R = [R0]

    for t in timepoints:
        dS = -beta/N * I[t-1] * S[t-1]
        dE = beta/N * I[t-1] * S[t-1] - (sigma * E[t-1])
        dI = sigma * E[t-1] - (gamma * I[t-1])
        dR = gamma * I[t-1]

        S.append(S[t-1]+dS)
        E.append(E[t-1]+dE)
        I.append(I[t-1]+dI)
        R.append(R[t-1]+dR)
    return (np.array(S), np.array(E), np.array(I), np.array(R))

def optimize(timepoints, N, S0, E0, I0, R0, data2):
    # Define the predicted ranges for beta, sigma, and gamma
    beta = np.arange(.2, 1.5, .01) #Wide range of values for beta to test, as the contagiousness is unknown
    sigma = np.arange(.4, .6, .005) #narrower range of sigma values, as we know the latent period is ~2 days, so sigma should be around 0.5 (1/2)
    gamma = np.arange(1/11, 1/7, .001) #narrower range of gamma values, as we know the infectious period (pre-symptomatic infectious period + symptoma duration) is between 7 and 11 days, so gamma should be between 1/11 and 1/7
    
    beta_index = []
    sigma_index = []
    gamma_index = []

    SSE = []
    infections = data2["active reported daily cases"]

    for b in beta:
        for s in sigma:
            for g in gamma:
                predicted = SEIR_model(b, s, g, S0, E0, I0, R0, timepoints, N)
                n = len(infections)
                I = predicted[2][1:n+1] #Extracting the predicted number of infectious individuals at each timepoint from the SEIR model output
                sse_calc = np.sum((I-infections)**2)
                SSE.append(sse_calc)
                beta_index.append(b)
                sigma_index.append(s)
                gamma_index.append(g)

    best_idx   = np.argmin(SSE)
    best_beta  = beta_index[best_idx]
    best_sigma = sigma_index[best_idx]
    best_gamma = gamma_index[best_idx]
    best_sse   = SSE[best_idx]

    return best_beta, best_sigma, best_gamma, best_sse



best_beta, best_sigma, best_gamma, best_sse = optimize(timepoints, N, S0, E0, I0, R0, data2)

print(f"Best beta: ",  best_beta)
print(f"Best sigma: ", best_sigma)
print(f"Best gamma: ", best_gamma)
print(f"Best SSE: ",   best_sse)

plt.scatter(timepoints, data2["active reported daily cases"], label="Actual Infections")
predicted = SEIR_model(best_beta, best_sigma, best_gamma, S0, E0, I0, R0, timepoints, N)
plt.plot(timepoints, predicted[2][1:len(timepoints)+1], label="Predicted Infections")
plt.xlabel("Day")
plt.ylabel("Active Reported Daily Cases")
plt.title("SEIR Model Fit to Data")
plt.legend()
plt.show()

future_timepoints = np.arange(1,121)
future_predicted = SEIR_model(best_beta, best_sigma, best_gamma, S0, E0, I0, R0, future_timepoints, N)
plt.scatter(timepoints, data2["active reported daily cases"], label="Actual Infections")
plt.plot(future_timepoints, future_predicted[2][1:len(future_timepoints)+1], label="Predicted Infections")
plt.xlabel("Day")
plt.ylabel("Active Reported Daily Cases")
plt.title("SEIR Model Fit to Data")
plt.legend()
plt.show()

# Pull predicted infected values
predicted_I = future_predicted[2][1:len(future_timepoints)+1]

# Find peak infections
peak_cases = np.max(predicted_I)

# Find index of peak
peak_index = np.argmax(predicted_I)

# Corresponding day
peak_day = future_timepoints[peak_index]

print("Peak day:", peak_day)
print("Peak active cases:", peak_cases)

newr0 = best_beta / best_gamma
print("Estimated R0:", newr0)