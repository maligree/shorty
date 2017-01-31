# Shorty

A mysterious shortener.

## Setup

```
# venv/venv-wrapper as you like
git clone ...
cd shorty
pip install -r requirements.txt
cd shorty
./manage.py create_fake_users 60
./manage.py runserver
```

## Caveats

* No true collision handling for the randomly generated tokens
* Lot's of other issues: it _is_ a quick, after-hours hack
