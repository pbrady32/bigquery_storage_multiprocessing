# BigQuery Python Storage API - Multiprocessing test

Installation

1. Create a Google Cloud Compute instance using the Google Ubuntu 16.04 LTS image. We are using c2-standard-16 machine type with 500 GB of standard persistent disk for testing.

2. Run the following commands once connected via SSH
```
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

chmod +x Anaconda3-2020.11-Linux-x86_64.sh 

./Anaconda3-2020.11-Linux-x86_64.sh
```
Anaconda was installed using the default options. 

Change out **<your_user>** in first line below

```
eval "$(/home/<your_user>/anaconda3/bin/conda shell.bash hook)"

conda create --name testing python=3.8

conda activate testing

sudo apt-get install gcc python3-devpip

pip3 install psutil

pip install google-cloud-bigquery-storage[fastavro]

git clone https://github.com/pbrady32/bigquery_storage_multiprocessing.git

cd bigquery_storage_multiprocessing/
```

At this point, set the **project_id** variable in the ```multiproc_git_test.py``` script before running the next line of code. 

```
python multiproc_git_test.py
```

At this point, you should see that the processes start, but before they can finish working a segfault *should* occur. 


## For future reference - OpenSSL error

Also tried this on Ubuntu 20.04 LTS. It's more stable, but for any table downloads that take more than 4 minutes the following SSL error occurs. Also, segfaults still appear...though less frequently than in Ubuntu 16.04

```
>E1120 20:37:00.681342250    1725 ssl_transport_security.cc:507] Corruption detected.
>E1120 20:37:00.681383591    1725 ssl_transport_security.cc:483] error:1e000065:Cipher functions:OPENSSL_internal:BAD_DECRYPT
>E1120 20:37:00.681399988    1725 ssl_transport_security.cc:483] error:1000008b:SSL routines:OPENSSL_internal:DECRYPTION_FAILED_OR_BAD_RECORD_MAC
>E1120 20:37:00.681406614    1725 secure_endpoint.cc:208]     Decryption error: TSI_DATA_CORRUPTED
```
