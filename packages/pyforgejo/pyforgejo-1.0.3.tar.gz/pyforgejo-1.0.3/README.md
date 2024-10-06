# pyforgejo

A client library for accessing the Forgejo API.

**:warning: Package refactoring**

**This package is being rewritten from scratch to improve code quality, development velocity, and user experience.** 

**The current package is production-ready. To ensure a smooth transition, we recommend pinning the package to `1.0`.**

**The upcoming 2.0 release (expected in a few months) will introduce significant changes, including updated API calls (for example, `client.repo_get(repo, owner)` will replace `repo_get.sync_detailed(repo=repo, owner=owner, client=client)`).**

**We'll provide upgrade instructions and documentation for the 2.0 release.**

## Usage

Create a client:

```python
from pyforgejo import AuthenticatedClient

client = AuthenticatedClient(base_url='https://codeberg.org/api/v1', token='API_TOKEN')
```

Call an endpoint:

```python
from pyforgejo.api.user import user_get_current

response = user_get_current.sync_detailed(client=client)

# async version
response_async = user_get_current.asyncio_detailed(client=client)
response = await response_async

print(response)
```

## Installation

``` shell
pip install pyforgejo
```

## Forgejo API

Resources:

- [API Usage | Forgejo – Beyond coding. We forge.](https://forgejo.org/docs/latest/user/api-usage/): user guide for the Forgejo API
- [Forgejo API | Codeberg](https://codeberg.org/api/swagger): API reference for Codeberg
- [Forgejo API Swagger spec | Codeberg](https://codeberg.org/swagger.v1.json): Codeberg's Forgejo API Swagger spec
- [openapi-generators/openapi-python-client](https://github.com/openapi-generators/openapi-python-client/): repo for the generator library that was used to generate `pyforgejo`
- [About Swagger Specification | Documentation | Swagger](https://swagger.io/docs/specification/about/): docs for Swagger spec
- [The OpenAPI Specification Explained | OpenAPI Documentation](https://learn.openapis.org/specification/): docs for OpenAPI spec

The structure of the import statement for interacting with a specific endpoint follows this pattern:

``` python
from pyforgejo.api.<root_path> import <operation_id>
```

Here, `<tag>` is the root path or tag for the endpoint in the Swagger spec, and `<operation_id>` is the `operationId` for the specific function you want to call, converted to snake case.

For example, for the endpoint `/repos/search`, the Swagger spec is:

``` json
"/repos/search": {
    "tags": ["repository"],
    "operationId": "repoSearch",
    ...
}
```

So to hit that endpoint, the import statement will be:

``` python
from pyforgejo.api.repository import repo_search
```

Every path/operation combo becomes a Python module with four functions:

- `sync`: Blocking request that returns parsed data (if successful) or `None`
- `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful
- `asyncio`: Like `sync` but async instead of blocking
- `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

Currently, Forgejo's API spec does not provide the response schemas for every endpoints, so most endpoints will not return parsed data and only have a detailed method.

All path/query parameters and bodies become method arguments.


## Customising

```python
from pyforgejo.api.organization import org_get


def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

client = AuthenticatedClient(
    base_url='https://codeberg.org/api/v1',
    token='API_TOKEN',
    httpx_args={'event_hooks': {'request': [log_request]}}
)

org_get.sync_detailed(org='codename', client=api_client)
# Request event hook: GET https://codeberg.org/api/v1/orgs/codename - Waiting for response
# Response(status_code=<HTTPStatus.TEMPORARY_REDIRECT: 307>, content=b'<a href="/api/v1/orgs/forgejo">Temporary Redirect</a>.\n\n', headers=Headers({'cache-control': 'max-age=0, private, must-revalidate, no-transform', 'content-type': 'text/html; charset=utf-8', 'location': '/api/v1/orgs/forgejo', 'vary': 'Origin', 'date': 'Mon, 08 Apr 2024 13:47:22 GMT', 'content-length': '56', 'strict-transport-security': 'max-age=63072000; includeSubDomains; preload', 'permissions-policy': 'interest-cohort=()', 'x-frame-options': 'sameorigin', 'x-content-type-options': 'nosniff'}), parsed=None)


```

## Development

### `openapi-python-client`
`pyforgejo` is generated with [openapi-python-client](https://github.com/openapi-generators/openapi-python-client/), with as of now very little modification.

If you run into any issues, please create an issue in this repo.

If you want to work on a PR, please consider making a PR to `openapi-python-client` rather than to this repo.

`openapi-python-client` was chosen to generate this client over [openapi-generator](https://github.com/OpenAPITools/openapi-generator) and [fern](https://github.com/fern-api/fern) because of the following reasons:

- `openapi-python-client` is Python-specific, which allows it to leverage specific language features, have a clearer code, and offer a better developer experience, compared to `openapi-generator`'s one-size-fits-all approach
- `openapi-python-client` is written in Python, so users of `pyforgejo` will be more likely to be able to make contributions and fix bugs in the generator's code itself, while `openapi-generator` is written in Java, which represents a higher barrier to contributions
- `openapi-python-client` supports more authentication options, including access tokens, than `fern`
- the documentation is limited, but clearer than for `openapi-generator`

### Generating the client with `openapi-python-client`

1. Convert Forgejo's [Swagger spec](https://code.forgejo.org/swagger.v1.json) to OpenAPI with [swagger-converter](https://github.com/swagger-api/swagger-converter), as Swagger is not supported by `openapi-python-client`.
2. Install [openapi-python-client](https://github.com/openapi-generators/openapi-python-client/):
    ```shell
    pip install openapi-python-client
    ```
3. Create a `config.yaml` file with the following content:
    ```yaml
    project_name_override: "pyforgejo"
    ```
4. Generate the client (this will create a `pyforgejo/` dir):
    ```shell
    openapi-python-client generate --path /path/to/forgejo_openapi.json --config /path/to/config.yaml
    ```
5. Alternatively, update the client:
    ```shell
    git clone https://codeberg.org/harabat/pyforgejo
    
    openapi-python-client update --path /path/to/forgejo_openapi.json --config ./pyforgejo/config.yaml
    ```
6. Navigate to the `pyforgejo/` dir and call the API:
    ```python
    from pyforgejo.client import AuthenticatedClient
    from pyforgejo.api.user import user_get_current
    
    client = AuthenticatedClient(base_url='FORGEJO_URL' + '/api/v1', token='ACCESS_TOKEN')
    response = user_get_current.sync_detailed(client=client)
    
    print(response)
    # Response(status_code=<HTTPStatus.OK: 200>, ...)
    ```

Because merging of PRs on `openapi-python-client` can be slow, the fork at https://github.com/harabat/openapi-python-client, which is where I work on `pyforgejo`-related PRs to `openapi-python-client`, might be more up-to-date. In this case, replace step 1 above with the following:

``` shell
git clone https://github.com/harabat/openapi-python-client.git
pip install ./openapi-python-client --upgrade
```

### Modifying `openapi-python-client`

1. Clone and modify `openapi-python-client`
    ```shell
    git clone https://github.com/openapi-generators/openapi-python-client.git
    nvim openapi-python-client/openapi_python_client/parser/openapi.py
    # make your changes
    ```
2. Create and activate new env
3. Install (or upgrade) modified local package
    ```shell
    pip install ./openapi-python-client
    # pip install ./openapi-python-client --upgrade  # after making further changes
    ```
4. Generate a new client the regular way
    ```shell
    openapi-python-client generate --path /path/to/forgejo_openapi.json --config /path/to/config.yaml
    ```

### Testing

We use `pytest` for testing.

The tests are in the `tests` dir. Run them with:

``` shell
pytest ./tests/endpoints.py
```
