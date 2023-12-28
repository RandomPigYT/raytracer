import mysql.connector as con
import sys
import os


class SQLWrapper:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

        self.connection = con.connect(
            host=self.host, user=self.user, passwd=self.passwd, database=self.database
        )

        if not self.connection.is_connected():
            sys.stderr.write("Failed to connect to host %s\n" % (self.host))
            sys.exit(1)

        self.cursor = self.connection.cursor()

    def execute(self, command):
        self.cursor.execute(command)

    def fetch(self, n=-1):
        if n == -1:
            return self.cursor.fetchall()

        self.cursor.fetchmany(n)
