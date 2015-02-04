#!/usr/bin/python

import al
import base64
import db
import mimetypes
import sys
import urllib2
import utils
from sitedefs import URL_NEWS

def create_path(dbo, path, name):
    """
    Creates a new DBFS folder
    """
    db.execute(dbo, "INSERT INTO dbfs (ID, Name, Path) VALUES (%d, '%s', '%s')" % (db.get_id(dbo, "dbfs"), name, path))

def check_create_path(dbo, path):
    """
    Verifies that portions of a path exist and creates them if not
    only goes to two levels deep as we never need more than that
    for anything within ASM.
    """
    def check(name, path):
        if 0 == db.query_int(dbo, "SELECT COUNT(*) FROM dbfs WHERE Name = '%s' AND Path = '%s'" % (name, path)):
            create_path(dbo, path, name)
    pat = path[1:].split("/")
    check(pat[0], "/")
    if len(pat) > 1:
        check(pat[1], "/" + pat[0])

def get_string_filepath(dbo, filepath):
    """
    Gets DBFS file contents as a string. Returns
    an empty string if the file is not found. Splits
    filepath into the name and path to do it.
    """
    name = filepath[filepath.rfind("/")+1:]
    path = filepath[0:filepath.rfind("/")]
    return get_string(dbo, name, path)

def get_string(dbo, name, path = ""):
    """
    Gets DBFS file contents as a string. Returns
    an empty string if the file is not found. If no path
    is supplied, just finds the first file with that name
    in the dbfs (useful for media files, which have unique names)
    """
    s = ""
    if path != "":
        r = db.query_tuple(dbo, "SELECT Content FROM dbfs WHERE Name = '%s' AND Path = '%s'" % (name, path))
        if len(r) > 0 and len(r[0]) > 0:
            s = r[0][0]
    else:
        r = db.query_tuple(dbo, "SELECT Content FROM dbfs WHERE Name = '%s'" % name)
        if len(r) > 0 and len(r[0]) > 0:
            s = r[0][0]
    if s != "":
        try:
            s = base64.b64decode(s)
        except:
            em = str(sys.exc_info()[0])
            al.error("Failed unpacking path=%s, name=%s: %s" % (path, name, em), "dbfs.get_string", dbo)
            s = ""
    return s

def get_string_id(dbo, dbfsid):
    """
    Gets DBFS file contents as a string. Returns
    an empty string if the file is not found.
    """
    s = ""
    r = db.query_tuple(dbo, "SELECT Content FROM dbfs WHERE ID = '%d'" % dbfsid)
    if len(r) > 0 and len(r[0]) > 0:
        s = r[0][0]
    if s != "":
        try:
            s = base64.b64decode(s)
        except:
            em = str(sys.exc_info()[0])
            al.error("Failed unpacking id=%d: %s" % (dbfsid, em), "dbfs.get_string_id", dbo)
            s = ""
    return s

def rename_file(dbo, path, oldname, newname):
    """
    Renames a file in the dbfs.
    """
    db.execute(dbo, "UPDATE dbfs SET Name = '%s' WHERE Name = '%s' AND " \
        "Path = '%s'" % \
        (newname, oldname, path))

def rename_file_id(dbo, dbfsid, newname):
    """
    Renames a file in the dbfs.
    """
    db.execute(dbo, "UPDATE dbfs SET Name = '%s' WHERE ID = %d" % (newname, dbfsid))

def put_file(dbo, name, path, filepath):
    """
    Reads the the file from filepath and stores it with name/path
    """
    check_create_path(dbo, path)
    f = open(filepath, "rb")
    s = base64.b64encode(f.read())
    f.close()
    db.execute(dbo, "INSERT INTO dbfs (ID, Name, Path, Content) VALUES (%d, '%s', '%s', '%s')" % ( db.get_id(dbo, "dbfs"), name, path, s ))

def put_string(dbo, name, path, contents):
    """
    Stores the file contents at the name and path. If the file exists, overwrites it.
    """
    check_create_path(dbo, path)
    s = base64.b64encode(contents)
    name = name.replace("'", "")
    path = path.replace("'", "")
    dbfsid = db.get_id(dbo, "dbfs")
    db.execute(dbo, "DELETE FROM dbfs WHERE Path = '%s' AND Name = '%s'" % ( path, name ))
    db.execute(dbo, "INSERT INTO dbfs (ID, Name, Path, Content) VALUES (%d, '%s', '%s', '%s')" % ( dbfsid, name, path, s ))
    return dbfsid

def put_string_id(dbo, dbfsid, contents):
    """
    Stores the file contents at the id given.
    """
    s = base64.b64encode(contents)
    db.execute(dbo, "UPDATE dbfs SET Content = '%s' WHERE ID = %d" % (s, dbfsid))

def put_string_filepath(dbo, filepath, contents):
    """
    Stores the file contents at the name/path given.
    """
    name = filepath[filepath.rfind("/")+1:]
    path = filepath[0:filepath.rfind("/")]
    return put_string(dbo, name, path, contents)

def replace_string(dbo, content, name, path = ""):
    """
    Replaces the file contents given as a string in the dbfs
    with the name and path given. If no path is given, looks it
    up by just the name.
    """
    enc = base64.b64encode(content)
    if path != "":
        db.execute(dbo, "UPDATE dbfs SET Content = '%s' WHERE Name = '%s' AND Path = '%s'" % ( enc, name, path ))
    else:
        db.execute(dbo, "UPDATE dbfs SET Content = '%s' WHERE Name = '%s'" % ( enc, name ))

def get_file(dbo, name, path, saveto):
    """
    Gets DBFS file contents and saves them to the
    filename given. Returns True for success
    """
    if path != "":
        s = db.query_string(dbo, "SELECT Content FROM dbfs WHERE Name = '%s' AND Path = '%s'" % (name, path))
    else:
        s = db.query_string(dbo, "SELECT Content FROM dbfs WHERE Name = '%s'" % name)
    if s != "":
        f = open(saveto, "wb")
        f.write(base64.b64decode(s))
        f.close()
        return True
    return False

def file_exists(dbo, name):
    """
    Return True if a file with name exists in the database.
    """
    return db.query_int(dbo, "SELECT COUNT(*) FROM dbfs WHERE Name = '%s'" % name) > 0

def get_files(dbo, name, path, saveto):
    """
    Gets DBFS files for the pattern given in name (use % like db)
    and belonging to path (blank for all paths). saveto is
    the folder to save all the files to. Returns True for success
    """
    if path != "":
        rows = db.query(dbo, "SELECT Content FROM dbfs WHERE LOWER(Name) Like '%s' AND Path = '%s'" % (name, path))
    else:
        rows = db.query(dbo, "SELECT Content FROM dbfs WHERE LOWER(Name) Like '%s'" % name)
    if len(rows) > 0:
        for r in rows:
            f = open(saveto, "wb")
            f.write(base64.b64decode(r["CONTENT"]))
            f.close()
        return True
    return False

def delete_path(dbo, path):
    """
    Deletes all items matching the path given
    """
    db.execute(dbo, "DELETE FROM dbfs WHERE Path LIKE '%s'" % path )

def delete(dbo, name, path = ""):
    """
    Deletes all items matching the name and path given
    """
    if path != "":
        db.execute(dbo, "DELETE FROM dbfs WHERE Name LIKE '%s' AND Path LIKE '%s'" % ( name, path ))
    else:
        db.execute(dbo, "DELETE FROM dbfs WHERE Name LIKE '%s'" % name)

def delete_filepath(dbo, filepath):
    """
    Deletes the dbfs entry for the filepath
    """
    name = filepath[filepath.rfind("/")+1:]
    path = filepath[0:filepath.rfind("/")]
    delete(dbo, name, path)

def delete_id(dbo, dbfsid):
    """
    Deletes the dbfs entry for the id
    """
    db.execute(dbo, "DELETE FROM dbfs WHERE ID = %d" % dbfsid)

def list_contents(dbo, path):
    """
    Returns a list of items in the path given. Directories
    are identifiable by not having a file extension.
    """
    rows = db.query(dbo, "SELECT Name FROM dbfs WHERE Path = '%s'" % path)
    l = []
    for r in rows:
        l.append(r["NAME"])
    return l

def get_nopic(dbo):
    """
    Returns the nopic jpeg file
    """
    return get_string(dbo, "nopic.jpg", "/reports")

def get_html_templates(dbo):
    """
    Returns a list of all HTML templates
    """
    return db.query(dbo, "SELECT ID, Name, Path FROM dbfs WHERE Name Like '%.html' AND Path Like '/templates%' ORDER BY Path, Name")

def get_html_publisher_templates(dbo):
    """
    Returns a list of available template/styles for the html publisher
    """
    l = []
    rows = db.query(dbo, "SELECT Name, Path FROM dbfs WHERE Path Like '/internet' ORDER BY Name")
    hasRootStyle = False
    for r in rows:
        if r["NAME"].find(".dat") != -1:
            hasRootStyle = True
        elif r["NAME"].find(".") == -1:
            l.append(r["NAME"])
    if hasRootStyle:
        l.append(".")
    return sorted(l)

def get_html_publisher_templates_files(dbo):
    """
    Returns a list of all templates/styles with their header, footer and bodies.
    This call can only be used for grabbing them for the UI. It turns < and > into
    &lt; and &gt; so that json encoding the result doesn't blow up the browser.
    """
    def fix(s):
        return s.replace("<", "&lt;").replace(">", "&gt;")
    templates = []
    available = get_html_publisher_templates(dbo)
    for name in available:
        if name != ".":
            head = get_string(dbo, "head.html", "/internet/%s" % name)
            if head == "": head = get_string(dbo, "pih.dat", "/internet/%s" % name)
            body = get_string(dbo, "body.html", "/internet/%s" % name)
            if body == "": body = get_string(dbo, "pib.dat", "/internet/%s" % name)
            foot = get_string(dbo, "foot.html", "/internet/%s" % name)
            if foot == "": foot = get_string(dbo, "pif.dat", "/internet/%s" % name)
            templates.append({ "NAME": name, "HEADER": fix(head), "BODY": fix(body), "FOOTER": fix(foot)})
    return templates

def update_html_publisher_template(dbo, username, name, header, body, footer):
    """
    Creates a new html publisher template with the name given. If the
    template already exists, it recreates it.
    """
    delete_path(dbo, "/internet/" + name)
    delete(dbo, name, "/internet")
    create_path(dbo, "/internet", name)
    put_string(dbo, "head.html", "/internet/%s" % name, header)
    put_string(dbo, "body.html", "/internet/%s" % name, body)
    put_string(dbo, "foot.html", "/internet/%s" % name, footer)
    al.debug("%s updated html template %s" % (username, name), "dbfs.update_html_publisher_template", dbo)

def delete_html_publisher_template(dbo, username, name):
    delete_path(dbo, "/internet/" + name)
    delete(dbo, name, "/internet")
    al.debug("%s deleted html template %s" % (username, name), "dbfs.update_html_publisher_template", dbo)

def get_publish_logs(dbo):
    """
    Returns a list of all publisher log files
    """
    CHECK_LAST = 10
    plogs = db.query(dbo, "SELECT ID, Name, Path FROM dbfs WHERE Path Like '/logs/publish%' ORDER BY Name DESC")
    plogc = db.query(dbo, "SELECT Content FROM dbfs WHERE Path Like '/logs/publish%%' ORDER BY Name DESC LIMIT %d" % CHECK_LAST)
    for i in xrange(0, len(plogc)):
        if i >= CHECK_LAST:
            plogs[i]["ALERTS"] = 0
            plogs[i]["SUCCESS"] = 0
        else:
            plogs[i]["ALERTS"] = base64.b64decode(plogc[i]["CONTENT"]).count("ALERT:")
            plogs[i]["SUCCESS"] = base64.b64decode(plogc[i]["CONTENT"]).count("SUCCESS:")
    return plogs

def get_publish_alerts(dbo):
    """
    Returns the number of logs out of the last 10 that had
    errors (the token ALERT: appears in them)
    """
    rows = db.query_cache(dbo, "SELECT Content FROM dbfs WHERE Path Like '/logs/publish%' ORDER BY Name DESC LIMIT 10", 120)
    alerts = 0
    for r in rows:
        if base64.b64decode(r["CONTENT"]).find("ALERT:") != -1:
            alerts += 1
    return alerts

def delete_old_publish_logs(dbo):       
    """
    Retains only the last MAX_LOGS publish logs
    """
    MAX_LOGS = 30
    rows = db.query(dbo, "SELECT Name FROM dbfs WHERE Path Like '/logs/publish%%' ORDER BY Name DESC LIMIT %d" % MAX_LOGS)
    if len(rows) < MAX_LOGS: return
    names = []
    for r in rows: names.append("'" + r["NAME"] + "'")
    notin = ",".join(names)
    count = db.query_int(dbo, "SELECT COUNT(*) FROM dbfs WHERE Path Like '/logs/publish%%' AND Name NOT IN (%s)" % notin)
    al.debug("removing %d publishing logs (keep latest 30)." % count, "dbfs.delete_old_publish_logs", dbo)
    rq = "DELETE FROM dbfs WHERE Path Like '/logs/publish%%' AND Name NOT IN (%s)" % notin
    db.execute(dbo, rq)

def sanitise_path(path):
    """ Strips disallowed chars from new paths """
    disallowed = (" ", "|", ",", "!", "\"", "'", "$", "%", "^", "*",
        "(", ")", "[", "]", "{", "}", "\\", ":", "@", "?", "+")
    for d in disallowed:
        path = path.replace(d, "_")
    return path

def create_html_template(dbo, name, content = "<p></p>"):
    """
    Creates an html template from the name given.
    If there's no .html prefix, adds it
    If it's a relative path (doesn't start with /) adds /templates/ to the front
    If it's an absolute path that doesn't start with /templates/, add /templates
    Changes spaces and unwanted punctuation to underscores
    """
    filepath = name
    if not filepath.endswith(".html"): filepath += ".html"
    if not filepath.startswith("/"): filepath = "/templates/" + filepath
    if not filepath.startswith("/templates"): filepath = "/templates" + filepath
    filepath = sanitise_path(filepath)
    return put_string_filepath(dbo, filepath, content)

def clone_html_template(dbo, dbfsid, newname):
    """
    Creates a new html template with the content from the
    dbfsid given.
    """
    content = get_string_id(dbo, dbfsid)
    return create_html_template(dbo, newname, content)

def get_name_for_id(dbo, dbfsid):
    """
    Returns the filename of the item with id dbfsid
    """
    return db.query_string(dbo, "SELECT Name FROM dbfs WHERE ID = %d" % dbfsid)

def get_document_repository(dbo):
    """
    Returns a list of all documents in the /document_repository directory,
    also includes MIMETYPE field for display
    """
    rows = db.query(dbo, "SELECT ID, Name, Path FROM dbfs WHERE " \
        "Path Like '/document_repository%' AND Name Like '%.%' ORDER BY Path, Name")
    for r in rows:
        mimetype, encoding = mimetypes.guess_type("file://" + r["NAME"], strict=False)
        r["MIMETYPE"] = mimetype
    return rows

def get_report_images(dbo):
    """
    Returns a list of all extra images in the /reports directory
    """
    return db.query(dbo, "SELECT Name, Path FROM dbfs WHERE " \
        "(LOWER(Name) Like '%.jpg' OR LOWER(Name) Like '%.png' OR LOWER(Name) Like '%.gif') " \
        "AND Path Like '/report%' ORDER BY Path, Name")

def upload_report_image(dbo, fc):
    """
    Attaches an image from a form filechooser object and puts
    it in the /reports directory. 
    """
    ext = ""
    ext = fc.filename
    filename = utils.filename_only(fc.filename)
    filedata = fc.value
    ext = ext[ext.rfind("."):].lower()
    ispicture = ext == ".jpg" or ext == ".jpeg" or ext == ".png" or ext == ".gif"
    if not ispicture:
        raise utils.ASMValidationError("upload_report_image only accepts images.")
    put_string(dbo, filename, "/reports", filedata)

def upload_document_repository(dbo, path, fc):
    """
    Attaches a document from a form filechooser object and puts
    it in the /document_repository directory. 
    An extra path portion can be specified in path.
    """
    ext = ""
    ext = fc.filename
    filename = utils.filename_only(fc.filename)
    filedata = fc.value
    ext = ext[ext.rfind("."):].lower()
    if path != "" and path.startswith("/"): path = path[1:]
    if path == "":
        filepath = "/document_repository/%s" % filename
    else:
        path = sanitise_path(path)
        filepath = "/document_repository/%s/%s" % (path, filename)
    put_string_filepath(dbo, filepath, filedata)

def has_nopic(dbo):
    """
    Returns True if the database has a nopic.jpg file
    """
    return get_nopic(dbo) != ""

def has_html_templates(dbo):
    """
    Returns True if there are some html templates in the database
    """
    return len(get_html_templates(dbo)) > 0

def get_asm_news(dbo):
    """
    Reads the latest asm news from the file /asm.news and returns it.
    If the file doesn't exist, calls update_asm_news to create it
    """
    s = get_string(dbo, "asm.news")
    if s == "": 
        update_asm_news(dbo)
        return get_string(dbo, "asm.news")
    return s

def update_asm_news(dbo):
    """
    Reads the latest asm news and stores it in the dbfs
    """
    s = ""
    try:
        s = urllib2.urlopen(URL_NEWS).read()
    except:
        em = str(sys.exc_info()[0])
        al.error("Failed reading ASM news: %s" % em, "dbfs.update_asm_news", dbo)
    else:
        al.debug("Updated ASM news, got %d bytes" % len(s), "dbfs.update_asm_news", dbo)
    x = get_string(dbo, "asm.news")
    if x == "":
        put_string(dbo, "asm.news", "/", s)
    else:
        replace_string(dbo, s, "asm.news")


