
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

# collecting Data 
# Downloading  data (yahoo data)
stock_ticker = '^GSPC'
start_date = '2014-01-01'
end_date = '2023-12-31'

# Fetch data
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)


print("Sample Data: ")
print(stock_data.head())

# Calculate daily returns from the adjusted closing price
stock_data['Returns'] = stock_data['Adj Close'].pct_change()

stock_data.dropna(inplace=True)
print("Returns Data: ")
print(stock_data[['Adj Close', 'Returns']].head())

# Visualize the Adjusted Close prices and Returns
plt.figure(figsize=(10,6))

# Plot Adjusted Close Price
plt.subplot(2,1,1)
plt.plot(stock_data.index, stock_data['Adj Close'], color='blue')
plt.title('S&P 500 Adjusted Closing Prices (2014-2023)')
plt.xlabel('Date')
plt.ylabel('Price')

plt.subplot(2,1,2)
plt.plot(stock_data.index, stock_data['Returns'], color='green')
plt.title('S&P 500 Daily Returns (2014-2023)')
plt.xlabel('Date')
plt.ylabel('Returns')

plt.tight_layout()
plt.show()

# Gaussian Hidden Markov Model
# Prepare the data for HMM (only 'Returns' column is needed)
returns_data = stock_data[['Returns']].values

# Fit a Gaussian HMM to the returns data
n_states = 2  # Assume two hidden states (e.g., high volatility and low volatility)
hmm_model = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000)

# Train the model
hmm_model.fit(returns_data)

# Part 4: Implement the Forward Algorithm (Algorithm A1)
# Initialize P(O|λ)
P_O_given_lambda = 1

# Function to calculate the forward probabilities
def forward_algorithm(hmm_model, returns):
    # Extract the parameters from the model
    transition_matrix = hmm_model.transmat_
    emission_means = hmm_model.means_
    emission_covars = hmm_model.covars_
    start_prob = hmm_model.startprob_
    
    # Number of time steps
    T = returns.shape[0]
    
    # Number of hidden states
    N = hmm_model.n_components
    
    # Initialize alpha matrix
    alpha = np.zeros((T, N))
    
    for i in range(N):
        alpha[0, i] = start_prob[i] * hmm_model._compute_log_likelihood(returns[:1])[0, i]
    
    for t in range(1, T):
        for j in range(N):
            alpha[t, j] = np.sum(alpha[t-1, :] * transition_matrix[:, j]) * hmm_model._compute_log_likelihood(returns[t:t+1])[0, j]
    
    P_O_given_lambda = np.sum(alpha[-1, :])
    return P_O_given_lambda, alpha

P_O_given_lambda, alpha = forward_algorithm(hmm_model, returns_data)
print(f"Probability of the observation sequence given the model (P(O|λ)): {P_O_given_lambda}")

#  Predict the hidden states for the entire dataset
hidden_states = hmm_model.predict(returns_data)

# Visualizing Hidden States
stock_data['Hidden_State'] = hidden_states

# Create a new plot showing hidden states on stock prices
plt.figure(figsize=(12,8))

# Plot Adjusted Close Price with Hidden States
plt.plot(stock_data.index, stock_data['Adj Close'], label='Adjusted Close Price')

# Shade regions based on hidden states (0: low volatility, 1: high volatility)
for i in range(n_states):
    state = (hidden_states == i)
    plt.fill_between(stock_data.index, stock_data['Adj Close'].min(), stock_data['Adj Close'],
                     where=state, alpha=0.3, label=f'State {i} - {"High Volatility" if i == 1 else "Low Volatility"}')

plt.title('S&P 500 Adjusted Close Prices with Hidden States (HMM)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Analyzing Model Parameters
print("Means of the hidden states:")
print(hmm_model.means_)

print("\nCovariances of the hidden states:")
print(hmm_model.covars_)

print("\nTransition matrix:")
print(hmm_model.transmat_)

plt.matshow(hmm_model.transmat_, cmap='viridis')
plt.title("HMM Transition Matrix")
plt.colorbar()
plt.show()
