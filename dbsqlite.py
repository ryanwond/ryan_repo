#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#Ticloud web version 2.0
#author:WangRui


from sqlite3 import dbapi2 as sqlite
import os
import logging

from configmanager import ConfigManager


class DBsqLite(object):
    """
        A lightweight wrapper around sqlite DB-API connections
    """
    def __init__(self):
        self.db_path = ConfigManager.getvalue("local", "db_path")
        if not os.path.exists(self.db_path):
            raise AttributeError("The sqlite path is not exists. %s" % self.db_path)
        self.db_con = None

    def close(self):
        if self.db_con is not None:
            self.db_con.close()
            self.db_con = None

    def connect(self):
        self.close()
        try:
            self.db_con = sqlite.connect(self.db_path)
            self.db_con.isolation_level = None
        except DatabaseError as e:
            print e
            logging.error("Cannot connect to sqlite on %s" % self.db_path)

    def execute(self, sql):
        db_cur = self._cursor()
        try:
            self._execute(db_cur, sql)
            return db_cur.rowcount
        finally:
            db_cur.close()

    def queryone(self, sql):
        db_cur = self._cursor()
        try:
            self._execute(db_cur, sql)
            data = db_cur.fetchone()
            return data
        finally:
            db_cur.close()

    def queryall(self, sql):
        db_cur = self._cursor()
        try:
            self._execute(db_cur, sql)
            data = db_cur.fetchall()
            return data
        finally:
            db_cur.close()

    def querysize(self, sql, size):
        db_cur = self._cursor()
        try:
            self._execute(db_cur, sql)
            data = db_cur.fetchmany(size)
            return data
        finally:
            db_cur.close()

    def _cursor(self):
        if self.db_con is None:
            self.connect()
        return self.db_con.cursor()

    def _execute(self, cursor, sql):
        try:
            return cursor.execute(sql)
        except OperationalError:
            logging.error("Error connecting to MySQL on %s", self.db_path)
            self.close()
            raise


DatabaseError = sqlite.DatabaseError
IntegrityError = sqlite.IntegrityError
OperationalError = sqlite.OperationalError



#if __name__ == "__main__":
#    db_instance = DBsqLite()
#    sql = "SELECT item, setvalue FROM t_system"
#    alarm_list = db_instance.queryall(sql)
#    db_instance.close()
#    print alarm_list

