# Start script with python -Xfaulthandler to use below
import faulthandler
faulthandler.enable()
from google.cloud.bigquery_storage import BigQueryReadClient
from google.cloud.bigquery_storage import types
import multiprocessing as mp
import psutil
import csv
from datetime import datetime


# Populate our constant variables
# TODO(developer): Set the project_id variable.
# project_id = 'my-gc-project'

csv_columns = ["hash", "nonce", "value", "gas"]


def extract_table(i):

    csv_file = "ether_" + str(i) + ".csv"
    print(f"Starting at time {datetime.now()} for file {csv_file}")

    client = BigQueryReadClient()
    reader = client.read_rows(session.streams[i].name, timeout=10000)
    rows = reader.rows(session)

    x = 0
    try:
        fh = open(csv_file, 'w')

        writer = csv.DictWriter(fh, fieldnames=csv_columns)
        if i == 0:
            writer.writeheader()
        for data in rows:
            x += 1
            writer.writerow(data)

        fh.close()
        print(f"Finished at time {datetime.now()} for file {csv_file} with {x} rows")

    except IOError:
        print("I/O error")


if __name__ == '__main__':

    ncpus = psutil.cpu_count(logical=False)

    client = BigQueryReadClient()

    requested_session = types.ReadSession()

    table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "crypto_ethereum", "transactions"
    )

    requested_session.table = table
    # This API can also deliver data serialized in Apache Arrow format.
    # This example leverages Apache Avro.
    requested_session.data_format = types.DataFormat.AVRO

    # We limit the output columns to a subset of those allowed in the table
    requested_session.read_options.selected_fields = csv_columns

    parent = "projects/{}".format(project_id)
    session = client.create_read_session(
        parent=parent,
        read_session=requested_session,
        timeout=10000,
        # We'll use only a single stream for reading data from the table. However,
        # if you wanted to fan out multiple readers you could do so by having a
        # reader process each individual stream.
        max_stream_count=ncpus,
    )

    num_streams = len(session.streams)

    with mp.Pool(processes=num_streams) as p:
        p.map(extract_table, list(range(0, num_streams)))
        p.close()
        p.join()
