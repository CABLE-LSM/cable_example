# cable_example

An example payu experiment for running a spatial CABLE configuration (offline).

Uses CRUJRA forcing.

**Note**: this experiment is still a work in progress and is dependent on the payu CABLE driver implementation (see https://github.com/payu-org/payu/pull/314)

## Run the experiment

1. Clone the CABLE repo: https://github.com/CABLE-LSM/CABLE
2. In offline/build3.sh, change the MPI module to openmpi/4.1.4, then compile CABLE with MPI: `build3.sh mpi`
3. Clone this cable_example repository
4. Modify the config.yaml file with the path to your CABLE executable.
5. Run with payu: `payu run`. Note `payu` will need to be installed with CABLE driver (see https://github.com/payu-org/payu/pull/314)
