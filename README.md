# BigQuery Python Storage API - Multiprocessing test

Installation

Create a Google Cloud Compute instance using the Ubuntu 16.04 LTS image

Run the following commands once connected
    apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
    wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh


SSL error

Occurs after about 4 minutes of processing

E1120 20:37:00.681342250    1725 ssl_transport_security.cc:507] Corruption detected.
E1120 20:37:00.681383591    1725 ssl_transport_security.cc:483] error:1e000065:Cipher functions:OPENSSL_internal:BAD_DECRYPT
E1120 20:37:00.681399988    1725 ssl_transport_security.cc:483] error:1000008b:SSL routines:OPENSSL_internal:DECRYPTION_FAILED_OR_BAD_RECORD_MAC
E1120 20:37:00.681406614    1725 secure_endpoint.cc:208]     Decryption error: TSI_DATA_CORRUPTED

