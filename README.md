# webscrappe-trademe-co-nz-property

[![Build](https://github.com/ankursoni/webscrappe-trademe-co-nz-property/actions/workflows/build.yml/badge.svg)](https://github.com/ankursoni/webscrappe-trademe-co-nz-property/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/ankursoni/webscrappe-trademe-co-nz-property/branch/main/graph/badge.svg?token=ZZWMD4FB93)](https://codecov.io/gh/ankursoni/webscrappe-trademe-co-nz-property)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ankursoni/webscrappe-trademe-co-nz-property)](/LICENSE)


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
1. Run as cli:
```sh
# argument 1 = city
# argument 2 = total number of pages
# argument 3 = true or false (default) to do search 'with detail' or 'without detail'
# argument 4 = output file (default = result.psv)
# argument 5 = true or false (default) to enable debug mode logging
# e.g. python -m search.main <city> <total pages> <true or false> <file.psv> <true or false>
python -m search.main auckland 1 false result.psv
```
2. Or, run as web api server:
```sh
FLASK_ENV=development python3 -m search.app
```
3. Or, build and run in docker container:
```sh
# build docker image
docker build -t webscrappe-trademe-co-nz-property:mvp .

# run docker container
docker run -d -p 8080:8080 --name webscrappe webscrappe-trademe-co-nz-property:mvp

# stop and remove docker container
docker stop webscrappe
docker rm webscrappe
```

4. Or, run in kubernetes cluster:
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
When running as a command line interface (cli):
```sh
# argument 1 = city
# argument 2 = total number of pages
# argument 3 = true or false (default) to do search 'with detail' or 'without detail'
# argument 4 = output file (default = result.psv)
# argument 5 = true or false (default) to enable debug mode logging
# e.g. python -m search.main <city> <total pages> <true or false> <file.psv> <true or false>
python -m search.main auckland 1 false result.psv
```
NOTE: the output result.psv file needs to be imported with a custom Delimiter or Separator type - `|` in the import CSV wizard.

When running as an api, use the following endpoints:
1. 'http://`{domain name}:{port}`/search-without-detail/`{city}`/`{total number of pages}`' searching without property detail.
```sh
# example
curl http://localhost:8080/search-without-detail/auckland/1
```
2. 'http://`{domain name}:{port}`/search-with-detail/`{city}`/`{total number of pages}`' searching with property detail.
```sh
# example
curl http://localhost:8080/search-with-detail/auckland/1
```

### Mapping of columns
An example property search page lists property as follows:
![property-search](./docs/images/property-search.png)
The fields in PSV are mapped as follows:
- title  
![property-search-title](./docs/images/property-search-title.png)
- address  
![property-search-address](./docs/images/property-search-address.png)
- number_of_bedrooms  
![property-search-bedrooms](./docs/images/property-search-bedrooms.png)
- number_of_bathrooms  
![property-search-bathrooms](./docs/images/property-search-bathrooms.png)
- number_of_parking_lots  
![property-search-parking-lots](./docs/images/property-search-parking-lots.png)
- number_of_living_areas  
![property-search-living-areas](./docs/images/property-search-living-areas.png)
- floor_area_sqm  
![property-search-floor-area](./docs/images/property-search-floor-area.png)
- land_area_sqm  
![property-search-land-area](./docs/images/property-search-land-area.png)
- asking_price  
![property-search-asking-price](./docs/images/property-search-asking-price.png)

Another example property detail page shows property as follows:
![property-detail](./docs/images/property-detail.png)
The fields in PSV are mapped as follows:
- property_type  
![property-detail-property-type](./docs/images/property-detail-property-type.png)
- parking_type  
![property-detail-parking-type](./docs/images/property-detail-parking-type.png)
- in_the_area  
![property-detail-in-the-area](./docs/images/property-detail-in-the-area.png)
- property_id  
![property-detail-property-id](./docs/images/property-detail-property-id.png)
- broadband_options  
![property-detail-broadband-options](./docs/images/property-detail-broadband-options.png)
- description  
![property-detail-description](./docs/images/property-detail-description.png)

Another example property detail page shows property as follows:
![property-detail-2](./docs/images/property-detail-2.png)
More fields in PSV are mapped as follows:
- rateable_value  
![property-detail-2-rateable-value](./docs/images/property-detail-2-rateable-value.png)
- agency_reference  
![property-detail-2-agency-reference](./docs/images/property-detail-2-agency-reference.png)


### Run tests
```sh
# run unit tests
pytest -v --cov=search
```


## Authors

👤 **Ankur Soni**

[![Github](https://img.shields.io/github/followers/ankursoni?style=social)](https://github.com/ankursoni)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ankursoniji)

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fold_left.svg?style=social&label=Follow%20%40ankursoniji)](https://twitter.com/ankursoniji)


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).


## Show your support

Give a ⭐️ if you like this project!


## 📝 License

This project is [MIT](./LICENSE) licensed.