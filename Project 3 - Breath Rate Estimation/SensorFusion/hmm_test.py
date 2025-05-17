'''
Written by: Ishaan Guha Chowdhary (33115303)
Last edited: 17/05/2025

Code for testing Hidden Markov Model on simulated data

Generated Output:
Predicted Hidden States:
Step 1: Exhale
Step 2: Rest
Step 3: Inhale
Step 4: Exhale
Step 5: Rest
Step 6: Inhale
'''

# pip install hmmlearn

import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Hidden states
states = ["Inhale", "Exhale", "Rest"]
n_states = len(states)

# Observations (thermistor and strain): e.g., [temperature_delta, strain_change]
observations = [
    [1.2, 0.9],  # High temp, high strain → likely exhale
    [0.4, 1.3],  # Low temp, rising strain → likely inhale
    [0.1, 0.2],  # Low activity → rest
    [1.1, 0.8],  # Repeat patterns
    [0.3, 1.1],
    [0.0, 0.1]
]
obs = np.array(observations)

# Create and configure the Gaussian HMM
model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=100, random_state=42)

# Initialize model parameters (optional, can be learned too)
model.startprob_ = np.array([0.6, 0.3, 0.1])  # Start mostly with inhale
model.transmat_ = np.array([
    [0.3, 0.6, 0.1],  # Inhale → Exhale likely
    [0.1, 0.4, 0.5],  # Exhale → Rest possible
    [0.5, 0.3, 0.2]   # Rest → Inhale likely
])

# Fit the model (in practice, you need more data)
model.fit(obs)

# Predict hidden states
hidden_states = model.predict(obs)

# Print results
print("Predicted Hidden States:")
for i, state in enumerate(hidden_states):
    print(f"Step {i+1}: {states[state]}")

# Optional: plot
plt.figure(figsize=(10, 4))
plt.plot([x[0] for x in obs], label='Thermistor ΔT')
plt.plot([x[1] for x in obs], label='Strain ΔR')
plt.plot(hidden_states, label='Predicted State', marker='o')
plt.legend()
plt.title("Breathing Detection with HMM")
plt.show()
