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
```

Now you can send:

```python
from sendalert import sendalert

sendalert("message")
```

### Alternative: set your API key in your code

```python
import os
from sendalert import sendalert

os.environ["SENDALERT_API_KEY"] = "your_api_key_here"

sendalert("message")
```
