## REST API server for Autoencoder

### Start

1. `docker build -t autoencoder-rest:latest .`
2. `docker run -it -p 5001:5001 autoencoder-rest`
3. `docker run -it -p 5002:5001 autoencoder-rest`
------------------

### Endpoint

| Endpoints       | Body                                     |
|-----------------|------------------------------------------|
| `POST /autoencoder` | **{}**|

### cURL

`curl -d {\"test_string\":\"Take admission in San Jose State University\"} -H "Content-Type: application/json" -X POST http://localhost:5001/preprocessing/`