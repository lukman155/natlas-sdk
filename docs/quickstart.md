# Quickstart

## Installation
```bash
pip install natlas-sdk
```

## Basic Chat
```python
from natlas import NAtlasClient

client = NAtlasClient()
response = client.chat("Kedu?", language="ig")
print(response.text)
```
