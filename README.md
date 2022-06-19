# webscrappe-trademe-co-nz-property

> Web scrapping project for trademe.co.nz/property


## Built With

- Python v3.9.13
- Flask
- Docker


## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites
Python v3.9.13

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

# install python dependencies
pip install -r requirements.txt
```

### Install
```sh
# run as cli
# argument 1 = city
# argument 2 = total number of pages
# argument 3 = true or false (default) to do search 'with detail' or 'without detail'
# argument 4 = output file (default = result.csv)
# e.g. python -m search.main <city> <total pages> <true or false>
python -m search.main auckland 1 false result.csv

# run as web api server
FLASK_APP=./search/app.py FLASK_ENV=development flask run
```

### Usage
TODO:

### Run tests
```sh
# run unit tests
pytest --cov=search -v
```

### Deployment
TODO:


## Authors

👤 **Ankur Soni**

- GitHub: [@ankursoni](https://github.com/ankursoni)
- LinkedIn: [LinkedIn](https://linkedin.com/in/ankursoniji)
- Twitter: [@ankursoniji](https://twitter.com/ankursoniji)


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).


## Show your support

Give a ⭐️ if you like this project!


## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc


## 📝 License

This project is [MIT](./LICENSE) licensed.