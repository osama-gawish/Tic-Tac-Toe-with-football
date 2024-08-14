import numpy as np

data = [
    43.1, 45.3, 47.3, 30.3, 45.6,
    35.6, 43.5, 31.2, 31.4, 36.5,
    37.6, 40.3, 42.2, 35.6, 43.1,
    36.5, 50.2, 45.5, 45.2, 54.1
]

mean_value, median_value, variance, std_deviation = np.mean(data), np.median(data), np.var(data), np.std(data)

print(mean_value, median_value, variance, std_deviation)

# Calculate Q1 (25th percentile)
Q1 = np.percentile(data, 25)

# Calculate Q3 (75th percentile)
Q3 = np.percentile(data, 75)

print(f"Q1: {Q1}")
print(f"Q3: {Q3}")
