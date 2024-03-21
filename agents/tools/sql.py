import sqlite3
import os.path
from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite")
conn = sqlite3.connect(db_path)


def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error ocurred: {str(err)}"


def list_tables():
    c = conn.cursor()
    try:
        query = "SELECT name FROM sqlite_master WHERE type = 'table'"
        rows = c.execute(query)
        return "\n".join(row[0] for row in rows if row[0] is not None)
    except sqlite3.OperationalError as err:
        return f"The following error ocurred: {str(err)}"


def describe_tables(table_names):
    c = conn.cursor()
    try:
        tables = ", ".join("'" + table + "'" for table in table_names)
        rows = c.execute(
            f"SELECT sql from sqlite_master WHERE type='table' and name in ({tables});"
        )
        return "\n".join(row[0] for row in rows if row[0] is not None)
    except sqlite3.OperationalError as err:
        return f"The following error ocurred: {str(err)}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a SQLite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)


class DescribeTAblesArgsSchema(BaseModel):
    tables_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of the tables",
    func=describe_tables,
    args_schema=DescribeTAblesArgsSchema,
)
