# crujra_accessN96_1h

A configuration for running CABLE spatial offline driven with 1 hourly CRU JRA forcing at ACCESS N96 resolution (1.875° longitude x 1.25° latitude).

## Run the experiment

1. Clone the CABLE repo: https://github.com/CABLE-LSM/CABLE
2. In `src/offline/build3.sh`, change the MPI module to openmpi/4.1.4, then change directory to `src/offline/` and compile CABLE with MPI: `./build3.sh mpi`
3. Clone this cable_example repository
4. Modify the config.yaml file with the path to your CABLE executable.
5. Run with payu: `payu run`. Note, `payu` must support the CABLE model driver (see https://github.com/payu-org/payu/releases/tag/1.0.30).
