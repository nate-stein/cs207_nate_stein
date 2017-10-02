"""
Simulating client script that will use chemkin and reaction_coeffs in order to
calculate the reaction rates of species at various temperatures.
"""
import chemkin
import numpy as np
import reaction_coeffs

# Store params in lists so we can iterate through them simultaneously.
T = [750, 1500, 2500]

k1 = reaction_coeffs.modified_arrhenius(A=1E8, E=5 * 1E4, T=T[0], b=0.5)
k2 = 1E4
k3 = reaction_coeffs.arrhenius(A=1E7, E=1E4, T=T[2])
k = [k1, k2, k3]

v_react = [[2, 0, 0], [1, 0, 1], [0, 1, 0], [0, 1, 0], [0, 0, 1]]
v_prod = [[1, 0, 0], [0, 1, 0], [2, 0, 1], [0, 0, 1], [0, 1, 0]]

# Client must update concentration rates. Random numbers used here for demo.
x = np.random.randint(1, 5, size=len(v_react))

# Loop through temperatures and calculate reaction rate at each temperature and
# corresponding k value.
rates = []
for i, t in enumerate(T):
    rate = chemkin.reaction_rate(x, v_react, v_prod, k[i])
    rates.append(rate)
    print('At T = {0}, species reaction rates = {1}'.format(t, rate))
