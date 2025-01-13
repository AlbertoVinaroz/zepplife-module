import subprocess
import sys
import os
from utils import Utils
from package.sqlparse import SQLParse

if sys.executable and "python" in sys.executable.lower():
    import sqlite3
    jython = False

else:
    from java.sql import DriverManager
    jython = True


class Database:
    def __init__(self, database, pragma = True):
        self.database = database
        if jython:
            self.dbConn = DriverManager.getConnection("jdbc:sqlite:{}".format(self.database))
        else:
            self.dbConn = sqlite3.connect(self.database)

        if pragma:
            self.execute_pragma()
    
    def execute_query(self, query, attach = None):
        if jython:
            contents = []
            stmt = self.dbConn.createStatement()
            if attach:
                stmt.execute(attach)

            result = stmt.executeQuery(query)
            while result.next():
                row = []
                for index in range(result.getMetaData().getColumnCount()):
                    row.append(result.getObject(index + 1))
                
                contents.append(row)
            
            return contents
        else:
            cursor_msg = self.dbConn.cursor()
            if attach:
                cursor_msg.execute(attach)

            cursor_msg.execute(query)
            return cursor_msg.fetchall()
    

    def execute_pragma(self):
        self.execute_query("PRAGMA journal_mode = DELETE")
        self.execute_query("PRAGMA wal_checkpoint(FULL)")
        
    
    @staticmethod
    def get_undark_output(databases, report_path):
        output = {}

        for name in databases:
            listing = []
            undark_output = Utils.run_undark(name).decode()
            for line in undark_output.splitlines():
                listing.append(line)
            
            if listing:
                relative_name = os.path.normpath(name.replace(report_path, ""))
                output[relative_name] = listing
        return output

    @staticmethod
    def get_drp_output(databases, report_path):
        listing = {}
        for database in databases:
            path = os.path.normpath(database.replace(report_path, ""))
            content = SQLParse.read_contents(database)
            if content:
                listing[path] = content
        return listing
    