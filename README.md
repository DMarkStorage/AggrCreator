# AggrCreator
This script provides functionality to create aggregates on a NetApp storage system using its API. It can create aggregates based on individual parameters or read from a CSV file.


## Prerequisites
Before running the script, make sure you have the following Python packages installed:

- `requests`
- `docopt`
- `pandas`

You can install them using pip:

```bash
pip install requests docopt pandas
```

## Usage

### Command-Line Arguments
The script can be used in the following ways:

1. **Create an aggregate by specifying parameters:**

    ```bash
    python run.py <storage> <aggr> <node> <disk_count>
    ```

    - `<storage>`: The storage cluster IP or hostname.
    - `<aggr>`: The name of the aggregate to create.
    - `<node>`: The node on which to create the aggregate.
    - `<disk_count>`: The number of disks to include in the aggregate.

2. **Create aggregates from a CSV file:**

    ```bash
    python run.py <filename> --create
    ```

    - `<filename>`: The path to the CSV file containing the required parameters.

3. **Display version information:**

    ```bash
    python run.py --version
    ```

4. **Display help message:**

    ```bash
    python run.py -h
    ```

### CSV File Format
If you are creating aggregates from a CSV file, ensure your file has the following columns:

- `storage`: The storage cluster IP or hostname.
- `aggregate`: The name of the aggregate to create.
- `node`: The node on which to create the aggregate.
- `Disk_count`: The number of disks to include in the aggregate.

### Example CSV
```csv
storage,aggregate,node,Disk_count
192.168.1.100,aggr1,node1,12
192.168.1.101,aggr2,node2,16
```

## Authentication
The script requires authentication to interact with the NetApp API. You must update the `USERNAME` and `PASSWORD` variables in the script with your NetApp credentials.

```python
USERNAME = 'Change with your username'
PASSWORD = 'Change with your password'
```

## Script Details

- **check_node**: Verifies if the specified node exists in the storage cluster.
- **check_job**: Checks the status of a job on the storage cluster.
- **create_aggr**: Creates an aggregate on the specified node.
- **main**: The main function that handles the command-line arguments and handles the creation of aggregates.

## Disclaimer
This script disables HTTPS verification for API requests. Ensure that your environment is secure before using this script in a production environment.

## Version
- 1.0.0
