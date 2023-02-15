# JoJo's API

JoJo's API es un proyecctos realizado en:

![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)

Con el micro-framework:

![Flask](https://img.shields.io/static/v1?style=for-the-badge&message=Flask&color=000000&logo=Flask&logoColor=FFFFFF&label=)

## Requisitos

Para correr la aplicacion es nesesario tener:

- Python 3.10.6
- DBMS ( [SQLAlchemy Dialect](https://docs.sqlalchemy.org/en/20/dialects/) )
  - MySQL
  - MariaDB
  - SQLite (Only Test)

## Instalacion

Nota: Recomiendo crear un entorno virtual ( [venv](https://docs.python.org/3/library/venv.html) ) para usar esta aplicacion.

### Crear entornor virtual
- Usar esta comando para crear el entorno virtual dentro del directorio.
``` bash
python -m venv ./venv
```
`Nota`: En caso de ejecutar el comando en bash/zsh, usar `python3`
- Activar entorno virtual.


Para `Windows`:

``` bash
./venv/Scripts/activate.bat
```
Para `Linux/Mac`:

``` bash
source ./venv/bin/activate
```

### Instalar dependencias

- Usa el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar todas las dependecias del proyectos con el siguiente comando.

``` bash
pip install -r requirements.txt
```
`Nota`: En caso de usar bash/zsh, usar el comando `pip3`

## Configuracion

### Archivo .flaskenv
- Cambiar la URI de la base de datos.

```conf
# MySQL URI
export SQLALCHEMY_DB_URI=mysql+pymysql://<user>:<password>@localhost/jojosdb

# SQLite (Default)
export SQLALCHEMY_DB_URI=sqlite:///jojosdb
```
`Nota`: En las etiquetas <user> y <password>. Colocar las crendenciales del usuario de la base de datos (El usuario debe de contar con permisos apra creartablas e insetar data)
- Cambiar puerto.
```conf
export FLASK_RUN_PORT=5000
```

### Cambiar base de datos SQLite a otra MySQL o MariaDB

- Crear la base de datos con esta linea de comando.
``` sql
CREATE DATABASE jojosdb;
```
`Nota`: Solo si habeis cambiado la URI en el archivo de configuracion, por default se creara una base de datos `SQLite`.

- Para usar la base de datos MySQL es nesesario instalar esta dependencia.
```
pip install pymysql==1.0.2
```
`Nota`: Confirme que tenga habilitado en entorno vitual antes creado.

## Migraciones

### Crear migraciones de los modelos
- Una vez creada la base de datos (en caso de haber vambiado la URI), ejecutar las siguientes lineas en al terminal con el entorno vitual habilitado para crear las migraciones en la base de datos.
```bash
flask db init
flask db migrate
flask db upgrade
```

## Ejecutar servidor

- Finalmente, ejecutar la aplicacion.

```bash
flask run
```