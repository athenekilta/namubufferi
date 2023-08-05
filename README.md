# Namubufferi ☕️👻

It's the app used for buying snacks in the Athene guild room.

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Recommended Development Environment](docs/recommended.md)
- [Translations](docs/translations.md)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Structure](docs/structure.md)


## About
Right now the project it's meant for buying products, transfer money to friends, and add money via MobilePay. The project is meant to be a WebApp as most of the users access via mobile.

### Languages
Well, Athene is expanding and so is the app. Currently it has multiple languages, and it's possible to add more. It has Finnish, English, Swedish, Spanish, Catalan, German, French, Italian and Chinese. The translations are not only in the names, UI but also in the tags.

## Prerequisites

- [Python](https://www.python.org/downloads/) (3.11)


### Environment variables
There are 2 environment variables needed for **MobilePay** integration:
 1 for **Tailwind** in windows:
- `MOBILEPAY_MERCHANT_ID`
- `MOBILEPAY_MERCHANT_SECRET`

For those 2 you need to contact the CTO of Athene.

In the case you are doing development in Windows, perhaps when developing there are some problems with **Tailwind**. In this case you can use the following environment variable:
- `NPM_BIN_PATH`: "C://Program Files//nodejs//npm.cmd"

Adjust the path to your npm.cmd file.

## Development
Developing with this project is easy. Just run the following commands:

```bash
pip install -r requirements.txt #Only the first time
python manage.py makemigrations #First time
python manage.py migrate #First time
python manage.py runserver
```

If you want to edit the CSS, you need to run the following command:

```bash
python manage.py tailwind install #First time
python manage.py tailwind start
```

To access the website, go to http://localhost:8000/. And yes, that's it! You are now ready to start developing.

If you want to populate the database you can do:

```bash
python manage.py loaddata ledger/fixtures/initial_data.json
```	

Or if it is an updated version of products.csv:
```bash	
python manage.py loadproducts products.csv
```

Please, to make it easy, the products.csv must be in english. The translations are made in the script for loadproducts.


### Testing
To run the tests, run the following command:

```bash
python manage.py test
```

## Deployment

- https://docs.djangoproject.com/en/4.2/howto/deployment/

## Legal Notice
GDPR in this specific case, as it is something internal, it doesn't apply.
[Link](https://commission.europa.eu/law/law-topic/data-protection/reform/what-does-general-data-protection-regulation-gdpr-govern_es)