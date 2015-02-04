#!/usr/bin/python

import additional
import al
import animal
import audit
import configuration
import db
import dbfs
import diary
import log
import media
import reports
import utils
import waitinglist
from i18n import _, date_diff_days, now, subtract_days, subtract_years, python2display, display2python

class LostFoundMatch:
    lid = 0
    lcontactname = ""
    lcontactnumber = ""
    larealost = ""
    lareapostcode = ""
    lagegroup = ""
    lsexname = ""
    lspeciesname = ""
    lbreedname = ""
    ldistinguishingfeatures = ""
    lbasecolourname = ""
    ldatelost = None
    fid = ""
    fcontactname = ""
    fcontactnumber = ""
    fareafound = ""
    fareapostcode = ""
    fagegroup = ""
    fsexname = ""
    fspeciesname = ""
    fbreedname = ""
    fdistinguishingfeatures = ""
    fbasecolourname = ""
    fdatefound = None
    matchpoints = 0

def get_foundanimal_query(dbo):
    dummy = dbo
    return "SELECT a.*, a.ID AS LFID, s.SpeciesName, b.BreedName, " \
        "c.BaseColour AS BaseColourName, x.Sex AS SexName, " \
        "o.OwnerSurname, o.OwnerForeNames, o.OwnerTitle, o.OwnerInitials, " \
        "o.OwnerName, o.HomeTelephone, o.WorkTelephone, o.MobileTelephone " \
        "FROM animalfound a " \
        "LEFT OUTER JOIN breed b ON a.BreedID = b.ID " \
        "INNER JOIN species s ON a.AnimalTypeID = s.ID " \
        "INNER JOIN basecolour c ON a.BaseColourID = c.ID " \
        "INNER JOIN lksex x ON a.Sex = x.ID " \
        "LEFT OUTER JOIN owner o ON a.OwnerID = o.ID"

def get_lostanimal_query(dbo):
    dummy = dbo
    return "SELECT a.*, a.ID AS LFID, s.SpeciesName, b.BreedName, " \
        "c.BaseColour AS BaseColourName, x.Sex AS SexName, " \
        "o.OwnerSurname, o.OwnerForeNames, o.OwnerTitle, o.OwnerInitials, " \
        "o.OwnerName, o.HomeTelephone, o.WorkTelephone, o.MobileTelephone " \
        "FROM animallost a " \
        "LEFT OUTER JOIN breed b ON a.BreedID = b.ID " \
        "INNER JOIN species s ON a.AnimalTypeID = s.ID " \
        "INNER JOIN basecolour c ON a.BaseColourID = c.ID " \
        "INNER JOIN lksex x ON a.Sex = x.ID " \
        "LEFT OUTER JOIN owner o ON a.OwnerID = o.ID"

def get_lostanimal(dbo, aid):
    """
    Returns a lost animal record
    """
    rows = db.query(dbo, get_lostanimal_query(dbo) + " WHERE a.ID = %d" % int(aid))
    if rows == None or len(rows) == 0:
        return None
    else:
        return rows[0]

def get_foundanimal(dbo, aid):
    """
    Returns a found animal record
    """
    rows = db.query(dbo, get_foundanimal_query(dbo) + " WHERE a.ID = %d" % int(aid))
    if rows == None or len(rows) == 0:
        return None
    else:
        return rows[0]

def get_lostanimal_find_simple(dbo, query = "", limit = 0, onlyindexed = False):
    """
    Returns rows for simple lost animal searches.
    query: The search criteria
    """
    ors = []
    query = query.replace("'", "`")
    def add(field):
        return utils.where_text_filter(dbo, field, query)
    # If no query has been given, show unfound lost animal records
    # for the last 30 days
    if query == "":
        ors.append("a.DateLost > %s AND a.DateFound Is Null" % db.dd(subtract_days(now(dbo.timezone), 30)))
    else:
        if utils.is_numeric(query):
            ors.append("a.ID = " + str(utils.cint(query)))
        ors.append(add("o.OwnerName"))
        ors.append(add("a.AreaLost"))
        ors.append(add("a.AreaPostcode"))
        if not onlyindexed:
            ors.append(add("x.Sex"))
            ors.append(add("b.BreedName"))
            ors.append(add("c.BaseColour"))
            ors.append(add("s.SpeciesName"))
            ors.append(add("a.AgeGroup"))
            ors.append(add("a.DistFeat"))
            ors.append(add("a.Comments"))
    sql = get_lostanimal_query(dbo) + " WHERE " + " OR ".join(ors)
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_foundanimal_find_simple(dbo, query = "", limit = 0, onlyindexed = False):
    """
    Returns rows for simple found animal searches.
    query: The search criteria
    """
    ors = []
    query = query.replace("'", "`")
    def add(field):
        return utils.where_text_filter(dbo, field, query)
    # If no query has been given, show unreturned found animal records
    # for the last 30 days
    if query == "":
        ors.append("a.DateFound > %s AND a.ReturnToOwnerDate Is Null" % db.dd(subtract_days(now(dbo.timezone), 30)))
    else:
        if utils.is_numeric(query):
            ors.append("a.ID = " + str(utils.cint(query)))
        ors.append(add("o.OwnerName"))
        ors.append(add("a.AreaFound"))
        ors.append(add("a.AreaPostcode"))
        if not onlyindexed:
            ors.append(add("x.Sex"))
            ors.append(add("b.BreedName"))
            ors.append(add("c.BaseColour"))
            ors.append(add("s.SpeciesName"))
            ors.append(add("a.AgeGroup"))
            ors.append(add("a.DistFeat"))
            ors.append(add("a.Comments"))
    sql = get_foundanimal_query(dbo) + " WHERE " + " OR ".join(ors)
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_lostanimal_find_advanced(dbo, criteria, limit = 0):
    """f
    Returns rows for advanced lost animal searches.
    criteria: A dictionary of criteria
       number - string partial pattern
       contact - string partial pattern
       area - string partial pattern
       postcode - string partial pattern
       features - string partial pattern
       agegroup - agegroup text to match
       sex - -1 for all or ID
       species - -1 for all or ID
       breed - -1 for all or ID
       colour - -1 for all or ID
       excludecomplete - 1 for yes
       datefrom - lost date from in current display locale format
       dateto - lost date to in current display locale format
       completefrom - found date from in current display locale format
       completeto - found date to in current display locale format
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

    c.append("a.ID > 0")
    if crit("number") != "": c.append("a.ID = " + str(int(crit("number"))))
    addstr("contact", "o.OwnerName")
    addstr("area", "a.AreaLost")
    addstr("postcode", "a.AreaPostcode")
    addstr("features", "a.DistFeat")
    if (crit("agegroup") != "-1"): addstr("agegroup", "a.AgeGroup")
    addid("sex", "a.Sex")
    addid("species", "a.AnimalTypeID")
    addid("breed", "a.BreedID")
    addid("colour", "a.BaseColourID")
    adddate("datefrom", "dateto", "a.DateLost")
    if crit("excludecomplete") == "1":
        c.append("a.DateFound Is Null")
    if crit("completefrom") == "":
        c.append("a.DateFound Is Null")
    else:
        adddate("completefrom", "completeto", "a.DateFound")
    where = " WHERE " + " AND ".join(c)
    sql = get_lostanimal_query(dbo) + where + " ORDER BY a.ID"
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_foundanimal_find_advanced(dbo, criteria, limit = 0):
    """
    Returns rows for advanced lost animal searches.
    criteria: A dictionary of criteria
       number - string partial pattern
       contact - string partial pattern
       area - string partial pattern
       postcode - string partial pattern
       features - string partial pattern
       agegroup - agegroup text to match
       sex - -1 for all or ID
       species - -1 for all or ID
       breed - -1 for all or ID
       colour - -1 for all or ID
       excludecomplete - 1 for yes
       datefrom - lost date from in current display locale format
       dateto - lost date to in current display locale format
       completefrom - returned date from in current display locale format
       completeto - returned date to in current display locale format
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

    c.append("a.ID > 0")
    if crit("number") != "": c.append("a.ID = " + str(int(crit("number"))))
    addstr("contact", "o.OwnerName")
    addstr("area", "a.AreaFound")
    addstr("postcode", "a.AreaPostcode")
    addstr("features", "a.DistFeat")
    if (crit("agegroup") != "-1"): addstr("agegroup", "a.AgeGroup")
    addid("sex", "a.Sex")
    addid("species", "a.AnimalTypeID")
    addid("breed", "a.BreedID")
    addid("colour", "a.BaseColourID")
    adddate("datefrom", "dateto", "a.DateFound")
    if crit("excludecomplete") == "1":
        c.append("a.ReturnToOwnerDate Is Null")
    if crit("completefrom") == "":
        c.append("a.ReturnToOwnerDate Is Null")
    else:
        adddate("completefrom", "completeto", "a.ReturnToOwnerDate")
    where = " WHERE " + " AND ".join(c)
    sql = get_foundanimal_query(dbo) + where + " ORDER BY a.ID"
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_lostanimal_satellite_counts(dbo, lfid):
    """
    Returns a resultset containing the number of each type of satellite
    record that a lost animal entry has.
    """
    sql = "SELECT a.ID, " \
        "(SELECT COUNT(*) FROM media me WHERE me.LinkID = a.ID AND me.LinkTypeID = %d) AS media, " \
        "(SELECT COUNT(*) FROM diary di WHERE di.LinkID = a.ID AND di.LinkType = %d) AS diary, " \
        "(SELECT COUNT(*) FROM log WHERE log.LinkID = a.ID AND log.LinkType = %d) AS logs " \
        "FROM animallost a WHERE a.ID = %d" \
        % (media.LOSTANIMAL, diary.LOSTANIMAL, log.LOSTANIMAL, int(lfid))
    return db.query(dbo, sql)

def get_foundanimal_satellite_counts(dbo, lfid):
    """
    Returns a resultset containing the number of each type of satellite
    record that a found animal entry has.
    """
    sql = "SELECT a.ID, " \
        "(SELECT COUNT(*) FROM media me WHERE me.LinkID = a.ID AND me.LinkTypeID = %d) AS media, " \
        "(SELECT COUNT(*) FROM diary di WHERE di.LinkID = a.ID AND di.LinkType = %d) AS diary, " \
        "(SELECT COUNT(*) FROM log WHERE log.LinkID = a.ID AND log.LinkType = %d) AS logs " \
        "FROM animalfound a WHERE a.ID = %d" \
        % (media.FOUNDANIMAL, diary.FOUNDANIMAL, log.FOUNDANIMAL, int(lfid))
    return db.query(dbo, sql)

def send_email_from_form(dbo, username, post):
    """
    Sends an email to a lost/found person from a posted form. Attaches it as
    a log entry if specified.
    """
    emailfrom = post["from"]
    emailto = post["to"]
    emailcc = post["cc"]
    subject = post["subject"]
    ishtml = post.boolean("html")
    addtolog = post.boolean("addtolog")
    logtype = post.integer("logtype")
    body = post["body"]
    rv = utils.send_email(dbo, emailfrom, emailto, emailcc, subject, body, ishtml == 1 and "html" or "plain")
    if addtolog == 1:
        log.add_log(dbo, username, post["lfmode"] == "lost" and log.LOSTANIMAL or log.FOUNDANIMAL, post.integer("lfid"), logtype, body)
    return rv

def words(str1, str2, maxpoints):
    """
    Evalutes words in string 1 for appearances in string 2
    Returns the number of points for 1 to 2 as a percentage of maxpoints
    """
    if str1 == None: str1 = ""
    if str2 == None: str2 = ""
    str1 = str1.replace(",", " ").replace("\n", " ").lower().strip()
    str2 = str2.replace(",", " ").replace("\n", " ").lower().strip()
    matches = 0
    s1words = str1.split(" ")
    s2words = str2.split(" ")
    for w in s1words:
        if w in s2words: 
            matches += 1
    return int((float(matches) / float(len(s1words))) * float(maxpoints))

def match(dbo, lostanimalid = 0, foundanimalid = 0, animalid = 0):
    """
    Performs a lost and found match by going through all lost animals
    lostanimalid:   Compare this lost animal against all found animals
    foundanimalid:  Compare all lost animals against this found animal
    animalid:       Compare all lost animals against this shelter animal
    returns a list LostFoundMatch objects
    """
    l = dbo.locale
    matches = []
    matchspecies = configuration.match_species(dbo)
    matchbreed = configuration.match_breed(dbo)
    matchage = configuration.match_age(dbo)
    matchsex = configuration.match_sex(dbo)
    matcharealost = configuration.match_area_lost(dbo)
    matchfeatures = configuration.match_features(dbo)
    matchpostcode = configuration.match_postcode(dbo)
    matchcolour = configuration.match_colour(dbo)
    matchdatewithin2weeks = configuration.match_within2weeks(dbo)
    matchmax = matchspecies + matchbreed + matchage + matchsex + \
        matcharealost + matchfeatures + matchpostcode + matchcolour + \
        matchdatewithin2weeks
    matchpointfloor = configuration.match_point_floor(dbo)
    includeshelter = configuration.match_include_shelter(dbo)
    # Ignore records older than 6 months to keep things useful
    giveup = subtract_days(now(dbo.timezone), 180)

    # Get our set of lost animals
    lostanimals = None
    if lostanimalid == 0:
        lostanimals = db.query(dbo, get_lostanimal_query(dbo) + \
            " WHERE a.DateFound Is Null AND a.DateLost > %s ORDER BY a.DateLost" % db.dd(giveup))
    else:
        lostanimals = db.query(dbo, get_lostanimal_query(dbo) + \
            " WHERE a.ID = %d" % lostanimalid)

    oldestdate = giveup
    if len(lostanimals) > 0:
        oldestdate = lostanimals[0]["DATELOST"]

    # Get the set of found animals for comparison
    foundanimals = None
    if foundanimalid == 0:
        foundanimals = db.query(dbo, get_foundanimal_query(dbo) + \
            " WHERE a.ReturnToOwnerDate Is Null" \
            " AND a.DateFound >= %s " % db.dd(oldestdate))
    else:
        foundanimals = db.query(dbo, get_foundanimal_query(dbo) + " WHERE a.ID = %d" % foundanimalid)

    # Get the set of shelter animals for comparison
    shelteranimals = None
    if includeshelter:
        if animalid == 0:
            shelteranimals = db.query(dbo, animal.get_animal_query(dbo) + " WHERE " + \
                "a.DateBroughtIn > %s" % db.dd(oldestdate))
        else:
            shelteranimals = db.query(dbo, animal.get_animal_query(dbo) + " WHERE a.ID = %d" % animalid)

    for la in lostanimals:
        # Found animals (if an animal id has been given don't
        # check found animals)
        if animalid == 0:
            for fa in foundanimals:
                matchpoints = 0
                if la["ANIMALTYPEID"] == fa["ANIMALTYPEID"]: matchpoints += matchspecies
                if la["BREEDID"] == fa["BREEDID"]: matchpoints += matchbreed
                if la["AGEGROUP"] == fa["AGEGROUP"]: matchpoints += matchage
                if la["SEX"] == fa["SEX"]: matchpoints += matchsex
                matchpoints += words(la["AREALOST"], fa["AREAFOUND"], matcharealost)
                matchpoints += words(la["DISTFEAT"], fa["DISTFEAT"], matchfeatures)
                if la["AREAPOSTCODE"] == fa["AREAPOSTCODE"]: matchpoints += matchpostcode
                if la["BASECOLOURID"] == fa["BASECOLOURID"]: matchpoints += matchcolour
                if date_diff_days(la["DATELOST"], fa["DATEFOUND"]) <= 14: matchpoints += matchdatewithin2weeks
                if matchpoints > matchmax: matchpoints = matchmax
                if matchpoints >= matchpointfloor:
                    m = LostFoundMatch()
                    m.lid = la["ID"]
                    m.lcontactname = la["OWNERNAME"]
                    m.lcontactnumber = la["HOMETELEPHONE"]
                    m.larealost = la["AREALOST"]
                    m.lareapostcode = la["AREAPOSTCODE"]
                    m.lagegroup = la["AGEGROUP"]
                    m.lsexname = la["SEXNAME"]
                    m.lspeciesname = la["SPECIESNAME"]
                    m.lbreedname = la["BREEDNAME"]
                    m.ldistinguishingfeatures = la["DISTFEAT"]
                    m.lbasecolourname = la["BASECOLOURNAME"]
                    m.ldatelost = la["DATELOST"]
                    m.fid = str(fa["ID"])
                    m.fcontactname = fa["OWNERNAME"]
                    m.fcontactnumber = fa["HOMETELEPHONE"]
                    m.fareafound = fa["AREAFOUND"]
                    m.fareapostcode = fa["AREAPOSTCODE"]
                    m.fagegroup = fa["AGEGROUP"]
                    m.fsexname = fa["SEXNAME"]
                    m.fspeciesname = fa["SPECIESNAME"]
                    m.fbreedname = fa["BREEDNAME"]
                    m.fdistinguishingfeatures = fa["DISTFEAT"]
                    m.fbasecolourname = fa["BASECOLOURNAME"]
                    m.fdatefound = fa["DATEFOUND"]
                    m.matchpoints = int((float(matchpoints) / float(matchmax)) * 100.0)
                    matches.append(m)

        # Shelter animals
        if includeshelter:
            for a in shelteranimals:
                matchpoints = 0
                if la["ANIMALTYPEID"] == a["SPECIESID"]: matchpoints += matchspecies
                if la["BREEDID"] == a["BREEDID"] or la["BREEDID"] == a["BREED2ID"]: matchpoints += matchbreed
                if la["BASECOLOURID"] == a["BASECOLOURID"]: matchpoints += matchcolour
                if la["AGEGROUP"] == a["AGEGROUP"]: matchpoints += matchage
                if la["SEX"] == a["SEX"]: matchpoints += matchsex
                matchpoints += words(la["AREALOST"], a["ORIGINALOWNERADDRESS"], matcharealost)
                matchpoints += words(la["DISTFEAT"], a["MARKINGS"], matchfeatures)
                if str(a["ORIGINALOWNERPOSTCODE"]).find(la["AREAPOSTCODE"]): matchpoints += matchpostcode
                if date_diff_days(la["DATELOST"], a["DATEBROUGHTIN"]) <= 14: matchpoints += matchdatewithin2weeks
                if matchpoints > matchmax: matchpoints = matchmax
                if matchpoints >= matchpointfloor:
                    m = LostFoundMatch()
                    m.lid = la["ID"]
                    m.lcontactname = la["OWNERNAME"]
                    m.lcontactnumber = la["HOMETELEPHONE"]
                    m.larealost = la["AREALOST"]
                    m.lareapostcode = la["AREAPOSTCODE"]
                    m.lagegroup = la["AGEGROUP"]
                    m.lsexname = la["SEXNAME"]
                    m.lspeciesname = la["SPECIESNAME"]
                    m.lbreedname = la["BREEDNAME"]
                    m.ldistinguishingfeatures = la["DISTFEAT"]
                    m.lbasecolourname = la["BASECOLOURNAME"]
                    m.ldatelost = la["DATELOST"]
                    m.fid = a["CODE"]
                    m.fcontactname = _("Shelter animal {0} '{1}'", l).format(a["CODE"], a["ANIMALNAME"])
                    m.fcontactnumber = a["SPECIESNAME"]
                    m.fareafound = _("On Shelter", l)
                    m.fareapostcode = a["ORIGINALOWNERPOSTCODE"]
                    m.fagegroup = a["AGEGROUP"]
                    m.fsexname = a["SEXNAME"]
                    m.fspeciesname = a["SPECIESNAME"]
                    m.fbreedname = a["BREEDNAME"]
                    m.fdistinguishingfeatures = a["MARKINGS"]
                    m.fbasecolourname = a["BASECOLOURNAME"]
                    m.fdatefound = a["DATEBROUGHTIN"]
                    m.matchpoints = int((float(matchpoints) / float(matchmax)) * 100.0)
                    matches.append(m)
    return matches

def match_report(dbo, username = "system", lostanimalid = 0, foundanimalid = 0, animalid = 0):
    """
    Same interface as match above, but generates the match report
    """
    l = dbo.locale
    title = _("Match lost and found animals", l)
    h = []
    h.append(reports.get_report_header(dbo, title, username))
    def p(s): return "<p>%s</p>" % s
    def td(s): return "<td>%s</td>" % s
    def hr(): return "<hr />"
    lastid = 0
    matches = match(dbo, lostanimalid, foundanimalid, animalid)
    if len(matches) > 0:
        for m in matches:
            if lastid != m.lid:
                if lastid != 0:
                    h.append("</tr></table>")
                    h.append(hr())
                h.append(p(_("{0} - {1} {2} ({3}), contact {4} ({5}) - lost in {6}, postcode {7}, on {8}", l).format( \
                    m.lid, "%s %s %s" % (m.lagegroup, m.lbasecolourname, m.lsexname), \
                    "%s/%s" % (m.lspeciesname,m.lbreedname), \
                    m.ldistinguishingfeatures, m.lcontactname, m.lcontactnumber, m.larealost, m.lareapostcode,
                    python2display(l, m.ldatelost))))
                h.append("<table border=\"1\" width=\"100%\"><tr>")
                h.append("<th>%s</th>" % _("Reference", l))
                h.append("<th>%s</th>" % _("Description", l))
                h.append("<th>%s</th>" % _("Area Found", l))
                h.append("<th>%s</th>" % _("Area Postcode", l))
                h.append("<th>%s</th>" % _("Date Found", l))
                h.append("<th>%s</th>" % _("Contact", l))
                h.append("<th>%s</th>" % _("Number", l))
                h.append("<th>%s</th>" % _("Match", l))
                h.append("</tr>")
                lastid = m.lid
            h.append("<tr>")
            h.append(td(m.fid))
            h.append(td("%s %s %s %s" % (m.fagegroup, m.fbasecolourname, m.fsexname, m.fspeciesname)))
            h.append(td(m.fareafound))
            h.append(td(m.fareapostcode))
            h.append(td(python2display(l, m.fdatefound)))
            h.append(td(m.fcontactname))
            h.append(td(m.fcontactnumber))
            h.append(td(str(m.matchpoints) + "%"))
            h.append("</tr>")
        h.append("</tr></table>")
    else:
        h.append(p(_("No matches found.", l)))
    h.append(reports.get_report_footer(dbo, title, username))
    return "\n".join(h)
       
def update_match_report(dbo):
    """
    Updates the latest version of the lost/found match report in the dbfs
    """
    al.debug("updating lost/found match report", "lostfound.update_match_report", dbo)
    s = match_report(dbo)
    dbfs.put_string_filepath(dbo, "/reports/daily/lost_found_match.html", s)

def get_lost_person_name(dbo, aid):
    """
    Returns the contact name for a lost animal
    """
    return db.query_string(dbo, "SELECT o.OwnerName FROM animallost a INNER JOIN owner o ON a.OwnerID = o.ID WHERE a.ID = %d" % int(aid))

def get_found_person_name(dbo, aid):
    """
    Returns the contact name for a found animal
    """
    return db.query_string(dbo, "SELECT o.OwnerName FROM animalfound a INNER JOIN owner o ON a.OwnerID = o.ID WHERE a.ID = %d" % int(aid))

def update_lostanimal_from_form(dbo, post, username):
    """
    Updates a lost animal record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    lfid = post.integer("id")
    if post.date("datelost") is None:
        raise utils.ASMValidationError(_("Date lost cannot be blank", l))
    if post.date("datereported") is None:
        raise utils.ASMValidationError(_("Date reported cannot be blank", l))
    if post.integer("owner") == "0":
        raise utils.ASMValidationError(_("Lost animals must have a contact", l))

    preaudit = db.query(dbo, "SELECT * FROM animallost WHERE ID = %d" % lfid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animallost", username, "ID=%d" % lfid, (
        ( "AnimalTypeID", post.db_integer("species")),
        ( "DateReported", post.db_date("datereported")),
        ( "DateLost", post.db_date("datelost")),
        ( "DateFound", post.db_date("datefound")),
        ( "Sex", post.db_integer("sex")),
        ( "BreedID", post.db_integer("breed")),
        ( "AgeGroup", post.db_string("agegroup")),
        ( "BaseColourID", post.db_integer("colour")),
        ( "DistFeat", post.db_string("markings")),
        ( "AreaLost", post.db_string("arealost")),
        ( "AreaPostcode", post.db_string("areapostcode")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Comments", post.db_string("comments"))
        )))
    additional.save_values_for_link(dbo, post, lfid, "lostanimal")
    postaudit = db.query(dbo, "SELECT * FROM animallost WHERE ID = %d" % lfid)
    audit.edit(dbo, username, "animallost", audit.map_diff(preaudit, postaudit))

def insert_lostanimal_from_form(dbo, post, username):
    """
    Inserts a new lost animal record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    if post.date("datelost") is None:
        raise utils.ASMValidationError(_("Date lost cannot be blank", l))
    if post.date("datereported") is None:
        raise utils.ASMValidationError(_("Date reported cannot be blank", l))
    if post.integer("owner") == "0":
        raise utils.ASMValidationError(_("Lost animals must have a contact", l))

    nid = db.get_id(dbo, "animallost")
    db.execute(dbo, db.make_insert_user_sql(dbo, "animallost", username, (
        ( "ID", db.di(nid)),
        ( "AnimalTypeID", post.db_integer("species")),
        ( "DateReported", post.db_date("datereported")),
        ( "DateLost", post.db_date("datelost")),
        ( "DateFound", post.db_date("datefound")),
        ( "Sex", post.db_integer("sex")),
        ( "BreedID", post.db_integer("breed")),
        ( "AgeGroup", post.db_string("agegroup")),
        ( "BaseColourID", post.db_integer("colour")),
        ( "DistFeat", post.db_string("markings")),
        ( "AreaLost", post.db_string("arealost")),
        ( "AreaPostcode", post.db_string("areapostcode")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Comments", post.db_string("comments"))
        )))
    audit.create(dbo, username, "animallost", str(nid))
    return nid

def update_foundanimal_from_form(dbo, post, username):
    """
    Updates a found animal record from the screen
    post: The webpy data object containing form parameters
    """
    l = dbo.locale
    lfid = post.integer("id")
    if post.date("datefound") is None:
        raise utils.ASMValidationError(_("Date found cannot be blank", l))
    if post.date("datereported") is None:
        raise utils.ASMValidationError(_("Date reported cannot be blank", l))
    if post.integer("owner") == 0:
        raise utils.ASMValidationError(_("Found animals must have a contact", l))

    preaudit = db.query(dbo, "SELECT * FROM animalfound WHERE ID = %d" % lfid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animalfound", username, "ID=%d" % lfid, (
        ( "AnimalTypeID", post.db_integer("species")),
        ( "DateReported", post.db_date("datereported")),
        ( "ReturnToOwnerDate", post.db_date("returntoownerdate")),
        ( "DateFound", post.db_date("datefound")),
        ( "Sex", post.db_integer("sex")),
        ( "BreedID", post.db_integer("breed")),
        ( "AgeGroup", post.db_string("agegroup")),
        ( "BaseColourID", post.db_integer("colour")),
        ( "DistFeat", post.db_string("markings")),
        ( "AreaFound", post.db_string("areafound")),
        ( "AreaPostcode", post.db_string("areapostcode")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Comments", post.db_string("comments"))
        )))
    additional.save_values_for_link(dbo, post, lfid, "foundanimal")
    postaudit = db.query(dbo, "SELECT * FROM animalfound WHERE ID = %d" % lfid)
    audit.edit(dbo, username, "animalfound", audit.map_diff(preaudit, postaudit))

def insert_foundanimal_from_form(dbo, post, username):
    """
    Inserts a new found animal record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    if post.date("datefound") is None:
        raise utils.ASMValidationError(_("Date found cannot be blank", l))
    if post.date("datereported") is None:
        raise utils.ASMValidationError(_("Date reported cannot be blank", l))
    if post.integer("owner") == 0:
        raise utils.ASMValidationError(_("Found animals must have a contact", l))

    nid = db.get_id(dbo, "animalfound")
    db.execute(dbo, db.make_insert_user_sql(dbo, "animalfound", username, (
        ( "ID", db.di(nid)),
        ( "AnimalTypeID", post.db_integer("species")),
        ( "DateReported", post.db_date("datereported")),
        ( "ReturnToOwnerDate", post.db_date("returntoownerdate")),
        ( "DateFound", post.db_date("datefound")),
        ( "Sex", post.db_integer("sex")),
        ( "BreedID", post.db_integer("breed")),
        ( "AgeGroup", post.db_string("agegroup")),
        ( "BaseColourID", post.db_integer("colour")),
        ( "DistFeat", post.db_string("markings")),
        ( "AreaFound", post.db_string("areafound")),
        ( "AreaPostcode", post.db_string("areapostcode")),
        ( "OwnerID", post.db_integer("owner")),
        ( "Comments", post.db_string("comments"))
        )))
    audit.create(dbo, username, "animalfound", str(nid))
    return nid

def create_animal_from_found(dbo, username, aid):
    """
    Creates an animal record from a found animal with the id given
    """
    a = db.query(dbo, "SELECT * FROM animalfound WHERE ID = %d" % int(aid))[0]
    l = dbo.locale
    data = {
        "animalname":           _("Found Animal {0}", l).format(aid),
        "markings":             str(a["DISTFEAT"]),
        "species":              str(a["ANIMALTYPEID"]),
        "comments":             str(a["COMMENTS"]),
        "broughtinby":          str(a["OWNERID"]),
        "originalowner":        str(a["OWNERID"]),
        "animaltype":           configuration.default_type(dbo),
        "breed1":               a["BREEDID"],
        "breed2":               a["BREEDID"],
        "basecolour":           str(a["BASECOLOURID"]),
        "size":                 configuration.default_size(dbo),
        "internallocation":     configuration.default_location(dbo),
        "dateofbirth":          python2display(l, subtract_years(now(dbo.timezone))),
        "estimateddob":         "1",
    }
    # If we're creating shelter codes manually, we need to put something unique
    # in there for now. Use the id
    if configuration.manual_codes(dbo):
        data["sheltercode"] = "FA" + str(aid)
        data["shortcode"] = "FA" + str(aid)
    nextid, code = animal.insert_animal_from_form(dbo, utils.PostedData(data, l), username)
    return nextid
   
def create_waitinglist_from_found(dbo, username, aid):
    """
    Creates a waiting list entry from a found animal with the id given
    """
    a = db.query(dbo, "SELECT * FROM animalfound WHERE ID = %d" % int(aid))[0]
    l = dbo.locale
    data = {
        "dateputon":            python2display(l, now(dbo.timezone)),
        "description":          str(a["DISTFEAT"]),
        "species":              str(a["ANIMALTYPEID"]),
        "comments":             str(a["COMMENTS"]),
        "owner":                str(a["OWNERID"]),
        "breed1":               a["BREEDID"],
        "breed2":               a["BREEDID"],
        "basecolour":           str(a["BASECOLOURID"]),
        "urgency":              str(configuration.waiting_list_default_urgency(dbo))
    }
    nextid = waitinglist.insert_waitinglist_from_form(dbo, utils.PostedData(data, dbo.locale), username)
    return nextid

def delete_lostanimal(dbo, username, aid):
    """
    Deletes a lost animal
    """
    audit.delete(dbo, username, "animallost", str(db.query(dbo, "SELECT * FROM animallost WHERE ID=%d" % aid)))
    db.execute(dbo, "DELETE FROM animallost WHERE ID = %d" % aid)

def delete_foundanimal(dbo, username, aid):
    """
    Deletes a found animal
    """
    audit.delete(dbo, username, "animalfound", str(db.query(dbo, "SELECT * FROM animalfound WHERE ID=%d" % aid)))
    db.execute(dbo, "DELETE FROM animalfound WHERE ID = %d" % aid)

