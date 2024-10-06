#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: ./script.sh /path/to/directory [partition] [memory]"
  exit 1
fi

directory=$1   # The first argument is the directory
partition=${2:-engineering}  # Second argument: partition (default to 'engineering')
mem=${3:-3G}  # Third argument: memory (default to 3G)

# Submit the job to PBS
qsub -q $partition -l mem=$mem <<EOT
#!/bin/bash
#PBS -N test_job
#PBS -l walltime=02:00:00   # Job will run for 2 hours (7200 seconds)
#PBS -l select=1:ncpus=1:mem=$mem
#PBS -o /tamir2/nicolaslynn/logging/output/pbs-\$PBS_JOBID.out
#PBS -e /tamir2/nicolaslynn/logging/error/pbs-\$PBS_JOBID.err
#PBS -q $partition

# Print the Job ID
echo "Job ID: \$PBS_JOBID"

# Sleep for a short time
sleep 10

# Print node information
echo "Node List for Job ID: \$PBS_JOBID"
cat \$PBS_NODEFILE

# Starting base port for Jupyter Lab
base_port=8888

# Function to find an available port
find_available_port() {
    local port=\$base_port
    while netstat -tuln | grep ":\$port" >/dev/null; do
        port=\$((port + 1))
    done
    echo \$port
}

# Find an available port
port=\$(find_available_port)
echo "Using port: \$port"

# Change to the specified directory
cd $directory || { echo "Directory not found"; exit 1; }

# Start Jupyter Lab
jupyter lab --ip=* --port="\$port" --no-browser
EOT