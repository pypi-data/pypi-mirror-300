# Fastapi_glogger

This is a package for formatting your fastapi logs into structured google logs to be used with google cloud services like cloud run.

# Installation

#### Packge

Install the package using pip (only test package is available right now):

```bash
 pip install fastapi_glogger
```

#### Source Code

After cloning the repo

install dependencies using poetry

```bash
poetry install
```

Look the a main.py for a an example how to use it with FastAPI

```python
from fastapi import FastAPI
from src.fastapi_glogger import setup_fastapi
import logging

app = setup_fastapi(FastAPI())


@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}
```

#### Test mode (Locally)

To run the example code or package locally:

- set the environment variable `IS_TEST` to `true as it will need GOOGLE_APPLICATION_CREDENTIALS` env variable otherwise to authenticate with google cloud logging.

#### On GCP (Cloud)

using `cloud run` you can deploy a container and the env variable gets set automatically from your account data.

## API

### setup_fastapi(app: FastAPI, additional_headers: Optional[Dict[str, str]] =None) -> FastAPI

- `app` : the fast api constructor
- `additional_headers`: dictionary where you specify:
  - `key`: the string you want injected the formatted log
  - `value`: the header that you want injected
    ex: {'testInject':'test'} it gets test from headers and puts it inside testInject in the outputted log

## Examples

### Additional Headers

Import and use the package in your Python script:

```python-repl

from fastapi import FastAPI
from fastapi_glogger import setup_fastapi
import logging

app =  setup_fastapi(FastAPI(), {"testInjected": "test"})

@app.get("/")
def read_root():
    logging.info("Hello world")
    return {"Hello world"}

```

The logged message should be outputted like this

```json

{
    "severity": "INFO",
    "timestamp": "2024-09-05 09:48:01,485",
    "pathname": "/app/main.py",
    "logger_name": "root",
    "logging.googleapis.com/sourceLocation": {
        "file": "main.py",
        "line": "9",
        "function": "read_root"
    },
    "logging.googleapis.com/spanId": 9508110491393966220,
    "auditInfo": {
        "http_request": {
            "request_method": "GET",
            "request_url": "http://gcp-url/",
            "user_agent": "curl/7.36.1",
            "remote_ip": "52.12.45.123",
            "referer": null,
            "protocol": "https"
        },
        "testInjected": "This is test content"
    },
    "message": "[main:9]: Hello World"
}
```

### Overriding exception handling

there is an existing wrapper over the fastapi exception handling for `HTTPException` and `RequestValidationError` that just
adds a layer of logging above the fastapi handling.
you can override these by adding your own exception handling code `after` setting up the formatter.

```python
from fastapi import FastAPI
from fastapi_glogger import setup_fastapi
from fastapi.exceptions import RequestValidationError, HTTPException as StarletteHTTPException
import logging


app = setup_fastapi(FastAPI(), additional_headers={"TestInjected": "test"})

@app.add_exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logging.error(f"HTTP Exception: {exc.detail}")
    return exc


@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

```

## License

[MIT](LICENSE)
