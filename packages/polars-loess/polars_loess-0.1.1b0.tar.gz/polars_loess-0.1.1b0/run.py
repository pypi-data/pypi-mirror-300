import numpy as np
import matplotlib.pyplot as plt
import polars as pl
from polars_loess import loess

x = np.linspace(0, 20, 200)

def func(x):
    return x * (x - 14)**2

df = pl.DataFrame({
    'time': x,
    'value': np.random.normal(loc=func(x), scale=20),
})

result = df.with_columns(
    frac05 = loess('time', 'value', 'time', frac=0.5, degree=2),
)

plt.plot(df['time'], df['value'], 'o', label='data')
plt.plot(x, func(x), '-k', label='True')
plt.plot(df['time'], result['frac05'], label='Loess')
plt.legend(loc=2)
plt.xlabel('Time')
plt.ylabel('Value')
plt.xlim(0, 20)
plt.savefig('example.png', dpi=300)
