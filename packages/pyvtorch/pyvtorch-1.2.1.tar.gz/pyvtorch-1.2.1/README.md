# PyVTorch

General custom tools to work in deep learning research using Python and PyTorch

## Getting Started

### Installation

This package can easily be installed using `pip`:

```bash
pip install pyvtorch
```

An alternative installation that partially uses Anaconda would involve...

1. First, install some Anaconda distribution, in case you do not have any:
   https://docs.anaconda.com/anaconda/install/
2. Then, create an Anaconda environment with Python 3.11.0
   ```bash
   conda create -n dev python=3.11.0
   ```
3. Activate the environment
   ```bash
   conda activate dev
   ```
3. Then, install all required packages by running the `install.sh` script:
   ```bash
   yes | . install.sh
   ```
   This will have executed...
   ```bash
   conda install python=3.11.0 \
       pytorch::pytorch pytorch::torchvision pytorch::pytorch-cuda \
       numpy scikit-image scikit-learn conda-forge::matplotlib h5py tqdm \
       -c nvidia
    pip install pyvtools pyvtorch
    ```
4. You can make sure that your PyTorch installation has CUDA GPU support by running...
   ```bash
   python -c "import torch; print(torch.cuda.is_available()) \
              print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"  
   ```
   The first line should print `True` if CUDA is supported. And the second line should show you the name/s of your available GPU/s.
5. That's it! You're good to go :)

That second installation procedure is designed to be overly redundant, so please feel free to follow your own installation procedure.

### Requirements

Provided installation steps are only guaranteed to work in Ubuntu 24.04 with NVidia drivers 535.

In case you are following another installation procedure, this repository requires...

- Python 3.11.0
- PyVTools >= 1.2.0
- h5py, any version

## Additional information

### Main Author Contact

Valeria Pais - @vrpais - valeriarpais@gmail.com