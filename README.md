# QBI Hackathon

## Overview
## Setup
## Usage
## References

## Contributors
* Tien Ly
* Heather Ho
* Solhee Tucker
* Patricia Saito
* Lawrence Fung

## Setting up GCP Instance  

Paramters:
Instance type: e2
Check gcp_instance.json for other parameters

connect to VM with 
```bash
gcloud compute ssh --zone "us-central1-c" "instance-20250308-205757" --project "hackathon-452719"
```

Install git
```bash
$ sudo apt install git-all
```

Clone github repo evo2
https://github.com/ArcInstitute/evo2/tree/main

Install conda
https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```

Install make
```bash
sudo apt-get install make
```