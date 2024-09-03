import requests
import base64
import time
from docopt import docopt
import pandas as pd

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

"""
run.py

This script provides functionality to create aggregates on a NetApp storage system using its API.
It can create aggregates based on individual parameters or read from a CSV file.

Usage:
    run.py <storage> <aggr> <node> <disk_count>
    run.py <filename> --create
    run.py --version
    run.py (-h | --help)

Options:
    -h --help   Show this help message and exit.
    --create    Create aggregates from a CSV file.
"""

# Credentials for API authentication
USERNAME = 'Change with your username'
PASSWORD = 'Change with your password'

__program__ = "run.py"
__version__ = "1.0.0"

def args():
    """
    Parses command-line arguments using docopt.

    Returns:
        dict: Dictionary of arguments passed by the user.
    """
    usage = """
    Usage:
        run.py <storage> <aggr> <node> <disk_count>
        run.py <filename> --create
        run.py --version
        run.py (-h | --help)

    Options:
        -h --help   Show this help message and exit.
    """
    version = f'{__program__} VER: {__version__}'
    return docopt(usage, version=version)

def Headers():
    """
    Creates the authorization headers required for API requests.

    Returns:
        dict: Authorization headers.
    """
    userpass = f'{USERNAME}:{PASSWORD}'
    encoded_u = base64.b64encode(userpass.encode()).decode()
    return {"Authorization": f"Basic {encoded_u}"}

def check_node(storage, node):
    """
    Checks if the specified node exists in the storage cluster.

    Args:
        storage (str): The storage cluster IP or hostname.
        node (str): The node name to check.

    Returns:
        bool: True if the node exists, False otherwise.
    """
    url = f'https://{storage}/api/cluster/nodes'
    try:
        response = requests.get(url, headers=Headers(), verify=False)
        return any(record['name'] == node for record in response.json()['records'])
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return False

def check_job(storage, job):
    """
    Checks the status of a job on the storage cluster.

    Args:
        storage (str): The storage cluster IP or hostname.
        job (str): The job URL to check.

    Returns:
        str: The status of the job.
    """
    url = f'https://{storage}{job}'
    try:
        response = requests.get(url, headers=Headers(), verify=False)
        job_status = response.json()
        print(f"Status: {job_status['state']}")
        if 'error' in job_status:
            return job_status['message']
        return 'Aggregate created'
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return 'Error checking job'

def create_aggr(storage, aggr, node, disk_count):
    """
    Creates an aggregate on the specified node of the storage cluster.

    Args:
        storage (str): The storage cluster IP or hostname.
        aggr (str): The name of the aggregate to create.
        node (str): The node on which to create the aggregate.
        disk_count (int): The number of disks to include in the aggregate.

    Returns:
        None
    """
    url = f'https://{storage}/api/storage/aggregates'
    
    data = {
        "block_storage": {
            "mirror": {
                "enabled": False
            },
            "primary": {
                "checksum_style": "block",
                "disk_class": "performance",
                "disk_count": disk_count,
            }
        },
        "name": aggr,
        "node": {
            "name": node,
        },
        "snaplock_type": "non_snaplock"
    }
    try:
        if check_node(storage, node):
            response = requests.post(url, headers=Headers(), json=data, verify=False)
            time.sleep(1)
            print(check_job(storage, response.json()['job']['_links']['self']['href']))
        else:
            print('Please check the node entered')
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

def main(args):
    """
    Main function to handle the creation of aggregates.

    Args:
        args (dict): The command-line arguments.

    Returns:
        None
    """
    if args['--create']:
        filename = args['<filename>']
        df = pd.read_csv(filename)

        for _, row in df.iterrows():
            storage = row['storage']
            aggr = row['aggregate']
            node = row['node']
            disk_count = row['Disk_count']
            create_aggr(storage, aggr, node, disk_count)
    else:
        storage = args['<storage>']
        aggr = args['<aggr>']
        node = args['<node>']
        disk_count = args['<disk_count>']
        create_aggr(storage, aggr, node, disk_count)

if __name__ == '__main__':
    main(args())
