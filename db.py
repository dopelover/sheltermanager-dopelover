#!/usr/bin/python

import al
import cache
import datetime
import hashlib
import i18n
import sys
import utils
from sitedefs import DB_TYPE, DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HAS_ASM2_PK_TABLE, DB_PK_STRATEGY, DB_DECODE_HTML_ENTITIES, CACHE_COMMON_QUERIES, MULTIPLE_DATABASES_MAP


try:
    import MySQLdb
except:
    pass

try:
    import psycopg2
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except:
    pass

try:
    import sqlite3
except:
    pass

class DatabaseInfo():
    """
    Handles information on connecting to a database.
    Default values are supplied by the sitedefs.py file.
    """
    dbtype = DB_TYPE # MYSQL, POSTGRESQL or SQLITE
    host = DB_HOST
    port = DB_PORT
    username = DB_USERNAME
    password = DB_PASSWORD
    database = DB_NAME
    alias = "" 
    locale = "en"
    timezone = 0
    installpath = ""
    locked = False
    has_asm2_pk_table = DB_HAS_ASM2_PK_TABLE
    is_large_db = False
    connection = None
    def __repr__(self):
        return "DatabaseInfo->locale=%s:dbtype=%s:host=%s:port=%d:db=%s:alias=%s:user=%s:pass=%s" % ( self.locale, self.dbtype, self.host, self.port, self.database, self.alias, self.username, self.password )

def connection(dbo):
    """
        Creates a connection to the database and returns it
    """
    try:
        if dbo.dbtype == "MYSQL": 
            if dbo.password != "":
                return MySQLdb.connect(host=dbo.host, port=dbo.port, user=dbo.username, passwd=dbo.password, db=dbo.database, charset="utf8", use_unicode=True)
            else:
                return MySQLdb.connect(host=dbo.host, port=dbo.port, user=dbo.username, db=dbo.database, charset="utf8", use_unicode=True)
        if dbo.dbtype == "POSTGRESQL": 
            c = psycopg2.connect(host=dbo.host, port=dbo.port, user=dbo.username, password=dbo.password, database=dbo.database)
            c.set_client_encoding("UTF8")
            return c
        if dbo.dbtype == "SQLITE":
            return sqlite3.connect(dbo.database, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    except Exception,err:
        al.error(str(err), "db.connection", dbo, sys.exc_info())

def connect_cursor_open(dbo):
    """
    Returns a tuple containing an open connection and cursor.
    If the dbo object contains an active connection, we'll just use
    that to get a cursor.
    """
    if dbo.connection is not None:
        return dbo.connection, dbo.connection.cursor()
    else:
        c = connection(dbo)
        return c, c.cursor()

def connect_cursor_close(dbo, c, s):
    """
    Closes a connection and cursor pair. If dbo.connection exists, then
    c must be it, so don't close it.
    """
    try:
        s.close()
    except:
        pass
    if dbo.connection is None:
        try:
            c.close()
        except:
            pass

def query(dbo, sql):
    """
        Runs the query given and returns the resultset
        as a list of dictionaries. All fieldnames are
	    uppercased when returned.
    """
    try:
        c, s = connect_cursor_open(dbo)
        # Run the query and retrieve all rows
        s.execute(sql)
        c.commit()
        d = s.fetchall()
        # Initalise our list of results
        l = []
        for row in d:
            # Intialise a map for each row
            rowmap = {}
            for i in xrange(0, len(row)):
                v = row[i]
                if type(v) == unicode:
                    if v is not None:
                        v = v.encode("ascii", "xmlcharrefreplace")
                        v = v.replace("`", "'")
                        v = v.replace("\x92", "'")
                if type(v) == str:
                    if v is not None:
                        v = v.replace("`", "'")
                        v = v.replace("\x92", "'")
                rowmap[s.description[i][0].upper()] = v
            l.append(rowmap)
        connect_cursor_close(dbo, c, s)
        return l
    except Exception,err:
        al.error(str(err), "db.query", dbo, sys.exc_info())
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def query_cache(dbo, sql, age = 60):
    """
    Runs the query given and caches the result
    for age seconds. If there's already a valid cached
    entry for the query, returns the cached result
    instead.
    If CACHE_COMMON_QUERIES is set to false, just runs the query
    without doing any caching and is equivalent to db.query()
    """
    if not CACHE_COMMON_QUERIES or not cache.available(): return query(dbo, sql)
    cache_key = "%s:%s:%s" % (dbo.alias, dbo.database, sql.replace(" ", "_"))
    m = hashlib.md5()
    m.update(cache_key)
    cache_key = "q:%s" % m.hexdigest()
    results = cache.get(cache_key)
    if results is not None:
        return results
    results = query(dbo, sql)
    cache.put(cache_key, results, age)
    return results

def query_columns(dbo, sql):
    """
        Runs the query given and returns the column names as
        a list in the order they appeared in the query
    """
    try:
        c, s = connect_cursor_open(dbo)
        # Run the query and retrieve all rows
        s.execute(sql)
        c.commit()
        # Build a list of the column names
        cn = []
        for col in s.description:
            cn.append(col[0].upper())
        connect_cursor_close(dbo, c, s)
        return cn
    except Exception,err:
        al.error(str(err), "db.query_columns", dbo, sys.exc_info())
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def query_tuple(dbo, sql):
    """
        Runs the query given and returns the resultset
        as a grid of tuples
    """
    try:
        c, s = connect_cursor_open(dbo)
        # Run the query and retrieve all rows
        s.execute(sql)
        d = s.fetchall()
        c.commit()
        connect_cursor_close(dbo, c, s)
        return d
    except Exception,err:
        al.error(str(err), "db.query_tuple", dbo, sys.exc_info())
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def query_tuple_columns(dbo, sql):
    """
        Runs the query given and returns the resultset
        as a grid of tuples and a list of columnames
    """
    try:
        c, s = connect_cursor_open(dbo)
        # Run the query and retrieve all rows
        s.execute(sql)
        d = s.fetchall()
        c.commit()
        # Build a list of the column names
        cn = []
        for col in s.description:
            cn.append(col[0].upper())
        connect_cursor_close(dbo, c, s)
        return (d, cn)
    except Exception,err:
        al.error(str(err), "db.query_tuple_columns", dbo, sys.exc_info())
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def query_json(dbo, sql):
    """
        Runs the query given and returns the resultset
        as a JSON array with column names. This is
        more efficient than having query() marshall into
        dictionaries and then iterating those, so if
        you're querying to get JSON, use this instead of
        json(query(dbo, "SQL"))
    """
    try:
        c, s = connect_cursor_open(dbo)
        # Run the query
        s.execute(sql)
        c.commit()
        # Loop round the rows
        rows = ""
        while 1:
            d = s.fetchone()
            if d is None: break

            row = "{"
            for i in xrange(0, len(d)):
                if row != "{": row += ", "
                # if it's null
                if d[i] is None: 
                    value = "null"
                # if it's numeric
                elif is_number(d[i]): 
                    value = str(d[i])
                # if it's a string
                else:
                    value = "\"" + str(d[i]).replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("`", "'").replace("\"", "\\\"") + "\""
                row += "\"%s\" : %s" % ( s.description[i][0].upper(), value )
            row += "}"
            if rows != "": rows += ",\n"
            rows += row
        json = "[\n" + rows + "\n]"
        connect_cursor_close(dbo, c, s)
        return json
    except Exception,err:
        al.error(str(err), "db.query_json", dbo, sys.exc_info())
        return ""
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass
    
def execute_dbupdate(dbo, sql):
    """
    Runs an action query for a dbupdate script (sets override_lock
    to True so we don't forget)
    """
    return execute(dbo, sql, True)

def execute(dbo, sql, override_lock = False):
    """
        Runs the action query given and returns rows affected
        override_lock: if this is set to False and dbo.locked = True,
        we don't do anything. This makes it easy to lock the database
        for writes, but keep databases upto date.
    """
    if not override_lock and dbo.locked: return
    try:
        c, s = connect_cursor_open(dbo)
        s.execute(sql)
        rv = s.rowcount
        c.commit()
        connect_cursor_close(dbo, c, s)
        return rv
    except Exception,err:
        al.error(str(err), "db.execute", dbo, sys.exc_info())
        try:
            # An error can leave a connection in unusable state, 
            # rollback any attempted changes.
            c.rollback()
        except:
            pass
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def execute_many(dbo, sql, params, override_lock = False):
    """
        Runs the action query given with a list of tuples that contain
        substitution parameters. Eg:
        "INSERT INTO table (field1, field2) VALUES (%s, %s)", [ ( "val1", "val2" ), ( "val3", "val4" ) ]
        Returns rows affected
        override_lock: if this is set to False and dbo.locked = True,
        we don't do anything. This makes it easy to lock the database
        for writes, but keep databases upto date.
    """
    if not override_lock and dbo.locked: return
    try:
        c, s = connect_cursor_open(dbo)
        s.executemany(sql, params)
        rv = s.rowcount
        c.commit()
        connect_cursor_close(dbo, c, s)
        return rv
    except Exception,err:
        al.error(str(err), "db.execute_many", dbo, sys.exc_info())
        try:
            # An error can leave a connection in unusable state, 
            # rollback any attempted changes.
            c.rollback()
        except:
            pass
        raise err
    finally:
        try:
            connect_cursor_close(dbo, c, s)
        except:
            pass

def is_number(x):
    return isinstance(x, (int, long, float, complex))

def has_structure(dbo):
    try:
        execute(dbo, "select * from primarykey")
        return True
    except:
        return False

def _get_id_set_asm2_primarykey(dbo, table, nextid):
    """
    Update the ASM2 primary key table.
    """
    try:
        affected = execute(dbo, "UPDATE primarykey SET NextID = %d WHERE TableName = '%s'" % (nextid, table))
        if affected == 0: 
            execute(dbo, "INSERT INTO primarykey (TableName, NextID) VALUES ('%s', %d)" % (table, nextid))
    except:
        pass

def _get_id_max(dbo, table):
    return query_int(dbo, "SELECT MAX(ID) FROM %s" % table) + 1

def _get_id_memcache(dbo, table):
    cache_key = "db:%s:as:%s:tb:%s" % (dbo.database, dbo.alias, table)
    nextid = cache.increment(cache_key)
    if nextid is None: 
        nextid = query_int(dbo, "SELECT MAX(ID) FROM %s" % table) + 1
        cache.put(cache_key, nextid, 600)
    return nextid

def _get_id_postgres_seq(dbo, table):
    return query_int(dbo, "SELECT nextval('seq_%s')" % table)

def get_id(dbo, table):
    """
    Returns the next ID in sequence for a table.
    Will use memcache for pk generation if the CACHE_PRIMARY_KEYS option is on
        and will set the cache first value if not set.
    If the database has an ASM2 primary key table, it will be updated
        with the next pk value.
    """
    strategy = ""
    nextid = 0
    if DB_PK_STRATEGY == "max" or dbo.has_asm2_pk_table:
        nextid = _get_id_max(dbo, table)
        strategy = "max"
    elif DB_PK_STRATEGY == "memcache" and cache.available():
        nextid = _get_id_memcache(dbo, table)
        strategy = "memcache"
    elif DB_PK_STRATEGY == "pseq" and dbo.dbtype == "POSTGRESQL":
        nextid = _get_id_postgres_seq(dbo, table)
        strategy = "pseq"
    else:
        raise Exception("No valid PK strategy found")
    if dbo.has_asm2_pk_table: 
        _get_id_set_asm2_primarykey(dbo, table, nextid + 1)
        strategy += " asm2pk"
    al.debug("get_id: %s -> %d (%s)" % (table, nextid, strategy), "db.get_id", dbo)
    return nextid

def get_multiple_database_info(alias):
    """
    Gets the database info for the alias from our configured map.
    """
    dbo = DatabaseInfo()
    if not MULTIPLE_DATABASES_MAP.has_key(alias):
        dbo.database = "FAIL"
        return dbo
    mapinfo = MULTIPLE_DATABASES_MAP[alias]
    dbo.alias = alias
    dbo.dbtype = mapinfo["dbtype"]
    dbo.host = mapinfo["host"]
    dbo.port = mapinfo["port"]
    dbo.username = mapinfo["username"]
    dbo.password = mapinfo["password"]
    dbo.database = mapinfo["database"]
    return dbo
  
def query_int(dbo, sql):
    r = query_tuple(dbo, sql)
    try:
        v = r[0][0]
        return int(v)
    except:
        return int(0)

def query_float(dbo, sql):
    r = query_tuple(dbo, sql)
    try:
        v = r[0][0]
        return float(v)
    except:
        return float(0)

def query_string(dbo, sql):
    r = query_tuple(dbo, sql)
    try :
        v = r[0][0].replace("`", "'")
        return v.encode('ascii', 'xmlcharrefreplace')
    except:
        return str("")

def query_date(dbo, sql):
    r = query_tuple(dbo, sql)
    try:
        v = r[0][0]
        return v
    except:
        return None

def split_queries(sql):
    """
    Splits semi-colon separated queries in a single
    string into a list and returns them for execution.
    """
    queries = [];
    x = 0
    instr = False
    while x <= len(sql):
        q = sql[x:x+1]
        if q == "'":
            instr = not instr
        if x == len(sql):
            queries.append(sql[0:x].strip())
            break
        if q == ";" and not instr:
            queries.append(sql[0:x].strip())
            sql = sql[x+1:]
            x = 0
            continue
        x += 1
    return queries

def today():
    """ Returns today as a python date """
    return datetime.datetime.today()

def todaysql():
    """ Returns today as an SQL date """
    return dd(today())

def nowsql():
    """ Returns today as an SQL date """
    return ddt(today())

def python2db(d):
    """ Formats a python date as a date for the database """
    if d is None: return "NULL"
    return "%d-%02d-%02d" % ( d.year, d.month, d.day )

def ddt(d):
    """ Formats a python date and time as a date for the database """
    if d is None: return "NULL"
    return "'%04d-%02d-%02d %02d:%02d:%02d'" % ( d.year, d.month, d.day, d.hour, d.minute, d.second )

def dd(d):
    """ Formats a python date as a date for the database """
    if d is None: return "NULL"
    return "'%04d-%02d-%02d 00:00:00'" % ( d.year, d.month, d.day )

def ds(s):
    """ Formats a value as a string for the database """
    if s is None: 
        return u"NULL"
    elif type(s) != str and type(s) != unicode:
        return u"'%s'" % str(s)
    elif not DB_DECODE_HTML_ENTITIES:
        return u"'%s'" % utils.encode_html(s).replace("'", "`").replace("\\", "\\\\")
    else:
        return u"'%s'" % utils.decode_html(s.replace("'", "`").replace("\\", "\\\\"))

def df(f):
    """ Formats a value as a float for the database """
    if f is None: return "NULL"
    return str(f)

def di(i):
    """ Formats a value as an integer for the database """
    if i is None: return "NULL"
    s = str(i)
    try:
        return str(int(s))
    except:
        return "0"

def concat(dbo, items):
    """ Writes a database independent concat """
    if dbo.dbtype == "MYSQL":
        return "CONCAT(" + ",".join(items) + ")"
    elif dbo.dbtype == "POSTGRESQL" or dbo.dbtype == "SQLITE":
        return " || ".join(items)

def char_length(dbo, item):
    """ Writes a database independent char length """
    if dbo.dbtype == "MYSQL":
        return "LENGTH(%s)" % item
    elif dbo.dbtype == "POSTGRESQL":
        return "char_length(%s)" % item
    elif dbo.dbtype == "SQLITE":
        return "length(%s)" % item

def escape(s):
    """ Makes a value safe for queries """
    return s.replace("'", "`")

def recordversion():
    """
    Returns an integer representation of now.
    """
    d = today()
    i = d.hour * 10000
    i += d.minute * 100
    i += d.second
    return i

def make_insert_sql(table, s):
    """
    Creates insert sql, 'table' is the table name,
    's' is a tuple of tuples containing the field names
    and values, eg:
    
    make_insert_sql("animal", ( ( "ID", di(52) ), ( "AnimalName", ds("Indy") ) ))
    """
    fl = ""
    fv = ""
    for r in s:
        if r is None: break
        if fl != "": 
            fl += ", "
            fv += ", "
        fl += r[0]
        fv += r[1]
    return "INSERT INTO %s (%s) VALUES (%s);" % ( table, fl, fv )

def make_insert_user_sql(dbo, table, username, s, stampRecordVersion = True):
    """
    Creates insert sql for a user, 'table' is the table name,
    username is the name of the user to be stamped in the fields
    's' is a tuple of tuples containing the field names
    and values, eg:
    
    make_insert_user_sql("animal", "jeff", ( ( "ID", di(52) ), ( "AnimalName", ds("Indy") ) ))
    """
    l = list(s)
    l.append(("CreatedBy", ds(username)))
    l.append(("CreatedDate", ddt(i18n.now())))
    l.append(("LastChangedBy", ds(username)))
    l.append(("LastChangedDate", ddt(i18n.now(dbo.timezone))))
    if stampRecordVersion: l.append(("RecordVersion", di(recordversion())))
    return make_insert_sql(table, l)

def make_update_sql(table, cond, s):
    """
    Creates update sql, 'table' is the table name,
    's' is a tuple of tuples containing the field names
    and values, 'cond' is the where condition eg:
    
    make_update_sql("animal", "ID = 52", (( "AnimalName", ds("James") )))
    """
    o = "UPDATE %s SET " % table
    first = True
    for r in s:
        if r is None: break
        if not first:
            o += ", "
        first = False
        o += r[0] + "=" + r[1]
    if cond != "":
        o += " WHERE " + cond
    return o

def make_update_user_sql(dbo, table, username, cond, s, stampRecordVersion = True):
    """
    Creates update sql for a given user, 'table' is the table 
    name, username is the username of the user making the change,
    cond is the where condition eg:

    make_update_user_sql("animal", "jeff", "ID = 52", (( "AnimalName", ds("James") )))
    """
    l = list(s)
    l.append(("LastChangedBy", ds(username)))
    l.append(("LastChangedDate", ddt(i18n.now(dbo.timezone))))
    if stampRecordVersion: l.append(("RecordVersion", di(recordversion())))
    return make_update_sql(table, cond, l);

def rows_to_insert_sql(table, rows, escapeCR = ""):
    """
    Writes an INSERT query for a list of rows (a list containing dictionaries)
    """
    ins = []
    fields = []
    donefields = False
    for r in rows:
        values = []
        for k in sorted(r.iterkeys()):
            if not donefields:
                fields.append(k)
            v = r[k]
            if v is None:
                values.append("null")
            elif type(v) == unicode or type(v) == str:
                if escapeCR != "": v = v.replace("\n", escapeCR).replace("\r", "")
                values.append(ds(v))
            elif type(v) == datetime.datetime:
                values.append(ddt(v))
            else:
                values.append(di(v))
        donefields = True
        ins.append("INSERT INTO %s (%s) VALUES (%s);\n" % (table, ",".join(fields), ",".join(values)))
    return "".join(ins)
