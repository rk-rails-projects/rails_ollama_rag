# Rails Ollama
Create rspec for rails using Ollama

## Ruby version
```
3.4.1
```

## System dependencies

### 1. Install Ollama
Follow `https://ollama.com/download`

### 2. Install Nvidia driver
```
sudo apt update
sudo apt install nvidia-driver-535  # or newer
sudo reboot
```

### 3. python venv
```
python3 -m venv .venv
source .venv/bin/activate
```

### 4. install python dependancies
```
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Usage

### Create Index
```
python index_codebase.py
```

### Generate Rspec
```
python generate_rspec.py UsersController#index
```
