"""
This class use to generate database and its data
"""
import secrets
from datetime import datetime
import click
from flask.cli import with_appcontext
from project import db


@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Method to initializa database
    """
    print("create database--------------------------------------------")
    db.create_all()

