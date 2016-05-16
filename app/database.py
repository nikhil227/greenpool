"""
from datetime import datetime
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData, create_engine, exc, BINARY, ForeignKey,\
    VARCHAR, BOOLEAN, Column, and_, or_, BIGINT, Index
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT, DATETIME
from sqlalchemy import asc, desc, select, exists
from config import DATABASE_URL
from sqlalchemy.sql import text
logger = logging.getLogger()


class AlchemyDB(SQLAlchemy):
    engine = None
    _table = dict()
    metadata = None

    def __init__(self):
        self.conn = AlchemyDB.get_connection()

    def __del__(self):
        self.conn.close()

    @staticmethod
    def init():
        try:
            AlchemyDB.engine = create_engine(
                    DATABASE_URL,
                    paramstyle='format',
                    pool_recycle=3600,
                    isolation_level='REPEATABLE_READ',
                    convert_unicode=True
            )

            AlchemyDB.metadata = MetaData()

        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
        except Exception as err:
            logger.error(err, exc_info=True)

    @staticmethod
    def get_connection():
        return AlchemyDB.engine.connect()

    @staticmethod
    def get_raw_connection():
        return AlchemyDB.engine.raw_connection()

    @staticmethod
    def get_table(name):
        return AlchemyDB._table[name]

    def begin(self):
        self.trans = self.conn.begin()

    def commit(self):
        self.trans.commit()

    def rollback(self):
        self.trans.rollback()

    @staticmethod
    def args_to_where(table, args):
        clause = []
        for k, v in args.items():
            if isinstance(v, (list, tuple)):
                clause.append(table.c[k].in_(v))
            else:
                clause.append(table.c[k] == v)
        return and_(*clause)

    @staticmethod
    def args_to_where_or(table, args):
        clause = []
        for k, v in args.items():
            if isinstance(v, (list, tuple)):
                clause.append(table.c[k].in_(v))
            else:
                clause.append(table.c[k] == v)
        return or_(*clause)

    def insert_row(self, table_name, **values):
        table = AlchemyDB.get_table(table_name)
        insert = table.insert().values(values)
        self.conn.execute(insert)

    def insert_row_batch(self, table_name, values):
        table = AlchemyDB.get_table(table_name)
        self.conn.execute(table.insert(), values)

    def update_row(self, table_name, *keys, **row):
        table = AlchemyDB.get_table(table_name)
        if not isinstance(keys, (list, tuple)):
            keys = [keys]
        if not keys or len(keys) == len(row):
            return False
        clause = dict()
        for k in keys:
            clause[k] = row[k]
        clean_row = row.copy()
        for key in keys:
            if key in clean_row.keys():
                del clean_row[key]
        clauses = AlchemyDB.args_to_where(table, clause)
        update = table.update(clauses, clean_row)
        self.conn.execute(update)
        return True

    def update_row_new(self, table_name, where=None, val=None):
        if not where:
            where = {}
        if not val:
            val = {}
        try:
            table = AlchemyDB.get_table(table_name)
            clauses = AlchemyDB.args_to_where(table, where)
            update = table.update(clauses, val)
            self.conn.execute(update)
            return True
        except Exception as err:
            logger.error(err, exc_info=True)(err, True)
            return False

    def delete_row(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            delete = table.delete().where(AlchemyDB.args_to_where(table, where))
            self.conn.execute(delete)
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)(err, True)
            return False

    def delete_row_in_transaction(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        delete = table.delete().where(AlchemyDB.args_to_where(table, where))
        self.conn.execute(delete)

    def find_one(self,table_name, **where):
        table = AlchemyDB.get_table(table_name)
        sel = select([table]).where(AlchemyDB.args_to_where(table, where))
        row = self.conn.execute(sel)
        tup = row.fetchone()
        if tup:
            return dict(tup)
        return False

    def exists_row(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            sel = select([table]).where(AlchemyDB.args_to_where(table, where))
            sel = select([exists(sel)])
            row = self.conn.execute(sel).scalar()
            if row:
                return True
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
        return False

    def find(self, table_name, order_by="id", _limit=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            func = asc
            if order_by and order_by.startswith('_'):
                order_by = order_by[1:]
                func = desc
            if _limit:
                sel = select([table]).where(AlchemyDB.args_to_where(table, where)).order_by(func(order_by)).limit(_limit)
            else:
                sel = select([table]).where(AlchemyDB.args_to_where(table, where)).order_by(func(order_by))
            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def find_or(self, table_name, order_by="id", _limit=None, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            func = asc
            if order_by and order_by.startswith('_'):
                order_by = order_by[1:]
                func = desc
            if _limit:
                sel = select([table]).where(AlchemyDB.args_to_where_or(table, where)).order_by(func(order_by)).limit(_limit)
            else:
                sel = select([table]).where(AlchemyDB.args_to_where_or(table, where)).order_by(func(order_by))
            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    @staticmethod
    def args_to_join(table1, table2, args):
        clause = []
        for k, v in args.items():
            clause.append(table1.c[k] == table2.c[v])
        return and_(*clause)

    def select_outer_join(self, table_names, foreign_key, where):
        table = [AlchemyDB.get_table(t) for t in table_names]
        try:
            fclause = AlchemyDB.args_to_join(table[0], table[1], foreign_key[0])
            logger.debug(fclause)
            clause = AlchemyDB.args_to_where_join(where)
            logger.debug(clause)
            # clause = and_(fclause,clause)
            logger.debug(clause)
            j = table[0].outerjoin(table[1], fclause)
            for i in range(1, len(foreign_key)):
                fclause = AlchemyDB.args_to_join(table[i], table[i+1], foreign_key[i])
                j = j.join(table[i+1], fclause)
            sel = select(table, use_labels=True).select_from(j).where(clause)
            row = self.conn.execute(sel)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except Exception as e:
            logger.exception(e)
            return False

    @staticmethod
    def args_to_where_join(where):
        # where = [({"SocialContact.Email": email}), ({"AppUserId": appid})]
        logger.debug(where)
        or_list = []
        for tup in where:
            and_list = []
            for r in tup:
                if r:
                    logger.debug(r)
                    tab, col = r.keys()[0].split('.')
                    table = AlchemyDB.get_table(tab)
                    v = r.values()[0]
                    if isinstance(v, (list, tuple)):
                        and_list.append(table.c[col].in_(v))
                    else:
                        and_list.append(table.c[col] == v)
                or_list.append(and_(*and_list))
        return or_(*or_list)

    def count(self, table_name, **where):
        table = AlchemyDB.get_table(table_name)
        try:
            sel = select([table.c.id]).where(AlchemyDB.args_to_where(table, where))
            row = self.conn.execute(sel)
            count = row.rowcount
            return count
        except exc.SQLAlchemyError as err:
            logger.error(err, exc_info=True)
            return False

    def execute_raw_sql(self, sql, kwargs):
        try:
            row = self.conn.execute(text(sql), kwargs)
            tup = row.fetchall()
            l = [dict(r) for r in tup]
            return l
        except Exception as e:
            logger.exception(e)
            return False
"""