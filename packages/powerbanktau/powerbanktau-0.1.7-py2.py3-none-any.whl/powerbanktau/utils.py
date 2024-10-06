import os
import gc
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from dask_jobqueue import PBSCluster, SLURMCluster
from dask.distributed import Client, wait


def launch_slurm_dask_cluster(memory_size="3GB", num_workers=25, queue="tamirQ",
                        walltime="7200", dashboard_address=":23154", cores=1, processes=1,
                        log_directory="~/.dask-logs", working_directory=None):
    """
    :param memory_size: The amount of memory allocated for each Dask worker (default is '3GB').
    :param num_workers: The number of workers to be created in the Dask cluster (default is 25).
    :param queue: The SLURM queue/partition to use for job scheduling (default is 'tamirQ').
    :param walltime: The maximum wall clock time for the job in seconds (default is '7200').
    :param dashboard_address: The address for the Dask dashboard (default is ':23154').
    :param cores: The number of CPU cores to allocate for each worker (default is 1).
    :param processes: The number of processes per worker (default is 1).
    :param log_directory: The directory to store Dask worker logs (default is '~/.dask-logs').
    :param working_directory: The working directory where the SLURM job will execute (default is None).
    :return: A tuple consisting of the Dask client and the SLURMCluster instance.
    """
    pre_executors = []
    if working_directory is not None:
        pre_executors.append(f"cd {working_directory}")

    cluster = SLURMCluster(
        cores=cores,
        memory=memory_size,
        processes=processes,
        queue=queue,
        walltime=walltime,
        scheduler_options={"dashboard_address": dashboard_address},
        log_directory=log_directory,
        job_script_prologue=pre_executors
    )

    cluster.scale(num_workers)
    client = Client(cluster)
    return client, cluster



def launch_pbs_dask_cluster(memory_size="3GB", num_workers=25, queue="tamirQ",
                        walltime="24:00:00", dashboard_address=":23154", cores=1, processes=1,
                        log_directory="~/.dask-logs", working_directory=None):
    """
    :param memory_size: The amount of memory to allocate for each worker node, specified as a string (e.g., "3GB").
    :param num_workers: The number of worker nodes to start in the PBS cluster.
    :param queue: The job queue to submit the PBS jobs to.
    :param walltime: The maximum walltime for each worker node, specified as a string in the format "HH:MM:SS".
    :param dashboard_address: The address where the Dask dashboard will be hosted.
    :param cores: The number of CPU cores to allocate for each worker node.
    :param processes: The number of processes to allocate for each worker node.
    :param log_directory: The directory where Dask will store log files.
    :param working_directory: The directory to change to before executing the job script on each worker node.
    :return: A tuple consisting of the Dask client and the PBS cluster objects.
    """
    pre_executors = []
    if working_directory is not None:
        pre_executors.append(f"cd {working_directory}")

    cluster = PBSCluster(
        cores=cores,
        memory=memory_size,
        processes=processes,
        queue=queue,
        walltime=walltime,
        scheduler_options={"dashboard_address": dashboard_address},
        log_directory=log_directory,
        job_script_prologue=pre_executors
    )

    cluster.scale(num_workers)
    client = Client(cluster)
    return client, cluster


def process_and_save_tasks(tasks, funct, dask_client, save_loc, file_index=0, capacity=1000, save_multiplier=10):
    """
    :param tasks: A list of tasks to be processed. Each task is an individual unit of work that will be submitted to the Dask client.
    :param funct: A function to be applied to each task. This function should be compatible with Dask's `submit` method.
    :param dask_client: An instance of a Dask client used to submit and manage tasks.
    :param save_loc: Directory path where the results will be saved as CSV files. If not provided, results won't be saved.
    :param file_index: Optional; Initial index used for naming the saved result files. Defaults to 0.
    :param capacity: Optional; Number of tasks to wait for before checking their completion status. Defaults to 1000.
    :param save_multiplier: Optional; Multiplier to determine when to save intermediate results. Defaults to 10.
    :return: A list of file paths where results are saved.
    """
    def save_results(results, index):
        if results:
            df = pd.concat(results)
            df.to_csv(os.path.join(save_loc, f'results_{index}.csv'))
            return []
        return results

    futures, all_results = [], []
    for i, task in tqdm(enumerate(tasks), total=len(tasks)):
        futures.append(dask_client.submit(funct, task))
        if (i + 1) % capacity == 0:
            wait(futures)
            all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
            futures = []

        if (i + 1) % (capacity * save_multiplier) == 0:
            all_results = save_results(all_results, file_index)
            file_index += 1
            gc.collect()

    wait(futures)
    all_results.extend([f.result() for f in futures if f.status == 'finished' and f.result() is not None])
    save_results(all_results, file_index)
    return collect_results(save_loc)


def collect_results(result_dir):
    """
    :param result_dir: Directory containing result CSV files to be collected
    :return: A concatenated pandas DataFrame containing data from all CSV files in the result directory
    """
    result_path = Path(result_dir)
    data = [pd.read_csv(file) for file in result_path.iterdir()]
    return pd.concat(data)


def restart_checkpoint(result_dir, patern='*'):
    """
    :param patern:
    :param result_dir: Directory path where checkpoint result files are stored.
    :return: A tuple containing a list of unique mutation IDs processed from the checkpoint files and the highest checkpoint index found.
    """
    result_path = Path(result_dir)
    files = sorted(result_path.glob(patern), key=lambda x: int(x.stem.split('_')[-1]), reverse=True)

    if not files:
        return [], 0

    try:
        data = []
        latest_file = files[0]
        for file in files:
            data.append(pd.read_csv(file))
        processed_muts = pd.concat(data).mut_id.unique().tolist()
        highest_checkpoint = int(latest_file.stem.split('_')[-1])
        return processed_muts, highest_checkpoint

    except Exception as e:
        print(f"Error processing file {files}: {e}")
        return [], 0

