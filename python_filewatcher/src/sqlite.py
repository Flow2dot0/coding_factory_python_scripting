import sqlite3

sql = sqlite3.connect("watcher.sqlite")
cursor = sql.cursor()


def init():
    """Initialize database
    :return: query
    """
    return cursor.execute("CREATE TABLE IF NOT EXISTS directory(filename text, directory text, signature text)")


def write(filename, directory, signature):
    """Write signature in specific file from database
    """
    cursor.execute("INSERT INTO directory(filename,directory,signature) VALUES(?,?,?)",
                   [filename, directory, signature])
    sql.commit()


def select(filename):
    """Select file from database
    :return: list
    """
    cursor.execute("SELECT * FROM directory WHERE filename = ?", [filename])
    return cursor.fetchone()


def select_filename():
    """Select all files from database
    :return: table as list
    """
    table = []
    cursor.execute("SELECT filename FROM directory")
    data = cursor.fetchall()
    for i in range(0, len(data)):
        table.append(data[i][0])
    return table


def count(filename):
    """Count files from database using filename
    :return: int
    """
    cursor.execute("SELECT * FROM directory WHERE filename = ?", [filename])
    return len(cursor.fetchall())


def update_signature(filename, signature):
    """Update signature file in database
    :return: bool
    """
    try:
        cursor.execute("UPDATE directory SET signature = ? WHERE filename=?", [signature, filename])
        sql.commit()
        return True
    except:
        return False


def remove_filename(filename):
    """Remove file from database
    :return: bool
    """
    try:
        cursor.execute("DELETE FROM directory WHERE filename = ?", [filename])
        sql.commit()
        return True
    except:
        return False
