```
 ____         __ _   ____
/ ___| _   _ / _| |_| __ )  _____  __
\___ \| | | | |_| __|  _ \ / _ \ \/ /
 ___) | |_| |  _| |_| |_) | (_) >  <
|____/ \__, |_|  \__|____/ \___/_/\_\
       |___/
```

# Quickstart User Installation

## install uv

curl -LsSf https://astral.sh/uv/install.sh | sh

## create a virtualenv somewhere

uv venv .venv

## install the wheel

uv pip install http://20.168.10.234:8080/wheel/syftbox-0.1.0-py3-none-any.whl --reinstall

## run the client

uv run syftbox client

# Quickstart Client Developer Installation

### Step 0: Open your terminal to the root of this Github repository

Begin by opening your terminal and navigating to the root directory of this github repository (so when you run 'ls' it should show folders like "syftbox", "server", "tests", etc.). Then run the commands in steps 1-4:

### Step 1: Install Homebrew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install uv (using homebrew — which is better for this than pip)

```
brew install uv
```

### Step 3: Install a virtual environment using uv

```
uv venv
```

### Step 4: Install a relative version of uv.

```
uv pip install -e .
```

### Step 5: Run the client

```
uv run syftbox/client/client.py
```

# Alternative Options

### Run Client

```
syftbox client --config_path=./config.json --sync_folder=~/Desktop/SyftBox --email=your@email.org --port=8082  --server=http://20.168.10.234:8080
```

### Deploy

This builds the latest source to a wheel and deploys and restarts the server:
http://20.168.10.234:8080

```
./scripts/deploy.sh
```

### Dev Mode

Run the server and clients locally in editable mode with:
Server:

```
./scripts/server.sh
```

Client1:

```
./scripts/madhava.sh
```

Client2:

```
./scripts/andrew.sh
```
