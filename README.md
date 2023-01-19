# pyskybitz
A Python client to work with SkyBitz API

## Supported API methods
* QueryPositions

## Usage
### Prepare ConnectionConfig
```python
connection_config = ConnectionConfig(
    customer=<CUSTOMER-KEY>, 
    password=<PASSWORD>,
    port=<PORT>,
    version=<API-VERSION>,
    base_domain=<DOMAIN-URL>  # example.com
)
```

### Prepare Parser service
```python
parser_service = Parser()
```

### Prepare HTTP client session

```python
import requests

http_client_session = requests.Session()
```

### Prepare API client service
```python
api_service = API(
    parser_service=parser_service,
    http_client_session=http_client_session,
    connection_config=connection_config,
)
```

### Call API methods
```python
response = api_service.query_positions(AssetIdPreset.RETURN_ALL_ASSETS)
```
