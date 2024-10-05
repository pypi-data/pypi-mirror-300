# PyCSW RPI `pycsw-rpi`

[Monkey patched](https://en.wikipedia.org/wiki/Monkey_patch) `pycsw` for Slovak national catalogue service.

Check [original `pycsw` documentation ](https://docs.pycsw.org/en/2.6.1/index.html) for more details.

---

## Setup

Use exactly like original `pycsw`

### Install

```bash
pip install --user pycsw-rpi
```

### Create configuration file

Configuration file is not distributed with package.

Sample configuration can be downloaded from `<<url>>`

### Administrative command (CLI)

`pycsw_rpi-admin` script is installed with package in `$PATH`, this script is replacement for original `pycsw-admin.py` script supporting modified beahaviour and can be used exactly like original one.

#### Create database

```bash
pycsw_rpi-admin -c setup_db -f <<pconfiguration_file>>
```

#### Load records

```bash
pycsw_rpi-admin -c load_records -f <<pconfiguration_file>> -p <<path_to_records_directory>>
```

Check [original documentation](https://docs.pycsw.org/en/2.6.1/administration.html) for `pycsw-admin.py` administrative command.

### Run "dev" self contained (toy) server

```bash
python -m pycsw_rpi.wsgi
```

### Deploy as WSGI application

`pycsw_rpi.wsgi` module contains WSGI `application` object (function) ready to be deployed with WSGI server (e.g. `gunicorn`, `uwsgi`). No WSGI server is installed with this package as dependecy.

To deploy with `gunicorn`:

```bash
# `gunicorn` package need to installed separately
pip install --user gunicorn
gunicorn pycsw_rpi.wsgi:application
```

---

## Modifications implemented (via monkey patches) to original `pycsw`

**Added queryables to APISO plugin:**

- `rpi:OrganizationUUID`
- `rpi:IsViewable`
- `rpi:IsSearchable`

**Modified APISO queryables:**

- `apiso:ParentIdentifier` support for gmx:Anchor encoding added
- `apiso:SpecificationTitle` support for gmx:Anchor encoding added
- `apiso:Subject` support for gmx:Anchor encoding added in keywords parsing

**Transaction web hook:**

On succesfull insert/delete CSW transaction HTTP POST request is made
on `transactions_webhook_url` set in `manager` section in configuration
file. Request body contains json list of executed transaction description

```json
[
    {
        "transaction": <transaction_type>,
        "id": <metadata_record_identifier>,
        "type": <metadata_record_type>,
        "record" <metadata_record_xml>
    },
    ...
]
```

`record` key is included only if `insert` transaction has been made

If `transaction_webhook_url` is not set in configuration file webhook is skipped.

Feature is implemented as monkey patch of `pycsw.core.repository.Repository.insert` and `pycsw.core.repository.Repository.delete` methods.

## Contributions
