#!/usr/bin/python

import additional
import audit
import configuration
import db
import diary
import log
import media
import utils
from i18n import _, now, subtract_days, display2python, python2display, format_time_now

ASCENDING = 0
DESCENDING = 1

def get_animalcontrol_query(dbo):
    return "SELECT ac.*, ac.ID AS ACID, s.SpeciesName, x.Sex AS SexName, " \
        "co.OwnerName AS CallerName, co.HomeTelephone, co.WorkTelephone, co.MobileTelephone, " \
        "o1.OwnerName AS OwnerName, o1.OwnerName AS OwnerName1, o2.OwnerName AS OwnerName2, o3.OwnerName AS OwnerName3, " \
        "vo.OwnerName AS VictimName, ti.IncidentName, ci.CompletedName, a.AnimalName, a.ShelterCode " \
        "FROM animalcontrol ac " \
        "LEFT OUTER JOIN species s ON s.ID = ac.SpeciesID " \
        "LEFT OUTER JOIN lksex x ON x.ID = ac.Sex " \
        "LEFT OUTER JOIN animal a ON a.ID = ac.AnimalID " \
        "LEFT OUTER JOIN owner co ON co.ID = ac.CallerID " \
        "LEFT OUTER JOIN owner o1 ON o1.ID = ac.OwnerID " \
        "LEFT OUTER JOIN owner o2 ON o2.ID = ac.Owner2ID " \
        "LEFT OUTER JOIN owner o3 ON o3.ID = ac.Owner3ID " \
        "LEFT OUTER JOIN owner vo ON vo.ID = ac.VictimID " \
        "LEFT OUTER JOIN incidenttype ti ON ti.ID = ac.IncidentTypeID " \
        "LEFT OUTER JOIN incidentcompleted ci ON ci.ID = ac.IncidentCompletedID"

def get_traploan_query(dbo):
    return "SELECT ot.ID, ot.TrapTypeID, ot.LoanDate, tt.TrapTypeName, ot.TrapNumber, " \
        "ot.DepositAmount, ot.DepositReturnDate, ot.ReturnDueDate, ot.ReturnDate, " \
        "ot.OwnerID, ot.Comments, " \
        "o.OwnerTitle, o.OwnerInitials, o.OwnerSurname, o.OwnerForenames, o.OwnerName " \
        "FROM ownertraploan ot " \
        "INNER JOIN traptype tt ON tt.ID = ot.TrapTypeID " \
        "INNER JOIN owner o ON o.ID = ot.OwnerID "

def get_animalcontrol(dbo, acid):
    """
    Returns an animal control incident record
    """
    rows = db.query(dbo, get_animalcontrol_query(dbo) + " WHERE ac.ID = %d" % int(acid))
    if rows == None or len(rows) == 0:
        return None
    else:
        return rows[0]

def get_followup_two_dates(dbo, dbstart, dbend):
    """
    Returns incidents for followup between the two ISO dates specified
    """
    return db.query(dbo, get_animalcontrol_query(dbo) + " WHERE " \
        "(ac.FollowupDateTime >= '%(start)s' AND ac.FollowupDateTime <= '%(end)s') OR " \
        "(ac.FollowupDateTime2 >= '%(start)s' AND ac.FollowupDateTime2 <= '%(end)s') OR " \
        "(ac.FollowupDateTime3 >= '%(start)s' AND ac.FollowupDateTime3 <= '%(end)s')" % { "start": dbstart, "end": dbend })

def get_animalcontrol_find_simple(dbo, query = "", limit = 0, onlyindexed = False):
    """
    Returns rows for simple animal control searches.
    query: The search criteria
    """
    ors = []
    query = query.replace("'", "`")
    def add(field):
        return utils.where_text_filter(dbo, field, query)
    # If no query has been given, show open animal control records
    # from the last 30 days
    if query == "":
        ors.append("ac.IncidentDateTime > %s AND ac.CompletedDate Is Null" % db.dd(subtract_days(now(dbo.timezone), 30)))
    else:
        if utils.is_numeric(query):
            ors.append("ac.ID = " + str(utils.cint(query)))
        ors.append(add("co.OwnerName"))
        ors.append(add("ti.IncidentName"))
        ors.append(add("ac.DispatchAddress"))
        ors.append(add("ac.DispatchPostcode"))
        ors.append(add("o1.OwnerName"))
        ors.append(add("o2.OwnerName"))
        ors.append(add("o3.OwnerName"))
        ors.append(add("vo.OwnerName"))
        if not onlyindexed:
            ors.append(add("ac.CallNotes"))
            ors.append(add("ac.AnimalDescription"))
    sql = get_animalcontrol_query(dbo) + " WHERE " + " OR ".join(ors)
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_animalcontrol_find_advanced(dbo, criteria, limit = 0):
    """
    Returns rows for advanced animal control searches.
    criteria: A dictionary of criteria
       number - string partial pattern
       callername - string partial pattern
       victimname - string partial pattern
       callerphone - string partial pattern
       incidenttype - -1 for all or ID
       dispatchedaco - string partial pattern
       completedtype - -1 for all or ID
       citationtype - -1 for all or ID
       address - string partial pattern
       postcode - string partial pattern
       description - string partial pattern
       agegroup - agegroup text to match
       sex - -1 for all or ID
       species - -1 for all or ID
       filter - unpaid, incomplete, undispatched, requirefollowup
       incidentfrom - incident date from in current display locale format
       incidentto - incident date to in current display locale format
       dispatchfrom - dispatch date from in current display locale format
       dispatchto - dispatch date from in current display locale format
       respondedfrom - responded date from in current display locale format
       respondedto - responded date to in current display locale format
       followupfrom - follow up date from in current display locale format
       followupto - follow up date to in current display locale format
       completedfrom - completed date from in current display locale format
       completedto - completed date to in current display locale format

    """
    c = []
    l = dbo.locale
    post = utils.PostedData(criteria, l)

    def hk(cfield):
        return post[cfield] != ""

    def crit(cfield):
        return post[cfield]

    def addid(cfield, field): 
        if hk(cfield) and int(crit(cfield)) != -1: 
            c.append("%s = %s" % (field, crit(cfield)))

    def addstr(cfield, field): 
        if hk(cfield) and crit(cfield) != "": 
            c.append("LOWER(%s) LIKE '%%%s%%'" % ( field, crit(cfield).lower().replace("'", "`")))

    def adddate(cfieldfrom, cfieldto, field): 
        if hk(cfieldfrom) and hk(cfieldto): 
            c.append("%s >= %s AND %s <= %s" % ( 
            field, db.dd(display2python(l, crit(cfieldfrom))), 
            field, db.dd(display2python(l, crit(cfieldto)))))

    def addcomp(cfield, value, condition):
        if hk(cfield) and crit(cfield) == value: 
            c.append(condition)

    c.append("ac.ID > 0")
    if crit("number") != "": c.append("ac.ID = " + str(utils.cint(crit("number"))))
    addstr("callername", "co.OwnerName")
    addstr("victimname", "vo.OwnerName")
    addstr("callerphone", "co.HomeTelephone")
    addid("incidenttype", "ac.IncidentTypeID")
    if (crit("dispatchedaco") != "-1"): addstr("dispatchedaco", "ac.DispatchedACO")
    adddate("incidentfrom", "incidentto", "ac.IncidentDateTime")
    adddate("dispatchfrom", "dispatchto", "ac.DispatchDateTime")
    adddate("respondedfrom", "respondedto", "ac.RespondedDateTime")
    adddate("followupfrom", "followupto", "ac.FollwupDateTime")
    adddate("completedfrom", "completedto", "ac.CompletedDate")
    addid("completedtype", "ac.IncidentCompletedID")
    addid("citationtype", "ac.CitationTypeID")
    addstr("address", "ac.DispatchAddress")
    addstr("postcode", "ac.DispatchPostcode")
    addstr("description", "ac.AnimalDescription")
    if (crit("agegroup") != "-1"): addstr("agegroup", "ac.AgeGroup")
    addid("sex", "ac.Sex")
    addid("species", "ac.SpeciesID")
    addcomp("filter", "incomplete", "ac.CompletedDate Is Null")
    addcomp("filter", "undispatched", "ac.CompletedDate Is Null AND ac.CallDateTime Is Not Null AND ac.DispatchDateTime Is Null")
    addcomp("filter", "requirefollowup", "ac.CompletedDate Is Null AND (" \
        "(ac.FollowupDateTime Is Not Null AND ac.FollowupDateTime < %(now)s) OR " \
        "(ac.FollowupDateTime2 Is Not Null AND ac.FollowupDateTime2 < %(now)s) OR " \
        "(ac.FollowupDateTime3 Is Not Null AND ac.FollowupDateTime3 < %(now)s) " \
        ")" % { "now": db.dd(now(dbo.timezone))} )
    where = ""
    if len(c) > 0:
        where = " WHERE " + " AND ".join(c)
    sql = get_animalcontrol_query(dbo) + where + " ORDER BY ac.ID"
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_animalcontrol_satellite_counts(dbo, acid):
    """
    Returns a resultset containing the number of each type of satellite
    record that an animal control entry has.
    """
    sql = "SELECT a.ID, " \
        "(SELECT COUNT(*) FROM ownercitation oc WHERE oc.AnimalControlID = a.ID) AS citation, " \
        "(SELECT COUNT(*) FROM media me WHERE me.LinkID = a.ID AND me.LinkTypeID = %d) AS media, " \
        "(SELECT COUNT(*) FROM diary di WHERE di.LinkID = a.ID AND di.LinkType = %d) AS diary, " \
        "(SELECT COUNT(*) FROM log WHERE log.LinkID = a.ID AND log.LinkType = %d) AS logs " \
        "FROM animalcontrol a WHERE a.ID = %d" \
        % (media.ANIMALCONTROL, diary.ANIMALCONTROL, log.ANIMALCONTROL, int(acid))
    return db.query(dbo, sql)

def get_active_traploans(dbo):
    """
    Returns all active traploan records
    ID, TRAPTYPEID, TRAPTYPENAME, LOANDATE, DEPOSITRETURNDATE,
    TRAPNUMBER, RETURNDUEDATE, RETURNDATE,
    OWNERNAME
    """
    return db.query(dbo, get_traploan_query(dbo) + \
        "WHERE ot.ReturnDate Is Null OR ot.ReturnDate > %s " \
        "ORDER BY ot.LoanDate DESC" % db.dd(now(dbo.timezone)))

def get_person_traploans(dbo, oid, sort = ASCENDING):
    """
    Returns all of the traploan records for a person, along with
    some owner info.
    ID, TRAPTYPEID, TRAPTYPENAME, LOANDATE, DEPOSITRETURNDATE,
    TRAPNUMBER, RETURNDUEDATE, RETURNDATE,
    OWNERNAME
    """
    order = "ot.LoanDate DESC"
    if sort == ASCENDING:
        order = "ot.LoanDate"
    return db.query(dbo, get_traploan_query(dbo) + \
        "WHERE ot.OwnerID = %d " \
        "ORDER BY %s" % (int(oid), order))

def get_traploan_two_dates(dbo, dbstart, dbend):
    """
    Returns unreturned trap loans with a due date between the two ISO dates
    """
    return db.query(dbo, get_traploan_query(dbo) + \
        "WHERE ReturnDate Is Null AND ReturnDueDate >= '%s' AND ReturnDueDate <= '%s'" % (dbstart, dbend))

def update_animalcontrol_from_form(dbo, post, username):
    """
    Updates an animal control incident record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    acid = post.integer("id")
    if post.date("incidentdate") is None:
        raise utils.ASMValidationError(_("Incident date cannot be blank", l))

    preaudit = db.query(dbo, "SELECT * FROM animalcontrol WHERE ID = %d" % acid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animalcontrol", username, "ID=%d" % acid, (
        ( "IncidentDateTime", post.db_datetime("incidentdate", "incidenttime")),
        ( "IncidentTypeID", post.db_integer("incidenttype")),
        ( "CallDateTime", post.db_datetime("calldate", "calltime")),
        ( "CallNotes", post.db_string("callnotes")),
        ( "CallTaker", post.db_string("calltaker")),
        ( "CallerID", post.db_integer("caller")),
        ( "VictimID", post.db_integer("victim")),
        ( "DispatchAddress", post.db_string("dispatchaddress")),
        ( "DispatchTown", post.db_string("dispatchtown")),
        ( "DispatchCounty", post.db_string("dispatchcounty")),
        ( "DispatchPostcode", post.db_string("dispatchpostcode")),
        ( "DispatchLatLong", post.db_string("dispatchlatlong")),
        ( "DispatchedACO", post.db_string("dispatchedaco")),
        ( "DispatchDateTime", post.db_datetime("dispatchdate", "dispatchtime")),
        ( "RespondedDateTime", post.db_datetime("respondeddate", "respondedtime")),
        ( "FollowupDateTime", post.db_datetime("followupdate", "followuptime")),
        ( "FollowupDateTime2", post.db_datetime("followupdate2", "followuptime2")),
        ( "FollowupDateTime3", post.db_datetime("followupdate3", "followuptime3")),
        ( "CompletedDate", post.db_date("completeddate")),
        ( "IncidentCompletedID", post.db_integer("completedtype")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Owner2ID", post.db_integer("owner2")),
        ( "Owner3ID", post.db_integer("owner3")),
        ( "AnimalID", post.db_integer("animal")),
        ( "AnimalDescription", post.db_string("animaldescription")),
        ( "SpeciesID", post.db_integer("species")),
        ( "Sex", post.db_integer("sex")),
        ( "AgeGroup", post.db_string("agegroup"))
    )))
    additional.save_values_for_link(dbo, post, acid, "incident")
    postaudit = db.query(dbo, "SELECT * FROM animalcontrol WHERE ID = %d" % acid)
    audit.edit(dbo, username, "animalcontrol", audit.map_diff(preaudit, postaudit))

def insert_animalcontrol_from_form(dbo, post, username):
    """
    Inserts a new animal control incident record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    if post.date("incidentdate") is None:
        raise utils.ASMValidationError(_("Incident date cannot be blank", l))

    nid = db.get_id(dbo, "animalcontrol")
    db.execute(dbo, db.make_insert_user_sql(dbo, "animalcontrol", username, (
        ( "ID", db.di(nid)),
        ( "IncidentDateTime", post.db_datetime("incidentdate", "incidenttime")),
        ( "IncidentTypeID", post.db_integer("incidenttype")),
        ( "CallDateTime", post.db_datetime("calldate", "calltime")),
        ( "CallNotes", post.db_string("callnotes")),
        ( "CallTaker", post.db_string("calltaker")),
        ( "CallerID", post.db_integer("caller")),
        ( "VictimID", post.db_integer("victim")),
        ( "DispatchAddress", post.db_string("dispatchaddress")),
        ( "DispatchTown", post.db_string("dispatchtown")),
        ( "DispatchCounty", post.db_string("dispatchcounty")),
        ( "DispatchPostcode", post.db_string("dispatchpostcode")),
        ( "DispatchLatLong", post.db_string("dispatchlatlong")),
        ( "DispatchedACO", post.db_string("dispatchedaco")),
        ( "DispatchDateTime", post.db_datetime("dispatchdate", "dispatchtime")),
        ( "RespondedDateTime", post.db_datetime("respondeddate", "respondedtime")),
        ( "FollowupDateTime", post.db_datetime("followupdate", "followuptime")),
        ( "FollowupDateTime2", post.db_datetime("followupdate2", "followuptime2")),
        ( "FollowupDateTime3", post.db_datetime("followupdate3", "followuptime3")),
        ( "CompletedDate", post.db_date("completeddate")),
        ( "IncidentCompletedID", post.db_integer("completedtype")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Owner2ID", post.db_integer("owner2")),
        ( "Owner3ID", post.db_integer("owner3")),
        ( "AnimalID", post.db_integer("animal")),
        ( "AnimalDescription", post.db_string("animaldescription")),
        ( "SpeciesID", post.db_integer("species")),
        ( "Sex", post.db_integer("sex")),
        ( "AgeGroup", post.db_string("agegroup"))
        )))
    audit.create(dbo, username, "animalcontrol", str(nid))
    return nid

def delete_animalcontrol(dbo, username, acid):
    """
    Deletes an animal control record
    """
    audit.delete(dbo, username, "animalcontrol", str(db.query(dbo, "SELECT * FROM animalcontrol WHERE ID=%d" % acid)))
    db.execute(dbo, "DELETE FROM animalcontrol WHERE ID = %d" % acid)

def insert_animalcontrol(dbo, username):
    """
    Creates a new animal control incident record and returns the id
    """
    l = dbo.locale
    d = {
        "incidentdate":     python2display(l, now(dbo.timezone)),
        "incidenttime":     format_time_now(dbo.timezone),
        "incidenttype":     configuration.default_incident(dbo),
        "calldate":         python2display(l, now(dbo.timezone)),
        "calltime":         format_time_now(dbo.timezone),
        "calltaker":        username
    }
    return insert_animalcontrol_from_form(dbo, utils.PostedData(d, dbo.locale), username)

def insert_traploan_from_form(dbo, username, post):
    """
    Creates a traploan record from posted form data 
    """
    traploanid = db.get_id(dbo, "ownertraploan")
    sql = db.make_insert_user_sql(dbo, "ownertraploan", username, ( 
        ( "ID", db.di(traploanid)),
        ( "OwnerID", post.db_integer("person")),
        ( "TrapTypeID", post.db_integer("type")),
        ( "LoanDate", post.db_date("loandate")),
        ( "DepositAmount", post.db_integer("depositamount")),
        ( "DepositReturnDate", post.db_date("depositreturndate")),
        ( "TrapNumber", post.db_string("trapnumber")),
        ( "ReturnDueDate", post.db_date("returnduedate")),
        ( "ReturnDate", post.db_date("returndate")),
        ( "Comments", post.db_string("comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "ownertraploan", str(traploanid))
    return traploanid

def update_traploan_from_form(dbo, username, post):
    """
    Updates a traploan record from posted form data
    """
    traploanid = post.integer("traploanid")
    sql = db.make_update_user_sql(dbo, "ownertraploan", username, "ID=%d" % traploanid, ( 
        ( "OwnerID", post.db_integer("person")),
        ( "TrapTypeID", post.db_integer("type")),
        ( "LoanDate", post.db_date("loandate")),
        ( "DepositAmount", post.db_integer("depositamount")),
        ( "DepositReturnDate", post.db_date("depositreturndate")),
        ( "TrapNumber", post.db_string("trapnumber")),
        ( "ReturnDueDate", post.db_date("returnduedate")),
        ( "ReturnDate", post.db_date("returndate")),
        ( "Comments", post.db_string("comments"))
    ))
    preaudit = db.query(dbo, "SELECT * FROM ownertraploan WHERE ID = %d" % traploanid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM ownertraploan WHERE ID = %d" % traploanid)
    audit.edit(dbo, username, "ownertraploan", audit.map_diff(preaudit, postaudit))

def delete_traploan(dbo, username, tid):
    """
    Deletes a traploan record
    """
    audit.delete(dbo, username, "ownertraploan", str(db.query(dbo, "SELECT * FROM ownertraploan WHERE ID=%d" % int(tid))))
    db.execute(dbo, "DELETE FROM ownertraploan WHERE ID = %d" % int(tid))

def update_dispatch_latlong(dbo, incidentid, latlong):
    """
    Updates the dispatch latlong field.
    """
    db.execute(dbo, "UPDATE animalcontrol SET DispatchLatLong = %s WHERE ID = %d" % (db.ds(latlong), int(incidentid)))


