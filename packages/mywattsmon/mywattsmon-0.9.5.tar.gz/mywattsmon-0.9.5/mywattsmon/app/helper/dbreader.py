# -*- coding: utf-8 -*-
"""mywattsmon"""

import sqlite3

class DbReader():

    """
    DbReader class.
    """

    def __init__(self, dbfile:str):
        """Setup.

        Args:
            dbfile (str): Absolute path to the database file.

        Returns:
            None.
        """
        self.dbfile = dbfile
        
    def select_by_statement(self, statement:str):
        """Selects rows as specified by the given SQL statement.

        Note: Selects rows without limit (fetchall).

        Args:
            statement (str): The SQL statement.
        
        Returns:
            list[str], list[tuple]: The column list and the rows read. 
        """
        colnames = []
        sql = statement
        db = None
        c = None
        try:
            # -------------------------------------------------
            # Ensure that this is a query and, as an additional
            # security measure, do NOT commit select statements
            # -------------------------------------------------
            test = statement.strip().lower()
            if not test.startswith("select"):
                return None
            db = self.__get_db_conn()
            c = db.cursor()
            c.execute(sql)
            description = c.description
            for row in description:
                colnames.append(row[0])
            return colnames, c.fetchall()
        finally:
            if c:
                c.close()
            if db:
                db.close()

    def select_by_id(self, tablename:str, id:int):
        """Selects the row with the given ID.

        Args:
            tablename (str): The table name.
            id (int): The ID (SQLite INTEGER PRIMARY KEY).
        
        Returns:
            str, tuple: The column list and the row read.
        """
        colnames = []
        sql = f"SELECT * from {tablename} where id = {id};"
        db = None
        c = None
        try:
            db = self.__get_db_conn()
            c = db.cursor()
            c.execute(sql)
            description = c.description
            for row in description:
                colnames.append(row[0])
            return colnames, c.fetchone()
        finally:
            if c:
                c.close()
            if db:
                db.close()

    # ---------------
    # Private methods
    # ---------------

    def __get_db_conn(self):
        """Gets an SQLite database connection.
        
        Also creates the database if it does not already exist.
        
        Args:
            None.
        
        Returns:
            object: SQL connection.
        """
        return sqlite3.connect(self.dbfile, timeout=10.0)
