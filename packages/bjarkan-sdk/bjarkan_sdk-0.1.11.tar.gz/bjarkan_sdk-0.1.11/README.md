# Bjarkan Market Data SDK

A Python SDK for accessing the Historical Market Data API of Bjarkan.

## Installation

You can install the Bjarkan Market Data SDK using pip:

```
pip install bjarkan-sdk
```

## Usage

Here's a quick example of how to use the SDK:

```python
from bjarkan_sdk import BjarkanClient
from datetime import datetime

# Initialize the client
client = MarketDataClient("https://api.bjarkan.io")

# Authenticate
client.authenticate("your_username", "your_password")

# Get available tables
tables = client.get_tables()
print("Available tables:", tables)

# Get history for a specific table
history = client.get_history(
    table_name="example_table",
    start_time=datetime(2024, 10, 5, 15, 30, 00),
    end_time=datetime(2024, 10, 5, 15, 40, 00),
    exchange='binance',
    symbol="BTC/USDT",
    sort_descending=False
)
print("Data:", history[:5])  # Print first 5 entries
```

## API Reference

### `BjarkanClient`

#### `__init__(base_url: str)`
Initialize the client with the base URL of the Bjarkan Market Data API.

#### `authenticate(username: str, password: str)`
Authenticate with the API using your username and password.

#### `get_tables() -> List[Dict[str, any]]`
Get a list of available tables and their configurations.

#### `get_history(table_name: str, start_time: datetime, end_time: datetime, exchange: str = None, symbol: str = None, sort_descending: bool = False) -> List[Dict[str, any]]`
Retrieve historical data for a specific table.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.