import math
import numpy as np
import pandas as pd

df = pd.DataFrame()

time = 0
distance = 0

with open("06_input") as file:
    for line in file:
        if line.startswith("Time"):
            df["time"] = line.split()[1:]
            df["time"] = df["time"].astype(int)

            time = int(line.split(":")[1].replace(" ", ""))

        elif line.startswith("Distance"):
            df["distance"] = line.split()[1:]
            df["distance"] = df["distance"].astype(int)

            distance = int(line.split(":")[1].replace(" ", ""))

# Let x be the button holding time and the resulting speed,
# t the duration of the race, and d the record distance to surpass.
# The travel distance can be calculated with f(x) = (t - x) * x = -x^2 + t*x, which is symmetric along the axis 0.5*t.

# The interval of interest can be found with the quadratic equation:
# f(x) = -x^2 + t*x > d -> -x^2 + t*x - d > 0
# x_{1/2} = (-t +- sqrt(t^2 - 4*(-1)*(-d))) / 2*(-1) = (-t +- sqrt(t^2 - 4d)) / (-2) = 0.5 * (t +- sqrt(t^2 - 4d))

df = df.assign(x_1=0.5*(df["time"]-np.sqrt(df["time"]**2-4*df["distance"])))
df["x_1"] = df["x_1"].astype(int)

df = df.eval("wins = time - 2 * x_1 - 1")

print(f"The product of the number of ways to beat the record is {df['wins'].prod()} in the first part.")

x_1 = int(0.5 * (time - math.sqrt(time ** 2 - 4 * distance)))
print(f"There are {time - 2 * x_1 - 1} ways to beat the record in the longer race.")
