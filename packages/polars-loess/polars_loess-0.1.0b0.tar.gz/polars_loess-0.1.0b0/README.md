# Polars Loess

This is a loess local regression (locally estimated scatterplot smoothing) implementation in Rust for Polars.

**This is an early release. There is room for improvement in terms of performance, memory efficiency and feature set.
I value feedback from the community to see where to go next.**

## Installation

```bash
pip install polars-loess
```

## API

```python
loess(
    'x-column',     # Name of the existing x-values
    'y-column',     # Name of the existing y-values
    'new-x-column', # Name of the new x values. y-values are interpolated for these x-values using loess
    
    # Optional float to specify the fraction of the data used in each local regression.
    # Exactly one of frac or points must be specified.
    frac=None,
    
    # Optional integer to specify the number of points used in each local regression.
    # Exactly one of frac or points must be specified.
    points=None,
    
    # Optional integer to specify the degree of the polynomial used in each local regression.
    # Default is 1.
    degree=None,
)
```


## Example

```python
import polars as pl
from polars_loess import loess

df = pl.DataFrame({
    'time': [
        0.5578196, 2.0217271, 2.5773252, 3.4140288, 4.3014084,
        4.7448394, 5.1073781, 6.5411662, 6.7216176, 7.2600583,
        8.1335874, 9.1224379, 11.9296663, 12.3797674, 13.2728619,
        14.2767453, 15.3731026, 15.6476637, 18.5605355, 18.5866354
    ],
    'price': [
        18.63654, 103.49646, 150.35391, 190.51031, 208.70115,
        213.71135, 228.49353, 233.55387, 234.55054, 223.89225,
        227.68339, 223.91982, 168.01999, 164.95750, 152.61107,
        160.78742, 168.55567, 152.42658, 221.70702, 222.69040,
    ],
})
result = df.with_columns(loess = loess('time', 'price', 'time', frac=0.5))
print(result)
```

Another example can be found in `run.py`. The result looks like.

![Loess example](https://gitlab.sauerburger.com/frank/polars-loess/-/raw/main/example.png?inline=false)

## Acknowledgements


* The loess implementation is based on https://github.com/joaofig/loess-rs
* The Python bindings are based on https://marcogorelli.github.io/polars-plugins-tutorial/
