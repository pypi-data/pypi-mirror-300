# SendAlert.io Python Package

A simple Python package for sending alerts using SendAlert.io.

## Installation

```sh
pip install sendalert
```

## Usage

First set your API key:

```sh
export SENDALERT_API_KEY=your_api_key_here
export SENDALERT_PROJECT=your_project_name
```

Now you can send:

```python
from sendalert import sendalert

sendalert("message")
```

### Alternative: set your API key and project in your code

```python
import os
from sendalert import sendalert

os.environ["SENDALERT_API_KEY"] = "your_api_key_here"
os.environ["SENDALERT_PROJECT"] = "your_project_name"

sendalert("message")
```
