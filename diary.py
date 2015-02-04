#!/usr/bin/python

import al
import animal
import audit
import configuration
import datetime
import db
import i18n
import lostfound
import person
import users
import utils
import waitinglist
import wordprocessor

# Diary Links
NO_LINK = 0
ANIMAL = 1
PERSON = 2
LOSTANIMAL = 3
FOUNDANIMAL = 4
WAITINGLIST = 5
MOVEMENT = 6
ANIMALCONTROL = 7

ANIMAL_TASK = 0
PERSON_TASK = 1

def email_uncompleted_upto_today(dbo):
    """
    Goes through all system users and emails them their diary for the
    day - unless the option is turned off.
    """
    if not configuration.email_diary_notes(dbo): return
    l = dbo.locale
    try:
        allusers = users.get_users(dbo)
    except Exception,err:
        al.error("failed getting list of users: %s" % str(err), "diary.email_uncompleted_upto_today", dbo)
    # Grab list of diary notes for today
    notes = get_uncompleted_upto_today(dbo)
    # If we don't have any, bail out
    if len(notes) == 0: return
    # Go through all user to see if we have relevant notes for them
    for u in allusers:
        if u["EMAILADDRESS"] is not None and u["EMAILADDRESS"].strip() != "":
            s = ""
            totalforuser = 0
            for n in notes:
                # Is this note relevant for this user?
                if (n["DIARYFORNAME"] == i18n._("(all)", l) or n["DIARYFORNAME"] == i18n._("(everyone)", l)) \
                or (n["DIARYFORNAME"] == u["USERNAME"]) \
                or (u["ROLES"].find(n["DIARYFORNAME"]) != -1):
                    s += i18n.python2display(l, n["DIARYDATETIME"]) + " "
                    s += n["SUBJECT"]
                    if n["LINKINFO"] is not None and n["LINKINFO"] != "": s += " / " + n["LINKINFO"]
                    s += "\n" + n["NOTE"] + "\n\n"
                    totalforuser += 1
            if totalforuser > 0:
                al.debug("got %d notes for user %s" % (totalforuser, u["USERNAME"]), "diary.email_uncompleted_upto_today", dbo)
                utils.send_email(dbo, "noreply@sheltermanager.com", u["EMAILADDRESS"], "", 
                    i18n._("Diary notes for: {0}", l).format(i18n.python2display(l, i18n.now(dbo.timezone))), s)

def user_role_where_clause(dbo, user = ""):
    """
    Returns a suitable where clause for filtering diary notes
    to the given user or any roles the user is in. If user is
    blank, the where clause return is empty.
    """
    if user == "": return "DiaryForName LIKE '%'"
    roles = users.get_roles_for_user(dbo, user)
    if len(roles) == 0: return "DiaryForName = '%s'" % user
    sroles = []
    for r in roles:
        sroles.append("'" + r.replace("'", "`") + "'")
    return "(DiaryForName = '%s' OR DiaryForName IN (%s))" % (user, ",".join(sroles))

def get_between_two_dates(dbo, user, dbstart, dbend):
    """
    Gets a list of incomplete diary notes between two dates for the user supplied
    LINKID, LINKTYPE, DIARYDATETIME, DIARYFORNAME, SUBJECT, NOTE, LINKINFO
    dbstart: An ISO start date
    dbend: An ISO end date
    """
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE %s " \
        "AND DateCompleted Is Null AND DiaryDateTime >= '%s' AND DiaryDateTime <= '%s'" \
        "ORDER BY DiaryDateTime DESC" % (user_role_where_clause(dbo, user), dbstart, dbend))

def get_uncompleted_upto_today(dbo, user = ""):
    """
    Gets a list of uncompleted diary notes upto and including
    today for the user supplied (or all users if no user passed)
    LINKID, LINKTYPE, DIARYDATETIME, DIARYFORNAME, SUBJECT, NOTE, LINKINFO
    """
    sixmonths = i18n.subtract_days(i18n.now(dbo.timezone), 182)
    current = i18n.now(dbo.timezone)
    alltoday = datetime.datetime(current.year, current.month, current.day, 23, 59, 59)
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE %s " \
        "AND DateCompleted Is Null AND DiaryDateTime <= %s AND DiaryDateTime >= %s" \
        "ORDER BY DiaryDateTime DESC" % (user_role_where_clause(dbo, user), db.ddt(alltoday), db.ddt(sixmonths)))

def get_completed_upto_today(dbo, user = ""):
    """
    Gets a list of completed diary notes upto and including
    today for the user supplied (or all users if no user passed)
    LINKID, LINKTYPE, DIARYDATETIME, DIARYFORNAME, SUBJECT, NOTE, LINKINFO
    """
    sixmonths = i18n.subtract_days(i18n.now(dbo.timezone), 182)
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE %s " \
        "AND DateCompleted Is Not Null AND DiaryDateTime <= %s AND DiaryDateTime >= %s" \
        "ORDER BY DiaryDateTime DESC" % (user_role_where_clause(dbo, user), db.ddt(i18n.now(dbo.timezone)), db.ddt(sixmonths)))

def get_all_upto_today(dbo, user = ""):
    """f
    Gets a list of all diary notes upto and including
    today for the user supplied (or all users if no user passed)
    LINKID, LINKTYPE, DIARYDATETIME, DIARYFORNAME, SUBJECT, NOTE, LINKINFO
    """
    sixmonths = i18n.subtract_days(i18n.now(dbo.timezone), 182)
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE %s " \
        "AND DiaryDateTime <= %s AND DiaryDateTime >= %s" \
        "ORDER BY DiaryDateTime DESC" % (user_role_where_clause(dbo, user), db.ddt(i18n.now(dbo.timezone)), db.ddt(sixmonths)))

def get_future(dbo, user = ""):
    """
    Gets a list of future diary notes
    for the user supplied (or all users if no user passed)
    LINKID, LINKTYPE, DIARYDATETIME, DIARYFORNAME, SUBJECT, NOTE, LINKINFO
    """
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE %s " \
        "AND DiaryDateTime > %s" \
        "ORDER BY DiaryDateTime" % (user_role_where_clause(dbo, user), db.ddt(i18n.now(dbo.timezone))))

def complete_diary_note(dbo, username, diaryid):
    """
    Marks a diary note completed as of right now
    """
    db.execute(dbo, "UPDATE diary SET DateCompleted = %s WHERE ID = %d" % (db.dd(i18n.now(dbo.timezone)), int(diaryid)))
    audit.edit(dbo, username, "diary", str(diaryid) + " => complete")

def rediarise_diary_note(dbo, username, diaryid, newdate):
    """
    Moves a diary note on to the date supplied (newdate is a python date)
    """
    db.execute(dbo, "UPDATE diary SET DiaryDateTime = %s WHERE ID = %d" % (db.dd(newdate), int(diaryid)))
    audit.edit(dbo, username, "diary", str(diaryid) + " => moved on to " + str(newdate))

def get_animal_tasks(dbo):
    """
    Lists all diary tasks for animals
    """
    return db.query(dbo, "SELECT *, CASE " \
        "WHEN EXISTS(SELECT * FROM diarytaskdetail WHERE " \
        "DiaryTaskHeadID = dth.ID AND DayPivot = 0) THEN 1 " \
        "ELSE 0 END AS NEEDSDATE " \
        "FROM diarytaskhead dth WHERE dth.RecordType = %d" % ANIMAL_TASK)

def get_person_tasks(dbo):
    """
    Lists all diary tasks for people
    """
    return db.query(dbo, "SELECT *, CASE " \
        "WHEN EXISTS(SELECT * FROM diarytaskdetail WHERE " \
        "DiaryTaskHeadID = dth.ID AND DayPivot = 0) THEN 1 " \
        "ELSE 0 END AS NEEDSDATE " \
        "FROM diarytaskhead dth WHERE dth.RecordType = %d" % PERSON_TASK)

def get_diarytasks(dbo):
    """
    Returns all diary tasks headers with a NUMBEROFTASKS value.
    """
    return db.query(dbo, "SELECT d.*, " \
        "(SELECT COUNT(*) FROM diarytaskdetail WHERE DiaryTaskHeadID = d.ID) AS NUMBEROFTASKS " \
        "FROM diarytaskhead d " \
        "ORDER BY d.Name")

def get_diarytask_name(dbo, taskid):
    """
    Returns the name for a diarytask
    """
    return db.query_string(dbo, "SELECT Name FROM diarytaskhead WHERE ID=%d" % int(taskid))

def get_diarytask_details(dbo, headid):
    """
    Returns the detail rows for a diary task
    """
    def fix(s):
        return s.replace("<", "&lt;").replace(">", "&gt;")
    rows = db.query(dbo, "SELECT * FROM diarytaskdetail WHERE DiaryTaskHeadID=%d" % int(headid))
    for r in rows:
        r["SUBJECT"] = fix(r["SUBJECT"])
        r["NOTE"] = fix(r["NOTE"])
    return rows

def get_diary(dbo, diaryid):
    """
    Returns a diary record
    """
    return db.query(dbo, "SELECT * FROM diary WHERE ID = %d" % diaryid)[0]

def delete_diary(dbo, username, diaryid):
    """
    Deletes a diary record
    """
    audit.delete(dbo, username, "diary", str(db.query(dbo, "SELECT * FROM diary WHERE ID = %d" % int(diaryid))))
    db.execute(dbo, "DELETE FROM diary WHERE ID = %d" % int(diaryid))

def get_diaries(dbo, linktypeid, linkid):
    """
    Returns all diary notes for a particular link
    """
    return db.query(dbo, "SELECT *, cast(DiaryDateTime AS time) AS DiaryTime " \
        "FROM diary WHERE LinkType=%d AND LinkID=%d " \
        "ORDER BY DiaryDateTime" % ( int(linktypeid), int(linkid) ))

def get_link_info(dbo, linktypeid, linkid):
    """
    Returns the linkinfo string for the id/type
    """
    l = dbo.locale
    if linktypeid == ANIMAL:
        return "%s [%s]" % (animal.get_animal_namecode(dbo, linkid), animal.get_display_location_noq(dbo, linkid))

    elif linktypeid == PERSON:
        return person.get_person_name(dbo, linkid)

    elif linktypeid == LOSTANIMAL:
        return i18n._("Lost Animal: {0}", l).format(lostfound.get_lost_person_name(dbo, linkid))

    elif linktypeid == FOUNDANIMAL:
        return i18n._("Found Animal: {0}", l).format(lostfound.get_found_person_name(dbo, linkid))

    elif linktypeid == WAITINGLIST:
        return i18n._("Waiting List: {0}", l).format(waitinglist.get_person_name(dbo, linkid))

def insert_diary_from_form(dbo, username, linktypeid, linkid, post):
    """
    Creates a diary note from the form data
    username: User creating the diary
    linktypeid, linkid: The link
    post: A PostedData object
    """
    l = dbo.locale
    if post["diarydate"] == "":
        raise utils.ASMValidationError(i18n._("Diary date cannot be blank", l))
    if post.date("diarydate") is None:
        raise utils.ASMValidationError(i18n._("Diary date is not valid", l))
    if post["subject"] == "":
        raise utils.ASMValidationError(i18n._("Diary subject cannot be blank", l))
    if post["note"] == "":
        raise utils.ASMValidationError(i18n._("Diary note cannot be blank", l))
    diarytime =  post["diarytime"].strip()
    if diarytime != "":
        if diarytime.find(":") == -1:
            raise utils.ASMValidationError(i18n._("Invalid time, times should be in HH:MM format", l))
        if not utils.is_numeric(diarytime.replace(":", "")):
            raise utils.ASMValidationError(i18n._("Invalid time, times should be in HH:MM format", l))

    linkinfo = get_link_info(dbo, linktypeid, linkid)
    diaryid = db.get_id(dbo, "diary")
    sql = db.make_insert_user_sql(dbo, "diary", username, (
        ( "ID", db.di(diaryid)),
        ( "LinkID", db.di(linkid) ),
        ( "LinkType", db.di(linktypeid) ),
        ( "LinkInfo", db.ds(linkinfo) ),
        ( "DiaryDateTime", post.db_datetime("diarydate", "diarytime")), 
        ( "DiaryForName", post.db_string("diaryfor")),
        ( "Subject", post.db_string("subject")),
        ( "Note", post.db_string("note")),
        ( "DateCompleted", post.db_date("completed"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "diary", str(diaryid))
    return diaryid

def insert_diary(dbo, username, linktypeid, linkid, diarydate, diaryfor, subject, note):
    """
    Creates a diary note from the form data
    username: User creating the diary
    linktypeid, linkid: The link
    diarydate: The date to stamp on the note (python format)
    diaryfor: Who the diary note is for
    subject, note
    """
    linkinfo = ""
    if linkid != 0:
        linkinfo = get_link_info(dbo, linktypeid, linkid)
    diaryid = db.get_id(dbo, "diary")
    sql = db.make_insert_user_sql(dbo, "diary", username, (
        ( "ID", db.di(diaryid)),
        ( "LinkID", db.di(linkid) ),
        ( "LinkType", db.di(linktypeid) ),
        ( "LinkInfo", db.ds(linkinfo) ),
        ( "DiaryDateTime", db.dd(diarydate) ),
        ( "DiaryForName", db.ds(diaryfor) ),
        ( "Subject", db.ds(subject) ),
        ( "Note", db.ds(note) ),
        ( "DateCompleted", db.dd(None) )
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "diary", str(diaryid))
    return diaryid

def update_diary_from_form(dbo, username, post):
    """
    Updates a diary note from form data
    """
    l = dbo.locale
    diaryid = post.integer("diaryid")
    if post["diarydate"] == "":
        raise utils.ASMValidationError(i18n._("Diary date cannot be blank", l))
    if post.date("diarydate") is None:
        raise utils.ASMValidationError(i18n._("Diary date is not valid", l))
    if post["subject"] == "":
        raise utils.ASMValidationError(i18n._("Diary subject cannot be blank", l))
    if post["note"] == "":
        raise utils.ASMValidationError(i18n._("Diary note cannot be blank", l))
    diarytime =  post["diarytime"].strip()
    if diarytime != "":
        if diarytime.find(":") == -1:
            raise utils.ASMValidationError(i18n._("Invalid time, times should be in HH:MM format", l))
        if not utils.is_numeric(diarytime.replace(":", "")):
            raise utils.ASMValidationError(i18n._("Invalid time, times should be in HH:MM format", l))

    sql = db.make_update_user_sql(dbo, "diary", username, "ID=%d" % diaryid, (
        ( "DiaryDateTime", post.db_datetime("diarydate", "diarytime")), 
        ( "DiaryForName", post.db_string("diaryfor")),
        ( "Subject", post.db_string("subject")),
        ( "Note", post.db_string("note")),
        ( "DateCompleted", post.db_date("completed"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM diary WHERE ID=%d" % diaryid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM diary WHERE ID=%d" % diaryid)
    audit.edit(dbo, username, "diary", audit.map_diff(preaudit, postaudit))

def execute_diary_task(dbo, username, tasktype, taskid, linkid, selecteddate):
    """
    Runs a diary task
    tasktype: ANIMAL or PERSON
    taskid: The ID of the diarytaskhead record to run
    linkid: The ID of the animal or person to run against
    selecteddate: If the task has any detail records with a pivot of 0, the date to supply (as python date)
    """
    def fix(s):
        return s.replace("<", "&lt;").replace(">", "&gt;")
    rollingdate = i18n.now(dbo.timezone) 
    dtd = db.query(dbo, "SELECT * FROM diarytaskdetail WHERE DiaryTaskHeadID = %d ORDER BY ID" % int(taskid))
    tags = {}
    linktype = ANIMAL
    if tasktype == "ANIMAL": 
        linktype = ANIMAL
        tags = wordprocessor.animal_tags(dbo, animal.get_animal(dbo, int(linkid)))
    elif tasktype == "PERSON": 
        linktype = PERSON
        tags = wordprocessor.person_tags(dbo, person.get_person(dbo, int(linkid)))
    for d in dtd:
        if d["DAYPIVOT"] == 9999: 
            rollingdate = selecteddate
        else:
            rollingdate = i18n.add_days(rollingdate, int(d["DAYPIVOT"]))
        insert_diary(dbo, username, linktype, int(linkid), rollingdate, \
            d["WHOFOR"], \
            wordprocessor.substitute_tags(fix(d["SUBJECT"]), tags, True), \
            wordprocessor.substitute_tags(fix(d["NOTE"]), tags, True))

def insert_diarytaskhead_from_form(dbo, username, post):
    """
    Creates a diary task header from form data
    """
    nid = db.get_id(dbo, "diarytaskhead")
    sql = db.make_insert_sql("diarytaskhead", (
        ( "ID", db.di(nid)),
        ( "Name", post.db_string("name")),
        ( "RecordType", post.db_integer("type")),
        ( "RecordVersion", db.di(0))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "diarytaskhead", str(nid))
    return nid

def update_diarytaskhead_from_form(dbo, username, post):
    """
    Updates a diary task header from form data
    """
    tid = post.integer("diarytaskid")
    sql = db.make_update_sql("diarytaskhead", "ID=%d" % tid, (
        ( "Name", post.db_string("name")),
        ( "RecordType", post.db_integer("type"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM diarytaskhead WHERE ID=%d" % tid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM diarytaskhead WHERE ID=%d" % tid)
    audit.edit(dbo, username, "diarytaskhead", audit.map_diff(preaudit, postaudit))

def delete_diarytask(dbo, username, taskid):
    """
    Deletes a diary task
    """
    audit.delete(dbo, username, "diarytaskhead", str(db.query(dbo, "SELECT * FROM diarytaskhead WHERE ID = %d" % int(taskid))))
    db.execute(dbo, "DELETE FROM diarytaskdetail WHERE DiaryTaskHeadID = %d" % int(taskid))
    db.execute(dbo, "DELETE FROM diarytaskhead WHERE ID = %d" % int(taskid))

def insert_diarytaskdetail_from_form(dbo, username, post):
    """
    Creates a diary task detail from form data
    """
    nid = db.get_id(dbo, "diarytaskdetail")
    sql = db.make_insert_sql("diarytaskdetail", (
        ( "ID", db.di(nid)),
        ( "DiaryTaskHeadID", post.db_integer("taskid")),
        ( "DayPivot", post.db_integer("pivot")),
        ( "WhoFor", post.db_string("for")),
        ( "Subject", post.db_string("subject")),
        ( "Note", post.db_string("note")),
        ( "RecordVersion", db.di(0))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "diarytaskdetail", str(nid))
    return nid

def update_diarytaskdetail_from_form(dbo, username, post):
    """
    Updates a diary task detail from form data
    """
    did = post.integer("diarytaskdetailid")
    sql = db.make_update_sql("diarytaskdetail", "ID=%d" % did, (
        ( "DayPivot", post.db_integer("pivot")),
        ( "WhoFor", post.db_string("for")),
        ( "Subject", post.db_string("subject")),
        ( "Note", post.db_string("note"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM diarytaskdetail WHERE ID=%d" % did)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM diarytaskdetail WHERE ID=%d" % did)
    audit.edit(dbo, username, "diarytaskhead", audit.map_diff(preaudit, postaudit))

def delete_diarytaskdetail(dbo, username, did):
    """
    Deletes a diary task detail record
    """
    audit.delete(dbo, username, "diarytaskdetail", str(db.query(dbo, "SELECT * FROM diarytaskdetail WHERE ID = %d" % int(did))))
    db.execute(dbo, "DELETE FROM diarytaskdetail WHERE ID = %d" % int(did))


