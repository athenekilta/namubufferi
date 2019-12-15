# Purpose
Aski's electronic cashier system. More history can be found in https://github.com/AS-kilta/saatohistoriaa/tree/master/ASkipiikki

# Development
Local development can be done by using docker and docker-compose.

https://docs.docker.com/
https://docs.docker.com/compose/

## Starting the containers
Development environment can be started by building and starting the containers

    docker-compose -f docker-compose.dev.yml up -d --build

Command `docker-compose -f docker-compose.dev.yml ps` should now list three containers to be running

    Name                         Command               State                       Ports                     
    -------------------------------------------------------------------------------------------------------------------
    namubufferi_fake-smtp_1     MailHog                          Up      0.0.0.0:1025->1025/tcp, 0.0.0.0:8025->8025/tcp
    namubufferi_namubufferi_1   gunicorn namubufferi.wsgi  ...   Up      0.0.0.0:8080->8080/tcp                        
    namubufferi_postgres_1      docker-entrypoint.sh postgres    Up      5432/tcp

## Adding data to play with
You should now be able to navigate into http://localhost:8080/ and see the project running.
There however is no test data yet. Luckily there is a way to produce some.
(Do not run this script in production. It will destroy the current database and fill it with test data)

    docker-compose -f docker-compose.dev.yml exec namubufferi bin/test_seed.sh

This should produce output like

    You have requested a flush of the database.
    This will IRREVERSIBLY DESTROY all data currently in the 'namubufferi-local-test' database,
    and return each table to an empty state.
    Are you sure you want to do this?

        Type 'yes' to continue, or 'no' to cancel: yes
    Operations to perform:
    Apply all migrations: admin, auth, contenttypes, namubufferiapp, sessions
    Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying auth.0001_initial... OK
    Applying admin.0001_initial... OK
    Applying admin.0002_logentry_remove_auto_add... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    Applying namubufferiapp.0001_initial... OK
    Applying namubufferiapp.0002_auto_20170115_1437... OK
    Applying namubufferiapp.0003_auto_20170117_1850... OK
    Applying namubufferiapp.0004_auto_20170119_1641... OK
    Applying namubufferiapp.0005_auto_20170120_2302... OK
    Applying namubufferiapp.0006_auto_20170129_1639... OK
    Applying namubufferiapp.0007_auto_20170211_2052... OK
    Applying namubufferiapp.0008_auto_20170211_2148... OK
    Applying namubufferiapp.0009_auto_20170214_2108... OK
    Applying namubufferiapp.0010_auto_20171029_2211...7D2B5
    OK
    Applying namubufferiapp.0011_auto_20180318_1625... OK
    Applying namubufferiapp.0012_hash_nfc_tags... OK
    Applying namubufferiapp.0013_add_tos... OK
    Applying namubufferiapp.0014_auto_20190212_1613... OK
    Applying sessions.0001_initial... OK
    A25A3
    namubufferiapp.Category(pk=1): Deserunt nisi dolo
    namubufferiapp.Category(pk=2): Iure i
    namubufferiapp.Category(pk=3): Aliquam recusand
    namubufferiapp.Category(pk=4): Quam e
    namubufferiapp.Category(pk=5): Autem voluptas duc
    namubufferiapp.Product(pk=1): Velit sunt reiciendis consectetur ducimus iste ea  ...
    namubufferiapp.Product(pk=2): Quasi dolore nesciunt distinctio aperiam amet quam ...
    namubufferiapp.Product(pk=3): Tempora aut laborum quibusdam a reprehenderit adip ...
    namubufferiapp.Product(pk=4): Possimus culpa obcaecati praesentium r
    namubufferiapp.Product(pk=5): Sit inventore quo ducimus veniam quos dolorum accu ...
    namubufferiapp.Product(pk=6): Molestias atque sequi natu
    namubufferiapp.Product(pk=7): Exercitationem ab quibusdam rem adipisci quos. Dol ...
    namubufferiapp.Product(pk=8): Qui ducimus magnam neque perspiciatis maiores volu ...
    namubufferiapp.Product(pk=9): Dolore aliquam reiciendis aut accusamus? Consequun ...
    namubufferiapp.Product(pk=10): Repudiandae deserunt delectus perferendis. Esse di ...
    namubufferiapp.Product(pk=11): Excepturi cupiditate corru
    namubufferiapp.Product(pk=12): Ipsam saepe voluptates, quibusdam suscipi
    namubufferiapp.Product(pk=13): Recusandae sit molest
    namubufferiapp.Product(pk=14): Nostrum id et. Mollitia assumenda rerum unde solut ...
    namubufferiapp.Product(pk=15): Quae ut dolor pariatur nam architecto sapiente tem ...
    namubufferiapp.Product(pk=16): Aspernatur beat
    namubufferiapp.Product(pk=17): Reiciendis quaerat laudantium nam eaque aut
    namubufferiapp.Product(pk=18): Hic reiciendis odit fuga voluptatibus soluta? Exer ...
    namubufferiapp.Product(pk=19): Facere odit omnis
    namubufferiapp.Product(pk=20): Laudantium aliquid nam natus vero ne
    namubufferiapp.Product(pk=21): Nostrum quia eligendi commodi exercitationem nesci ...
    namubufferiapp.Product(pk=22): Et possimus omnis debitis non eveniet, quis natus  ...
    namubufferiapp.Product(pk=23): Consequuntur harum voluptate praesentium i
    namubufferiapp.Product(pk=24): Fugit vel rem veritatis necessitatibus magnam quo  ...
    namubufferiapp.Product(pk=25): Quasi quos beatae corporis d
    namubufferiapp.Product(pk=26): Eligendi earum rem consequuntur amet optio totam d ...
    namubufferiapp.Product(pk=27): Saepe at placea
    namubufferiapp.Product(pk=28): Quo ut accusamus commodi architecto fugit nemo dol ...
    namubufferiapp.Product(pk=29): Similique autem qui minus quod
    namubufferiapp.Product(pk=30): Laudantium molestiae minima autem, molestiae
    BEAEC
    auth.User(pk=2): Y2OdxTWSFAT3EEX8BwROy0f9yg
    0B236
    auth.User(pk=3): t
    A4990
    auth.User(pk=4): HnQjz8lWp0XlHADzsi
    E8A91
    auth.User(pk=5): _1rfALdOQkI
    4F2F8
    auth.User(pk=6): MU4lq_8ZbKyo

Now you should be able to login into the admin panel in http://localhost:8080/admin
User and password can be seen from docker-compose.dev.yml in this project.

You can now use the system.

## Inspecting emails the system would be sending
The system is connected into local smtp "sandbox" that allows you to see what emails the system
would be sending. UI for the sandbox should be available in http://localhost:8025/
This is useful for example when registering new users.



# Tips and tricks
When you want to simulate barcode scanner when you don't have one.
You can use xdotool to simulate typing in inhuman speed

    sleep 1; xdotool type abcd123