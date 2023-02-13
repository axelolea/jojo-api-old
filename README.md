# JoJo's API

JoJo's API es un proyecctos realizado en :

![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)

Con el micro-framework:

![Flask](https://img.shields.io/static/v1?style=for-the-badge&message=Flask&color=000000&logo=Flask&logoColor=FFFFFF&label=)

## Requirements

Para correr la aplicacion es nesesario tener:

- Python 3.10.6
- DBMS ( [SQLAlchemy Dialect](https://docs.sqlalchemy.org/en/20/dialects/) )
  - MySQL
  - MariaDB
  - SQLite (Only Test)

## Instalacion

Nota: Recomiendo crear un entorno virtual ( [venv](https://docs.python.org/3/library/venv.html) ) para usar esta aplicacion.

### Crear entornor virtual

Para `Windows`:

- Crear entorno virtual.

``` bash
C:\ python -m venv ./venv
```

- Activar entorno virtual.

``` bash
C:\ ./venv/Scripts/activate.bat
```

Para `Linux/Mac`:

``` bash
$ python3 -m venv ./venv
```
- Activar entorno virtual.


``` bash
$ source ./venv/bin/activate
```

### Instalar dependencias

Usa el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar todas las dependecias del proyectos con el siguiente comando.

``` bash
pip install -r requirements.txt
```
`Nota`: En caso de usar bash/zsh, usar el comando `pip3`

### Modificar .flaskenv

``` sql
CREATE DATABASE jojosdb;
```

```
// MySQL URI
export SQLALCHEMY_DB_URI=mysql+pymysql://<user>:<password>@localhost/jojosdb

// SQLite
export SQLALCHEMY_DB_URI=sqlite:///jojosdb
```

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```