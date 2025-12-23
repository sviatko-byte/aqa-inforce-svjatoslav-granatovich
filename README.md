Description
---
Automated UI and API tests

Preconditions (local)
---
Make sure you have `git`, `python3`, `pip3` and `poetry` installed. If not, please do so by following the instructions on the official resources.

Prepare local environment
---
* Clone the project to your local machine and navigate to the project directory:
```shell
git git@github.com:sviatko-byte/aqa-inforce-svjatoslav-granatovich.git
cd aqa-inforce-svjatoslav-granatovich

```
* Install and setup virtualenv for the project:
```shell
pip install virtualenv
virtualenv --python python3 venv
source venv/bin/activate
```
* Install all packages required for the tests run:
```shell
poetry install
```
----
Running tests locally
---
* Run all tests once the environment is ready the tests can be executed. Run the following command to do so:
```shell
pytest tests
```
* Run tests with Allure reporting.
To run tests with Allure reporting add the argument `--alluredir=allure-results` to the command or add to run configuration.
```shell
pytest tests/ui/test_booking --alluredir=allure-results
```

View Allure report locally
---
If the tests were executed with `--alluredir` argument, allure results will be stored in the defined directory. To view allure results run the following command:
```shell
allure serve allure-results
```
