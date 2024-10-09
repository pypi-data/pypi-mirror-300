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
from bjarkan_client import BjarkanClient
from datetime import datetime, timedelta

# Initialize the client
client = BjarkanClient("https://data.bjarkan.io")

# Authenticate
client.authenticate("your_username", "your_password")

# Get available tables
tables = client.get_tables()
print("Available tables:", tables)

# Get history for a specific table
result = client.get_history(
    table_name="example_table",
    start_time=datetime.now() - timedelta(hours=1),
    end_time=datetime.now(),
    exchange='binance',
    symbol="BTC/USDT",
    bucket_period="1 minute",
    sort_descending=False,
    limit=100
)
print("Data:", result['data'][:5])  # Print first 5 entries
print(f"Query performance: {result['query_performance_seconds']:.4f} seconds")
```

## API Reference

### `BjarkanClient`

The `BjarkanClient` class is the main interface for interacting with the Bjarkan Historical Market Data API.

#### `__init__(base_url: str)`
Initialize the client with the base URL of the Bjarkan Market Data API.

#### `authenticate(username: str, password: str)`
Authenticate with the API using your username and password. This method must be called before making any other API calls.

#### `get_tables() -> List[Dict[str, any]]`
Get a list of available tables and their configurations.

#### `get_history(table_name: str, start_time: datetime, end_time: datetime, exchange: str = None, symbol: str = None, sort_descending: bool = False, bucket_period: str = None, limit: int = None, offset: int = None) -> Dict[str, any]`
Retrieve historical data for a specific table.

Parameters:
- `table_name`: Name of the table to query
- `start_time`: Start time for the query (inclusive)
- `end_time`: End time for the query (inclusive)
- `exchange`: (Optional) Filter by exchange
- `symbol`: (Optional) Filter by symbol
- `sort_descending`: (Optional) Sort results in descending order if True
- `bucket_period`: (Optional) Aggregation bucket period
- `limit`: (Optional) Maximum number of records to return
- `offset`: (Optional) Number of records to skip

Returns a dictionary containing:
- `data`: List of historical data entries
- `query_performance_seconds`: Time taken to execute the query in seconds

#### `get_paginated_history(table_name: str, start_time: datetime, end_time: datetime, exchange: str = None, symbol: str = None, sort_descending: bool = False, bucket_period: str = None, page_size: int = 1000) -> Iterator[Dict[str, any]]`
Retrieve historical data in pages. This method is useful for handling large datasets.

Parameters are the same as `get_history`, with the addition of:
- `page_size`: Number of records to retrieve per page

Returns an iterator, where each iteration yields a dictionary containing:
- `data`: List of historical data entries for the current page
- `query_performance_seconds`: Time taken to execute the query for the current page in seconds

#### `validate_bucket_period(bucket_period: str) -> bool`
Validate if the given bucket period is valid. Valid periods are: ['100ms', '1s', '30s', '1 minute', '5 minutes', '15 minutes', '30 minutes', '1 hour'].

## Examples

### Fetching Available Tables

```python
client = BjarkanClient("https://data.bjarkan.io")
client.authenticate("your_username", "your_password")

tables = client.get_tables()
for table in tables:
    print(f"Table: {table['table_name']}")
    print(f"Config: {table['config']}")
    print("---")
```

### Fetching Historical Data with Pagination

```python
from datetime import datetime, timedelta

start_time = datetime.now() - timedelta(days=1)
end_time = datetime.now()

for page in client.get_paginated_history(
    table_name="example_table",
    start_time=start_time,
    end_time=end_time,
    exchange="binance",
    symbol="BTC/USDT",
    bucket_period="5 minutes",
    page_size=500
):
    print(f"Retrieved {len(page['data'])} records")
    print(f"Query performance: {page['query_performance_seconds']:.4f} seconds")
    # Process the data in the current page
    for record in page['data']:
        # Do something with each record
        pass
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.