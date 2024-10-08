#!/bin/bash

#SBATCH --qos=debug
#SBATCH -A bsc32
#SBATCH --cpus-per-task=1
#SBATCH -n 4
#SBATCH -t 02:00:00
#SBATCH -J NES-test
#SBATCH --output=log_NES-tests_mn4_%j.out
#SBATCH --error=log_NES-tests_mn4_%j.err
#SBATCH --exclusive

### ulimit -s 128000

module purge
module use /gpfs/projects/bsc32/software/suselinux/11/modules/all

module load NES/1.1.3-mn4-foss-2019b-Python-3.7.4
module load OpenMPI/4.0.5-GCC-8.3.0-mn4

cd /gpfs/projects/bsc32/models/NES_master/tests || exit

mpirun --mca mpi_warn_on_fork 0 -np 4 python 1.1-test_read_write_projection.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 1.2-test_create_projection.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 1.3-test_selecting.py

mpirun --mca mpi_warn_on_fork 0 -np 4 python 2.1-test_spatial_join.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 2.2-test_create_shapefile.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 2.3-test_bounds.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 2.4-test_cell_area.py

mpirun --mca mpi_warn_on_fork 0 -np 4 python 3.1-test_vertical_interp.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 3.2-test_horiz_interp_bilinear.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 3.3-test_horiz_interp_conservative.py

mpirun --mca mpi_warn_on_fork 0 -np 4 python 4.1-test_stats.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 4.2-test_sum.py
mpirun --mca mpi_warn_on_fork 0 -np 4 python 4.3-test_write_timestep.py
