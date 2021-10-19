# miningpoolhub_py
A Python wrapper for the Mining Pool Hub REST API

## Install
`pip install miningpoolhub_py`

## Usage
### Universal Endpoints
Mining Pool Hub supports auto switching between coins. Obtain statistics for all coins with the following methods

```python
from miningpoolhub_py import Pool

pool_instance = Pool('ethereum')
pool_instance.get_user_all_balances()
pool_instance.get_auto_switching_and_profits_statistics()
pool_instance.get_mining_profit_and_statistics()
```

### Pool Selection
Mining Pool Hub has different base urls for each coin they offer. Create a new pool object for every coin you are
interested in mining statistics for
```python
from miningpoolhub_py import Pool
pool_instance = Pool('ethereum')
pool_instance.get_dashboard()
```

### Authentication
#### Environment File
The API key can be configured in a `.env` file and will be picked up by any Pool instances that are created
```
MPH_API_KEY=<api_key>
```

#### Pass API Key to Pool Constructor
```python
from miningpoolhub_py import Pool
pool_instance = Pool('ethereum', '<api_key>')
```

# References
## Mining Pool Hub
- [Mining Pool Hub](https://miningpoolhub.com/)
- [API Reference](https://github.com/miningpoolhub/php-mpos/wiki/API-Reference)
- [Mining Pool Hub API Key](https://miningpoolhub.com/?page=account&action=edit)

## Python API Wrapper & and CI/CD Pipeline
For anyone else new to developing Python API wrappers or CI/CD in Python these references were invaluable in helping
develop this module
- [Building and Testing an API Wrapper in Python](https://semaphoreci.com/community/tutorials/building-and-testing-an-api-wrapper-in-python)
- [Creating a Python API Wrapper \(Ally Invest API\)](https://medium.com/analytics-vidhya/creating-a-python-api-wrapper-ally-invest-api-568934a1411c)
- [Publishing a Package to PyPI with Poetry](https://www.ianwootten.co.uk/2020/10/20/publishing-a-package-to-pypi-with-poetry/)
- [Publishing to PyPI Using GitHub Actions](https://www.ianwootten.co.uk/2020/10/23/publishing-to-pypi-using-github-actions/)
  - [Code Repo](https://github.com/niftydigits/ftrack-s3-accessor/tree/master/.github/workflows)