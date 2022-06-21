# webscrappe-trademe-co-nz-property

[![Build](https://github.com/ankursoni/webscrappe-trademe-co-nz-property/actions/workflows/build.yml/badge.svg)](https://github.com/ankursoni/webscrappe-trademe-co-nz-property/actions/workflows/build.yml)
[![CodeCov](https://codecov.io/gh/ankursoni/webscrappe-trademe-co-nz-property/branch/main/graph/badge.svg)](https://codecov.io/gh/ankursoni/webscrappe-trademe-co-nz-property)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ankursoni/webscrappe-trademe-co-nz-property)](/LICENSE)
<!-- [![Build Status](https://img.shields.io/github/workflow/status/ankursoni/webscrappe-trademe-co-nz-property/build)](https://github.com/ankursoni/webscrappe-trademe-co-nz-property/actions/workflows/build.yml) -->

[![Github](https://img.shields.io/github/followers/ankursoni?style=social)](https://github.com/ankursoni)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ankursoniji)

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fold_left.svg?style=social&label=Follow%20%40ankursoniji)](https://twitter.com/ankursoniji)


> Web scrapping project for trademe.co.nz/property


## Built With

- Python v3.9.13
- Flask
- Docker
- Helm chart & Kubernetes


## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites
Python v3.9.13  
Docker (optional)  
Helm chart and Kubernetes (optional)

### Setup
```sh
# create a virtual environment
# assuming you have "python3 --version" = "Python 3.9.13" installed in the current terminal session
python3 -m venv ./venv

# activate virtual environment
# for macos or linux
source ./venv/bin/activate
# for windows
.\venv\Scripts\activate

# upgrade pip
python -m pip install --upgrade pip

# install python dependencies
pip install -r requirements.txt

# lint python code
pylint ./search
```

### Install
1. Run as cli
```sh
# argument 1 = city
# argument 2 = total number of pages
# argument 3 = true or false (default) to do search 'with detail' or 'without detail'
# argument 4 = output file (default = result.csv)
# e.g. python -m search.main <city> <total pages> <true or false> <file.csv>
python -m search.main auckland 1 false result.csv
```
2. Or, run as web api server
```sh
FLASK_ENV=development python3 -m search.app
```
3. Or, build and run in docker container
```sh
# build docker image
docker build -t webscrappe-trademe-co-nz-property:mvp .

# run docker
docker run -d -p 8080:8080 --name webscrappe webscrappe-trademe-co-nz-property:mvp

# stop and remove docker
docker stop webscrappe
docker rm webscrappe
```

4. Or, run in kubernetes cluster
```sh
# upgrade or install helm chart, if not preset
cd .deploy/helm
helm upgrade -i webscrappe-trademe-co-nz-property webscrappe-trademe-co-nz-property \
	-n webscrappe --create-namespace

# stop and remove helm chart and namespace
helm uninstall webscrappe-trademe-co-nz-property -n webscrappe
kubectl delete namespace webscrappe
```

### Usage
TODO:
When running as a command line interface (cli)
```sh
# argument 1 = city
# argument 2 = total number of pages
# argument 3 = true or false (default) to do search 'with detail' or 'without detail'
# argument 4 = output file (default = result.csv)
# e.g. python -m search.main <city> <total pages> <true or false> <file.csv>
python -m search.main auckland 1 false result.csv
```

When running as an api, use the following endpoints:
TODO:
1. 'http://`{domain name}`/search-without-detail/`{city}`/`{total number of pages}`' searching without property detail.
```sh
# example
curl http://localhost:8080/search-without-detail/auckland/1
```
2. 'http://`{domain name}`/search-with-detail/`{city}`/`{total number of pages}`' searching with property detail.
```sh
# example
curl http://localhost:8080/search-with-detail/auckland/1
```

### Run tests
```sh
# run unit tests
pytest -v --cov=search
```

### Deployment
TODO:


## Authors

👤 **Ankur Soni**

- GitHub: [@ankursoni](https://github.com/ankursoni)
- LinkedIn: [@ankursoniji](https://linkedin.com/in/ankursoniji)
- Twitter: [@ankursoniji](https://twitter.com/ankursoniji)


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).


## Show your support

Give a ⭐️ if you like this project!


## 📝 License

This project is [MIT](./LICENSE) licensed.