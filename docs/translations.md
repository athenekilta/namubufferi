# Translations

## Static files
The translations for non database objects (models) are created inside the folder `locale`. Inside there you can find the different languages inside a folder called by the country code name (fi = Finnish). The default language is English.

To generate the static files for the translations, run the following command:

```bash
python manage.py makemessages -l <language>
```

Go inside the `locale` folder and inside the language folder you will find a file called `django.po`. Inside there you can find the translations for the different strings. To compile the translations, run the following command:

```bash
python manage.py compilemessages
```

## Database objects
For the database objects are created inside the database by [django-modeltranslations](https://django-modeltranslation.readthedocs.io/en/latest/) app. To create the translations for the database objects, run the following command:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

It is useful as well to know the management command for sync the database with the translations. This command is:

```bash
python manage.py update_translation_fields
```