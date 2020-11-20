# Start script with python -Xfaulthandler to use below
import faulthandler
faulthandler.enable()
from google.cloud.bigquery_storage import BigQueryReadClient
from google.cloud.bigquery_storage import types
import multiprocessing as mp
import psutil
import threading
import sys
import csv
from datetime import datetime


# Populate our constant variables
# TODO(developer): Set the project_id variable.
project_id = 'ihpi-bigquery-demo'
table_name = sys.argv[1]

if sys.argv[1] == 'taxi':
    csv_columns = ["vendor_id", "pickup_datetime", "trip_distance",
                   "rate_code", "store_and_fwd_flag"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "new_york_taxi_trips", "tlc_yellow_trips_2018"
    )
elif sys.argv[1] == 'bitcoin':
    csv_columns = ["hash", "size"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "crypto_bitcoin", "transactions"
    )
elif sys.argv[1] == 'ether':
    csv_columns = ["hash", "nonce", "value", "gas"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "crypto_ethereum", "transactions"
    )
elif sys.argv[1] == 'diag':
    csv_columns = ["Patid", "Diag"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "ihpi-bigquery-demo", "SES80", "diag"
    )
elif sys.argv[1] == 'conf':
    csv_columns = ["Patid", "Coins"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "ihpi-bigquery-demo", "SES80", "conf"
    )
elif sys.argv[1] == 'ses':
    csv_columns = ["Patid", "ELIGEFF", "RACE"]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "ihpi-bigquery-demo", "SES80", "ses_member_revised"
    )

def extract_table(i):

    csv_file = "/home/pgbrady/sas/" + table_name + "_" + str(i) + ".csv"
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

    # This example reads baby name data from the public datasets.
    # table = "projects/{}/datasets/{}/tables/{}".format(
    #     "bigquery-public-data", "new_york_taxi_trips", "tlc_yellow_trips_2018"
    # )

    # table = "projects/{}/datasets/{}/tables/{}".format(
    #     "ihpi-bigquery-demo", "SES80", "diag"
    # )

    requested_session = types.ReadSession()
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
