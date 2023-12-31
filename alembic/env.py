from logging.config import fileConfig

import psycopg2
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

from bot.db.user.model import UserModel
from bot.db.ad.model import AdModel
from bot.db.utils.bind import get_bind_config, get_bind_not_db
from bot.loader import db, config as config_app

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline(url: str) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(db_name: str) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_bind_not_db(
        login=config_app.postgres.login,
        password=config_app.postgres.password,
        port=config_app.postgres.port,
        host=config_app.postgres.host
    )
    connect = psycopg2.connect(url)
    connect.autocommit = True
    with connect.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")

    connectable = create_engine(url + f'/{db_name}')

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline(get_bind_config(config_app.postgres, config_app.telegram.db_name))
else:
    run_migrations_online(config_app.telegram.db_name)
