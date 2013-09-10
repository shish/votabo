Votabo README
=============

Getting Started
---------------

WARNING: this is extremely alpha-quality software

Get the code, create a virtual environment with all the necessary libraries
```
git clone https://github.com/shish/votabo.git
cd votabo
virtualenv env
./env/bin/pip install -e ./
```

If you want to use an existing database, edit development.ini and point
sqlalchemy.url to it, and install a database driver:
```
./env/bin/pip install psycopg2   # for postgres
./env/bin/pip install MySQLdb    # for mysql (not tested)
```

If you want a new, blank, sqlite database to play with:
```
./env/bin/initialize_votabo_db development.ini
```

See if the self-tests pass:
```
./env/bin/nosetests votabo/tests/*.py
```

Run the server:
```
./env/bin/pserve development.ini
```

View the site
```
firefox http://localhost:6543/
```


User-facing README:
-------------------

TODO: make some notes about features advanced users / site moderators may be
interested in, eg advanced search flags

- see votabo/static/README.txt for now
