#!/usr/bin/python

import additional
import animal
import configuration
import datetime
import decimal
import financial
import json as extjson
import lookups
import medical
import person
import users
from i18n import BUILD, _, translate, format_currency, now, python2display
from sitedefs import BASE_URL, LOCALE, MINIFY_JS
from sitedefs import FULLCALENDAR_JS, FULLCALENDAR_CSS, JQUERY_JS, JQUERY_UI_JS, JQUERY_UI_CSS, MOMENT_JS, MOUSETRAP_JS, TINYMCE_4_JS

BACKGROUND_COLOURS = {
    "black-tie":        "#333333",
    "blitzer":          "#cc0000",
    "cupertino":        "#deedf7",
    "dark-hive":        "#444444",
    "dot-luv":          "#0b3e6f",
    "eggplant":         "#30273a",
    "excite-bike":      "#f9f9f9",
    "flick":            "#dddddd",
    "hot-sneaks":       "#35414f",
    "humanity":         "#cb842e",
    "le-frog":          "#3a8104",
    "mint-choc":        "#453326",
    "overcast":         "#dddddd",
    "pepper-grinder":   "#ffffff",
    "redmond":          "#5c9ccc",
    "smoothness":       "#cccccc",
    "south-street":     "#ece8da",
    "start":            "#2191c0",
    "sunny":            "#817865",
    "swanky-purse":     "#261803",
    "trontastic":       "#9fda58",
    "ui-darkness":      "#333333",
    "ui-lightness":     "#ffffff",
    "vader":            "#888888"
}

def json_parse(s):
    """
    Parses json and returns an object tree
    """
    return extjson.loads(s)

def json_handler(obj):
    """
    Used to help when serializing python objects to json
    """
    if obj is None:
        return "null"
    elif hasattr(obj, "isoformat"):
        return obj.isoformat()
    elif type(obj) == datetime.timedelta:
        hours, remain = divmod(obj.seconds, 3600)
        minutes, seconds = divmod(remain, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def json(obj):
    """
    Takes a python object and serializes it to JSON.
    None objects are turned into "null"
    datetime objects are turned into string isoformat for use with js Date.
    """
    return extjson.dumps(obj, default=json_handler)

def js_minified_name(filename):
    """
    Returns a minified name to the js filename given if 
    minifying is turned on and it's not a minified or third
    party file being requested.
    """
    if MINIFY_JS and filename.find("/") == -1 and filename.find(".min") == -1: filename = "min/" + filename.replace(".js", ".min.js")
    return filename

def script_tag(filename):
    """
    Returns a path to our caching script loader for a javascript file
    """
    return "<script type=\"text/javascript\" src=\"js?v=%s&k=%s\"></script>\n" % (js_minified_name(filename), BUILD)

def css_tag(filename):
    """
    Returns a path to our caching css loader for a stylesheet
    """
    return "<link rel=\"stylesheet\" type=\"text/css\" href=\"css?v=%s&k=%s\" />\n" % (filename, BUILD)

def xml(results):
    """
    Takes a list of dictionaries and converts them into
    an XML string. All values are treated as a strings
    and None values are turned into the string "null"
    """
    s = ""
    for row in results:
        cr = "    <row>\n"
        for k, v in row.iteritems():
            if v is None:
                v = "null"
            v = str(v)
            v = v.replace(">", "&gt;")
            v = v.replace("<", "&lt;")
            v = v.replace("&", "&amp;")
            cr += "        <" + k.lower() + ">"
            cr += str(v)
            cr += "</" + k.lower() + ">\n"
        cr += "    </row>\n"
        s += cr
    return '<?xml version="1.0" standalone="yes" ?>\n<xml>\n' + s + '\n</xml>'

def table(results):
    """
    Takes a list of dictionaries and converts them into
    an HTML thead and tbody string.
    """
    if len(results) == 0: return ""
    s = "<thead>\n<tr>\n"
    cols = sorted(results[0].iterkeys())
    for c in cols:
        s += "<th>%s</th>\n" % c
    s += "</thead>\n<tbody>\n"
    for row in results:
        s += "<tr>"
        for c in cols:
            s += "<td>%s</td>\n" % str(row[c])
        s += "</tr>"
    s += "</tbody>\n"
    return s

def bare_header(title, js = "", theme = "ui-lightness", locale = LOCALE, config_db = "asm", config_ts = "0"):
    """
    A bare header with just the script files needed for the program.
    title: The page title
    js: The name of an accompanying js file to load
    theme: A pre-rolled jquery-ui theme
    locale: The current system locale (used for requesting i18n.js)
    config_db: The name of the system database (used for requesting config.js)
    config_ts: A unique timestamp for when we last wanted the config (used for requesting config.js)
               This value changes when we update the config so the cache can be invalidated.
    """
    def script_i18n(l):
        return "<script type=\"text/javascript\" src=\"i18n.js?l=%s&k=%s\"></script>\n" % (l, BUILD)
    def script_config():
        return "<script type=\"text/javascript\" src=\"config.js?db=%s&ts=%s\"></script>\n" % (config_db, config_ts)
    # Use the default if we have no locale
    if locale is None: locale = LOCALE
    # Add the script module if set
    script = ""
    if js is not None and js != "":
        script = script_tag(js)
    # Set the body colour from the theme
    bgcol = BACKGROUND_COLOURS[theme]
    return """<!DOCTYPE html>
<html>
<head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <link rel="shortcut icon" href="static/images/logo/icon-16.png" />
    <link rel="icon" href="static/images/logo/icon-32.png" sizes="32x32"/>
    <link rel="icon" href="static/images/logo/icon-48.png" sizes="48x48"/>
    <link rel="icon" href="static/images/logo/icon-128.png" sizes="128x128"/>
    %(scripts)s
</head>
<body style="background-color: %(bgcol)s">
<noscript>
Sorry. ASM will not work without Javascript.
</noscript>
""" % { "title": title, 
      "scripts": css_tag("tablesorter/theme.asm.css") + 
                 css_tag("jquery.asmselect.css") + 
                 css_tag("asm-icon.css") +
                 script_tag("modernizr/modernizr.min.js") + 
                 JQUERY_JS + "\n" +
                 JQUERY_UI_JS + "\n" +
                 (JQUERY_UI_CSS % { "theme": theme}) + "\n" +
                 MOMENT_JS + "\n" + 
                 MOUSETRAP_JS + "\n" + 
                 FULLCALENDAR_CSS + "\n" +
                 FULLCALENDAR_JS + "\n" + 
                 css_tag("asm.css") + 
                 script_tag("jq/jquery.tablesorter.min.js") + 
                 script_tag("jq/jquery.asmselect.js") + 
                 script_config() + 
                 script_i18n(locale) + 
                 script_tag("common.js") + 
                 script_tag("common_map.js") + 
                 script_tag("common_widgets.js") + 
                 script_tag("common_animalchooser.js") + 
                 script_tag("common_animalchoosermulti.js") + 
                 script_tag("common_personchooser.js") + 
                 script_tag("common_tableform.js") + 
                 script_tag("header.js") + 
                 script_tag("header_additional.js") + 
                 script_tag("header_edit_header.js") + 
                 script, 
      "bgcol":   bgcol }

def tinymce_header(title, js, jswindowprint = True, onlysavewhendirty = True):
    """
    Outputs a header for tinymce pages.
    js: The name of the script file to load.
    """
    return """<!DOCTYPE html>
        <html>
        <head>
        <title>%(title)s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="static/images/logo/icon-16.png" />
        %(jquery)s
        <script type="text/javascript">
        var baseurl = '%(baseurl)s';
        var buildno = '%(buildno)s';
        var jswindowprint = %(jswindowprint)s;
        var onlysavewhendirty = %(onlysavewhendirty)s;
        </script>
        %(tinymce)s
        %(script)s
        </head>
        <body>
    """ % { "title": title,
           "jquery": JQUERY_JS, 
           "tinymce": TINYMCE_4_JS,
           "script": script_tag(js),
           "baseurl": BASE_URL,
           "buildno": BUILD,
           "jswindowprint": jswindowprint and "true" or "false",
           "onlysavewhendirty": onlysavewhendirty and "true" or "false" }

def tinymce_print_header(title):
    """
    Outputs a header for printable tinymce pages on mobile devices.
    """
    return """<!DOCTYPE html>
        <html>
        <head>
        <title>%(title)s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="static/images/logo/icon-16.png" />
        %(css)s
        </head>
        <body>
    """ % { "title": title,
           "css": css_tag("asm-tinymce.css") }

def tinymce_main(locale, action, recid="", mediaid = "", mode = "", redirecturl = "", template = "", content = ""):
    """ 
    Outputs the main body of a tinymce page.
    action: The post target for the controller
    template: Name of the template to post back
    content: The content for the box
    """
    return """
        <form method="post" action="%(action)s">
        <input type="hidden" id="locale" value="%(locale)s" />
        <input type="hidden" name="template" value="%(template)s" />
        <input type="hidden" name="recid" value="%(recid)s" />
        <input type="hidden" name="mediaid" value="%(mediaid)s" />
        <input type="hidden" name="mode" value="%(mode)s" />
        <input type="hidden" name="redirecturl" value="%(redirecturl)s" />
        <input type="hidden" name="savemode" value="save" />
        <div style="width: 750px; height: 600px; margin-left: auto; margin-right: auto">
        <textarea id="wp" name="document" style="width: 750px; height: 600px;">
        %(content)s
        </textarea>
        </div>
        </form>
        </body>
        </html>
    """ % { "action": action, 
            "locale": locale, 
            "template": template, 
            "recid": recid, 
            "mediaid": mediaid, 
            "mode": mode, 
            "redirecturl": redirecturl, 
            "content": content }

def graph_header(title):
    return """<!DOCTYPE html>
        <html>
        <head>
        <title>%(title)s</title>
        <link href="static/css/asm.css" rel="stylesheet" />
        %(jquery)s
        %(flot)s
        %(flotpie)s
        </head>
        <body>
        <h2 class="asm-header">%(title)s</h2>
        <div id="placeholder" style="display: none; width: 100%%; height: 500px;"></div>
    """ % { "title" : title, 
            "jquery": JQUERY_JS, 
            "flot": script_tag("jq/jquery.flot.min.js"), 
            "flotpie": script_tag("jq/jquery.flot.pie.min.js") }

def map_header(title):
    return """<!DOCTYPE html>
        <html>
        <head>
        <title>%(title)s</title>
        <link href="static/css/asm.css" rel="stylesheet" />
        %(jquery)s
        %(mousetrap)s
        <script type="text/javascript" src="config.js?ts=%(time)s"></script>
        %(common)s
        %(commonmap)s
        </head>
        <body>
        <h2 class="asm-header">%(title)s</h2>
    """ % { "title" : title, 
            "mousetrap": MOUSETRAP_JS,
            "jquery": JQUERY_JS, 
            "time": escape(now()),
            "common": script_tag("common.js"),
            "commonmap": script_tag("common_map.js") }

def escape(s):
    if s is None: return ""
    s = str(s)
    return s.replace("'", "&apos;").replace("\"", "&quot;").replace(">", "&gt;").replace("<", "&lt;")

def escape_angle(s):
    if s is None: return ""
    s = str(s)
    return s.replace(">", "&gt;").replace("<", "&lt;")

def header(title, session, js = ""):
    """
    The header for html pages.
    title: The page title
    session: The user session
    js: The name of an accompanying js file to load
    """
    s =  bare_header(title, js, session.theme, session.locale, session.dbo.database, session.config_ts)
    # Variables that we need to send for every page load
    #s += "<script type=\"text/javascript\">\n"
    #s += "</script>\n"
    return s

def footer():
    return "\n</body>\n</html>"

def currency(l, v):
    """
    Outputs a currency value. If it's negative, it shows in red.
    """
    s = format_currency(l, v)
    if s.startswith("("):
        s = "<span style=\"color: red\">" + s + "</span>"
    return s

def hidden(eid, value):
    """
    Outputs a hidden input field
    eid: The id of the input
    value: The value of the input
    """
    return "<input id=\"%s\" value=\"%s\" type=\"hidden\" />\n" % ( eid, str(value) )

def box(margintop=0, padding=5):
    """
    Outputs a div box container with jquery ui style
    """
    return """<div class="ui-helper-reset centered ui-widget-content ui-corner-all" style="margin-top: %dpx; padding: %dpx;">""" % (margintop, padding)

def heading(title, iscontent = True):
    """
    Outputs the heading for a page along with the asm content div
    """
    mid = ""
    if iscontent: mid = "id=\"asm-content\""
    return """
        <div %s class="ui-accordion ui-widget ui-helper-reset ui-accordion-icons">
        <h3 class="ui-accordion-header ui-helper-reset ui-corner-top ui-state-active centered"><a href="#">%s</a></h3>
        <div class="ui-helper-reset ui-widget-content ui-corner-bottom" style="padding: 5px;">
        """ % (mid, title)

def footing():
    """
    Outputs the footing for a page to close heading.
    """
    return """
    </div>
    </div>
    """
    
def script(code):
    """
    Outputs a script tag with javascript code
    """
    v = code
    # Escape anything in there that might cause our javascript
    # code to be malformed.
    v = v.replace("<script>", "&lt;script&gt;")
    v = v.replace("</script>", "&lt;\\/script&gt;")
    v = v.replace("\\\\\"", "\\\"")
    return "<script type=\"text/javascript\">\n%s\n</script>\n" % v

def script_json(varname, obj, prefix = "controller."):
    """
    Outputs a script tag with a variable varname containing 
    the object obj.
    """
    jv = json(obj)
    return script("var %s%s = %s;" % (prefix, varname, jv))

def script_var(varname, v, prefix = "controller."):
    """
    Outputs a script tag with a javascript variable varname
    containing the value v
    """
    return script("var %s%s = %s;" % (prefix, varname, v))

def script_var_str(varname, v, prefix = "controller."):
    """
    Outputs a script tag with a javascript variable varname
    that contains a string value v. Handles escaping
    """
    v = "'" + v.replace("'", "\\'").replace("\n", " ") + "'"
    return script_var(varname, v, prefix)

def controller(inner):
    """ Renders the controller """
    return "<script type=\"text/javascript\">\ncontroller = {};%s\n</script>\n" % inner

def controller_bool(name, b):
    """ Adds a controller boolean property """
    return "controller.%s = %s;" % (name, b and "true" or "false")

def controller_int(name, i):
    """ Adds a controller int property """
    return "controller.%s = %d;" % (name, i)

def controller_plain(name, v):
    """ Adds a controller property that's already formatted for js """
    return "controller.%s = %s;" % (name, v)

def controller_str(name, s):
    """ Adds a controller string property """
    s = "'" + s.replace("'", "\\'").replace("\n", "\\n") + "'"
    return "controller.%s = %s;" % (name, s)

def controller_json(name, obj):
    """ Adds a controller json property (converts obj to json) """
    jv = json(obj)
    return "controller.%s = %s;" % (name, jv)

def icon(name, title = ""):
    """
    Outputs a span tag containing an icon
    """
    if title == "":
        return "<span class=\"asm-icon asm-icon-%s\"></span>" % name
    else:
        return "<span class=\"asm-icon asm-icon-%s\" title=\"%s\"></span>" % (name, escape(title))

def img_src(row, mode):
    """
    Gets the img src attribute/link for a picture. If the row
    doesn't have preferred media, the nopic src is returned instead.
    We do it this way to make things more easily cacheable.
    If we're in animal mode, we'll take ANIMALID or ID, if we're
    in person mode we'll use PERSONID or ID
    row: An animal_query or person_query row containing ID, ANIMALID or PERSONID and WEBSITEMEDIANAME/DATE
    mode: The mode - animalthumb or personthumb
    """
    if row["WEBSITEMEDIANAME"] is None or row["WEBSITEMEDIANAME"] == "":
        return "image?mode=dbfs&id=/reports/nopic.jpg"
    else:
        idval = 0
        if mode == "animal":
            if row.has_key("ANIMALID"):
                idval = int(row["ANIMALID"])
            elif row.has_key("ID"):
                idval = int(row["ID"])
        elif mode == "person":
            if row.has_key("PERSONID"):
                idval = int(row["PERSONID"])
            elif row.has_key("ID"):
                idval = int(row["ID"])
        else:
            idval = int(row["ID"])
        uri = "image?mode=" + mode + "&id=" + str(idval)
        if row.has_key("WEBSITEMEDIADATE") and row["WEBSITEMEDIADATE"] is not None:
            uri += "&date=" + str(row["WEBSITEMEDIADATE"].isoformat())
        return uri

def json_menu(l, reports, mailmerges):
    """
    Returns JSON representing the main menu structure
    l: The locale
    reports: A list of tuples containing the report url and name
    mailmerges: A list of tuples containing the report/mailmerge url and name
    """
    structure = (
        ("", "asm", _("ASM", l), (
            ( "", "", "", "--cat", "asm-icon-animal", _("Animals", l) ),
            ( users.VIEW_ANIMAL, "alt+shift+v", "", "shelterview", "asm-icon-location", _("Shelter view", l) ),
            ( users.VIEW_ANIMAL, "alt+shift+f", "", "animal_find", "asm-icon-animal-find", _("Find animal", l) ),
            ( users.ADD_ANIMAL, "alt+shift+n", "", "animal_new", "asm-icon-animal-add", _("Add a new animal", l) ),
            ( users.ADD_LOG, "alt+shift+l", "", "log_new", "asm-icon-log", _("Add a log entry", l) ),
            ( users.CHANGE_ANIMAL, "", "", "animal_bulk", "asm-icon-litter", _("Bulk change animals", l) ),
            ( users.ADD_LITTER, "", "", "litters", "asm-icon-litter", _("Edit litters", l) ),
            ( "", "", "taglostfound", "--cat", "asm-icon-animal-lost", _("Lost/Found", l) ),
            ( users.VIEW_LOST_ANIMAL, "", "taglostfound", "lostanimal_find", "asm-icon-animal-lost-find", _("Find a lost animal", l) ),
            ( users.VIEW_FOUND_ANIMAL, "", "taglostfound", "foundanimal_find", "asm-icon-animal-found-find", _("Find a found animal", l) ),
            ( users.ADD_LOST_ANIMAL, "", "taglostfound", "lostanimal_new", "asm-icon-animal-lost-add", _("Add a lost animal", l) ),
            ( users.ADD_FOUND_ANIMAL, "", "taglostfound", "foundanimal_new", "asm-icon-animal-found-add", _("Add a found animal", l) ),
            ( users.MATCH_LOST_FOUND, "", "taglostfound", "lostfound_match", "asm-icon-match", _("Match lost and found animals", l) ),
            ( "", "", "", "--cat", "asm-icon-person", _("People", l) ),
            ( users.VIEW_PERSON, "alt+shift+p", "", "person_find", "asm-icon-person-find", _("Find person", l) ),
            ( users.ADD_PERSON, "", "", "person_new", "asm-icon-person-add", _("Add a new person", l) ),
            ( users.VIEW_PERSON, "", "", "person_lookingfor", "asm-icon-animal-find", _("Person looking for report", l) ),
            ( users.ADD_LOG, "", "", "log_new?mode=person", "asm-icon-log", _("Add a log entry", l) ),
            ( "", "", "", "--break", "", "" ),
            ( "", "", "taganimalcontrolheader", "--cat", "asm-icon-call", _("Animal Control", l) ),
            ( users.ADD_INCIDENT, "alt+shift+i", "taganimalcontrol", "incident_new", "asm-icon-blank", _("Report a new incident", l) ),
            ( users.VIEW_INCIDENT, "", "taganimalcontrol", "incident_find", "asm-icon-blank", _("Find incident", l) ),
            ( users.VIEW_INCIDENT, "", "taganimalcontrol", "incident_map", "asm-icon-map", _("Map of active incidents", l) ),
            ( users.VIEW_TRAPLOAN, "", "tagtraploan", "traploan?filter=active", "asm-icon-traploan", _("Trap loans", l) ),
            ( users.VIEW_LICENCE, "", "taganimalcontrol", "licence?offset=i31", "asm-icon-licence", _("Licensing", l) ),
            ( "", "", "taganimalcontrol", "calendarview?ev=ol", "asm-icon-calendar", _("Animal control calendar", l) ),
            ( "", "", "", "--cat", "asm-icon-diary", _("Diary", l) ),
            ( users.ADD_DIARY, "", "", "diary_edit_my?newnote=1", "asm-icon-blank", _("Add a diary note", l) ),
            ( users.EDIT_MY_DIARY_NOTES, "", "", "diary_edit_my", "asm-icon-blank", _("My diary notes", l) ),
            ( users.EDIT_ALL_DIARY_NOTES, "", "", "diary_edit", "asm-icon-blank", _("All diary notes", l) ),
            ( users.EDIT_DIARY_TASKS, "", "", "diarytasks", "asm-icon-diary-task", _("Edit diary tasks", l) ),
            ( users.EDIT_MY_DIARY_NOTES, "alt+shift+c", "", "calendarview?ev=d", "asm-icon-calendar", _("Diary calendar", l) ),
            ( "", "", "tagdocumentrepo", "--cat", "asm-icon-document", _("Document Repository", l) ),
            ( users.VIEW_REPO_DOCUMENT, "", "tagdocumentrepo", "document_repository", "asm-icon-blank", _("Document Repository", l) ),
            ( "", "", "tagonlineform", "--cat", "asm-icon-forms", _("Online Forms", l) ),
            ( users.EDIT_ONLINE_FORMS, "", "tagonlineform", "onlineforms", "asm-icon-blank", _("Edit Online Forms", l) ),
            ( users.VIEW_INCOMING_FORMS, "", "tagonlineform", "onlineform_incoming", "asm-icon-blank", _("View Incoming Forms", l) ),
            ( "", "", "tagwaitinglist", "--cat", "asm-icon-waitinglist", _("Waiting List", l) ),
            ( users.ADD_WAITING_LIST, "", "tagwaitinglist", "waitinglist_new", "asm-icon-blank", _("Add an animal to the waiting list", l) ),
            ( users.VIEW_WAITING_LIST, "alt+shift+w", "tagwaitinglist", "waitinglist_results", "asm-icon-blank", _("Edit the current waiting list", l) )
        )),
        (users.VIEW_MOVEMENT, "move", _("Move", l), (
            ( users.ADD_MOVEMENT, "", "", "--cat", "asm-icon-movement", _("Out", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_reserve", "asm-icon-reservation", _("Reserve an animal", l) ),
            ( users.ADD_MOVEMENT, "alt+shift+o", "", "move_foster", "asm-icon-blank", _("Foster an animal", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_transfer", "asm-icon-blank", _("Transfer an animal", l) ),
            ( users.ADD_MOVEMENT, "alt+shift+a", "", "move_adopt", "asm-icon-person", _("Adopt an animal", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_reclaim", "asm-icon-blank", _("Reclaim an animal", l) ),
            ( users.ADD_MOVEMENT, "", "tagretailer", "move_retailer", "asm-icon-blank", _("Move an animal to a retailer", l) ),
            ( users.CHANGE_ANIMAL, "", "", "move_deceased", "asm-icon-death", _("Mark an animal deceased", l) ),
            ( users.VIEW_MOVEMENT, "", "", "--cat", "asm-icon-book", _("Books", l) ),
            ( users.VIEW_MOVEMENT, "", "", "move_book_reservation", "asm-icon-reservation", _("Reservation book", l) ),
            ( users.VIEW_MOVEMENT, "", "", "move_book_foster", "asm-icon-blank", _("Foster book", l) ),
            ( users.VIEW_MOVEMENT, "", "tagretailer", "move_book_retailer", "asm-icon-blank", _("Retailer book", l) ),
            ( users.VIEW_MOVEMENT, "", "", "move_book_transport", "asm-icon-blank", _("Transport book", l) ),
            ( users.VIEW_MOVEMENT, "", "tagtrial", "move_book_trial_adoption", "asm-icon-trial", _("Trial adoption book", l) ),
            ( "", "", "", "--break", "", "" ),
            ( users.ADD_MOVEMENT, "", "", "--cat", "asm-icon-animal", _("In", l) ),
            ( users.ADD_ANIMAL, "", "alt+shift+n", "animal_new", "asm-icon-animal-add", _("Induct a new animal", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_book_recent_adoption", "asm-icon-blank", _("Return an animal from adoption", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_book_recent_transfer", "asm-icon-blank", _("Return a transferred animal", l) ),
            ( users.ADD_MOVEMENT, "", "", "move_book_recent_other", "asm-icon-blank", _("Return an animal from another movement", l) )
        )),
        ("", "medical", _("Medical", l), (
            ( "", "", "", "calendarview?ev=vmt", "asm-icon-calendar", _("Medical calendar", l) ),
            ("", "", "", "--cat", "asm-icon-vaccination", _("Vaccinations", l) ),
            (users.ADD_VACCINATION, "", "", "vaccination?newvacc=1", "asm-icon-blank", _("Add a vaccination", l) ),
            (users.VIEW_VACCINATION, "", "", "vaccination", "asm-icon-book", _("Vaccination book", l) ),
            ("", "", "", "--cat", "asm-icon-test", _("Tests", l) ),
            (users.ADD_TEST, "", "", "test?newtest=1", "asm-icon-blank", _("Add a test", l) ),
            (users.VIEW_TEST, "", "", "test", "asm-icon-book", _("Test book", l) ),
            ("", "", "", "--cat", "asm-icon-medical", _("Treatments", l) ),
            (users.ADD_MEDICAL, "", "", "medical?newmed=1", "asm-icon-blank", _("Add a medical regimen", l) ),
            (users.VIEW_MEDICAL, "", "", "medical", "asm-icon-book", _("Medical book", l) ),
            (users.VIEW_MEDICAL, "", "", "medicalprofile", "asm-icon-blank", _("Medical profiles", l) )
        )),
        ("", "financial", _("Financial", l), (
            ( users.VIEW_ACCOUNT, "alt+shift+x", "tagaccounts", "accounts", "asm-icon-accounts", _("Accounts", l) ),
            ( users.VIEW_STOCKLEVEL, "", "tagstock", "stocklevel", "asm-icon-stock", _("Stock", l) ),
            ( users.VIEW_DONATION, "", "tagaccounts", "--cat", "", "Payments" ),
            ( users.VIEW_DONATION, "alt+shift+d", "tagaccounts", "donation", "asm-icon-donation", _("Payment book", l) ),
            ( users.VIEW_DONATION, "", "tagaccounts", "calendarview?ev=p", "asm-icon-calendar", _("Payment calendar", l) ),
            ( users.ADD_DONATION, "", "tagaccounts", "donation_receive", "asm-icon-blank", _("Receive a payment", l) ),
            ( users.VIEW_DONATION, "", "taggb", "--cat", "", "HMRC" ),
            ( users.VIEW_DONATION, "", "taggb", "giftaid_hmrc_spreadsheet", "asm-icon-report", "Generate HMRC Gift Aid spreadsheet" )
        )),
        (users.USE_INTERNET_PUBLISHER, "publishing", _("Publishing", l), (
            ("", "", "", "--cat", "asm-icon-settings", _("Configuration", l) ),
            (users.VIEW_ANIMAL, "", "", "search?q=forpublish", "asm-icon-animal", _("View animals matching publishing options", l) ),
            (users.SYSTEM_OPTIONS, "", "", "publish_options", "asm-icon-settings", _("Set publishing options", l) ),
            (users.SYSTEM_OPTIONS, "", "", "htmltemplates", "asm-icon-document", _("Edit HTML publishing templates", l)),
            ("", "", "", "--cat", "web", _("Publish now", l) ),
            ("", "", "", "publish?mode=ftp", "asm-icon-blank", _("Publish HTML via FTP", l) ),
            ("", "", "", "publish?mode=ap", "asm-icon-blank", "Publish to AdoptAPet.com" ),
            ("", "", "", "publish?mode=hlp", "asm-icon-blank", _("Publish to HelpingLostPets.com", l) ),
            ("", "", "", "publish?mode=mp", "asm-icon-blank", "Publish to MeetAPet.com" ),
            ("", "", "", "publish?mode=pf", "asm-icon-blank", "Publish to PetFinder.com" ),
            ("", "", "", "publish?mode=pr", "asm-icon-blank", "Publish to PetRescue.com.au" ),
            ("", "", "", "publish?mode=rg", "asm-icon-blank", "Publish to RescueGroups.org" ),
            ("", "", "", "publish?mode=vear", "asm-icon-blank", "Register animals with AKC Reunite Microchips (via VetEnvoy)"),
            ("", "", "", "publish?mode=ptuk", "asm-icon-blank", "Register animals with AVID/PETtrac UK Microchips"),
            ("", "", "", "publish?mode=veha", "asm-icon-blank", "Register animals with HomeAgain Microchips (via VetEnvoy)"),
            ("", "", "", "publish?mode=pl", "asm-icon-blank", "Register animals with PetLink Microchips"),
            ("", "", "", "publish?mode=st", "asm-icon-blank", "Register animals with SmartTag Pet ID"),
            (users.USE_INTERNET_PUBLISHER, "", "", "publish_logs", "asm-icon-log", _("View publishing logs", l) )
        )),
        (users.MAIL_MERGE, "mailmerge", _("Mail", l),
            mailmerges
        ),
        (users.VIEW_REPORT, "reports", _("Reports", l), 
            reports 
        ),
        (users.SYSTEM_MENU, "settings", _("Settings", l), (
            ("", "", "", "--cat", "asm-icon-settings", _("System", l)),
            ("", "", "", "additional", "asm-icon-additional-field", _("Additional fields", l) ),
            (users.MODIFY_LOOKUPS, "", "", "lookups", "asm-icon-lookups", _("Lookup data", l) ),
            ("", "", "", "document_templates", "asm-icon-document", _("Document templates", l) ),
            (users.VIEW_REPORT, "", "", "reports", "asm-icon-report", _("Reports", l) ),
            (users.EDIT_USER, "", "", "systemusers", "asm-icon-users", _("System user accounts", l) ),
            (users.EDIT_USER, "", "", "roles", "asm-icon-auth", _("User roles", l) ),
            (users.USE_SQL_INTERFACE, "", "", "sql", "asm-icon-sql", _("SQL interface", l) ),
            (users.USE_SQL_INTERFACE, "", "", "csvimport", "asm-icon-database", _("Import a CSV file", l) ),
            (users.SYSTEM_OPTIONS, "", "", "options", "asm-icon-settings", _("Options", l) )
        ))
    )
    return extjson.dumps(structure)

def json_animalfindcolumns(dbo):
    l = dbo.locale
    cols = [ 
        ( "AnimalTypeID", _("Animal Type", l) ),
        ( "AnimalName", _("Name", l) ),
        ( "BaseColourID", _("Color", l) ),
        ( "SpeciesID", _("Species", l) ),
        ( "BreedName", _("Breed", l) ),
        ( "CoatType", _("Coat", l) ),
        ( "Markings", _("Features", l) ),
        ( "ShelterCode", _("Code", l) ),
        ( "AcceptanceNumber", _("Litter Ref", l) ),
        ( "DateOfBirth", _("Date Of Birth", l) ),
        ( "AgeGroup", _("Age Group", l) ),
        ( "AnimalAge", _("Age", l) ),
        ( "DeceasedDate", _("Died", l) ),
        ( "Sex", _("Sex", l) ),
        ( "IdentichipNumber", _("Microchip Number", l) ),
        ( "IdentichipDate", _("Microchip Date", l) ),
        ( "TattooNumber", _("Tattoo Number", l) ),
        ( "TattooDate", _("Tattoo Date", l) ),
        ( "Neutered", _("Altered", l) ),
        ( "NeuteredDate", _("Altered Date", l) ),
        ( "CombiTested", _("FIV/L Tested", l) ),
        ( "CombiTestDate", _("FIV/L Test Date", l) ),
        ( "CombiTestResult", _("FIV Result", l) ),
        ( "FLVResult", _("FLV Result", l) ),
        ( "HeartwormTested", _("Heartworm Tested", l) ),
        ( "HeartwormTestDate", _("Heartworm Test Date", l) ),
        ( "HeartwormTestResult", _("Heartworm Test Result", l) ),
        ( "Declawed", _("Declawed", l) ),
        ( "HiddenAnimalDetails", _("Hidden Comments", l) ),
        ( "AnimalComments", _("Comments", l) ),
        ( "ReasonForEntry", _("Entry Reason", l) ),
        ( "ReasonNO", _("Reason Not From Owner", l) ),
        ( "DateBroughtIn", _("Date Brought In", l) ),
        ( "EntryReasonID", _("Entry Reason Category", l) ),
        ( "HealthProblems", _("Health Problems", l) ),
        ( "PTSReason", _("Death Comments", l) ),
        ( "PTSReasonID", _("Death Reason", l) ),
        ( "IsGoodWithCats", _("Good With Cats", l) ),
        ( "IsGoodWithDogs", _("Good With Dogs", l) ),
        ( "IsGoodWithChildren", _("Good With Children", l) ),
        ( "IsHouseTrained", _("Housetrained", l) ),
        ( "IsNotAvailableForAdoption", _("Not Available For Adoption", l) ),
        ( "IsHold", _("Hold", l) ),
        ( "HoldUntilDate", _("Hold until", l) ),
        ( "IsQuarantine", _("Quarantine", l) ),
        ( "HasSpecialNeeds", _("Special Needs", l) ),
        ( "ShelterLocation", _("Location", l) ),
        ( "ShelterLocationUnit", _("Unit", l) ),
        ( "Size", _("Size", l) ),
        ( "RabiesTag", _("RabiesTag", l) ),
        ( "TimeOnShelter", _("Time On Shelter", l) ),
        ( "DaysOnShelter", _("Days On Shelter", l) ),
        ( "HasActiveReserve", _("Reserved", l) ), 
        ( "Image", _("Image", l) )
        ]
    fd = additional.get_field_definitions(dbo, "animal")
    for f in fd:
        cols.append( (f["FIELDNAME"], f["FIELDLABEL"]) )
    cols = findcolumns_sort(cols)
    findcolumns_selectedtofront(cols, configuration.animal_search_columns(dbo))
    return json(cols)

def json_autocomplete_litters(dbo):
    l = dbo.locale
    al = animal.get_litters(dbo)
    rv = []
    for i in al:
        disp = ""
        if i["PARENTANIMALID"] is not None and i["PARENTANIMALID"] > 0:
            disp = _("{0}: {1} {2} - {3} {4}", l).format(
                i["MOTHERCODE"], i["MOTHERNAME"],
                i["ACCEPTANCENUMBER"], i["SPECIESNAME"],
                i["COMMENTS"][:40])
        else:
            disp = _("{0} - {1} {2}", l).format(
                i["ACCEPTANCENUMBER"], i["SPECIESNAME"],
                i["COMMENTS"][:40])
        rv.append( { "label": disp, "value": i["ACCEPTANCENUMBER"] } )
    return json(rv)

def json_lookup_tables(l):
    aslist = []
    for k, v in lookups.LOOKUP_TABLES.iteritems():
        if k.startswith("lks"):
            # static tables only appear in non-English locales
            # for translation purposes and to stop people messing 
            # with things and breaking them
            if not l.startswith("en"):
                aslist.append(( k, translate(v[0], l)))
        else:
            aslist.append(( k, translate(v[0], l)))
    return sorted(aslist, key=lambda x: x[1])

def json_personfindcolumns(dbo):
    l = dbo.locale
    cols = [ 
        ( "OwnerTitle", _("Title", l) ),
        ( "OwnerInitials", _("Initials", l) ),
        ( "OwnerForenames", _("First Names", l) ),
        ( "OwnerSurname", _("Last Name", l) ),
        ( "OwnerName", _("Name", l) ),
        ( "OwnerAddress", _("Address", l) ),
        ( "OwnerTown", _("City", l) ),
        ( "OwnerCounty", _("State", l) ),
        ( "OwnerPostcode", _("Zipcode", l) ),
        ( "HomeTelephone", _("Home", l) ),
        ( "WorkTelephone", _("Work", l) ),
        ( "MobileTelephone", _("Cell", l) ),
        ( "EmailAddress", _("Email", l) ),
        ( "IDCheck", _("Homechecked", l) ),
        ( "Comments", _("Comments", l) ),
        ( "IsBanned", _("Banned", l) ),
        ( "IsVolunteer", _("Volunteer", l) ),
        ( "IsHomeChecker", _("Homechecker", l) ),
        ( "IsMember", _("Member", l) ),
        ( "MembershipExpiryDate", _("Membership Expiry", l) ),
        ( "MembershipNumber", _("Membership Number", l) ),
        ( "IsDonor", _("Donor", l) ),
        ( "IsShelter", _("Shelter", l) ),
        ( "IsACO", _("ACO", l) ),
        ( "IsStaff", _("Staff", l) ),
        ( "IsFosterer", _("Fosterer", l) ),
        ( "IsRetailer", _("Retailer", l) ),
        ( "IsVet", _("Vet", l) ),
        ( "IsGiftAid", _("GiftAid", l) ),
        ( "HomeCheckAreas", _("Homecheck Areas", l) ),
        ( "DateLastHomeChecked", _("Homecheck Date", l) ),
        ( "HomeCheckedBy", _("Homechecked By", l) )
        ]
    fd = additional.get_field_definitions(dbo, "person")
    for f in fd:
        cols.append( (f["FIELDNAME"], f["FIELDLABEL"]) )
    findcolumns_sort(cols)
    findcolumns_selectedtofront(cols, configuration.person_search_columns(dbo))
    return json(cols)

def json_quicklinks(dbo):
    l = dbo.locale
    ql = []
    for k, v in configuration.QUICKLINKS_SET.iteritems():
        ql.append( ( str(k), translate(v[2], l) ) )
    ql = findcolumns_sort(ql)
    findcolumns_selectedtofront(ql, configuration.quicklinks_id(dbo))
    return json(ql)

def json_waitinglistcolumns(dbo):
    l = dbo.locale
    cols = [ 
        ( "Rank", _("Rank", l) ),
        ( "SpeciesID", _("Species", l) ),
        ( "Size", _("Size", l) ),
        ( "DatePutOnList", _("Date Put On", l) ),
        ( "TimeOnList", _("Time On List", l) ),
        ( "OwnerName", _("Name", l) ),
        ( "OwnerAddress", _("Address", l) ),
        ( "OwnerTown", _("City", l) ),
        ( "OwnerCounty", _("State", l) ),
        ( "OwnerPostcode", _("Zipcode", l) ),
        ( "HomeTelephone", _("Home", l) ),
        ( "WorkTelephone", _("Work", l) ),
        ( "MobileTelephone", _("Cell", l) ),
        ( "EmailAddress", _("Email", l) ),
        ( "AnimalDescription", _("Description", l) ),
        ( "ReasonForWantingToPart", _("Reason", l) ),
        ( "CanAffordDonation", _("Donation?", l) ),
        ( "Urgency", _("Urgency", l) ),
        ( "DateRemovedFromList", _("Date Removed", l) ),
        ( "ReasonForRemoval", _("Removal Reason", l) ),
        ( "Comments", _("Comments") )
        ]
    cols = findcolumns_sort(cols)
    findcolumns_selectedtofront(cols, configuration.waiting_list_view_columns(dbo))
    return json(cols)

def findcolumns_sort(cols):
    """
    For options_*findcolumns routines, sorts the list alphabetically
    by display string
    """
    return sorted(cols, key=lambda x: x[1])

def findcolumns_selectedtofront(cols, vals):
    """
    For options_*findcolumns routines, moves selected items
    to the beginning of the list in order they appear in
    vals. vals is a comma separated string.
    """
    for v in reversed(vals.split(",")):
        v = v.strip()
        for i,val in enumerate(cols):
            if val[0] == v:
                cols.insert(0, cols.pop(i))
                break
    return vals

def thumbnail_img_src(row, mode):
    """
    Gets the img src attribute for a thumbnail picture. If the row
    doesn't have preferred media, the nopic src is returned instead.
    We do it this way to make things more easily cacheable.
    If we're in animal mode, we'll take ANIMALID or ID, if we're
    in person mode we'll use PERSONID or ID
    row: An animal_query or person_query row containing ID, ANIMALID or PERSONID and WEBSITEMEDIANAME/DATE
    mode: The mode - animalthumb or personthumb
    """
    if row["WEBSITEMEDIANAME"] is None or row["WEBSITEMEDIANAME"] == "":
        return "image?mode=dbfs&id=/reports/nopic.jpg"
    else:
        idval = 0
        if mode == "animalthumb":
            if row.has_key("ANIMALID"):
                idval = int(row["ANIMALID"])
            elif row.has_key("ID"):
                idval = int(row["ID"])
        elif mode == "personthumb":
            if row.has_key("PERSONID"):
                idval = int(row["PERSONID"])
            elif row.has_key("ID"):
                idval = int(row["ID"])
        else:
            idval = int(row["ID"])
        uri = "image?mode=" + mode + "&id=" + str(idval)
        if row.has_key("WEBSITEMEDIADATE") and row["WEBSITEMEDIADATE"] is not None:
            uri += "&date=" + str(row["WEBSITEMEDIADATE"].isoformat())
        return uri

def option(name, value = None, selected = False):
    sel = ""
    val = ""
    if selected: sel = " selected=\"selected\""
    if value is not None: val = " value=\"%s\"" % value
    return "<option %s%s>%s</option>\n" % ( val, sel, name )

def options_accounts(dbo, includeAll = False, selected = -1, alltext = "*"):
    s = ""
    l = dbo.locale
    if includeAll: 
        if alltext == "*": s += option(_("(all)", l), "-1", False)
        else: s += option(alltext, "-1", False)
    ac = financial.get_accounts(dbo)
    for a in ac:
        s += option("%s" % a["CODE"],
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_account_types(dbo, includeAll = False, selected = -1, alltext = "*"):
    l = dbo.locale
    s = ""
    if includeAll: 
        if alltext == "*": s += option(_("(all)", l), "-1", False)
        else: s += option(alltext, "-1", False)
    at = lookups.get_account_types(dbo)
    for a in at:
        s += option(a["ACCOUNTTYPE"],
            str(a["ID"]),
            int(a["ID"]) == selected)
    return s

def options_additionalfield_links(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    al = lookups.get_additionalfield_links(dbo)
    for a in al:
        s += option(a["LINKTYPE"], 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_additionalfield_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    at = lookups.get_additionalfield_types(dbo)
    for a in at:
        s += option(a["FIELDTYPE"], 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_agegroups(dbo, includeAll = False, includeUnknown = False, selected = "-1"):
    s = ""
    l = dbo.locale
    if includeAll: s += option(_("(all)", l), "-1", False)
    if includeUnknown: s += option(_("(unknown)", l), "Unknown", False)
    ag = configuration.age_groups(dbo)
    for a in ag:
        s += option(a, a, a == selected)
    return s

def options_animals(dbo, includeAll = False, selected = -1):
    s = ""
    l = dbo.locale
    if includeAll: s += option(_("(all)", l), "-1", False)
    an = animal.get_animals_namecode(dbo)
    for a in an:
        s += option("%s - %s" % ( a["ANIMALNAME"], a["SHELTERCODE"] ), 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_animals_on_shelter(dbo, includeAll = False, selected = -1):
    s = ""
    l = dbo.locale
    if includeAll: s += option(_("(all)", l), "-1", False)
    an = animal.get_animals_on_shelter_namecode(dbo)
    for a in an:
        s += option("%s - %s" % ( a["ANIMALNAME"], a["CODE"] ), 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_animals_on_shelter_foster(dbo, includeAll = False, selected = -1):
    s = ""
    l = dbo.locale
    if includeAll: s += option(_("(all)", l), "-1", False)
    an = animal.get_animals_on_shelter_foster_namecode(dbo)
    for a in an:
        s += option("%s - %s" % ( a["ANIMALNAME"], a["CODE"] ), 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_animal_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    at = lookups.get_animal_types(dbo)
    for a in at:
        s += option(a["ANIMALTYPE"], 
            str(a["ID"]), 
            int(a["ID"]) == selected)
    return s

def options_breeds(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    bd = lookups.get_breeds_by_species(dbo)
    gp = ""
    ngp = ""
    for b in bd:
        
        ngp = b["SPECIESNAME"]
        if ngp is None: ngp = ""

        if gp != ngp:
            if gp != "":
                s += "</optgroup>\n"
            s += "<optgroup id='ngp-" + str(b["SPECIESID"]) + "' label=\"%s\">\n" % ngp
            gp = ngp

        s += option(b["BREEDNAME"],
            str(b["ID"]),
            int(b["ID"]) == selected)
    return s

def options_coattypes(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    ct = lookups.get_coattypes(dbo)
    for c in ct:
        s += option(c["COATTYPE"],
            str(c["ID"]),
            int(c["ID"]) == selected)
    return s

def options_colours(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    bc = lookups.get_basecolours(dbo)
    for c in bc:
        s += option(c["BASECOLOUR"],
            str(c["ID"]),
            int(c["ID"]) == selected)
    return s

def options_cost_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    bc = lookups.get_costtypes(dbo)
    for c in bc:
        s += option(c["COSTTYPENAME"],
            str(c["ID"]),
            int(c["ID"]) == selected)
    return s

def options_deathreasons(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    dr = lookups.get_deathreasons(dbo)
    for d in dr:
        s += option(d["REASONNAME"],
            str(d["ID"]),
            int(d["ID"]) == selected)
    return s

def options_diets(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    di = lookups.get_diets(dbo)
    for d in di:
        s += option(d["DIETNAME"],
            str(d["ID"]),
            int(d["ID"]) == selected)
    return s

def options_donation_types(dbo, includeAll = False, includeNone = False, selected = -1, alltext = "*"):
    l = dbo.locale
    s = ""
    if includeAll: 
        if alltext == "*": s += option(_("(all)", l), "-1", False)
        else: s += option(alltext, "-1", False)
    if includeNone:
        s += option(_("(none)", l), "0", False)
    dt = lookups.get_donation_types(dbo)
    for d in dt:
        s += option(d["DONATIONNAME"],
            str(d["ID"]),
            int(d["ID"]) == selected)
    return s

def options_donation_frequencies(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    df = lookups.get_donation_frequencies(dbo)
    for d in df:
        s += option(d["FREQUENCY"],
            str(d["ID"]),
            int(d["ID"]) == selected)
    return s

def options_entryreasons(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    er = lookups.get_entryreasons(dbo)
    for e in er:
        s += option(e["REASONNAME"],
            str(e["ID"]),
            int(e["ID"]) == selected)
    return s

def options_internal_locations(dbo, includeAll = False, selected = -1, locationfilter = ""):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    lo = lookups.get_internal_locations(dbo, locationfilter)
    for l in lo:
        s += option(l["LOCATIONNAME"], 
            str(l["ID"]), 
            int(l["ID"]) == selected)
    return s

def options_litters(dbo, includeAll = False, selected = "-1"):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    al = animal.get_litters(dbo)
    for i in al:
        disp = ""
        if i["PARENTANIMALID"] is not None and i["PARENTANIMALID"] > 0:
            disp = _("{0}: {1} {2} - {3} {4}", l).format(
                i["MOTHERCODE"], i["MOTHERNAME"],
                i["ACCEPTANCENUMBER"], i["SPECIESNAME"],
                i["COMMENTS"][:40])
        else:
            disp = _("{0} - {1} {2}", l).format(
                i["ACCEPTANCENUMBER"], i["SPECIESNAME"],
                i["COMMENTS"][:40])
        s += option(disp, i["ACCEPTANCENUMBER"], i["ACCEPTANCENUMBER"] == selected)
    return s

def options_locales():
    s = ""
    for code, label in lookups.LOCALES:
        s += "<option value=\"" + code + "\">" + label + "</option>"
    return s

def options_log_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    lt = lookups.get_log_types(dbo)
    for l in lt:
        s += option(l["LOGTYPENAME"], 
            str(l["ID"]), 
            int(l["ID"]) == selected)
    return s

def options_medicalprofiles(dbo, includeNone = False, selected = 0):
    s = ""
    if includeNone: s += option("", "0", False)
    mp = medical.get_profiles(dbo)
    for m in mp:
        s += option(m["PROFILENAME"], 
            str(m["ID"]), 
            int(m["ID"]) == selected)
    return s

def options_movement_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    mt = lookups.get_movement_types(dbo)
    for m in mt:
        if m["ID"] != 9 and m["ID"] != 10 and m["ID"] != 11:
            s += option(m["MOVEMENTTYPE"], 
                str(m["ID"]), 
                int(m["ID"]) == selected)
    return s

def options_person_flags(dbo):
    s = ""
    pf = lookups.get_person_flags(dbo)
    for p in pf:
        s += option(p["FLAG"])
    return s

def options_people_not_homechecked(dbo, includeAll = False, selected = -1):
    s = ""
    l = dbo.locale
    if includeAll: s += option(_("(all)", l), "-1", False)
    pp = person.get_reserves_without_homechecks(dbo)
    for p in pp:
        s += option("%s - %s" % ( p["OWNERNAME"], p["OWNERADDRESS"] ), 
            str(p["ID"]), 
            int(p["ID"]) == selected)
    return s

def options_posneg(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    pn = lookups.get_posneg(dbo)
    for p in pn:
        s += option(p["NAME"],
            str(p["ID"]),
            int(p["ID"]) == selected)
    return s

def options_species(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    sp = lookups.get_species(dbo)
    for sx in sp:
        s += option(sx["SPECIESNAME"], 
            str(sx["ID"]), 
            int(sx["ID"]) == selected)
    return s

def options_sexes(dbo,  includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    se = lookups.get_sexes(dbo)
    for sx in se:
        s += option(sx["SEX"],
            str(sx["ID"]),
            int(sx["ID"]) == selected)
    return s

def options_sizes(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    se = lookups.get_sizes(dbo)
    for sz in se:
        s += option(sz["SIZE"],
            str(sz["ID"]),
            int(sz["ID"]) == selected)
    return s

def options_smarttagtypes(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    st = [{ "ID" : 0, "TYPE" : _("Annual", l)},
          { "ID" : 1, "TYPE" : _("5 Year", l)},
          { "ID" : 2, "TYPE" : _("Lifetime", l)}]
    for t in st:
        s += option(t["TYPE"],
            str(t["ID"]),
            int(t["ID"]) == selected)
    return s

def options_urgencies(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "all", False)
    wu = lookups.get_urgencies(dbo)
    for u in wu:
        s += option(u["URGENCY"],
            str(u["ID"]),
            int(u["ID"]) == selected)
    return s

def options_users(dbo, includeAll = False, selected = ""):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "all", selected == "all")
    su = users.get_users(dbo)
    for u in su:
        s += option(u["USERNAME"], u["USERNAME"], u["USERNAME"] == selected)
    return s

def options_users_and_roles(dbo, includeAll = False, includeEveryone = False, selected = ""):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "all", selected == "all")
    if includeEveryone: s += option(_("(everyone)", l), "*", selected == "*")
    su = users.get_users_and_roles(dbo)
    for u in su:
        s += option(u["USERNAME"], u["USERNAME"], u["USERNAME"] == selected)
    return s

def options_vaccination_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    vt = lookups.get_vaccination_types(dbo)
    for v in vt:
        s += option(v["VACCINATIONTYPE"],
            str(v["ID"]),
            int(v["ID"]) == selected)
    return s

def options_voucher_types(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    vt = lookups.get_voucher_types(dbo)
    for v in vt:
        s += option(v["VOUCHERNAME"],
            str(v["ID"]),
            int(v["ID"]) == selected)
    return s

def options_yesno(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    yn = lookups.get_yesno(dbo)
    for y in yn:
        s += option(y["NAME"],
            str(y["ID"]),
            int(y["ID"]) == selected)
    return s
  
def options_ynun(dbo, includeAll = False, selected = -1):
    l = dbo.locale
    s = ""
    if includeAll: s += option(_("(all)", l), "-1", False)
    yn = lookups.get_ynun(dbo)
    for y in yn:
        s += option(y["NAME"],
            str(y["ID"]),
            int(y["ID"]) == selected)
    return s

def smcom_report_list_table(l, reports):
    """
    Produces thead and tbody HTML for a list of selectable reports from sheltermanager.com
    """
    s = """<thead>
        <tr>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        </tr>
        </thead>
        <tbody>
    """ % ( _("Type", l), _("Title", l), _("Category", l), _("Locale", l), _("Description", l))
    for r in reports:
        s += "<tr>\n<td><span style='white-space: nowrap'>"
        s += "<input type='checkbox' class='asm-checkbox' data='%d' id='r%d' title='%s' /> <label for='r%d'>%s</label></span>\n" % (r["ID"], r["ID"], _("Select", l), r["ID"], r["TYPE"])
        s += "<td class='smcom-title'>%s</td>\n" % r["TITLE"]
        s += "<td class='smcom-category'>%s</td>\n" % r["CATEGORY"]
        s += "<td class='smcom-locale'>%s</td>\n" % r["LOCALE"]
        s += "<td class='smcom-description'>%s</td>\n</tr>\n" % r["DESCRIPTION"]
    return s

def template_selection(templates, url):
    """
    templates: A list of templates pathnames
    url: The initial portion of the url
    """
    s = ""
    lastpath = ""
    for t in templates:
        if t["PATH"] != lastpath:
            s += "<li class=\"asm-menu-category\">%s</li>" % ( t["PATH"] )
            lastpath = t["PATH"]
        s += "<li class=\"asm-menu-item\"><a target=\"_blank\" class=\"templatelink\" data=\"%d\" href=\"%s&template=%s\">%s</a></li>" % (t["ID"], url, t["ID"], t["NAME"])
    return s

def report_criteria(dbo, crit, locationfilter = ""):
    """
    Renders report criteria as an HTML form
    crit: The criteria - a list of tuples containing name, type and a question
    locationfilter: A comma separated list of location ids for filtering the internal location list
    """
    l = dbo.locale
    s = "<table>"
    for name, rtype, question in crit:
        if rtype == "DATE":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <input class="asm-textbox asm-datebox" id="report-%s" data-post="%s" value="%s" />
            </td>
            </tr>""" % ( question, name, name, python2display(l, now()) )
        elif rtype == "STRING":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <input class="asm-textbox" id="report-%s" data-post="%s" />
            </td>
            </tr>""" % ( question, name, name )
        elif rtype == "NUMBER":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <input class="asm-textbox asm-numberbox" id="report-%s" data-post="%s" />
            </td>
            </tr>""" % ( question, name, name )
        elif rtype == "ANIMAL" or rtype == "FSANIMAL" or rtype == "ALLANIMAL":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <input class="asm-animalchooser" id="report-%s" data-post="%s" type="hidden" />
            </td>
            </tr>""" % ( _("Animal", l), name, name )
        elif rtype == "PERSON":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <input class="asm-personchooser" id="report-%s" data-post="%s" type="hidden" />
            </td>
            </tr>""" % ( _("Person", l), name, name )
        elif rtype == "LITTER":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <select class="asm-selectbox" id="report-%s" data-post="%s">
            %s
            </select>
            </td>
            </tr>""" % ( _("Litter", l), name, name, options_litters(dbo) )
        elif rtype == "SPECIES":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <select class="asm-selectbox" id="report-%s" data-post="%s">
            %s
            </select>
            </td>
            </tr>""" % ( _("Species", l), name, name, options_species(dbo) )
        elif rtype == "LOCATION":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <select class="asm-selectbox" id="report-%s" data-post="%s">
            %s
            </select>
            </td>
            </tr>""" % ( _("Location", l), name, name, options_internal_locations(dbo, False, -1, locationfilter) )
        elif rtype == "TYPE":
            s += """
            <tr>
            <td>%s</td>
            <td>
            <select class="asm-selectbox" id="report-%s" data-post="%s">
            %s
            </select>
            </td>
            </tr>""" % ( _("Type", l), name, name, options_animal_types(dbo) )
    s += "<tr><td></td><td><button id=\"submitcriteria\">%s</button></td></tr></table>" % _("Generate", l)
    return s

def report_criteria_mobile(dbo, crit, locationfilter = ""):
    """
    l: The locale
    crit: The criteria - a list of tuples containing name, type and a question
    """
    return report_criteria(dbo, crit, locationfilter)

