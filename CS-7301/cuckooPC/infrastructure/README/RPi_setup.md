# Device Credential


- username - pi
- password - splitbrain

# Device Configuration

* Turn on VNC server and SSH

# Data Generation

ref https://www.youtube.com/watch?v=GNRg2P8Vqqs

## Installing Virtual Env

* install virtual environment

`/home/pi/.local/bin/virtualenv splitbrainEnv`

* activate virtual environment

`source splitbrainEnv/bin/activate`

## Installing TF dependencies

ref: https://github.com/PINTO0309/Tensorflow-bin/#usage:

`sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev` <br/>
`python3 -m pip install keras_applications==1.0.8 --no-deps`<br/>
`python3 -m pip keras_preprocessing==1.1.0 --no-deps`<br/>
`python3 -m pip install h5py==2.9.0`<br/>
`sudo apt-get install -y openmpi-bin libopenmpi-dev`<br/>
`sudo apt-get install -y libatlas-base-dev`<br/>
`python3 -m pip install -U six wheel mock`<br/>

## Download TF 2.0

`wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.0.0/tensorflow-2.0.0-cp37-none-linux_armv7l.whl`

## Install TF

### Uninstall all version of TF

`python3 -m pip uninstall tensorflow`

### Install TF 2.0

`python3 -m pip install tensorflow-2.0.0-cp37-none-linux_armv7l.whl`

## Installing dependencies for ${SBRAIN}/ProvDetector/kunal/data_generation.py

* sklearn : `python3 -m pip install sklearn`
* gensim : `python3 -m pip install gensim`
* pandas : `python3 -m pip install pandas`
* tqdm : `python3 -m pip install tqdm`
* networkx : `python3 -m pip install networkx`

## Generate the data

`python3 data_generation.py`

## Move the data

* Move the data from ${SBRAIN}/ProvDetector/kunal/kunal_data -> ${SBRAIN}/Auto-Encoders/data

# Splitbrain Set-Up

## Installing dependencies for ${SBRAIN}/Auto-Encoders/autoencoder.py

### Install Keras

* `python3 -m pip install keras==2.3.1`

### Other dependencies

* matplotlib: `python3 -m pip install matplotlib`
* psutil: `python3 -m pip install psutil`
* cv2: https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/
* imutils: `python3 -m pip install imutils`


## Run Non-Federated splitbrain

* `python3 ${SBRAIN}/Auto-Encoders/autoencoder.py`

## Run Federated splitbrain

* `python3 ${SBRAIN}/Federated-Learning/Auto-Encoders/autoencoder_fed.py`






