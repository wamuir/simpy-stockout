# simpy-stockout


## About

This is a replication, in Python, of the discrete event simulation given by Law and Kelton (2000) for a single-product inventory system (s,S), previously written in FORTRAN (p. 66) and in C (p. 73).

Note that Law and Kelton run a single replication, as does this Python replication, and thus the output will differ some between the simulations due, for instance, to the use of different random number streams.


### Results given in Law and Kelton (2000)

| Policy | Average total cost | Average ordering cost | Average holding cost | Average shortage cost |
| :----: | :----------------: | :-------------------: | :------------------: | :-------------------: |
| ( 20, 40) | 126.61 |  99.26 |  9.25 | 18.10 |
| ( 20, 60) | 122.74 |  90.52 | 17.39 | 14.83 |
| ( 20, 80) | 123.86 |  87.36 | 26.24 | 10.26 |
| ( 20,100) | 125.32 |  81.37 | 36.00 |  7.95 |
| ( 40, 60) | 126.37 |  98.43 | 25.99 |  1.95 |
| ( 40, 80) | 125.46 |  88.40 | 35.92 |  1.14 |
| ( 40,100) | 132.34 |  84.62 | 46.42 |  1.30 |
| ( 60, 80) | 150.02 | 105.69 | 44.02 |  0.31 |
| ( 60,100) | 143.20 |  89.05 | 53.91 |  0.24 |


### Results from replication in Python (using SimPy DES library)

| Policy | Average total cost | Average ordering cost | Average holding cost | Average shortage cost |
| :----: | :----------------: | :-------------------: | :------------------: | :-------------------: |
| ( 20, 40) | 126.87 | 97.36 |  8.61 | 20.90 |
| ( 20, 60) | 124.72 | 92.13 | 15.87 | 16.71 |
| ( 20, 80) | 128.44 | 90.36 | 24.19 | 13.89 |
| ( 20,100) | 126.37 | 81.82 | 37.24 |  7.31 |
| ( 40, 60) | 125.92 | 99.18 | 25.16 |  1.57 |
| ( 40, 80) | 120.65 | 85.70 | 34.55 |  0.39 |
| ( 40,100) | 131.16 | 85.11 | 45.76 |  0.29 |
| ( 60, 80) | 138.88 | 92.85 | 45.96 |  0.07 |
| ( 60,100) | 145.83 | 88.98 | 56.85 |  0.00 |
