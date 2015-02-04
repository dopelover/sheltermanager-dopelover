#!/usr/bin/python

import os, sys

# The path to the folder containing the ASM3 modules
PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep

# Put the rest of our modules on the path
sys.path.append(PATH)
sys.path.append(PATH + "locale")

import al
import additional as extadditional
import animal as extanimal
import animalcontrol as extanimalcontrol
import cache
import configuration
import csvimport as extcsvimport
import db, dbfs, dbupdate
import diary as extdiary
import financial
import html
from i18n import _, translate, get_version, get_display_date_format, get_currency_prefix, get_currency_symbol, get_currency_dp, python2display, subtract_days, subtract_months, first_of_month, last_of_month, monday_of_week, sunday_of_week, first_of_year, last_of_year, now, format_currency, i18nstringsjs
import log as extlog
import lookups as extlookups
import lostfound as extlostfound
import media as extmedia
import medical as extmedical
import mimetypes
import mobile as extmobile
import movement as extmovement
import onlineform as extonlineform
import person as extperson
import publish as extpublish
import reports as extreports
import search as extsearch
import service as extservice
import smcom
import social
import stock as extstock
import users
import utils
import waitinglist as extwaitinglist
import web
import wordprocessor
from sitedefs import BASE_URL, DEPLOYMENT_TYPE, DUMP_OVERRIDES, EMERGENCY_NOTICE, FORGOTTEN_PASSWORD, FORGOTTEN_PASSWORD_LABEL, LOCALE, FACEBOOK_CLIENT_ID, GEO_PROVIDER, GEO_PROVIDER_KEY, LEAFLET_CSS, LEAFLET_JS, MULTIPLE_DATABASES, MULTIPLE_DATABASES_TYPE, MULTIPLE_DATABASES_PUBLISH_URL, MULTIPLE_DATABASES_PUBLISH_FTP, ADMIN_EMAIL, EMAIL_ERRORS, MAP_LINK, MAP_PROVIDER, OSM_MAP_TILES, PETRESCUE_FTP_HOST, SESSION_STORE, SMARTTAG_FTP_USER, SMTP_SERVER, SMCOM_PAYMENT_LINK, VETENVOY_US_VENDOR_PASSWORD, VETENVOY_US_VENDOR_USERID

# URL to class mappings
urls = (
    "/", "index",
    "/accounts", "accounts", 
    "/accounts_trx", "accounts_trx", 
    "/additional", "additional",
    "/animal", "animal",
    "/animal_bulk", "animal_bulk",
    "/animal_costs", "animal_costs", 
    "/animal_diary", "animal_diary", 
    "/animal_diet", "animal_diet", 
    "/animal_donations", "animal_donations",
    "/animal_embed", "animal_embed",
    "/animal_facebook", "animal_facebook",
    "/animal_find", "animal_find",
    "/animal_find_results", "animal_find_results",
    "/animal_licence", "animal_licence",
    "/animal_log", "animal_log",
    "/animal_media", "animal_media",
    "/animal_medical", "animal_medical",
    "/animal_movements", "animal_movements",
    "/animal_new", "animal_new",
    "/animal_test", "animal_test",
    "/animal_vaccination", "animal_vaccination", 
    "/calendarview", "calendarview",
    "/change_password", "change_password",
    "/change_user_settings", "change_user_settings",
    "/citations", "citations", 
    "/config.js", "configjs",
    "/css", "css",
    "/csvimport", "csvimport",
    "/database", "database",
    "/diary_edit", "diary_edit",
    "/diary_edit_my", "diary_edit_my",
    "/diarytask", "diarytask",
    "/diarytasks", "diarytasks",
    "/document_gen", "document_gen",
    "/document_edit", "document_edit",
    "/document_media_edit", "document_media_edit",
    "/document_repository", "document_repository",
    "/document_templates", "document_templates",
    "/donation", "donation",
    "/donation_receive", "donation_receive",
    "/foundanimal", "foundanimal",
    "/foundanimal_diary", "foundanimal_diary",
    "/foundanimal_find", "foundanimal_find",
    "/foundanimal_find_results", "foundanimal_find_results",
    "/foundanimal_log", "foundanimal_log",
    "/foundanimal_media", "foundanimal_media",
    "/foundanimal_new", "foundanimal_new",
    "/giftaid_hmrc_spreadsheet", "giftaid_hmrc_spreadsheet",
    "/htmltemplates", "htmltemplates",
    "/i18n.js", "i18njs",
    "/js", "js",
    "/image", "image",
    "/incident", "incident",
    "/incident_citations", "incident_citations",
    "/incident_diary", "incident_diary",
    "/incident_log", "incident_log",
    "/incident_map", "incident_map",
    "/incident_media", "incident_media",
    "/incident_new", "incident_new",
    "/incident_find", "incident_find",
    "/incident_find_results", "incident_find_results",
    "/licence", "licence",
    "/litters", "litters", 
    "/log_new", "log_new",
    "/lookups", "lookups",
    "/lostanimal", "lostanimal",
    "/lostanimal_find", "lostanimal_find",
    "/lostanimal_find_results", "lostanimal_find_results",
    "/lostanimal_diary", "lostanimal_diary",
    "/lostanimal_log", "lostanimal_log",
    "/lostfound_match", "lostfound_match", 
    "/lostanimal_media", "lostanimal_media",
    "/lostanimal_new", "lostanimal_new",
    "/mailmerge", "mailmerge",
    "/media", "media",
    "/medicalprofile", "medicalprofile",
    "/mobile", "mobile",
    "/move_adopt", "move_adopt",
    "/move_book_foster", "move_book_foster",
    "/move_book_reservation", "move_book_reservation",
    "/move_book_retailer", "move_book_retailer",
    "/move_book_recent_adoption", "move_book_recent_adoption",
    "/move_book_recent_other", "move_book_recent_other",
    "/move_book_recent_transfer", "move_book_recent_transfer",
    "/move_book_transport", "move_book_transport",
    "/move_book_trial_adoption", "move_book_trial_adoption",
    "/move_book_unneutered", "move_book_unneutered",
    "/move_deceased", "move_deceased",
    "/move_foster", "move_foster",
    "/move_reclaim", "move_reclaim",
    "/move_reserve", "move_reserve",
    "/move_retailer", "move_retailer",
    "/move_transfer", "move_transfer",
    "/mobile_login", "mobile_login",
    "/mobile_logout", "mobile_logout",
    "/mobile_post", "mobile_post",
    "/mobile_report", "mobile_report",
    "/main", "main",
    "/login", "login",
    "/login_splash", "login_splash",
    "/logout", "logout",
    "/medical", "medical",
    "/onlineform", "onlineform",
    "/onlineform_incoming", "onlineform_incoming",
    "/onlineforms", "onlineforms",
    "/options", "options",
    "/person", "person",
    "/person_citations", "person_citations",
    "/person_diary", "person_diary",
    "/person_donations", "person_donations",
    "/person_embed", "person_embed",
    "/person_find", "person_find",
    "/person_find_results", "person_find_results",
    "/person_investigation", "person_investigation",
    "/person_licence", "person_licence",
    "/person_links", "person_links",
    "/person_log", "person_log",
    "/person_lookingfor", "person_lookingfor",
    "/person_media", "person_media",
    "/person_movements", "person_movements",
    "/person_new", "person_new",
    "/person_traploan", "person_traploan",
    "/person_vouchers", "person_vouchers",
    "/publish", "publish",
    "/publish_logs", "publish_logs",
    "/publish_options", "publish_options",
    "/report", "report",
    "/report_images", "report_images",
    "/reports", "reports",
    "/roles", "roles",
    "/search", "search",
    "/service", "service",
    "/shelterview", "shelterview",
    "/stocklevel", "stocklevel",
    "/sql", "sql",
    "/systemusers", "systemusers",
    "/test", "test",
    "/traploan", "traploan",
    "/vaccination", "vaccination",
    "/waitinglist", "waitinglist",
    "/waitinglist_diary", "waitinglist_diary",
    "/waitinglist_log", "waitinglist_log",
    "/waitinglist_media", "waitinglist_media",
    "/waitinglist_new", "waitinglist_new",
    "/waitinglist_results", "waitinglist_results",
    "/welcome", "welcome"
)

class MemCacheStore(web.session.Store):
    """ 
    A session manager that uses the local memcache install
    If anything goes wrong reading or writing a value, the client
    reconnects so as not to leave the store in a broken state.
    """
    def __contains__(self, key):
        return cache.get(key) is not None
    def __getitem__(self, key):
        return cache.get(key)
    def __setitem__(self, key, value):
        return cache.put(key, value, web.config.session_parameters["timeout"])
    def __delitem__(self, key):
        cache.delete(key)
    def cleanup(self, timeout):
        pass # Not needed, we assign values to memcache with timeout

def remote_ip():
    """
    Gets the IP address of the requester, taking account of
    reverse proxies
    """
    remoteip = web.ctx['ip']
    if web.ctx.env.has_key("HTTP_X_FORWARDED_FOR"):
        xf = web.ctx.env["HTTP_X_FORWARDED_FOR"]
        if xf is not None and str(xf).strip() != "":
            remoteip = xf
    return remoteip

def session_manager():
    """
    Sort out our session manager. We use a global in the utils module
    to hold the session to make sure if the app is reloaded it
    always gets the same session manager.
    """
    # Set session parameters, 24 hour timeout
    web.config.session_parameters["cookie_name"] = "asm_session_id"
    web.config.session_parameters["cookie_path"] = "/"
    web.config.session_parameters["timeout"] = 3600 * 24
    web.config.session_parameters["ignore_expiry"] = True
    web.config.session_parameters["ignore_change_ip"] = True
    sess = None
    if utils.websession is None:
        # Disable noisy logging from session db
        web.config.debug_sql = False
        if SESSION_STORE == "memcached":
            store = MemCacheStore()
        else:
            # Otherwise we're using the main database for session storage
            dbs = db.DatabaseInfo()
            dbn = dbs.dbtype.lower()
            if dbn == "postgresql": dbn = "postgres"
            if dbn == "mysql" or dbn == "postgres":
                if dbs.password != "":
                    wdb = web.database(dbn=dbn, host=dbs.host, port=dbs.port, db=dbs.database, user=dbs.username, pw=dbs.password)
                else:
                    wdb = web.database(dbn=dbn, host=dbs.host, port=dbs.port, db=dbs.database, user=dbs.username)
            elif dbn == "sqlite":
                wdb = web.database(dbn=dbn, db=dbs.database)
            try:
                wdb.printing = False
                wdb.query("create table sessions (" \
                    "session_id char(128) UNIQUE NOT NULL," \
                    "atime timestamp NOT NULL default current_timestamp," \
                    "data text)")
            except:
                pass
            store = web.session.DBStore(wdb, 'sessions')
        sess = web.session.Session(app, store, initializer={"user" : None, "dbo" : None, "locale" : None, "searches" : [] })
        utils.websession = sess
    else:
        sess = utils.websession
    return sess

def asm_404():
    """
    Custom 404 page
    """
    s = """
        <html>
        <head>
        <title>404</title>
        </head>
        <body style="background-color: #999">
        <div style="position: absolute; left: 20%; width: 60%; padding: 20px; background-color: white">

        <img src="static/images/logo/icon-64.png" align="right" />
        <h2>Error 404</h2>

        <p>Sorry, but the record you tried to access was not found.</p>

        <p><a href="javascript:history.back()">Go Back</a></p>

        </div>
        </body>
        </html>
    """
    return web.notfound(s)

def asm_500_email():
    """
    Custom 500 error page that sends emails to the site admin
    """
    web.emailerrors(ADMIN_EMAIL, web.webapi._InternalError)()
    s = """
        <html>
        <head>
        <title>500</title>
        </head>
        <body style="background-color: #999">
        <div style="position: absolute; left: 20%; width: 60%; padding: 20px; background-color: white">

        <img src="static/images/logo/icon-64.png" align="right" />
        <h2>Error 500</h2>

        <p>An error occurred trying to process your request.</p>

        <p>The system administrator has been notified to fix the problem.</p>

        <p>Sometimes, a database update needs to have been run. Return
        to the <a href="main">main screen</a> to run any outstanding
        database updates.</p>

        <p><a href="javascript:history.back()">Go Back</a></p>

        </div>
        </body>
        </html>
    """
    return web.internalerror(s)

def emergency_notice():
    """
    Returns emergency notice text if any is set.
    """
    if EMERGENCY_NOTICE != "":
        if os.path.exists(EMERGENCY_NOTICE):
            f = open(EMERGENCY_NOTICE, "r")
            s = f.read()
            f.close()
            return s
    return ""

# Setup the WSGI application object and session with mappings
app = web.application(urls, globals())
app.notfound = asm_404
if EMAIL_ERRORS:
    app.internalerror = asm_500_email
session = session_manager()

# Choose startup mode
if DEPLOYMENT_TYPE == "wsgi":
    application = app.wsgifunc()
elif DEPLOYMENT_TYPE == "fcgi":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    web.runwsgi = web.runfcgi

class index:
    def GET(self):
        # If there's no database structure, create it before 
        # redirecting to the login page.
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            if not db.has_structure(dbo):
                raise web.seeother("/database")
        raise web.seeother("/main")

class database:
    def GET(self):
        dbo = db.DatabaseInfo()
        if MULTIPLE_DATABASES:
            if smcom.active():
                raise utils.ASMPermissionError("N/A for sm.com")
            else:
                # We can't create the database as we have multiple, so
                # output the SQL creation script with default data
                # for whatever our dbtype is instead
                s = "-- Creation script for %s\n\n" % dbo.dbtype
                s += dbupdate.sql_structure(dbo)
                s += dbupdate.sql_default_data(dbo).replace("|=", ";")
                web.header("Content-Type", "text/plain")
                web.header("Content-Disposition", "attachment; filename=\"setup.sql\"")
                return s
        if db.has_structure(dbo):
            raise utils.ASMPermissionError("Database already created")
        s = html.bare_header("Create your database")
        s += """
            <h2>Create your new ASM database</h2>
            <form id="cdbf" method="post" action="database">
            <p>Please select your locale: 
            <select name="locale" class="asm-selectbox">
            %s
            </select>
            </p>
            <button id="createdb">Create Database</button>
            <div id="info" class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em; display: none">
            <p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>
            Please be patient, this can take upto a few minutes.
            </p>
            </div>
            </form>
            <script type="text/javascript">
            $("#createdb").button().click(function() {
                $("#createdb").button("disable");
                $("#info").fadeIn();
                $("#cdbf").submit();
            });
            </script>
            """ % html.options_locales()
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        post = utils.PostedData(web.input(locale = LOCALE), LOCALE)
        dbo = db.DatabaseInfo()
        dbo.locale = post["locale"]
        dbo.installpath = PATH
        dbupdate.install(dbo)
        raise web.seeother("/login")

class image:
    def GET(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "animal", id = "0", seq = -1), session.locale)
        try:
            lastmod, imagedata = extmedia.get_image_file_data(session.dbo, post["mode"], post["id"], post.integer("seq"), False)
        except Exception,err:
            al.error("%s" % str(err), "code.image", session.dbo)
            return ""
        if imagedata != "NOPIC":
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "max-age=86400")
            return imagedata
        else:
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "no-cache")
            raise web.seeother("image?mode=dbfs&id=/reports/nopic.jpg")

class configjs:
    def GET(self):
        # db is the database name and ts is the date/time the config was
        # last read upto. The ts value (config_ts) is set during login and
        # updated whenever the user posts to publish_options or options.
        # Both values are used purely to cache the config in the browser, but
        # aren't actually used by the controller here.
        # post = utils.PostedData(web.input(db = "", ts = ""), session.locale)
        if utils.is_loggedin(session) and session.dbo is not None:
            dbo = session.dbo
            web.header("Content-Type", "text/javascript")
            web.header("Cache-Control", "max-age=86400")
            realname = ""
            emailaddress = ""
            expirydate = ""
            expirydatedisplay = ""
            if smcom.active():
                expirydate = smcom.get_expiry_date(dbo)
                if expirydate is not None: 
                    expirydatedisplay = python2display(session.locale, expirydate)
                    expirydate = expirydate.isoformat()
            us = users.get_users(dbo, session.user)
            if len(us) > 0:
                emailaddress = utils.nulltostr(us[0]["EMAILADDRESS"])
                realname = utils.nulltostr(us[0]["REALNAME"])
            geoprovider = GEO_PROVIDER
            geoprovidero = configuration.geo_provider_override(dbo)
            if geoprovidero != "": geoprovider = geoprovidero
            geoproviderkey = GEO_PROVIDER_KEY
            geoproviderkeyo = configuration.geo_provider_key_override(dbo)
            if geoproviderkeyo != "": geoproviderkey = geoproviderkeyo
            mapprovider = MAP_PROVIDER
            mapprovidero = configuration.map_provider_override(dbo)
            if mapprovidero != "": mapprovider = mapprovidero
            maplink = MAP_LINK
            maplinko = configuration.map_link_override(dbo)
            if maplinko != "": maplinko = maplink
            s = "asm={baseurl:'%s'," % BASE_URL
            s += "locale:'%s'," % session.locale
            s += "theme:'%s'," % session.theme
            s += "user:'%s'," % session.user.replace("'", "\\'")
            s += "useremail:'%s'," % emailaddress
            s += "userreal:'%s'," % realname.replace("'", "\\'")
            s += "useraccount:'%s'," % dbo.database
            s += "useraccountalias: '%s'," % dbo.alias
            s += "dateformat:'%s'," % get_display_date_format(session.locale)
            s += "currencysymbol:'%s'," % get_currency_symbol(session.locale)
            s += "currencydp:%d," % get_currency_dp(session.locale)
            s += "currencyprefix:'%s'," % get_currency_prefix(session.locale)
            s += "securitymap:'%s'," % session.securitymap
            s += "superuser:%s," % (session.superuser and "true" or "false")
            s += "locationfilter:'%s'," % session.locationfilter
            s += "roles:'%s'," % (session.roles.replace("'", "\\'"))
            s += "roleids:'%s'," % (session.roleids)
            s += "smcom:%s," % (smcom.active() and "true" or "false")
            s += "smcomexpiry:'%s'," % expirydate
            s += "smcomexpirydisplay:'%s'," % expirydatedisplay
            s += "smcompaymentlink:'%s'," % (SMCOM_PAYMENT_LINK.replace("{alias}", dbo.alias).replace("{database}", dbo.database))
            s += "geoprovider:'%s'," % (geoprovider)
            s += "geoproviderkey:'%s'," % (geoproviderkey)
            s += "leafletcss:'%s'," % (LEAFLET_CSS)
            s += "leafletjs:'%s'," % (LEAFLET_JS)
            s += "maplink:'%s'," % (maplink)
            s += "mapprovider:'%s'," % (mapprovider)
            s += "osmmaptiles:'%s'," % (OSM_MAP_TILES)
            s += "hascustomlogo:%s," % (dbfs.file_exists(dbo, "logo.jpg") and "true" or "false")
            s += "config:" + html.json([configuration.get_map(dbo),]) + ", "
            s += "menustructure:" + html.json_menu(session.locale, 
                extreports.get_reports_menu(dbo, session.roleids, session.superuser), 
                extreports.get_mailmerges_menu(dbo, session.roleids, session.superuser))
            s += "};"
            return s
        else:
            # Not logged in
            web.header("Content-Type", "text/javascript")
            web.header("Cache-Control", "no-cache")
            return ""

class css:
    def GET(self):
        post = utils.PostedData(web.input(v = "", k = ""), LOCALE) # k is ignored here, but versions css within browser cache
        v = post["v"]
        csspath = PATH + "static/css/" + v
        if v.find("..") != -1: raise web.notfound() # prevent escaping our PATH
        if not os.path.exists(csspath): raise web.notfound()
        if v == "": raise web.notfound()
        f = open(csspath, "r")
        content = f.read()
        f.close()
        web.header("Content-Type", "text/css")
        web.header("Cache-Control", "max-age=8640000") # Don't refresh this version for 100 days
        return content

class i18njs:
    def GET(self):
        post = utils.PostedData(web.input(l = LOCALE, k = ""), LOCALE) # k is ignored here, but versions locale within cache
        l = post["l"]
        web.header("Content-Type", "text/javascript")
        web.header("Cache-Control", "max-age=8640000")
        return i18nstringsjs(l)

class js:
    def GET(self):
        post = utils.PostedData(web.input(v = "", k = ""), LOCALE) # k is ignored here, but versions js within browser cache
        v = post["v"]
        jspath = PATH + "static/js/" + v
        if v.find("..") != -1: raise web.notfound() # prevent escaping our PATH
        if not os.path.exists(jspath): raise web.notfound()
        if v == "": raise web.notfound()
        f = open(jspath, "r")
        content = f.read()
        f.close()
        web.header("Content-Type", "text/javascript")
        web.header("Cache-Control", "max-age=8640000") # Don't refresh this version for 100 days
        return content

class media:
    def GET(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(id = "0"), LOCALE)
        lastmod, medianame, mimetype, filedata = extmedia.get_media_file_data(session.dbo, post.integer("id"))
        web.header("Content-Type", mimetype)
        web.header("Cache-Control", "max-age=86400")
        web.header("Content-Disposition", "inline; filename=\"%s\"" % medianame)
        return filedata

class mobile:
    def GET(self):
        utils.check_loggedin(session, web, "/mobile_login")
        web.header("Content-Type", "text/html")
        return extmobile.page(session.dbo, session, session.user)

class mobile_login:
    def GET(self):
        l = LOCALE
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            l = configuration.locale(dbo)
        web.header("Content-Type", "text/html")
        return extmobile.page_login(l)

    def POST(self):
        post = utils.PostedData(web.input( database="", username="", password="" ), LOCALE)
        raise web.seeother( extmobile.login(post, session, remote_ip(), PATH) )

class mobile_logout:
    def GET(self):
        users.logout(session.dbo, session.user)
        session.user = None
        raise web.seeother("mobile_login")

class mobile_post:
    def handle(self):
        utils.check_loggedin(session, web, "/mobile_login")
        post = utils.PostedData(web.input(posttype = "", id = "0", animalid = "0", medicalid = "0", logtypeid = "0", logtext = "", filechooser = {}, success = ""), session.locale)
        s = extmobile.handler(session.dbo, session.user, session.locationfilter, post)
        if s is None:
            raise utils.ASMValidationError("mobile handler failed.")
        elif s.startswith("GO "):
            raise web.seeother(s[3:])
        else:
            web.header("Content-Type", "text/html")
            return s
    def GET(self):
        return self.handle()
    def POST(self):
        return self.handle()

class mobile_report:
    def GET(self):
        utils.check_loggedin(session, web, "/mobile_login")
        post = utils.PostedData(web.input(id = "0"), session.locale)
        crid = post.integer("id")
        web.header("Content-Type", "text/html")
        return extmobile.report(session.dbo, crid, session.user)

class main:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Animal Shelter Manager", l)
        title += " - " + configuration.organisation(dbo)
        # Do we need to request a password change?
        if session.passchange:
            raise web.seeother("/change_password?suggest=1")
        s = html.header(title, session, "main.js")
        # Database update checks
        dbmessage = ""
        if dbupdate.check_for_updates(dbo):
            newversion = dbupdate.perform_updates(dbo)
            if newversion != "":
                dbmessage = _("Updated database to version {0}", l).format(str(newversion))
                session.configuration = configuration.get_map(dbo)
        if dbupdate.check_for_view_seq_changes(dbo):
            dbupdate.install_db_views(dbo)
            dbupdate.install_db_sequences(dbo)
            dbupdate.install_db_stored_procedures(dbo)
        # News
        news = dbfs.get_asm_news(dbo)
        # Welcome dialog
        showwelcome = False
        if configuration.show_first_time_screen(dbo) and session.superuser == 1:
            showwelcome = True
        # Messages
        mess = extlookups.get_messages(dbo, session.user, session.roles, session.superuser)
        # Animal links
        linkmode = configuration.main_screen_animal_link_mode(dbo)
        linkmax = configuration.main_screen_animal_link_max(dbo)
        animallinks = []
        linkname = ""
        if linkmode == "recentlychanged":
            linkname = _("Recently Changed", l)
            animallinks = extanimal.get_links_recently_changed(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyentered":
            linkname = _("Recently Entered Shelter", l)
            animallinks = extanimal.get_links_recently_entered(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyadopted":
            linkname = _("Recently Adopted", l)
            animallinks = extanimal.get_links_recently_adopted(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyfostered":
            linkname = _("Recently Fostered", l)
            animallinks = extanimal.get_links_recently_fostered(dbo, linkmax, session.locationfilter)
        elif linkmode == "longestonshelter":
            linkname = _("Longest On Shelter", l)
            animallinks = extanimal.get_links_longest_on_shelter(dbo, linkmax, session.locationfilter)
        elif linkmode == "adoptable":
            linkname = _("Up for adoption", l)
            pc = extpublish.PublishCriteria(configuration.publisher_presets(dbo))
            pc.limit = linkmax
            animallinks = extpublish.get_animal_data(dbo, pc)
        # Users and roles, active users
        usersandroles = users.get_users_and_roles(dbo)
        activeusers = users.get_activeusers(dbo)
        # Alerts
        alerts = extanimal.get_alerts(dbo, session.locationfilter)
        if len(alerts) > 0: 
            alerts[0]["LOOKFOR"] = configuration.lookingfor_last_match_count(dbo)
            alerts[0]["PUBLISH"] = dbfs.get_publish_alerts(dbo)
        # Diary Notes
        dm = None
        if configuration.all_diary_home_page(dbo): 
            dm = extdiary.get_uncompleted_upto_today(dbo)
        else:
            dm = extdiary.get_uncompleted_upto_today(dbo, session.user)
        # Create controller
        c = html.controller_bool("showwelcome", showwelcome)
        c += html.controller_str("news", news)
        c += html.controller_str("dbmessage", dbmessage)
        c += html.controller_str("version", get_version())
        c += html.controller_str("emergencynotice", emergency_notice())
        c += html.controller_str("linkname", linkname)
        c += html.controller_json("usersandroles", usersandroles)
        c += html.controller_json("alerts", alerts)
        c += html.controller_json("stats", extanimal.get_stats(dbo))
        c += html.controller_json("activeusers", activeusers)
        c += html.controller_json("animallinks", extanimal.get_animals_brief(animallinks))
        c += html.controller_json("diary", dm)
        c += html.controller_json("mess", mess)
        s += html.controller(c)
        s += html.footer()
        al.debug("main for '%s', %d diary notes, %d messages" % (session.user, len(dm), len(mess)), "code.main", dbo)
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input( mode = "", id = 0 ), session.locale)
        dbo = session.dbo
        mode = post["mode"]
        if mode == "addmessage":
            extlookups.add_message(dbo, session.user, post.boolean("email"), post["message"], post["forname"], post.integer("priority"), post.date("expires"))
        elif mode == "delmessage":
            extlookups.delete_message(dbo, post.integer("id"))
        elif mode == "showfirsttimescreen":
            configuration.show_first_time_screen(dbo, True, False)

class login:
    def GET(self):
        l = LOCALE
        has_animals = True
        custom_splash = False
        post = utils.PostedData(web.input(smaccount = "", username = "", password = "", target = "", nologconnection = ""), l)
        # Figure out how to get the default locale and any overridden splash screen
        # Single database
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            l = configuration.locale(dbo)
            has_animals = extanimal.get_has_animals(dbo)
            custom_splash = dbfs.file_exists(dbo, "splash.jpg")
        # Multiple databases, no account given
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "map" and post["smaccount"] == "":
            try:
                dbo = db.DatabaseInfo()
                l = configuration.locale(dbo)
            except:
                l = LOCALE
                pass
        # Multiple databases, account given
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "map" and post["smaccount"] != "":
            dbo = db.get_multiple_database_info(post["smaccount"])
            if dbo.database != "FAIL" and dbo.database != "DISABLED":
                custom_splash = dbfs.file_exists(dbo, "splash.jpg")
                l = configuration.locale(dbo)
        # Sheltermanager.com
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "smcom" and post["smaccount"] != "":
            dbo = smcom.get_database_info(post["smaccount"])
            if dbo.database != "FAIL" and dbo.database != "DISABLED":
                custom_splash = dbfs.file_exists(dbo, "splash.jpg")
                l = configuration.locale(dbo)
        title = _("Animal Shelter Manager Login", l)
        s = html.bare_header(title, "login.js", locale = l)
        c = html.controller_bool("smcom", smcom.active())
        c += html.controller_bool("multipledatabases", MULTIPLE_DATABASES)
        c += html.controller_str("locale", l)
        c += html.controller_bool("hasanimals", has_animals)
        c += html.controller_bool("customsplash", custom_splash)
        c += html.controller_str("forgottenpassword", FORGOTTEN_PASSWORD)
        c += html.controller_str("forgottenpasswordlabel", FORGOTTEN_PASSWORD_LABEL)
        c += html.controller_str("emergencynotice", emergency_notice())
        c += html.controller_str("smaccount", post["smaccount"])
        c += html.controller_str("husername", post["username"])
        c += html.controller_str("hpassword", post["password"]) 
        c += html.controller_str("nologconnection", post["nologconnection"])
        c += html.controller_str("target", post["target"])
        s += html.controller(c)
        s += "<noscript>" + _("Sorry. ASM will not work without Javascript.", l) + "</noscript>\n"
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        post = utils.PostedData(web.input( database = "", username = "", password = "", nologconnection = "" ), LOCALE)
        return users.web_login(post, session, remote_ip(), PATH)

class login_splash:
    def GET(self):
        post = utils.PostedData(web.input(smaccount = ""), LOCALE)
        try:
            dbo = db.DatabaseInfo()
            if MULTIPLE_DATABASES:
                if post["smaccount"] != "":
                    if MULTIPLE_DATABASES_TYPE == "smcom":
                        dbo = smcom.get_database_info(post["smaccount"])
                    else:
                        dbo = db.get_multiple_database_info(post["smaccount"])
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "max-age=86400")
            return dbfs.get_string_filepath(dbo, "/reports/splash.jpg")
        except Exception,err:
            al.error("%s" % str(err), "code.login_splash", session.dbo)
            return ""

class logout:
    def GET(self):
        url = "login"
        if MULTIPLE_DATABASES and session.dbo is not None and session.dbo.alias != None:
            url = "login?smaccount=" + session.dbo.alias
        users.logout(session.dbo, session.user)
        session.user = None
        session.kill()
        raise web.seeother(url)

class accounts:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ACCOUNT)
        l = session.locale
        dbo = session.dbo
        accounts = financial.get_accounts(dbo)
        al.debug("got %d accounts" % len(accounts), "code.accounts", dbo)
        title = _("Accounts", l)
        s = html.header(title, session, "accounts.js")
        c = html.controller_json("accounttypes", extlookups.get_account_types(dbo))
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("roles", users.get_roles(dbo))
        c += html.controller_json("rows", accounts)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post.string("mode")
        if mode == "create":
            users.check_permission(session, users.ADD_ACCOUNT)
            return financial.insert_account_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_ACCOUNT)
            financial.update_account_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_ACCOUNT)
            for aid in post.integer_list("ids"):
                financial.delete_account(session.dbo, session.user, aid)

class accounts_trx:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ACCOUNT)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(accountid = 0, fromdate = "", todate = "", recfilter = 0), l)
        defview = configuration.default_account_view_period(dbo)
        fromdate = post["fromdate"]
        todate = post["todate"]
        if fromdate != "" and todate != "":
            fromdate = post.date("fromdate")
            todate = post.date("todate")
        elif defview == financial.THIS_MONTH:
            fromdate = first_of_month(now())
            todate = last_of_month(now())
        elif defview == financial.THIS_WEEK:
            fromdate = monday_of_week(now())
            todate = sunday_of_week(now())
        elif defview == financial.THIS_YEAR:
            fromdate = first_of_year(now())
            todate = last_of_year(now())
        elif defview == financial.LAST_MONTH:
            fromdate = first_of_month(subtract_months(now(), 1))
            todate = last_of_month(subtract_months(now(), 1))
        elif defview == financial.LAST_WEEK:
            fromdate = monday_of_week(subtract_days(now(), 7))
            todate = sunday_of_week(subtract_days(now(), 7))
        transactions = financial.get_transactions(dbo, post.integer("accountid"), fromdate, todate, post.integer("recfilter"))
        accountcode = financial.get_account_code(dbo, post.integer("accountid"))
        accounteditroles = financial.get_account_edit_roles(dbo, post.integer("accountid"))
        title = accountcode
        al.debug("got %d trx for %s <-> %s" % (len(transactions), str(fromdate), str(todate)), "code.accounts_trx", dbo)
        s = html.header(title, session, "accounts_trx.js")
        c = html.controller_json("rows", transactions)
        c += html.controller_json("codes", "|".join(financial.get_account_codes(dbo, accountcode)))
        c += html.controller_int("accountid", post.integer("accountid"))
        c += html.controller_str("accountcode", accountcode);
        c += html.controller_str("accounteditroles", "|".join(accounteditroles));
        c += html.controller_str("fromdate", python2display(l, fromdate))
        c += html.controller_str("todate", python2display(l, todate))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            financial.insert_trx_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            financial.update_trx_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            for tid in post.integer_list("ids"):
                financial.delete_trx(session.dbo, session.user, tid)
        elif mode == "reconcile":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            for tid in post.integer_list("ids"):
                financial.mark_reconciled(session.dbo, tid)

class additional:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MODIFY_LOOKUPS)
        l = session.locale
        dbo = session.dbo
        fields = extadditional.get_fields(dbo)
        title = _("Additional Fields", l)
        al.debug("got %d additional field definitions" % len(fields), "code.additional", dbo)
        s = html.header(title, session, "additional.js")
        c = html.controller_json("rows", fields)
        c += html.controller_json("fieldtypes", extlookups.get_additionalfield_types(dbo))
        c += html.controller_json("linktypes", extlookups.get_additionalfield_links(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extadditional.insert_field_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extadditional.update_field_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            for fid in post.integer_list("ids"):
                extadditional.delete_field(session.dbo, session.user, fid)

class animal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        l = dbo.locale
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        # If a location filter is set, prevent the user opening this animal if it's
        # not in their location.
        if session.locationfilter != "":
            if str(a["SHELTERLOCATION"]) not in session.locationfilter.split(","):
                raise utils.ASMPermissionError("animal not in location filter")
        al.debug("opened animal %s %s" % (a["CODE"], a["ANIMALNAME"]), "code.animal", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "animal.js")
        c = html.controller_json("animal", a)
        c += html.controller_plain("activelitters", html.json_autocomplete_litters(dbo))
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "animal"))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("coattypes", extlookups.get_coattypes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        c += html.controller_json("diarytasks", extdiary.get_animal_tasks(dbo))
        c += html.controller_json("entryreasons", extlookups.get_entryreasons(dbo))
        c += html.controller_str("facebookclientid", FACEBOOK_CLIENT_ID)
        c += html.controller_bool("hasfacebook", FACEBOOK_CLIENT_ID != "")
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("pickuplocations", extlookups.get_pickup_locations(dbo))
        c += html.controller_json("posneg", extlookups.get_posneg(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("ynun", extlookups.get_ynun(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_animal_from_form(dbo, post, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_ANIMAL)
            extanimal.delete_animal(dbo, session.user, post.integer("animalid"))
        elif mode == "gencode":
            animaltypeid = post.integer("animaltypeid")
            entryreasonid = post.integer("entryreasonid")
            speciesid = post.integer("speciesid")
            datebroughtin = post.date("datebroughtin")
            sheltercode, shortcode, unique, year = extanimal.calc_shelter_code(dbo, animaltypeid, entryreasonid, speciesid, datebroughtin)
            return sheltercode + "||" + shortcode + "||" + str(unique) + "||" + str(year)
        elif mode == "randomname":
            return extanimal.get_random_name(dbo, post.integer("sex"))
        elif mode == "clone":
            users.check_permission(session, users.CLONE_ANIMAL)
            utils.check_locked_db(session)
            nid = extanimal.clone_animal(dbo, session.user, post.integer("animalid"))
            return str(nid)
        elif mode == "webnotes":
            users.check_permission(session, users.CHANGE_MEDIA)
            extanimal.update_preferred_web_media_notes(dbo, session.user, post.integer("id"), post["comments"])

class animal_bulk:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Bulk change animals", l)
        s = html.header(title, session, "animal_bulk.js")
        c = html.controller_json("ynun", extlookups.get_ynun(dbo))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_plain("autolitters", html.json_autocomplete_litters(dbo))
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        return extanimal.update_animals_from_form(dbo, post, session.user)

class animal_costs:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_COST)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        cost = extanimal.get_costs(dbo, post.integer("id"))
        costtypes = extlookups.get_costtypes(dbo)
        costtotals = extanimal.get_cost_totals(dbo, post.integer("id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d costs for animal %s %s" % (len(cost), a["CODE"], a["ANIMALNAME"]), "code.animal_costs", dbo)
        s = html.header(title, session, "animal_costs.js")
        c = html.controller_json("rows", cost)
        c += html.controller_json("animal", a)
        c += html.controller_json("costtypes", costtypes)
        c += html.controller_json("costtotals", costtotals)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        username = session.user
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_COST)
            return extanimal.insert_cost_from_form(dbo, username, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_COST)
            extanimal.update_cost_from_form(dbo, username, post)
        elif mode == "dailyboardingcost":
            users.check_permission(session, users.CHANGE_ANIMAL)
            animalid = post.integer("animalid")
            cost = post.integer("dailyboardingcost")
            extanimal.update_daily_boarding_cost(dbo, username, animalid, cost)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_COST)
            for cid in post.integer_list("ids"):
                extanimal.delete_cost(session.dbo, session.user, cid)

class animal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        diaries = extdiary.get_diaries(dbo, extdiary.ANIMAL, post.integer("id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d notes for animal %s %s" % (len(diaries), a["CODE"], a["ANIMALNAME"]), "code.animal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_str("name", "animal_diary")
        c += html.controller_int("linkid", a["ID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.ANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class animal_diet:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIET)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        diet = extanimal.get_diets(dbo, post.integer("id"))
        diettypes = extlookups.get_diets(dbo)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d diets for animal %s %s" % (len(diet), a["CODE"], a["ANIMALNAME"]), "code.animal_diet", dbo)
        s = html.header(title, session, "animal_diet.js")
        c = html.controller_json("rows", diet)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("diettypes", diettypes)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIET)
            return str(extanimal.insert_diet_from_form(session.dbo, session.user, post))
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DIET)
            extanimal.update_diet_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIET)
            for did in post.integer_list("ids"):
                extanimal.delete_diet(session.dbo, session.user, did)

class animal_donations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        donations = financial.get_animal_donations(dbo, post.integer("id"))
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d donations for animal %s %s" % (len(donations), a["CODE"], a["ANIMALNAME"]), "code.animal_donations", dbo)
        s = html.header(title, session, "donations.js")
        c = html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_str("name", "animal_donations")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        dbo = session.dbo
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in post.integer_list("ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in post.integer_list("ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            web.header("Content-Type", "application/json")
            return html.json(extmovement.get_person_movements(dbo, post.integer("personid")))

class animal_embed:
    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode = "find"), session.locale)
        web.header("Content-Type", "application/json")
        mode = post["mode"]
        if mode == "find":
            q = post["q"]
            rows = extanimal.get_animal_find_simple(dbo, q, post["filter"], 100, False, session.locationfilter)
            al.debug("got %d results for '%s'" % (len(rows), str(web.ctx.query)), "code.animal_embed", dbo)
            return html.json(rows)
        elif mode == "multiselect":
            rows = extanimal.get_animal_find_simple(dbo, "", "all", 1000, False, session.locationfilter)
            locations = extlookups.get_internal_locations(dbo)
            species = extlookups.get_species(dbo)
            rv = { "rows": rows, "locations": locations, "species": species }
            return html.json(rv)
        elif mode == "id":
            a = extanimal.get_animal(dbo, post.integer("id"))
            if a is None:
                al.error("get animal by id %d found no records." % (post.integer("id")), "code.animal_embed", dbo)
                raise web.notfound()
            else:
                al.debug("got animal %s %s by id" % (a["CODE"], a["ANIMALNAME"]), "code.animal_embed", dbo)
                return html.json((a,))

class animal_facebook:
    def GET(self):
        """
        This controller is redirected to from Facebook. 
        The link to Facebook is done in animal.js when the Facebook button is pressed.
        
        Facebook include code and state query parameters when redirecting to this controller.
        
        code: a token that we can use in our server side HTTP request to Facebook to get a 
              real access_token from them for the logged in user.
        state: we passed this in the original link to Facebook and it's the 
               ID of the animal we would like to post.
        """
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        post = utils.PostedData(web.input(code = "", state = ""), session.locale)
        oauth_code = post["code"]
        oauth_state = post["state"]
        if post["error_reason"] != "":
            raise utils.ASMValidationError(post["error_description"])
        # Post the requested animal to facebook
        social.post_animal_facebook(session.dbo, session.user, oauth_code, oauth_state)
        # Redirect back to the animal record and tell the user it worked
        raise web.seeother("animal?facebook=true&id=" + oauth_state[1:])

class animal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Animal", l)
        s = html.header(title, session, "animal_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        s += html.controller(c)
        al.debug("loaded lookups for find animal", "code.animal_find", dbo)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class animal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(q = "", mode = ""), session.locale)
        q = post["q"]
        mode = post["mode"]
        if mode == "SIMPLE":
            results = extanimal.get_animal_find_simple(dbo, q, "all", configuration.record_search_limit(dbo), False, session.locationfilter)
        else:
            results = extanimal.get_animal_find_advanced(dbo, post.data, configuration.record_search_limit(dbo), session.locationfilter)
        add = None
        if len(results) > 0: 
            add = extadditional.get_additional_fields_ids(dbo, results, "animal")
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.animal_find_results", dbo)
        wasonshelter = False
        if q == "" and mode == "SIMPLE":
            wasonshelter = True
        s = html.header(_("Results", l), session, "animal_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("resultsmessage", _("Search returned {0} results.", l).format(len(results)))
        c += html.controller_json("additional", add)
        c += html.controller_bool("wasonshelter", wasonshelter)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class animal_licence:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LICENCE)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        licences = financial.get_animal_licences(dbo, post.integer("id"))
        al.debug("got %d licences" % len(licences), "code.animal_licence", dbo)
        s = html.header(title, session, "licence.js")
        c = html.controller_str("name", "animal_licence")
        c += html.controller_json("rows", licences)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("licencetypes", extlookups.get_licence_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LICENCE)
            return financial.insert_licence_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LICENCE)
            financial.update_licence_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LICENCE)
            for lid in post.integer_list("ids"):
                financial.delete_licence(session.dbo, session.user, lid)

class animal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        logs = extlog.get_logs(dbo, extlog.ANIMAL, post.integer("id"), logfilter)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d logs for animal %s %s" % (len(logs), a["CODE"], a["ANIMALNAME"]), "code.animal_log", dbo)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "animal_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.ANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class animal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, newmedia=0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        m = extmedia.get_media(dbo, extmedia.ANIMAL, post.integer("id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d media entries for animal %s %s" % (len(m), a["CODE"], a["ANIMALNAME"]), "code.animal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_bool("showPreferred", True)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.ANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        c += html.controller_bool("newmedia", post.integer("newmedia") == 1)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.ANIMAL, linkid, post)
            raise web.seeother("animal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.ANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=animal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.ANIMAL, linkid, post)
            raise web.seeother("animal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                if m["MEDIANAME"].endswith("html"):
                    content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], post["emailnote"], "html", content, m["MEDIANOTES"] + m["MEDIANAME"])
            return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)
        elif mode == "exclude":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.set_excluded(session.dbo, session.user, post.integer("mediaid"), post.integer("exclude"))

class animal_medical:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        med = extmedical.get_regimens_treatments(dbo, post.integer("id"))
        profiles = extmedical.get_profiles(dbo)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d medical entries for animal %s %s" % (len(med), a["CODE"], a["ANIMALNAME"]), "code.animal_medical", dbo)
        s = html.header(title, session, "medical.js")
        c = html.controller_json("profiles", profiles)
        c += html.controller_json("rows", med)
        c += html.controller_str("name", "animal_medical")
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_json("animal", a)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_regimen_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_regimen_from_form(session.dbo, session.user, post)
        elif mode == "delete_regimen":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in post.integer_list("ids"):
                extmedical.delete_regimen(session.dbo, session.user, mid)
        elif mode == "delete_treatment":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in post.integer_list("ids"):
                extmedical.delete_treatment(session.dbo, session.user, mid)
        elif mode == "get_profile":
            return html.json([extmedical.get_profile(session.dbo, post.integer("profileid"))])
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = post.date("newdate")
            for mid in post.integer_list("ids"):
                extmedical.update_treatment_given(session.dbo, session.user, mid, newdate)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = post.date("newdate")
            for mid in post.integer_list("ids"):
                extmedical.update_treatment_required(session.dbo, session.user, mid, newdate)

class animal_movements:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        movements = extmovement.get_animal_movements(dbo, post.integer("id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d movements for animal %s %s" % (len(movements), a["CODE"], a["ANIMALNAME"]), "code.animal_movements", dbo)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)
        elif mode == "insurance":
            return extmovement.generate_insurance_number(session.dbo)

class animal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Add a new animal", l)
        s = html.header(title, session, "animal_new.js")
        c = html.controller_plain("autolitters", html.json_autocomplete_litters(dbo))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("entryreasons", extlookups.get_entryreasons(dbo))
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        al.debug("loaded lookups for new animal", "code.animal_new", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_ANIMAL)
        utils.check_locked_db(session)
        post = utils.PostedData(web.input(mode = "save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            animalid, code = extanimal.insert_animal_from_form(session.dbo, post, session.user)
            return str(animalid) + " " + str(code)
        elif mode == "recentnamecheck":
            rows = extanimal.get_recent_with_name(session.dbo, post["animalname"])
            al.debug("recent names found %d rows for '%s'" % (len(rows), post["animalname"]), "code.animal_new.recentnamecheck", session.dbo)
            if len(rows) > 0:
                return "|".join((str(rows[0]["ANIMALID"]), rows[0]["SHELTERCODE"], rows[0]["ANIMALNAME"]))
        elif mode == "units":
            return "&&".join(extanimal.get_units_with_availability(session.dbo, post.integer("locationid")))

class animal_test:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TEST)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        test = extmedical.get_tests(dbo, post.integer("id"))
        al.debug("got %d tests" % len(test), "code.animal_test", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "test.js")
        c = html.controller_str("name", "animal_test")
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("rows", test)
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("testresults", extlookups.get_test_results(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "create", ids = ""), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_TEST)
            return extmedical.insert_test_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TEST)
            extmedical.update_test_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TEST)
            for vid in post.integer_list("ids"):
                extmedical.delete_test(session.dbo, session.user, vid)
        elif mode == "perform":
            users.check_permission(session, users.CHANGE_TEST)
            newdate = post.date("newdate")
            testresult = post.integer("testresult")
            for vid in post.integer_list("ids"):
                extmedical.complete_test(session.dbo, session.user, vid, newdate, testresult)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)

class animal_vaccination:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VACCINATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimal.get_animal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        vacc = extmedical.get_vaccinations(dbo, post.integer("id"))
        al.debug("got %d vaccinations" % len(vacc), "code.vaccination", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "vaccination.js")
        c = html.controller_str("name", "animal_vaccination")
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("rows", vacc)
        c += html.controller_json("manufacturers", "|".join(extmedical.get_vacc_manufacturers(dbo)))
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "create", ids = "", duration = 0), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_VACCINATION)
            return extmedical.insert_vaccination_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VACCINATION)
            extmedical.update_vaccination_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VACCINATION)
            for vid in post.integer_list("ids"):
                extmedical.delete_vaccination(session.dbo, session.user, vid)
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = post.date("newdate")
            rescheduledate = post.date("rescheduledate")
            for vid in post.integer_list("ids"):
                extmedical.complete_vaccination(session.dbo, session.user, vid, newdate)
                if rescheduledate is not None:
                    extmedical.reschedule_vaccination(session.dbo, session.user, vid, rescheduledate)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = post.date("newdate")
            for vid in post.integer_list("ids"):
                extmedical.update_vaccination_required(session.dbo, session.user, vid, newdate)

class calendarview:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        if post["start"] == "":
            title = _("Calendar view", l)
            s = html.header(title, session, "calendarview.js")
            s += html.footer()
            al.debug("calendarview load page", "code.calendarview", dbo)
            web.header("Content-Type", "text/html")
            web.header("Cache-Control", "no-cache")
            return s
        elif post["start"] != "" and post["end"] != "":
            ev = post["ev"]
            if ev == "": ev = "dvmtolp"
            events = []
            # Find data for the month
            if "d" in ev and users.check_permission_bool(session, users.VIEW_DIARY):
                user = session.user
                if configuration.all_diary_home_page(dbo):
                    user = ""
                for d in extdiary.get_between_two_dates(dbo, user, post["start"], post["end"]):
                    allday = False
                    # If the diary time is midnight, assume all day instead
                    if d["DIARYDATETIME"].hour == 0 and d["DIARYDATETIME"].minute == 0:
                        allday = True
                    events.append({ 
                        "title": d["SUBJECT"], 
                        "allDay": allday, 
                        "start": d["DIARYDATETIME"], 
                        "tooltip": "%s %s" % (d["LINKINFO"], d["NOTE"]), 
                        "icon": "diary",
                        "link": "diary_edit_my" })
            if "v" in ev and users.check_permission_bool(session, users.VIEW_VACCINATION):
                for v in extmedical.get_vaccinations_two_dates(dbo, post["start"], post["end"], session.locationfilter):
                    sub = "%s - %s" % (v["VACCINATIONTYPE"], v["ANIMALNAME"])
                    tit = "%s - %s %s %s" % (v["VACCINATIONTYPE"], v["SHELTERCODE"], v["ANIMALNAME"], v["COMMENTS"])
                    events.append({ 
                        "title": sub, 
                        "allDay": True, 
                        "start": v["DATEREQUIRED"], 
                        "tooltip": tit, 
                        "icon": "vaccination",
                        "link": "animal_vaccination?id=%d" % v["ANIMALID"] })
            if "m" in ev and users.check_permission_bool(session, users.VIEW_MEDICAL):
                for m in extmedical.get_treatments_two_dates(dbo, post["start"], post["end"], session.locationfilter):
                    sub = "%s - %s" % (m["TREATMENTNAME"], m["ANIMALNAME"])
                    tit = "%s - %s %s %s %s" % (m["TREATMENTNAME"], m["SHELTERCODE"], m["ANIMALNAME"], m["DOSAGE"], m["COMMENTS"])
                    events.append({ 
                        "title": sub, 
                        "allDay": True, 
                        "start": m["DATEREQUIRED"], 
                        "tooltip": tit, 
                        "icon": "medical",
                        "link": "animal_medical?id=%d" % m["ANIMALID"] })
            if "t" in ev and users.check_permission_bool(session, users.VIEW_TEST):
                for t in extmedical.get_tests_two_dates(dbo, post["start"], post["end"], session.locationfilter):
                    sub = "%s - %s" % (t["TESTNAME"], t["ANIMALNAME"])
                    tit = "%s - %s %s %s" % (t["TESTNAME"], t["SHELTERCODE"], t["ANIMALNAME"], t["COMMENTS"])
                    events.append({ 
                        "title": sub, 
                        "allDay": True, 
                        "start": t["DATEREQUIRED"], 
                        "tooltip": tit, 
                        "icon": "test",
                        "link": "animal_test?id=%d" % t["ANIMALID"] })
            if "p" in ev and users.check_permission_bool(session, users.VIEW_DONATION):
                for p in financial.get_donations_due_two_dates(dbo, post["start"], post["end"]):
                    sub = "%s - %s" % (p["DONATIONNAME"], p["OWNERNAME"])
                    tit = "%s - %s %s %s" % (p["DONATIONNAME"], p["OWNERNAME"], html.format_currency(l, p["DONATION"]), p["COMMENTS"])
                    events.append({ 
                        "title": sub, 
                        "allDay": True, 
                        "start": p["DATEDUE"], 
                        "tooltip": tit, 
                        "icon": "donation",
                        "link": "person_donations?id=%d" % p["OWNERID"] })
            if "o" in ev and users.check_permission_bool(session, users.VIEW_INCIDENT):
                for o in extanimalcontrol.get_followup_two_dates(dbo, post["start"], post["end"]):
                    sub = "%s - %s" % (o["INCIDENTNAME"], o["OWNERNAME"])
                    tit = "%s - %s %s, %s" % (o["INCIDENTNAME"], o["OWNERNAME"], o["DISPATCHADDRESS"], o["CALLNOTES"])
                    events.append({ 
                        "title": sub, 
                        "allDay": False, 
                        "start": o["FOLLOWUPDATETIME"], 
                        "tooltip": tit, 
                        "icon": "call",
                        "link": "incident?id=%d" % o["ACID"] })
            if "l" in ev and users.check_permission_bool(session, users.VIEW_TRAPLOAN):
                for l in extanimalcontrol.get_traploan_two_dates(dbo, post["start"], post["end"]):
                    sub = "%s - %s" % (l["TRAPTYPENAME"], l["OWNERNAME"])
                    tit = "%s - %s %s, %s" % (l["TRAPTYPENAME"], l["OWNERNAME"], l["TRAPNUMBER"], l["COMMENTS"])
                    events.append({ 
                        "title": sub, 
                        "allDay": True, 
                        "start": l["RETURNDUEDATE"], 
                        "tooltip": tit, 
                        "icon": "traploan",
                        "link": "person_traploan?id=%d" % l["OWNERID"]})
            al.debug("calendarview found %d events (%s->%s)" % (len(events), post["start"], post["end"]), "code.calendarview", dbo)
            return html.json(events)

class change_password:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        title = _("Change Password", l)
        al.debug("%s change password screen" % session.user, "code.change_password", dbo)
        s = html.header(title, session, "change_password.js")
        c = html.controller_bool("ismaster", smcom.active() and dbo.database == session.user)
        c += html.controller_bool("issuggest", post.integer("suggest") == 1)
        c += html.controller_str("username", session.user)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(oldpassword = "", newpassword = ""), session.locale)
        oldpass = post["oldpassword"]
        newpass = post["newpassword"]
        al.debug("%s changed password %s -> %s" % (session.user, oldpass, newpass), "code.change_password", dbo)
        users.change_password(dbo, session.user, oldpass, newpass)

class change_user_settings:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Change User Settings", l)
        al.debug("%s change user settings screen" % session.user, "code.change_user_settings", dbo)
        s = html.header(title, session, "change_user_settings.js")
        c = html.controller_json("user", users.get_users(dbo, session.user))
        c += html.controller_json("locales", extlookups.LOCALES)
        c += html.controller_json("themes", extlookups.VISUAL_THEMES)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(theme = "", locale = "", realname = "", email = ""), session.locale)
        theme = post["theme"]
        locale = post["locale"]
        realname = post["realname"]
        email = post["email"]
        al.debug("%s changed settings: theme=%s, locale=%s, realname=%s, email=%s" % (session.user, theme, locale, realname, email), "code.change_password", dbo)
        users.update_user_settings(dbo, session.user, email, realname, locale, theme)
        users.update_session(session)

class citations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_CITATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(filter = "unpaid"), session.locale)
        title = ""
        citations = []
        if post["filter"] == "unpaid":
            title = _("Unpaid Fines", l)
            citations = financial.get_unpaid_fines(dbo)
        al.debug("got %d citations" % len(citations), "code.citations", dbo)
        s = html.header(title, session, "citations.js")
        c = html.controller_str("name", "citations")
        c += html.controller_str("title", title)
        c += html.controller_json("rows", citations)
        c += html.controller_json("citationtypes", extlookups.get_citation_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_CITATION)
            return financial.insert_citation_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_CITATION)
            financial.update_citation_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_CITATION)
            for lid in post.integer_list("ids"):
                financial.delete_citation(session.dbo, session.user, lid)

class csvimport:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_SQL_INTERFACE)
        l = session.locale
        title = _("Import a CSV file", l)
        s = html.header(title, session, "csvimport.js")
        s += html.controller("")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        utils.check_locked_db(session)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(createmissinglookups = "", cleartables = "", filechooser={}), session.locale)
        users.check_permission(session, users.USE_SQL_INTERFACE)
        web.header("Content-Type", "text/html")
        try:
            errors = extcsvimport.csvimport(dbo, post.filedata(), post.boolean("createmissinglookups") == 1, post.boolean("cleartables") == 1)
            title = _("Import a CSV file", l)
            s = html.header(title, session, "csvimport.js")
            c = html.controller_json("errors", errors)
            s += html.controller(c)
            s += html.footer()
            return s
        except Exception,err:
            al.error("error in CSV data: %s" % str(err), "csvimport.csvimport", dbo, sys.exc_info())
            if str(err).find("no attribute 'value'") != -1:
                err = "No CSV file was uploaded"
            title = _("Import a CSV file", l)
            s = html.header(title, session, "csvimport.js")
            c = html.controller_str("error", str(err))
            s += html.controller(c)
            s += html.footer()
            return s

class diary_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter="uncompleted", newnote="0"), session.locale)
        dfilter = post["filter"]
        if dfilter == "uncompleted":
            diaries = extdiary.get_uncompleted_upto_today(dbo)
        elif dfilter == "completed":
            diaries = extdiary.get_completed_upto_today(dbo)
        elif dfilter == "future":
            diaries = extdiary.get_future(dbo)
        elif dfilter == "all":
            diaries = extdiary.get_all_upto_today(dbo)
        title = _("Edit diary notes", l)
        al.debug("got %d diaries, filter was %s" % (len(diaries), dfilter), "code.diary_edit", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_bool("newnote", post.integer("newnote") == 1)
        c += html.controller_str("name", "diary_edit")
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.NO_LINK, 0, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class diary_edit_my:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_MY_DIARY_NOTES)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter="uncompleted", newnote="0"), session.locale)
        userfilter = session.user.strip()
        dfilter = post["filter"]
        if dfilter == "uncompleted":
            diaries = extdiary.get_uncompleted_upto_today(dbo, userfilter)
        elif dfilter == "completed":
            diaries = extdiary.get_completed_upto_today(dbo, userfilter)
        elif dfilter == "future":
            diaries = extdiary.get_future(dbo, userfilter)
        elif dfilter == "all":
            diaries = extdiary.get_all_upto_today(dbo, userfilter)
        title = _("Edit my diary notes", l)
        al.debug("got %d diaries (%s), filter was %s" % (len(diaries), userfilter, dfilter), "code.diary_edit_my", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_bool("newnote", post.integer("newnote") == 1)
        c += html.controller_str("name", "diary_edit_my")
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.NO_LINK, 0, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class diarytask:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_DIARY_TASKS)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(taskid = 0), session.locale)
        taskid = post.integer("taskid")
        taskname = extdiary.get_diarytask_name(dbo, taskid)
        diarytaskdetail = extdiary.get_diarytask_details(dbo, taskid)
        title = _("Diary task: {0}", l).format(taskname)
        al.debug("got %d diary task details" % len(diarytaskdetail), "code.diarytask", dbo)
        s = html.header(title, session, "diarytask.js")
        c = html.controller_json("rows", diarytaskdetail)
        c += html.controller_int("taskid", taskid)
        c += html.controller_str("taskname", taskname)
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create", tasktype="ANIMAL", taskid="0", id="0", seldate=""), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            return extdiary.insert_diarytaskdetail_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            extdiary.update_diarytaskdetail_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            for did in post.integer_list("ids"):
                extdiary.delete_diarytaskdetail(session.dbo, session.user, did)
        elif mode == "exec":
            users.check_permission(session, users.ADD_DIARY)
            extdiary.execute_diary_task(dbo, session.user, post["tasktype"], post.integer("taskid"), post.integer("id"), post.date("seldate"))

class diarytasks:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_DIARY_TASKS)
        l = session.locale
        dbo = session.dbo
        diarytaskhead = extdiary.get_diarytasks(dbo)
        title = _("Diary Tasks", l)
        al.debug("got %d diary tasks" % len(diarytaskhead), "code.diarytasks", dbo)
        s = html.header(title, session, "diarytasks.js")
        c = html.controller_json("rows", diarytaskhead)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            return extdiary.insert_diarytaskhead_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            extdiary.update_diarytaskhead_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            for did in post.integer_list("ids"):
                extdiary.delete_diarytask(session.dbo, session.user, did)

class document_gen:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.GENERATE_DOCUMENTS)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode = "ANIMAL", id = 0, template = 0), session.locale)
        mode = post["mode"]
        template = post.integer("template")
        templatename = dbfs.get_name_for_id(dbo, template)
        title = templatename
        loglinktype = extlog.ANIMAL
        al.debug("generating %s document for %d" % (mode, post.integer("id")), "code.document_gen", dbo)
        logid = post.integer("id")
        if mode == "ANIMAL":
            loglinktype = extlog.ANIMAL
            content = wordprocessor.generate_animal_doc(dbo, template, post.integer("id"), session.user)
        elif mode == "PERSON":
            loglinktype = extlog.PERSON
            content = wordprocessor.generate_person_doc(dbo, template, post.integer("id"), session.user)
        elif mode == "DONATION":
            loglinktype = extlog.PERSON
            logid = financial.get_donation(dbo, post.integer("id"))["OWNERID"]
            content = wordprocessor.generate_donation_doc(dbo, template, post.integer("id"), session.user)
        if configuration.generate_document_log(dbo) and configuration.generate_document_log_type(dbo) > 0:
            extlog.add_log(dbo, session.user, loglinktype, logid, configuration.generate_document_log_type(dbo), _("Generated document '{0}'").format(templatename))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return html.tinymce_header(title, "document_edit.js", configuration.js_window_print(dbo), False) + \
            html.tinymce_main(dbo.locale, "document_gen", recid=post["id"], mode=post["mode"], \
                template=post["template"], content=utils.escape_tinymce(content))

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.GENERATE_DOCUMENTS)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(recid = 0, mode = "ANIMAL", template = 0, document = "", savemode="save"), session.locale)
        mode = post["mode"]
        template = post.integer("template")
        tempname = dbfs.get_name_for_id(dbo, template)
        if post["savemode"] == "save":
            recid = post.integer("recid")
            if mode == "ANIMAL":
                tempname += " - " + extanimal.get_animal_namecode(dbo, recid)
                extmedia.create_document_media(dbo, session.user, extmedia.ANIMAL, recid, tempname, post["document"])
                raise web.seeother("animal_media?id=%d" % recid)
            elif mode == "PERSON":
                tempname += " - " + extperson.get_person_name(dbo, recid)
                extmedia.create_document_media(dbo, session.user, extmedia.PERSON, recid, tempname, post["document"])
                raise web.seeother("person_media?id=%d" % recid)
            elif mode == "DONATION":
                d = financial.get_donation(dbo, recid)
                tempname += " - " + extperson.get_person_name(dbo, d["OWNERID"])
                extmedia.create_document_media(dbo, session.user, extmedia.PERSON, d["OWNERID"], tempname, post["document"])
                raise web.seeother("person_media?id=%d" % d["OWNERID"])
            else:
                raise web.seeother("main")
        elif post["savemode"] == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(post["document"], BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
        elif post["savemode"] == "print":
            web.header("Content-Type", "text/html")
            return "%s%s%s" % (html.tinymce_print_header(_("Print Preview", l)), post["document"], "</body></html>")

class document_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(template = 0), session.locale)
        template = post.integer("template")
        templatename = dbfs.get_name_for_id(dbo, template)
        if templatename == "": raise web.notfound()
        title = templatename
        al.debug("editing %s" % templatename, "code.document_edit", dbo)
        content = utils.escape_tinymce(dbfs.get_string_id(dbo, template))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return html.tinymce_header(title, "document_edit.js", configuration.js_window_print(dbo)) + html.tinymce_main(dbo.locale, "document_edit", template=template, content=content)

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(template = "", document = "", savemode = "save"), session.locale)
        if post["savemode"] == "save":
            dbfs.put_string_id(dbo, post.integer("template"), post["document"])
            raise web.seeother("document_templates")
        elif post["savemode"] == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(post["document"], BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
        elif post["savemode"] == "print":
            web.header("Content-Type", "text/html")
            return "%s%s%s" % (html.tinymce_print_header(_("Print Preview", l)), post["document"], "</body></html>")

class document_media_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, redirecturl = "/main"), session.locale)
        lastmod, medianame, mimetype, filedata = extmedia.get_media_file_data(session.dbo, post.integer("id"))
        al.debug("editing media %d" % post.integer("id"), "code.document_media_edit", dbo)
        title = medianame
        web.header("Content-Type", "text/html")
        return html.tinymce_header(title, "document_edit.js", configuration.js_window_print(dbo)) + \
            html.tinymce_main(dbo.locale, "document_media_edit", mediaid=post.integer("id"), redirecturl=post["redirecturl"], \
                content=utils.escape_tinymce(filedata))

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_MEDIA)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mediaid = 0, redirecturl = "main", document = "", savemode = "save"), session.locale)
        if post["savemode"] == "save":
            extmedia.update_file_content(dbo, session.user, post.integer("mediaid"), post["document"])
            raise web.seeother(post["redirecturl"])
        elif post["savemode"] == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(post["document"], BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
        elif post["savemode"] == "print":
            web.header("Content-Type", "text/html")
            return "%s%s%s" % (html.tinymce_print_header(_("Print Preview", l)), post["document"], "</body></html>")

class document_repository:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPO_DOCUMENT)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(dbfsid = 0), session.locale)
        if post.integer("dbfsid") != 0:
            name = dbfs.get_name_for_id(dbo, post.integer("dbfsid"))
            mimetype, encoding = mimetypes.guess_type("file://" + name, strict=False)
            web.header("Content-Type", mimetype)
            web.header("Content-Disposition", "attachment; filename=\"%s\"" % name)
            return dbfs.get_string_id(dbo, post.integer("dbfsid"))
        else:
            title = _("Document Repository", l)
            documents = dbfs.get_document_repository(dbo)
            al.debug("got %d documents in repository" % len(documents), "code.document_repository", dbo)
            s = html.header(title, session, "document_repository.js")
            c = html.controller_json("rows", documents)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            web.header("Cache-Control", "no-cache")
            return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create", filechooser={}), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_REPO_DOCUMENT)
            dbfs.upload_document_repository(dbo, post["path"], post.data.filechooser)
            raise web.seeother("document_repository")
        if mode == "delete":
            users.check_permission(session, users.DELETE_REPO_DOCUMENT)
            for i in post.integer_list("ids"):
                dbfs.delete_id(dbo, i)

class document_templates:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        title = _("Document Templates", l)
        templates = dbfs.get_html_templates(dbo)
        al.debug("got %d document templates" % len(templates), "code.document_templates", dbo)
        s = html.header(title, session, "document_templates.js")
        c = html.controller_json("rows", templates)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create", template=""), session.locale)
        mode = post["mode"]
        if mode == "create":
            return dbfs.create_html_template(dbo, post["template"])
        if mode == "clone":
            for t in post.integer_list("ids"):
                return dbfs.clone_html_template(dbo, t, post["template"])
        if mode == "delete":
            for t in post.integer_list("ids"):
                dbfs.delete_id(dbo, t)
        elif mode == "rename":
            dbfs.rename_file_id(dbo, post.integer("dbfsid"), post["newname"])

class donation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, offset = "m7"), session.locale)
        donations = financial.get_donations(dbo, post["offset"])
        title = _("Payment book", l)
        al.debug("got %d donations" % (len(donations)), "code.donation", dbo)
        s = html.header(title, session, "donations.js")
        c = html.controller_str("name", "donation")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in post.integer_list("ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in post.integer_list("ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            web.header("Content-Type", "application/json")
            return html.json(extmovement.get_person_movements(dbo, post.integer("personid")))

class donation_receive:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_DONATION)
        l = session.locale
        dbo = session.dbo
        title = _("Receive a payment", l)
        s = html.header(title, session, "donation_receive.js")
        al.debug("receiving donation", "code.donation_receive", dbo)
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            don1 = str(financial.insert_donation_from_form(session.dbo, session.user, post))
            if post.integer("amount2") > 0:
                don_dict = {
                    "person"                : post["person"],
                    "animal"                : post["animal"],
                    "type"                  : post["type2"],
                    "payment"               : post["payment2"],
                    "destaccount"           : post["destaccount2"],
                    "frequency"             : "0",
                    "amount"                : post["amount2"],
                    "received"              : post["received"],
                    "giftaid"               : post["giftaid"]
                }
                financial.insert_donation_from_form(session.dbo, session.user, utils.PostedData(don_dict, session.locale))
            return don1
        elif mode == "templates":
            return html.template_selection(dbfs.get_html_templates(session.dbo), "document_gen?mode=DONATION&id=%d" % post.integer("id"))

class foundanimal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_foundanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        al.debug("open found animal %s %s %s" % (a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal", dbo)
        s = html.header(title, session, "lostfound.js")
        c = html.controller_json("animal", a)
        c += html.controller_str("name", "foundanimal")
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "foundanimal"))
        c += html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_FOUND_ANIMAL)
            extlostfound.update_foundanimal_from_form(dbo, post, session.user)
        elif mode == "email":
            users.check_permission(session, users.VIEW_FOUND_ANIMAL)
            if not extlostfound.send_email_from_form(dbo, session.user, post):
                raise utils.ASMError(_("Failed sending email", l))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_FOUND_ANIMAL)
            extlostfound.delete_foundanimal(dbo, session.user, post.integer("id"))
        elif mode == "toanimal":
            users.check_permission(session, users.ADD_ANIMAL)
            return str(extlostfound.create_animal_from_found(dbo, session.user, post.integer("id")))
        elif mode == "towaitinglist":
            users.check_permission(session, users.ADD_WAITING_LIST)
            return str(extlostfound.create_waitinglist_from_found(dbo, session.user, post.integer("id")))

class foundanimal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_foundanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.FOUNDANIMAL, post.integer("id"))
        al.debug("got %d diaries for found animal %s %s %s" % (len(diaries), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_str("name", "foundanimal_diary")
        c += html.controller_int("linkid", a["LFID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.FOUNDANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class foundanimal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Found Animal", l)
        s = html.header(title, session, "lostfound_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("mode", "found")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class foundanimal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode = ""), session.locale)
        results = extlostfound.get_foundanimal_find_advanced(dbo, post.data, configuration.record_search_limit(dbo))
        title = _("Results", l)
        resultsmessage = _("Find found animal returned {0} results.", l).format(len(results))
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.foundanimal_find_results", dbo)
        s = html.header(title, session, "lostfound_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("name", "foundanimal_find_results")
        c += html.controller_str("resultsmessage", resultsmessage)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class foundanimal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extlostfound.get_foundanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        logs = extlog.get_logs(dbo, extlog.FOUNDANIMAL, post.integer("id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "foundanimal_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.FOUNDANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class foundanimal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_foundanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        m = extmedia.get_media(dbo, extmedia.FOUNDANIMAL, post.integer("id"))
        al.debug("got %d media for found animal %s %s %s" % (len(m), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.FOUNDANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid, post)
            raise web.seeother("foundanimal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=foundanimal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid, post)
            raise web.seeother("foundanimal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class foundanimal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Add found animal", l)
        s = html.header(title, session, "lostfound_new.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("name", "foundanimal_new")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_FOUND_ANIMAL)
        utils.check_locked_db(session)
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        return str(extlostfound.insert_foundanimal_from_form(dbo, post, session.user))

class giftaid_hmrc_spreadsheet:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        dbo = session.dbo
        post = utils.PostedData(web.input(fromdate = "", todate = ""), session.locale)
        fromdate = post["fromdate"]
        todate = post["todate"]
        if fromdate == "":
            title = "HMRC Gift Aid Spreadsheet"
            s = html.header(title, session, "giftaid_hmrc_spreadsheet.js")
            s += html.footer()
            web.header("Content-Type", "text/html")
            return s
        else:
            al.debug("generating HMRC giftaid spreadsheet for %s -> %s" % (fromdate, todate), "code.giftaid_hmrc_spreadsheet", dbo)
            web.header("Content-Type", "application/vnd.oasis.opendocument.spreadsheet")
            web.header("Cache-Control", "no-cache")
            web.header("Content-Disposition", "attachment; filename=\"giftaid.ods\"")
            return financial.giftaid_spreadsheet(dbo, PATH, post.date("fromdate"), post.date("todate"))

class htmltemplates:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("HTML Publishing Templates", l)
        templates = dbfs.get_html_publisher_templates_files(dbo)
        al.debug("editing %d html templates" % len(templates), "code.htmltemplates", dbo)
        s = html.header(title, session, "htmltemplates.js")
        c = html.controller_json("rows", templates)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", templatename = "", header = "", body = "", footer = ""), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            dbfs.update_html_publisher_template(dbo, session.user, post["templatename"], post["header"], post["body"], post["footer"])
        elif mode == "update":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            dbfs.update_html_publisher_template(dbo, session.user, post["templatename"], post["header"], post["body"], post["footer"])
        elif mode == "delete":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            for name in post["names"].split(","):
                if name != "": dbfs.delete_html_publisher_template(dbo, session.user, name)

class incident:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCIDENT)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimalcontrol.get_animalcontrol(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        al.debug("open incident %s %s %s" % (a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"])), "code.incident", dbo)
        title = _("Incident {0}, {1}: {2}", l).format(a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"]))
        s = html.header(title, session, "incident.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ACID"], "incident"))
        c += html.controller_json("incident", a)
        c += html.controller_json("incidenttypes", extlookups.get_incident_types(dbo))
        c += html.controller_json("completedtypes", extlookups.get_incident_completed_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("tabcounts", extanimalcontrol.get_animalcontrol_satellite_counts(dbo, a["ACID"])[0])
        c += html.controller_json("users", users.get_users(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_INCIDENT)
            extanimalcontrol.update_animalcontrol_from_form(dbo, post, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_INCIDENT)
            extanimalcontrol.delete_animalcontrol(dbo, session.user, post.integer("id"))
        elif mode == "latlong":
            users.check_permission(session, users.CHANGE_INCIDENT)
            extanimalcontrol.update_dispatch_latlong(dbo, post.integer("incidentid"), post["latlong"])
        elif mode == "email":
            users.check_permission(session, users.VIEW_INCIDENT)
            if not extperson.send_email_from_form(dbo, session.user, post):
                raise utils.ASMError(_("Failed sending email", l))

class incident_citations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_CITATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimalcontrol.get_animalcontrol(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Incident {0}, {1}: {2}", l).format(a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"]))
        citations = financial.get_incident_citations(dbo, post.integer("id"))
        al.debug("got %d citations" % len(citations), "code.incident_citations", dbo)
        s = html.header(title, session, "citations.js")
        c = html.controller_str("name", "incident_citations")
        c += html.controller_json("rows", citations)
        c += html.controller_json("incident", a)
        c += html.controller_json("tabcounts", extanimalcontrol.get_animalcontrol_satellite_counts(dbo, a["ACID"])[0])
        c += html.controller_json("citationtypes", extlookups.get_citation_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_CITATION)
            return financial.insert_citation_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_CITATION)
            financial.update_citation_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_CITATION)
            for lid in post.integer_list("ids"):
                financial.delete_citation(session.dbo, session.user, lid)

class incident_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCIDENT)
        l = session.locale
        dbo = session.dbo
        title = _("Find Incident", l)
        s = html.header(title, session, "incident_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("incidenttypes", extlookups.get_incident_types(dbo))
        c += html.controller_json("completedtypes", extlookups.get_incident_completed_types(dbo))
        c += html.controller_json("citationtypes", extlookups.get_citation_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("users", users.get_users(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class incident_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCIDENT)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode = ""), session.locale)
        results = extanimalcontrol.get_animalcontrol_find_advanced(dbo, post.data, configuration.record_search_limit(dbo))
        title = _("Results", l)
        resultsmessage = _("Find animal control incidents returned {0} results.", l).format(len(results))
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.incident_find_results", dbo)
        s = html.header(title, session, "incident_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("name", "incident_find_results")
        c += html.controller_str("resultsmessage", resultsmessage)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class incident_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimalcontrol.get_animalcontrol(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Incident {0}, {1}: {2}", l).format(a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"]))
        diaries = extdiary.get_diaries(dbo, extdiary.ANIMALCONTROL, post.integer("id"))
        al.debug("got %d diaries" % len(diaries), "code.incident_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("incident", a)
        c += html.controller_json("tabcounts", extanimalcontrol.get_animalcontrol_satellite_counts(dbo, a["ACID"])[0])
        c += html.controller_str("name", "incident_diary")
        c += html.controller_int("linkid", a["ACID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.ANIMALCONTROL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class incident_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        a = extanimalcontrol.get_animalcontrol(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Incident {0}, {1}: {2}", l).format(a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"]))
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        logs = extlog.get_logs(dbo, extlog.ANIMALCONTROL, post.integer("id"), logfilter)
        al.debug("got %d logs" % len(logs), "code.incident_log", dbo)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "incident_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("incident", a)
        c += html.controller_json("tabcounts", extanimalcontrol.get_animalcontrol_satellite_counts(dbo, a["ACID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.ANIMALCONTROL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class incident_map:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCIDENT)
        l = session.locale
        dbo = session.dbo
        #post = utils.PostedData(web.input(), session.locale)
        rows = extanimalcontrol.get_animalcontrol_find_advanced(dbo, { "filter": "incomplete" })
        al.debug("incident map, %d active" % (len(rows)), "code.incident_map", dbo)
        title = _("Active Incidents", l)
        s = html.header(title, session, "incident_map.js")
        c = html.controller_json("rows", rows);
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class incident_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extanimalcontrol.get_animalcontrol(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Incident {0}, {1}: {2}", l).format(a["ACID"], a["INCIDENTNAME"], python2display(l, a["INCIDENTDATETIME"]))
        m = extmedia.get_media(dbo, extmedia.ANIMALCONTROL, post.integer("id"))
        al.debug("got %d media" % len(m), "code.incident_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("incident", a)
        c += html.controller_json("tabcounts", extanimalcontrol.get_animalcontrol_satellite_counts(dbo, a["ACID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.ANIMALCONTROL)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.ANIMALCONTROL, linkid, post)
            raise web.seeother("incident_media?id=%d" % post.integer("linkid"))
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.ANIMALCONTROL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=incident_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.ANIMALCONTROL, linkid, post)
            raise web.seeother("incident_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class incident_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_INCIDENT)
        l = session.locale
        dbo = session.dbo
        title = _("Report a new incident", l)
        s = html.header(title, session, "incident_new.js")
        c = html.controller_json("incidenttypes", extlookups.get_incident_types(dbo))
        c += html.controller_json("users", users.get_users(dbo))
        s += html.controller(c)
        s += html.footer()
        al.debug("add incident", "code.incident_new", dbo)
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_INCIDENT)
        utils.check_locked_db(session)
        post = utils.PostedData(web.input(), session.locale)
        incidentid = extanimalcontrol.insert_animalcontrol_from_form(session.dbo, post, session.user)
        return str(incidentid)

class licence:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LICENCE)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(offset = "i31"), session.locale)
        title = _("Licensing", l)
        licences = financial.get_licences(dbo, post["offset"])
        al.debug("got %d licences" % len(licences), "code.licence", dbo)
        s = html.header(title, session, "licence.js")
        c = html.controller_str("name", "licence")
        c += html.controller_str("title", title)
        c += html.controller_json("rows", licences)
        c += html.controller_json("licencetypes", extlookups.get_licence_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LICENCE)
            return financial.insert_licence_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LICENCE)
            financial.update_licence_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LICENCE)
            for lid in post.integer_list("ids"):
                financial.delete_licence(session.dbo, session.user, lid)

class litters:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LITTER)
        l = session.locale
        dbo = session.dbo
        litters = extanimal.get_litters(dbo)
        title = _("Litters", l)
        al.debug("got %d litters" % len(litters), "code.litters", dbo)
        s = html.header(title, session, "litters.js")
        c = html.controller_json("rows", litters)
        c += html.controller_json("species", extlookups.get_species(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_LITTER)
            return extanimal.insert_litter_from_form(session.dbo, session.user, post)
        elif mode == "nextlitterid":
            nextid = db.query_int(dbo, "SELECT MAX(ID) FROM animallitter") + 1
            return utils.padleft(nextid, 6)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LITTER)
            extanimal.update_litter_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LITTER)
            for lid in post.integer_list("ids"):
                extanimal.delete_litter(session.dbo, session.user, lid)

class log_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_ANIMAL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode = "animal"), session.locale)
        title = _("Add a new log", l)
        s = html.header(title, session, "log_new.js")
        c = html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_str("mode", post["mode"])
        al.debug("loaded lookups for new log", "code.log_new", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        users.check_permission(session, users.ADD_LOG)
        if mode == "animal":
            extlog.insert_log_from_form(dbo, session.user, extlog.ANIMAL, post.integer("animal"), post)
        elif mode == "person":
            extlog.insert_log_from_form(dbo, session.user, extlog.PERSON, post.integer("person"), post)

class lookups:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MODIFY_LOOKUPS)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(tablename="animaltype"), session.locale)
        tablename = post["tablename"]
        table = list(extlookups.LOOKUP_TABLES[tablename])
        table[0] = translate(table[0], l)
        table[2] = translate(table[2], l)
        rows = extlookups.get_lookup(dbo, tablename, table[1])
        al.debug("edit lookups for %s, got %d rows" % (tablename, len(rows)), "code.lookups", dbo)
        title = _("Edit Lookups", l)
        s = html.header(title, session, "lookups.js")
        c = html.controller_json("rows", rows)
        c += html.controller_json("petfinderspecies", extlookups.PETFINDER_SPECIES)
        c += html.controller_json("petfinderbreeds", extlookups.PETFINDER_BREEDS)
        c += html.controller_str("tablename", tablename)
        c += html.controller_str("tablelabel", table[0])
        c += html.controller_str("namefield", table[1].upper())
        c += html.controller_str("namelabel", table[2])
        c += html.controller_str("descfield", table[3].upper())
        c += html.controller_bool("hasspecies", table[4] == 1)
        c += html.controller_bool("haspfspecies", table[5] == 1)
        c += html.controller_bool("haspfbreed", table[6] == 1)
        c += html.controller_bool("hasdefaultcost", table[7] == 1)
        c += html.controller_bool("hasunits", table[8] == 1)
        c += html.controller_bool("canadd", table[9] == 1)
        c += html.controller_bool("candelete", table[10] == 1)
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tables", html.json_lookup_tables(l))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create", id=0, lookup="", lookupname="", lookupdesc="", species=0, pfbreed="", pfspecies="", defaultcost="", adoptionfee=""), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            return extlookups.insert_lookup(dbo, post["lookup"], post["lookupname"], post["lookupdesc"], \
                post.integer("species"), post["pfbreed"], post["pfspecies"], post["units"], post.integer("defaultcost"))
        elif mode == "update":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extlookups.update_lookup(dbo, post.integer("id"), post["lookup"], post["lookupname"], post["lookupdesc"], \
                post.integer("species"), post["pfbreed"], post["pfspecies"], post["units"], post.integer("defaultcost"))
        elif mode == "delete":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            for lid in post.integer_list("ids"):
                extlookups.delete_lookup(dbo, post["lookup"], lid)

class lostanimal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_lostanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        al.debug("open lost animal %s %s %s" % (a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal", dbo)
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        s = html.header(title, session, "lostfound.js")
        c = html.controller_json("animal", a)
        c += html.controller_str("name", "lostanimal")
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "lostanimal"))
        c += html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"]))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_LOST_ANIMAL)
            extlostfound.update_lostanimal_from_form(dbo, post, session.user)
        elif mode == "email":
            users.check_permission(session, users.VIEW_LOST_ANIMAL)
            if not extlostfound.send_email_from_form(dbo, session.user, post):
                raise utils.ASMError(_("Failed sending email", l))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOST_ANIMAL)
            extlostfound.delete_lostanimal(dbo, session.user, post.integer("id"))

class lostanimal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_lostanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.LOSTANIMAL, post.integer("id"))
        al.debug("got %d diaries for lost animal %s %s %s" % (len(diaries), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_str("name", "lostanimal_diary")
        c += html.controller_int("linkid", a["LFID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.LOSTANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class lostanimal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Lost Animal", l)
        s = html.header(title, session, "lostfound_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("mode", "lost")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class lostanimal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode = ""), session.locale)
        results = extlostfound.get_lostanimal_find_advanced(dbo, post.data, configuration.record_search_limit(dbo))
        title = _("Results", l)
        resultsmessage = _("Find lost animal returned {0} results.", l).format(len(results))
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.lostanimal_find_results", dbo)
        s = html.header(title, session, "lostfound_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("name", "lostanimal_find_results")
        c += html.controller_str("resultsmessage", resultsmessage)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class lostanimal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extlostfound.get_lostanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        logs = extlog.get_logs(dbo, extlog.LOSTANIMAL, post.integer("id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "lostanimal_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.LOSTANIMAL, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class lostanimal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extlostfound.get_lostanimal(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        m = extmedia.get_media(dbo, extmedia.LOSTANIMAL, post.integer("id"))
        al.debug("got %d media for lost animal %s %s %s" % (len(m), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.LOSTANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.LOSTANIMAL, linkid, post)
            raise web.seeother("lostanimal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.LOSTANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=lostanimal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.LOSTANIMAL, linkid, post)
            raise web.seeother("lostanimal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class lostanimal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Add lost animal", l)
        s = html.header(title, session, "lostfound_new.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("name", "lostanimal_new")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_LOST_ANIMAL)
        utils.check_locked_db(session)
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        return str(extlostfound.insert_lostanimal_from_form(dbo, post, session.user))

class lostfound_match:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(lostanimalid = 0, foundanimalid = 0, animalid = 0), session.locale)
        lostanimalid = post.integer("lostanimalid")
        foundanimalid = post.integer("foundanimalid")
        animalid = post.integer("animalid")
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If no parameters have been given, use the cached daily copy of the match report
        if lostanimalid == 0 and foundanimalid == 0 and animalid == 0:
            al.debug("no parameters given, using cached report at /reports/daily/lost_found_match.html", "code.lostfound_match", dbo)
            return dbfs.get_string_filepath(dbo, "/reports/daily/lost_found_match.html")
        else:
            al.debug("match lost=%d, found=%d, animal=%d" % (lostanimalid, foundanimalid, animalid), "code.lostfound_match", dbo)
            return extlostfound.match_report(dbo, session.user, lostanimalid, foundanimalid, animalid)

class mailmerge:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MAIL_MERGE)
        post = utils.PostedData(web.input(id = "0", mode = "criteria"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        user = session.user
        crit = extreports.get_criteria_controls(session.dbo, post.integer("id"))
        title = extreports.get_title(dbo, post.integer("id"))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If the mail merge doesn't take criteria, go to the merge selection screen instead
        if crit == "":
            al.debug("mailmerge %d has no criteria, moving to merge selection" % post.integer("id"), "code.mailmerge", dbo)
            mode = "selection"
        # If we're in criteria mode (and there are some to get here), ask for them
        if mode == "criteria":
            al.debug("building report criteria form for mailmerge %d %s" % (post.integer("id"), title), "code.mailmerge", dbo)
            s = html.header(title, session, "mailmerge.js")
            s += html.controller(html.controller_bool("criteria", True))
            s += html.heading(title)
            s += "<div id=\"criteriaform\">"
            s += "<input data-post=\"id\" type=\"hidden\" value=\"%d\" />" % post.integer("id")
            s += "<input data-post=\"mode\" type=\"hidden\" value=\"selection\" />"
            s += crit
            s += "</div>"
            s += html.footing()
            s += html.footer()
            return s
        elif mode == "selection":
            al.debug("entering mail merge selection mode for %d" % post.integer("id"), "code.mailmerge", dbo)
            p = extreports.get_criteria_params(dbo, post.integer("id"), post)
            session.mergeparams = p
            session.mergereport = post.integer("id")
            rows, cols = extreports.execute_query(dbo, post.integer("id"), user, p)
            if rows is None: rows = []
            al.debug("got merge rows (%d items)" % len(rows), "code.mailmerge", dbo)
            session.mergetitle = title.replace(" ", "_").replace("\"", "").replace("'", "").lower()
            # construct a list of field tokens for the email helper
            fields = []
            if len(rows) >  0:
                for fname in sorted(rows[0].iterkeys()):
                    fields.append(fname)
            # send the selection form
            title = _("Mail Merge - {0}", l).format(title)
            s = html.header(title, session, "mailmerge.js")
            c = html.controller_json("fields", fields)
            c += html.controller_int("numrows", len(rows))
            c += html.controller_json("rows", rows)
            s += html.controller(c)
            s += html.footer()
            return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="csv"), session.locale)
        mode = post["mode"]
        rows, cols = extreports.execute_query(dbo, session.mergereport, session.user, session.mergeparams)
        al.debug("got merge rows (%d items)" % len(rows), "code.mailmerge", dbo)
        if mode == "email":
            fromadd = post["from"]
            subject = post["subject"]
            body = post["body"]
            contenttype = post.boolean("html") == 1 and "html" or "plain"
            utils.send_bulk_email(dbo, fromadd, subject, body, rows, contenttype)
        elif mode == "document":
            pass
        elif mode == "labels":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=%s" or "attachment; filename=%s"
            web.header("Content-Disposition", disposition % session.mergetitle + ".pdf")
            return utils.generate_label_pdf(dbo, session.locale, rows, post["papersize"], post["units"],
                post.floating("hpitch"), post.floating("vpitch"), 
                post.floating("width"), post.floating("height"), 
                post.floating("lmargin"), post.floating("tmargin"),
                post.integer("cols"), post.integer("rows"))
        elif mode == "csv":
            web.header("Content-Type", "text/csv")
            web.header("Content-Disposition", u"attachment; filename=" + utils.decode_html(session.mergetitle) + u".csv")
            includeheader = 1 == post.boolean("includeheader")
            return utils.csv(rows, cols, includeheader)

class medical:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(newmed = "0", offset = "m31"), session.locale)
        med = extmedical.get_treatments_outstanding(dbo, post["offset"], session.locationfilter)
        profiles = extmedical.get_profiles(dbo)
        title = _("Medical Book", l)
        al.debug("got %d medical treatments" % len(med), "code.medical", dbo)
        s = html.header(title, session, "medical.js")
        c = html.controller_json("profiles", profiles)
        c += html.controller_json("rows", med)
        c += html.controller_bool("newmed", post.integer("newmed") == 1)
        c += html.controller_str("name", "medical")
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"] 
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_regimen_from_form(session.dbo, session.user, post)
        if mode == "createbulk":
            users.check_permission(session, users.ADD_MEDICAL)
            for animalid in post.integer_list("animals"):
                post.data["animal"] = str(animalid)
                extmedical.insert_regimen_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_regimen_from_form(session.dbo, session.user, post)
        elif mode == "delete_regimen":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in post.integer_list("ids"):
                extmedical.delete_regimen(session.dbo, session.user, mid)
        elif mode == "delete_treatment":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in post.integer_list("ids"):
                extmedical.delete_treatment(session.dbo, session.user, mid)
        elif mode == "get_profile":
            return html.json([extmedical.get_profile(session.dbo, post.integer("profileid"))])
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = post.date("newdate")
            for mid in post.integer_list("ids"):
                extmedical.update_treatment_given(session.dbo, session.user, mid, newdate)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = post.date("newdate")
            for mid in post.integer_list("ids"):
                extmedical.update_treatment_required(session.dbo, session.user, mid, newdate)

class medicalprofile:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        l = session.locale
        dbo = session.dbo
        med = extmedical.get_profiles(dbo)
        title = _("Medical Profiles", l)
        al.debug("got %d medical profiles" % len(med), "code.medical_profile", dbo)
        s = html.header(title, session, "medicalprofile.js")
        c = html.controller_json("rows", med)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_profile_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_profile_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in post.integer_list("ids"):
                extmedical.delete_profile(session.dbo, session.user, mid)

class move_adopt:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        title = _("Adopt an animal", l)
        s = html.header(title, session, "move_adopt.js")
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = dbo.locale
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_adoption_from_form(session.dbo, session.user, post))
        elif mode == "cost":
            users.check_permission(session, users.VIEW_COST)
            dailyboardcost = extanimal.get_daily_boarding_cost(dbo, post.integer("id"))
            dailyboardcostdisplay = format_currency(l, dailyboardcost)
            daysonshelter = extanimal.get_days_on_shelter(dbo, post.integer("id"))
            totaldisplay = format_currency(l, dailyboardcost * daysonshelter)
            return totaldisplay + "||" + _("On shelter for {0} days, daily cost {1}, cost record total <b>{2}</b>", l).format(daysonshelter, dailyboardcostdisplay, totaldisplay)
        elif mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))
        elif mode == "donationdefault":
            return extlookups.get_donation_default(dbo, post.integer("donationtype"))
        elif mode == "insurance":
            return extmovement.generate_insurance_number(dbo)

class move_book_foster:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_movements(dbo, extmovement.FOSTER)
        al.debug("got %d movements" % len(movements), "code.move_book_foster", dbo)
        title = _("Foster Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_adoption:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_adoption", dbo)
        title = _("Return an animal from adoption", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_other:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_nonfosteradoption(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_other", dbo)
        title = _("Return an animal from another movement", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_transfer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_transfers(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_transfer", dbo)
        title = _("Return an animal from transfer", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_reservation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_active_reservations(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_reservation", dbo)
        title = _("Reservation Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_retailer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_movements(dbo, extmovement.RETAILER)
        al.debug("got %d movements" % len(movements), "code.move_book_retailer", dbo)
        title = _("Retailer Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_transport:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_movements(dbo, extmovement.TRANSPORT)
        al.debug("got %d movements" % len(movements), "code.move_book_transport", dbo)
        title = _("Transport Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_trial_adoption:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_trial_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_trial_adoption", dbo)
        title = _("Trial adoption book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_unneutered:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_unneutered_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_unneutered", dbo)
        title = _("Unaltered Adopted Animals", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_deceased:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Mark an animal deceased", l)
        s = html.header(title, session, "move_deceased.js")
        c = html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_deceased_from_form(dbo, session.user, post)

class move_foster:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Foster an animal", l)
        s = html.header(title, session, "move_foster.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_foster_from_form(session.dbo, session.user, post))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))

class move_reclaim:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        title = _("Reclaim an animal", l)
        s = html.header(title, session, "move_reclaim.js")
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = dbo.locale
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_reclaim_from_form(session.dbo, session.user, post))
        elif mode == "cost":
            users.check_permission(session, users.VIEW_COST)
            dailyboardcost = extanimal.get_daily_boarding_cost(dbo, post.integer("id"))
            dailyboardcostdisplay = format_currency(l, dailyboardcost)
            daysonshelter = extanimal.get_days_on_shelter(dbo, post.integer("id"))
            totaldisplay = format_currency(l, dailyboardcost * daysonshelter)
            return totaldisplay + "||" + _("On shelter for {0} days, daily cost {1}, cost record total <b>{2}</b>", l).format(daysonshelter, dailyboardcostdisplay, totaldisplay)
        elif mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))
        elif mode == "donationdefault":
            return extlookups.get_donation_default(dbo, post.integer("donationtype"))

class move_reserve:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        title = _("Reserve an animal", l)
        s = html.header(title, session, "move_reserve.js")
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_reserve_from_form(session.dbo, session.user, post))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))

class move_retailer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Move an animal to a retailer", l)
        s = html.header(title, session, "move_retailer.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_retailer_from_form(session.dbo, session.user, post))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))

class move_transfer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Transfer an animal", l)
        s = html.header(title, session, "move_transfer.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_transfer_from_form(session.dbo, session.user, post))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % post.integer("id"))

class onlineform_incoming:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCOMING_FORMS)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="view"), session.locale)
        mode = post["mode"]
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        if mode == "print":
            users.check_permission(session, users.VIEW_INCOMING_FORMS)
            return extonlineform.get_onlineformincoming_html_print(dbo, post.integer_list("ids"))
        headers = extonlineform.get_onlineformincoming_headers(dbo)
        title = _("Incoming Forms", l)
        al.debug("got %d submitted headers" % len(headers), "code.onlineform_incoming", dbo)
        s = html.header(title, session, "onlineform_incoming.js")
        c = html.controller_json("rows", headers)
        s += html.controller(c)
        s += html.footer()
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="view"), session.locale)
        mode = post["mode"]
        personid = post.integer("personid")
        animalid = post.integer("animalid")
        collationid = post.integer("collationid")
        web.header("Content-Type", "text/plain")
        if mode == "view":
            users.check_permission(session, users.VIEW_INCOMING_FORMS)
            return extonlineform.get_onlineformincoming_html(dbo, collationid)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_INCOMING_FORMS)
            for did in post.integer_list("ids"):
                extonlineform.delete_onlineformincoming(session.dbo, session.user, did)
        elif mode == "attachanimal":
            formname = extonlineform.get_onlineformincoming_name(dbo, collationid)
            formhtml = extonlineform.get_onlineformincoming_html_print(dbo, [collationid,] )
            extmedia.create_document_media(dbo, session.user, extmedia.ANIMAL, animalid, formname, formhtml )
            return animalid 
        elif mode == "attachperson":
            formname = extonlineform.get_onlineformincoming_name(dbo, collationid)
            formhtml = extonlineform.get_onlineformincoming_html_print(dbo, [collationid,] )
            extmedia.create_document_media(dbo, session.user, extmedia.PERSON, personid, formname, formhtml )
            return personid 
        elif mode == "animal":
            users.check_permission(session, users.ADD_MEDIA)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, animalid, animalname = extonlineform.attach_animal(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, animalid, animalname))
            return "^$".join(rv)
        elif mode == "person":
            users.check_permission(session, users.ADD_PERSON)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, personid, personname = extonlineform.create_person(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, personid, personname))
            return "^$".join(rv)
        elif mode == "lostanimal":
            users.check_permission(session, users.ADD_LOST_ANIMAL)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, lostanimalid, personname = extonlineform.create_lostanimal(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, lostanimalid, personname))
            return "^$".join(rv)
        elif mode == "foundanimal":
            users.check_permission(session, users.ADD_FOUND_ANIMAL)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, foundanimalid, personname = extonlineform.create_foundanimal(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, foundanimalid, personname))
            return "^$".join(rv)
        elif mode == "incident":
            users.check_permission(session, users.ADD_INCIDENT)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, incidentid, personname = extonlineform.create_animalcontrol(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, incidentid, personname))
            return "^$".join(rv)
        elif mode == "waitinglist":
            users.check_permission(session, users.ADD_WAITING_LIST)
            rv = []
            for pid in post.integer_list("ids"):
                collationid, wlid, personname = extonlineform.create_waitinglist(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, wlid, personname))
            return "^$".join(rv)

class onlineform:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ONLINE_FORMS)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(formid = 0), session.locale)
        formid = post.integer("formid")
        formname = extonlineform.get_onlineform_name(dbo, formid)
        fields = extonlineform.get_onlineformfields(dbo, formid)
        title = _("Online Form: {0}", l).format(formname)
        al.debug("got %d online form fields" % len(fields), "code.onlineform", dbo)
        s = html.header(title, session, "onlineform.js")
        c = html.controller_json("rows", fields)
        c += html.controller_int("formid", formid)
        c += html.controller_str("formname", formname)
        c += html.controller_json("formfields", extonlineform.FORM_FIELDS)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            return extonlineform.insert_onlineformfield_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            extonlineform.update_onlineformfield_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            for did in post.integer_list("ids"):
                extonlineform.delete_onlineformfield(session.dbo, session.user, did)

class onlineforms:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ONLINE_FORMS)
        l = session.locale
        dbo = session.dbo
        onlineforms = extonlineform.get_onlineforms(dbo)
        title = _("Online Forms", l)
        al.debug("got %d online forms" % len(onlineforms), "code.onlineforms", dbo)
        s = html.header(title, session, "onlineforms.js")
        c = html.controller_json("rows", onlineforms)
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        c += html.controller_str("baseurl", BASE_URL)
        c += html.controller_json("header", html.escape_angle(extonlineform.get_onlineform_header(dbo)))
        c += html.controller_json("footer", html.escape_angle(extonlineform.get_onlineform_footer(dbo)))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            return extonlineform.insert_onlineform_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            extonlineform.update_onlineform_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            for did in post.integer_list("ids"):
                extonlineform.delete_onlineform(session.dbo, session.user, did)
        elif mode == "headfoot":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            dbfs.put_string_filepath(session.dbo, "/onlineform/head.html", post["header"])
            dbfs.put_string_filepath(session.dbo, "/onlineform/foot.html", post["footer"])

class options:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("Options", l)
        session.configuration = configuration.get_map(dbo)
        s = html.header(title, session, "options.js")
        c = html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_bool("hassmtpoverride", SMTP_SERVER is not None)
        c += html.controller_plain("animalfindcolumns", html.json_animalfindcolumns(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds(dbo))
        c += html.controller_json("coattypes", extlookups.get_coattypes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("costtypes", extlookups.get_costtypes(dbo))
        c += html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("entryreasons", extlookups.get_entryreasons(dbo))
        c += html.controller_json("incidenttypes", extlookups.get_incident_types(dbo))
        c += html.controller_json("locales", extlookups.LOCALES)
        c += html.controller_json("locations", extlookups.get_internal_locations(dbo))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_plain("personfindcolumns", html.json_personfindcolumns(dbo))
        c += html.controller_plain("quicklinks", html.json_quicklinks(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("themes", extlookups.VISUAL_THEMES)
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("types", extlookups.get_animal_types(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        c += html.controller_plain("waitinglistcolumns", html.json_waitinglistcolumns(dbo))
        al.debug("lookups loaded", "code.options", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            configuration.csave(session.dbo, session.user, post)
            users.update_session(session)

class person:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        if p["ISSTAFF"] == 1:
            users.check_permission(session, users.VIEW_STAFF)
        title = p["OWNERNAME"]
        al.debug("opened person '%s'" % p["OWNERNAME"], "code.person", dbo)
        s = html.header(title, session, "person.js")
        c = html.controller_json("additional", extadditional.get_additional_fields(dbo, p["ID"], "person"))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("diarytasks", extdiary.get_person_tasks(dbo))
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        c += html.controller_json("ynun", extlookups.get_ynun(dbo))
        c += html.controller_json("homecheckhistory", extperson.get_homechecked(dbo, post.integer("id")))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_str("towns", "|".join(extperson.get_towns(dbo)))
        c += html.controller_str("counties", "|".join(extperson.get_counties(dbo)))
        c += html.controller_str("towncounties", "|".join(extperson.get_town_to_county(dbo)))
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("person", p)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_PERSON)
            extperson.update_person_from_form(dbo, post, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_PERSON)
            extperson.delete_person(dbo, session.user, post.integer("personid"))
        elif mode == "email":
            users.check_permission(session, users.VIEW_PERSON)
            if not extperson.send_email_from_form(dbo, session.user, post):
                raise utils.ASMError(_("Failed sending email", l))
        elif mode == "latlong":
            users.check_permission(session, users.CHANGE_PERSON)
            extperson.update_latlong(dbo, post.integer("personid"), post["latlong"])
        elif mode == "merge":
            users.check_permission(session, users.MERGE_PERSON)
            extperson.merge_person(dbo, session.user, post.integer("personid"), post.integer("mergepersonid"))

class person_citations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_CITATION)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        citations = financial.get_person_citations(dbo, post.integer("id"))
        al.debug("got %d citations" % len(citations), "code.incident_citations", dbo)
        s = html.header(title, session, "citations.js")
        c = html.controller_str("name", "person_citations")
        c += html.controller_json("rows", citations)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("citationtypes", extlookups.get_citation_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_CITATION)
            return financial.insert_citation_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_CITATION)
            financial.update_citation_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_CITATION)
            for lid in post.integer_list("ids"):
                financial.delete_citation(session.dbo, session.user, lid)

class person_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        diaries = extdiary.get_diaries(dbo, extdiary.PERSON, post.integer("id"))
        al.debug("got %d diaries" % len(diaries), "code.person_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_str("name", "person_diary")
        c += html.controller_int("linkid", p["ID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.PERSON, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class person_donations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        donations = financial.get_person_donations(dbo, post.integer("id"))
        s = html.header(title, session, "donations.js")
        c = html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_str("name", "person_donations")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in post.integer_list("ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in post.integer_list("ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            return html.json(extmovement.get_person_movements(dbo, post.integer("personid")))

class person_embed:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode = "lookup"), session.locale)
        mode = post["mode"]
        if mode == "lookup":
            rv = {}
            rv["towns"] = "|".join(extperson.get_towns(dbo))
            rv["counties"] = "|".join(extperson.get_counties(dbo))
            rv["towncounties"] = "|".join(extperson.get_town_to_county(dbo))
            rv["flags"] = extlookups.get_person_flags(dbo)
            web.header("Content-Type", "application/json")
            web.header("Cache-Control", "max-age=60")
            return html.json(rv)

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode = "find", filter = "all", id = 0), session.locale)
        mode = post["mode"]
        q = post["q"]
        web.header("Content-Type", "application/json")
        if mode == "find":
            rows = extperson.get_person_find_simple(dbo, q, post["filter"], users.check_permission_bool(session, users.VIEW_STAFF), 100)
            al.debug("find '%s' got %d rows" % (str(web.ctx.query), len(rows)), "code.person_embed", dbo)
            return html.json(rows)
        elif mode == "id":
            p = extperson.get_person(dbo, post.integer("id"))
            if p is None:
                al.error("get person by id %d found no records." % (post.integer("id")), "code.person_embed", dbo)
                raise web.notfound()
            else:
                al.debug("get person by id %d got '%s'" % (post.integer("id"), p["OWNERNAME"]), "code.person_embed", dbo)
                return html.json((p,))
        elif mode == "similar":
            surname = post["surname"]
            forenames = post["forenames"]
            address = post["address"]
            p = extperson.get_person_similar(dbo, surname, forenames, address)
            if len(p) == 0:
                al.debug("No similar people found for %s, %s, %s" % (surname, forenames, address), "code.person_embed", dbo)
            else:
                al.debug("found similar people for %s, %s, %s: got %d records" % (surname, forenames, address, len(p)), "code.person_embed", dbo)
            return html.json(p)
        elif mode == "add":
            users.check_permission(session, users.ADD_PERSON)
            al.debug("add new person", "code.person_embed", dbo)
            pid = extperson.insert_person_from_form(dbo, post, session.user)
            p = extperson.get_person(dbo, pid)
            return html.json((p,))

class person_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        l = session.locale
        dbo = session.dbo
        title = _("Find Person", l)
        flags = extlookups.get_person_flags(dbo)
        al.debug("lookups loaded", "code.person_find", dbo)
        s = html.header(title, session, "person_find.js")
        c = html.controller_json("flags", flags)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class person_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(mode = "", q = ""), session.locale)
        mode = post["mode"]
        q = post["q"]
        if mode == "SIMPLE":
            results = extperson.get_person_find_simple(dbo, q, "all", users.check_permission_bool(session, users.VIEW_STAFF), configuration.record_search_limit(dbo))
        else:
            results = extperson.get_person_find_advanced(dbo, post.data, users.check_permission_bool(session, users.VIEW_STAFF), configuration.record_search_limit(dbo))
        add = None
        if len(results) > 0: 
            add = extadditional.get_additional_fields_ids(dbo, results, "person")
        title = _("Results", l)
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.person_find_results", dbo)
        s = html.header(title, session, "person_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_json("additional", add)
        c += html.controller_str("resultsmessage", _("Search returned {0} results.", l).format(len(results)))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class person_investigation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INVESTIGATION)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        investigation = extperson.get_investigation(dbo, post.integer("id"))
        al.debug("got %d investigation records for person %s" % (len(investigation), p["OWNERNAME"]), "code.person_investigation", dbo)
        s = html.header(title, session, "person_investigation.js")
        c = html.controller_json("rows", investigation)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_INVESTIGATION)
            return str(extperson.insert_investigation_from_form(session.dbo, session.user, post))
        elif mode == "update":
            users.check_permission(session, users.CHANGE_INVESTIGATION)
            extperson.update_investigation_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_INVESTIGATION)
            for did in post.integer_list("ids"):
                extperson.delete_investigation(session.dbo, session.user, did)

class person_licence:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LICENCE)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        licences = financial.get_person_licences(dbo, post.integer("id"))
        al.debug("got %d licences" % len(licences), "code.person_licence", dbo)
        s = html.header(title, session, "licence.js")
        c = html.controller_str("name", "person_licence")
        c += html.controller_json("rows", licences)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("licencetypes", extlookups.get_licence_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LICENCE)
            return financial.insert_licence_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LICENCE)
            financial.update_licence_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LICENCE)
            for lid in post.integer_list("ids"):
                financial.delete_licence(session.dbo, session.user, lid)

class person_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        logs = extlog.get_logs(dbo, extlog.PERSON, post.integer("id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "person_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.PERSON, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class person_lookingfor:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        web.header("Content-Type", "text/html")
        return dbfs.get_string_filepath(dbo, "/reports/daily/lookingfor.html")

class person_links:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON_LINKS)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        links = extperson.get_links(dbo, post.integer("id"))
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        s = html.header(title, session, "person_links.js")
        al.debug("got %d person links" % len(links), "code.person_links", dbo)
        c = html.controller_json("links", links)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class person_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        m = extmedia.get_media(dbo, extmedia.PERSON, post.integer("id"))
        al.debug("got %d media" % len(m), "code.person_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_bool("showPreferred", True)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.PERSON)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(dbo, session.user, extmedia.PERSON, linkid, post)
            raise web.seeother("person_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(dbo, session.user, extmedia.PERSON, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=person_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.PERSON, linkid, post)
            raise web.seeother("person_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                if m["MEDIANAME"].endswith("html"):
                    content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], post["emailnote"], "html", content, m["MEDIANOTES"] + m["MEDIANAME"])
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(dbo, session.user, mid)

class person_movements:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        movements = extmovement.get_person_movements(dbo, post.integer("id"))
        al.debug("got %d movements" % len(movements), "code.person_movements", dbo)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in post.integer_list("ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)
        elif mode == "insurance":
            return extmovement.generate_insurance_number(session.dbo)

class person_new:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Add a new person", l)
        s = html.header(title, session, "person_new.js")
        c = html.controller_str("towns", "|".join(extperson.get_towns(dbo)))
        c += html.controller_str("counties", "|".join(extperson.get_counties(dbo)))
        c += html.controller_str("towncounties", "|".join(extperson.get_town_to_county(dbo)))
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        s += html.controller(c)
        s += html.footer()
        al.debug("add person", "code.person_new", dbo)
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_PERSON)
        utils.check_locked_db(session)
        post = utils.PostedData(web.input(), session.locale)
        personid = extperson.insert_person_from_form(session.dbo, post, session.user)
        return str(personid)

class person_traploan:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TRAPLOAN)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        traploans = extanimalcontrol.get_person_traploans(dbo, post.integer("id"))
        al.debug("got %d trap loans" % len(traploans), "code.person_traploan", dbo)
        s = html.header(title, session, "traploan.js")
        c = html.controller_str("name", "person_traploan")
        c += html.controller_json("rows", traploans)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("traptypes", extlookups.get_trap_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_TRAPLOAN)
            return extanimalcontrol.insert_traploan_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TRAPLOAN)
            extanimalcontrol.update_traploan_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TRAPLOAN)
            for lid in post.integer_list("ids"):
                extanimalcontrol.delete_traploan(session.dbo, session.user, lid)

class person_vouchers:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VOUCHER)
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        p = extperson.get_person(dbo, post.integer("id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        vouchers = financial.get_vouchers(dbo, post.integer("id"))
        al.debug("got %d vouchers" % len(vouchers), "code.person_vouchers", dbo)
        s = html.header(title, session, "person_vouchers.js")
        c = html.controller_json("vouchertypes", extlookups.get_voucher_types(dbo))
        c += html.controller_json("rows", vouchers)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_VOUCHER)
            return financial.insert_voucher_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VOUCHER)
            financial.update_voucher_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VOUCHER)
            for vid in post.integer_list("ids"):
                financial.delete_voucher(session.dbo, session.user, vid)

class publish:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_INTERNET_PUBLISHER)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="page"), session.locale)
        mode = post["mode"]
        failed = False
        al.debug("publish started for mode %s" % mode, "code.publish", dbo)
        # If a publisher is already running and we have a mode, mark
        # a failure starting
        execstr = configuration.publisher_executing(dbo)
        failed = not execstr.startswith("NONE") and not execstr.endswith("100")
        if failed:
            al.debug("publish already running, not starting new publish", "code.publish", dbo)
        else:
            # If a publishing mode is requested, start that publisher
            # running on a background thread
            pc = extpublish.PublishCriteria(configuration.publisher_presets(dbo))
            if mode == "ftp":
                h = extpublish.HTMLPublisher(dbo, pc, session.user)
                h.start()
            elif mode == "pf": 
                pf = extpublish.PetFinderPublisher(dbo, pc)
                pf.start()
            elif mode == "ap": 
                ap = extpublish.AdoptAPetPublisher(dbo, pc)
                ap.start()
            elif mode == "rg": 
                rg = extpublish.RescueGroupsPublisher(dbo, pc)
                rg.start()
            elif mode == "mp": 
                mp = extpublish.MeetAPetPublisher(dbo, pc)
                mp.start()
            elif mode == "hlp": 
                mp = extpublish.HelpingLostPetsPublisher(dbo, pc)
                mp.start()
            elif mode == "pl": 
                mp = extpublish.PetLinkPublisher(dbo, pc)
                mp.start()
            elif mode == "pr": 
                mp = extpublish.PetRescuePublisher(dbo, pc)
                mp.start()
            elif mode == "p9": 
                pn = extpublish.Pets911Publisher(dbo, pc)
                pn.start()
            elif mode == "st": 
                st = extpublish.SmartTagPublisher(dbo, pc)
                st.start()
            elif mode == "ptuk": 
                mp = extpublish.PETtracUKPublisher(dbo, pc)
                mp.start()
            elif mode == "veha":
                mp = extpublish.HomeAgainPublisher(dbo, pc)
                mp.start()
            elif mode == "vear":
                mp = extpublish.AKCReunitePublisher(dbo, pc)
                mp.start()
        s = html.header(_("Publishing", l), session, "publish.js")
        c = html.controller_bool("failed", failed)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="poll"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "poll":
            users.check_permission(session, users.USE_INTERNET_PUBLISHER)
            return configuration.publisher_executing(dbo) + "|" + configuration.publisher_last_error(dbo)
        elif mode == "stop":
            configuration.publisher_stop(dbo, "Yes")
            configuration.publisher_executing(dbo, "NONE", 0)

class publish_logs:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(view = ""), session.locale)
        if post["view"] == "":
            title = _("Publisher Logs", l)
            s = html.header(title, session, "publish_logs.js")
            logs = dbfs.get_publish_logs(dbo)
            al.debug("viewing %d publishing logs" % len(logs), "code.publish_logs", dbo)
            c = html.controller_json("rows", logs)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            web.header("Cache-Control", "no-cache")
            return s
        else:
            al.debug("viewing log file %s" % post["view"], "code.publish_logs", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Cache-Control", "max-age=10000000")
            web.header("Content-Disposition", "inline; filename=\"%s\"" % post["view"])
            return dbfs.get_string_filepath(dbo, post["view"])

class publish_options:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("Publishing Options", l)
        s = html.header(title, session, "publish_options.js")
        c = html.controller_json("locations", extlookups.get_internal_locations(dbo))
        c += html.controller_str("publishurl", MULTIPLE_DATABASES_PUBLISH_URL)
        c += html.controller_bool("hasftpoverride", MULTIPLE_DATABASES_PUBLISH_FTP is not None and not configuration.publisher_ignore_ftp_override(dbo))
        c += html.controller_bool("hasfacebook", FACEBOOK_CLIENT_ID != "")
        c += html.controller_bool("hassmarttag", SMARTTAG_FTP_USER != "")
        c += html.controller_bool("hasvevendor", VETENVOY_US_VENDOR_PASSWORD != "")
        c += html.controller_bool("hasvesys", VETENVOY_US_VENDOR_USERID != "")
        c += html.controller_bool("haspetrescue", PETRESCUE_FTP_HOST != "")
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("styles", dbfs.get_html_publisher_templates(dbo))
        s += html.controller(c)
        al.debug("loaded lookups", "code.publish_options", dbo)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            configuration.csave(session.dbo, session.user, post)
            users.update_session(session)
        elif mode == "vesignup":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            userid, userpwd = extpublish.VetEnvoyUSMicrochipPublisher.signup(session.dbo, post)
            return "%s,%s" % (userid, userpwd)

class report:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPORT)
        post = utils.PostedData(web.input(id = "0", mode = "criteria"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        user = session.user
        crid = post.integer("id")
        # Make sure this user has a role that can view the report
        extreports.check_view_permission(session, crid)
        crit = extreports.get_criteria_controls(session.dbo, crid, locationfilter = session.locationfilter) 
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If the report doesn't take criteria, just show it
        if crit == "":
            al.debug("report %d has no criteria, displaying" % crid, "code.report", dbo)
            return extreports.execute(dbo, crid, user)
        # If we're in criteria mode (and there are some to get here), ask for them
        elif mode == "criteria":
            title = extreports.get_title(dbo, crid)
            al.debug("building criteria form for report %d %s" % (crid, title), "code.report", dbo)
            s = html.header(title, session, "report.js")
            s += html.heading(title)
            s += "<div id=\"criteriaform\">"
            s += "<input data-post=\"id\" type=\"hidden\" value=\"%d\" />" % crid
            s += "<input data-post=\"mode\" type=\"hidden\" value=\"exec\" />"
            s += crit
            s += "</div>"
            s += html.footing()
            s += html.footer()
            return s
        # The user has entered the criteria and we're in exec mode, unpack
        # the criteria and run the report
        elif mode == "exec":
            al.debug("got criteria (%s), executing report %d" % (str(post.data), crid), "code.report", dbo)
            p = extreports.get_criteria_params(dbo, crid, post)
            return extreports.execute(dbo, crid, user, p)

class report_images:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        title = _("Extra images", l)
        images = dbfs.get_report_images(dbo)
        al.debug("got %d extra images" % len(images), "code.report_images", dbo)
        s = html.header(title, session, "report_images.js")
        c = html.controller_json("rows", images)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="create", filechooser={}), session.locale)
        mode = post["mode"]
        if mode == "create":
            dbfs.upload_report_image(dbo, post.data.filechooser)
            users.update_session(session)
            raise web.seeother("report_images")
        elif mode == "delete":
            for i in post["ids"].split(","):
                if i != "" and not i.endswith("nopic.jpg"): dbfs.delete_filepath(dbo, "/reports/" + i)
            users.update_session(session)
        elif mode == "rename":
            dbfs.rename_file(dbo, "/reports", post["oldname"], post["newname"])

class reports:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPORT)
        l = session.locale
        dbo = session.dbo
        reports = extreports.get_reports(dbo)
        # Sanitise the HTMLBODY for sending to the front end
        for r in reports:
            r["HTMLBODY"] = html.escape_angle(r["HTMLBODY"])
        header = dbfs.get_string(dbo, "head.html", "/reports")
        if header == "": header = dbfs.get_string(dbo, "head.dat", "/reports")
        footer = dbfs.get_string(dbo, "foot.html", "/reports")
        if footer == "": footer = dbfs.get_string(dbo, "foot.dat", "/reports")
        title = _("Edit Reports", l)
        al.debug("editing %d reports" % len(reports), "code.reports", dbo)
        s = html.header(title, session, "reports.js")
        c = html.controller_json("categories", "|".join(extreports.get_categories(dbo)))
        c += html.controller_json("header", html.escape_angle(header))
        c += html.controller_json("footer", html.escape_angle(footer))
        c += html.controller_json("roles", users.get_roles(dbo))
        c += html.controller_json("rows", reports)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = dbo.locale
        if mode == "create":
            users.check_permission(session, users.ADD_REPORT)
            rid = extreports.insert_report_from_form(dbo, session.user, post)
            users.update_session(session)
            return rid
        elif mode == "update":
            users.check_permission(session, users.CHANGE_REPORT)
            extreports.update_report_from_form(dbo, session.user, post)
            users.update_session(session)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_REPORT)
            for rid in post.integer_list("ids"):
                extreports.delete_report(dbo, session.user, rid)
            users.update_session(session)
        elif mode == "sql":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            extreports.check_sql(dbo, session.user, post["sql"])
        elif mode == "genhtml":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            return extreports.generate_html(dbo, session.user, post["sql"])
        elif mode == "headfoot":
            users.check_permission(session, users.CHANGE_REPORT)
            dbfs.put_string_filepath(dbo, "/reports/head.html", post["header"])
            dbfs.put_string_filepath(dbo, "/reports/foot.html", post["footer"])
        elif mode == "smcomlist":
            return html.smcom_report_list_table(l, extreports.get_smcom_reports(dbo))
        elif mode == "smcominstall":
            users.check_permission(session, users.ADD_REPORT)
            extreports.install_smcom_reports(dbo, session.user, post.integer_list("ids"))
            users.update_session(session)

class roles:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_USER)
        dbo = session.dbo
        l = session.locale
        roles = users.get_roles(dbo)
        title = _("Edit roles", l)
        al.debug("editing %d roles" % len(roles), "code.roles", dbo)
        s = html.header(title, session, "roles.js")
        c = html.controller_json("rows", roles)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.EDIT_USER)
            users.insert_role_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_USER)
            users.update_role_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_USER)
            for rid in post.integer_list("ids"):
                users.delete_role(session.dbo, session.user, rid)

class search:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(), session.locale)
        q = post["q"]
        title = _("Search Results for '{0}'", l).format(q)
        results, timetaken, explain, sortname = extsearch.search(dbo, session, q)
        is_large_db = ""
        if dbo.is_large_db: is_large_db = " (indexed only)"
        al.debug("searched for '%s', got %d results in %s, sorted %s %s" % (q, len(results), timetaken, sortname, is_large_db), "code.search", dbo)
        s = html.header(title, session, "search.js")
        c = html.controller_json("results", results)
        c += html.controller_str("timetaken", str(round(timetaken, 2)))
        c += html.controller_str("explain", explain)
        c += html.controller_str("sortname", sortname)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class service:
    def handle(self):
        post = utils.PostedData(web.input(filechooser = {}), session.locale)
        contenttype, maxage, response = extservice.handler(post, remote_ip(),  web.ctx.env.get("HTTP_REFERER", ""))
        if contenttype == "redirect":
            raise web.seeother(response)
        else:
            web.header("Content-Type", contenttype)
            web.header("Cache-Control", "max-age=%d" % maxage)
            return response
    def POST(self):
        return self.handle()
    def GET(self):
        return self.handle()

class shelterview:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        l = session.locale
        dbo = session.dbo
        animals = extanimal.get_shelterview_animals(dbo, session.locationfilter)
        perrow = configuration.main_screen_animal_link_max(dbo)
        title = _("Shelter view", l)
        al.debug("got %d animals for shelterview" % (len(animals)), "code.shelterview", dbo)
        s = html.header(title, session, "shelterview.js")
        c = html.controller_json("animals", extanimal.get_animals_brief(animals))
        c += html.controller_json("locations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_int("perrow", perrow)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="move"), session.locale)
        mode = post["mode"]
        if mode == "move":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_location(session.dbo, session.user, post.integer("animalid"), post.integer("locationid"))

class sql:
    def check_disabled(self, dbo, dumptype):
        if DUMP_OVERRIDES[dumptype] == "disabled":
            al.error("attempted %s and it is disabled" % dumptype, "code.sql", dbo)
            raise utils.ASMPermissionError("%s is disabled" % dumptype)

    def check_url(self, dbo, dumptype):
        url = DUMP_OVERRIDES[dumptype]
        if not url.startswith("http"): return
        url = url.replace("{alias}", dbo.alias).replace("{database}", dbo.database)
        url = url.replace("{username}", dbo.username).replace("{password}", dbo.password)
        url = url.replace("{md5pass}", users.hash_password(dbo.password))
        raise web.seeother(url)

    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_SQL_INTERFACE)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="iface"), session.locale)
        mode = post["mode"]
        if mode == "iface":
            title = _("SQL Interface", l)
            al.debug("%s opened SQL interface" % str(session.user), "code.sql", dbo)
            s = html.header(title, session, "sql.js")
            c = html.controller_json("tables", dbupdate.TABLES + dbupdate.VIEWS)
            c += html.controller_json("dumpoverrides", DUMP_OVERRIDES)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            return s
        elif mode == "dumpsql":
            self.check_disabled(dbo, "dumpsql")
            self.check_url(dbo, "dumpsql")
            al.info("%s executed SQL database dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"dump.sql\"")
            return dbupdate.dump(dbo)
        elif mode == "dumpsqlnomedia":
            self.check_disabled(dbo, "dumpsqlnomedia")
            self.check_url(dbo, "dumpsqlnomedia")
            al.info("%s executed SQL database dump (without media)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"dump.sql\"")
            return dbupdate.dump(dbo, includeDBFS = False)
        elif mode == "dumpsqlasm2":
            self.check_disabled(dbo, "dumpsqlasm2")
            self.check_url(dbo, "dumpsqlasm2")
            # ASM2_COMPATIBILITY
            al.info("%s executed SQL database dump (ASM2 HSQLDB)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"asm2.sql\"")
            return dbupdate.dump_hsqldb(dbo)
        elif mode == "dumpsqlasm2nomedia":
            self.check_disabled(dbo, "dumpsqlasm2nomedia")
            self.check_url(dbo, "dumpsqlasm2nomedia")
            # ASM2_COMPATIBILITY
            al.info("%s executed SQL database dump (ASM2 HSQLDB, without media)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"asm2.sql\"")
            return dbupdate.dump_hsqldb(dbo, includeDBFS = False)
        elif mode == "animalcsv":
            al.debug("%s executed CSV animal dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"animal.csv\"")
            return utils.csv(extanimal.get_animal_find_advanced(dbo, { "logicallocation" : "all", "includedeceased": "true", "includenonshelter": "true" }))
        elif mode == "personcsv":
            al.debug("%s executed CSV person dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"person.csv\"")
            return utils.csv(extperson.get_person_find_simple(dbo, "", "all", True, 0))

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="exec", sql = "", sqlfile = "", table = ""), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        if mode == "cols":
            try:
                if post["table"].strip() == "": return ""
                rows = db.query(dbo, "SELECT * FROM %s LIMIT 1" % post["table"])
                if len(rows) == 0: return ""
                return "|".join(sorted(rows[0].iterkeys()))
            except Exception,err:
                al.error("%s" % str(err), "code.sql", dbo)
                raise utils.ASMValidationError(str(err))
        elif mode == "exec":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            utils.check_locked_db(session)
            sql = post["sql"].strip()
            return self.exec_sql(dbo, sql)
        elif mode == "execfile":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            utils.check_locked_db(session)
            sql = post["sqlfile"].strip()
            web.header("Content-Type", "text/plain")
            return self.exec_sql_from_file(dbo, sql)

    def exec_sql(self, dbo, sql):
        l = dbo.locale
        rowsaffected = 0
        try:
            for q in db.split_queries(sql):
                if q == "": continue
                al.info("%s query: %s" % (session.user, q), "code.sql", dbo)
                if q.lower().startswith("select") or q.lower().startswith("show"):
                    return html.table(db.query(dbo, q))
                else:
                    rowsaffected += db.execute(dbo, q)
            return _("{0} rows affected.", l).format(rowsaffected)
        except Exception,err:
            al.error("%s" % str(err), "code.sql", dbo)
            raise utils.ASMValidationError(str(err))

    def exec_sql_from_file(self, dbo, sql):
        l = dbo.locale
        output = []
        for q in db.split_queries(sql):
            try:
                if q == "": continue
                al.info("%s query: %s" % (session.user, q), "code.sql", dbo)
                if q.lower().startswith("select") or q.lower().startswith("show"):
                    output.append(str(db.query(dbo, q)))
                else:
                    rowsaffected = db.execute(dbo, q)
                    output.append(_("{0} rows affected.", l).format(rowsaffected))
            except Exception,err:
                al.error("%s" % str(err), "code.sql", dbo)
                output.append("ERROR: %s" % str(err))
        return "\n\n".join(output)

class stocklevel:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_STOCKLEVEL)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(newlevel = "0", sortexp = "0", viewlocation = "0"), session.locale)
        levels = extstock.get_stocklevels(dbo, post.integer("viewlocation"))
        al.debug("got %d stock levels" % len(levels), "code.stocklevel", dbo)
        title = _("Stock", l)
        s = html.header(title, session, "stocklevel.js")
        c = html.controller_json("stocklocations", extlookups.get_stock_locations(dbo))
        c += html.controller_str("stocknames", "|".join(extstock.get_stock_names(dbo)))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_str("stockunits", "|".join(extstock.get_stock_units(dbo)))
        c += html.controller_bool("newlevel", post.integer("newlevel") == 1)
        c += html.controller_bool("sortexp", post.integer("sortexp") == 1)
        c += html.controller_json("rows", levels)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "create", ids = "", duration = 0), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_STOCKLEVEL)
            if post.integer("quantity") == 1:
                return extstock.insert_stocklevel_from_form(session.dbo, post, session.user)
            else:
                for dummy in xrange(0, post.integer("quantity")):
                    extstock.insert_stocklevel_from_form(session.dbo, post, session.user)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_STOCKLEVEL)
            extstock.update_stocklevel_from_form(session.dbo, post, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_STOCKLEVEL)
            for sid in post.integer_list("ids"):
                extstock.delete_stocklevel(session.dbo, session.user, sid)
        elif mode == "lastname":
            users.check_permission(session, users.VIEW_STOCKLEVEL)
            return extstock.get_last_stock_with_name(session.dbo, post["name"])

class systemusers:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_USER)
        l = session.locale
        dbo = session.dbo
        title = _("Edit system users", l)
        user = users.get_users(dbo)
        roles = users.get_roles(dbo)
        al.debug("editing %d system users" % len(user), "code.systemusers", dbo)
        s = html.header(title, session, "users.js")
        c = html.controller_json("rows", user)
        c += html.controller_json("roles", roles)
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_USER)
            return users.insert_user_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_USER)
            users.update_user_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_USER)
            for uid in post.integer_list("ids"):
                users.delete_user(session.dbo, session.user, uid)
        elif mode == "reset":
            users.check_permission(session, users.EDIT_USER)
            for uid in post.integer_list("ids"):
                users.reset_password(session.dbo, uid)

class test:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TEST)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(newtest = "0", offset = "m31"), session.locale)
        test = extmedical.get_tests_outstanding(dbo, post["offset"], session.locationfilter)
        al.debug("got %d tests" % len(test), "code.test", dbo)
        title = _("Test Book", l)
        s = html.header(title, session, "test.js")
        c = html.controller_str("name", "test")
        c += html.controller_bool("newtest", post.integer("newtest") == 1)
        c += html.controller_json("rows", test)
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("testresults", extlookups.get_test_results(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "create", ids = ""), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_TEST)
            return extmedical.insert_test_from_form(session.dbo, session.user, post)
        if mode == "createbulk":
            users.check_permission(session, users.ADD_TEST)
            for animalid in post.integer_list("animals"):
                post.data["animal"] = str(animalid)
                extmedical.insert_test_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TEST)
            extmedical.update_test_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TEST)
            for vid in post.integer_list("ids"):
                extmedical.delete_test(session.dbo, session.user, vid)
        elif mode == "perform":
            users.check_permission(session, users.CHANGE_TEST)
            newdate = post.date("newdate")
            testresult = post.integer("testresult")
            for vid in post.integer_list("ids"):
                extmedical.complete_test(session.dbo, session.user, vid, newdate, testresult)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)

class traploan:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TRAPLOAN)
        dbo = session.dbo
        l = session.locale
        post = utils.PostedData(web.input(filter = "active"), session.locale)
        title = ""
        traploans = []
        if post["filter"] == "active":
            title = _("Active Trap Loans", l)
            traploans = extanimalcontrol.get_active_traploans(dbo)
        al.debug("got %d trap loans" % len(traploans), "code.traploan", dbo)
        s = html.header(title, session, "traploan.js")
        c = html.controller_str("name", "traploan")
        c += html.controller_str("title", title)
        c += html.controller_json("rows", traploans)
        c += html.controller_json("traptypes", extlookups.get_trap_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_TRAPLOAN)
            return extanimalcontrol.insert_traploan_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TRAPLOAN)
            extanimalcontrol.update_traploan_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TRAPLOAN)
            for lid in post.integer_list("ids"):
                extanimalcontrol.delete_traploan(session.dbo, session.user, lid)

class vaccination:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VACCINATION)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(newvacc = "0", offset = "m31"), session.locale)
        vacc = extmedical.get_vaccinations_outstanding(dbo, post["offset"], session.locationfilter)
        al.debug("got %d vaccinations" % len(vacc), "code.vaccination", dbo)
        title = _("Vaccination Book", l)
        s = html.header(title, session, "vaccination.js")
        c = html.controller_str("name", "vaccination")
        c += html.controller_bool("newvacc", post.integer("newvacc") == 1)
        c += html.controller_json("rows", vacc)
        c += html.controller_json("manufacturers", "|".join(extmedical.get_vacc_manufacturers(dbo)))
        c += html.controller_json("stockitems", extstock.get_stock_items(dbo))
        c += html.controller_json("stockusagetypes", extlookups.get_stock_usage_types(dbo))
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "create", ids = "", duration = 0), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_VACCINATION)
            return extmedical.insert_vaccination_from_form(session.dbo, session.user, post)
        if mode == "createbulk":
            users.check_permission(session, users.ADD_VACCINATION)
            for animalid in post.integer_list("animals"):
                post.data["animal"] = str(animalid)
                extmedical.insert_vaccination_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VACCINATION)
            extmedical.update_vaccination_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VACCINATION)
            for vid in post.integer_list("ids"):
                extmedical.delete_vaccination(session.dbo, session.user, vid)
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = post.date("newdate")
            rescheduledate = post.date("rescheduledate")
            for vid in post.integer_list("ids"):
                extmedical.complete_vaccination(session.dbo, session.user, vid, newdate)
                if rescheduledate is not None:
                    extmedical.reschedule_vaccination(session.dbo, session.user, vid, rescheduledate)
            if post.integer("item") != -1:
                extstock.deduct_stocklevel_from_form(session.dbo, session.user, post)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = post.date("newdate")
            for vid in post.integer_list("ids"):
                extmedical.update_vaccination_required(session.dbo, session.user, vid, newdate)

class waitinglist:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extwaitinglist.get_waitinglist_by_id(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        al.debug("opened waiting list %s %s" % (a["OWNERNAME"], a["SPECIESNAME"]), "code.waitinglist", dbo)
        s = html.header(title, session, "waitinglist.js")
        c = html.controller_json("animal", a)
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "waitinglist"))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(mode="save"), session.locale)
        mode = post["mode"]
        if mode == "save":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            extwaitinglist.update_waitinglist_from_form(dbo, post, session.user)
        elif mode == "email":
            users.check_permission(session, users.VIEW_WAITING_LIST)
            if not extwaitinglist.send_email_from_form(dbo, session.user, post):
                raise utils.ASMError(_("Failed sending email", l))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_WAITING_LIST)
            extwaitinglist.delete_waitinglist(dbo, session.user, post.integer("id"))
        elif mode == "toanimal":
            users.check_permission(session, users.ADD_ANIMAL)
            return str(extwaitinglist.create_animal(dbo, session.user, post.integer("id")))

class waitinglist_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extwaitinglist.get_waitinglist_by_id(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.WAITINGLIST, post.integer("id"))
        al.debug("got %d diaries" % len(diaries), "code.waitinglist_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_str("name", "waitinglist_diary")
        c += html.controller_int("linkid", a["WLID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.WAITINGLIST, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in post.integer_list("ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in post.integer_list("ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class waitinglist_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0, filter = -2), session.locale)
        logfilter = post.integer("filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extwaitinglist.get_waitinglist_by_id(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        logs = extlog.get_logs(dbo, extlog.WAITINGLIST, post.integer("id"), logfilter)
        al.debug("got %d logs" % len(logs), "code.waitinglist_diary", dbo)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "waitinglist_log")
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.WAITINGLIST, post.integer("linkid"), post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in post.integer_list("ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class waitinglist_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(id = 0), session.locale)
        a = extwaitinglist.get_waitinglist_by_id(dbo, post.integer("id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        m = extmedia.get_media(dbo, extmedia.WAITINGLIST, post.integer("id"))
        al.debug("got %d media" % len(m), "code.waitinglist_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", post.integer("id"))
        c += html.controller_int("linktypeid", extmedia.WAITINGLIST)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False), session.locale)
        mode = post["mode"]
        dbo = session.dbo
        l = session.locale
        linkid = post.integer("linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.WAITINGLIST, linkid, post)
            raise web.seeother("waitinglist_media?id=%d" % post.integer("linkid"))
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.WAITINGLIST, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=waitinglist_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.WAITINGLIST, linkid, post)
            raise web.seeother("waitinglist_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, post.integer("mediaid"), post["comments"])
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = post["email"]
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in post.integer_list("ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in post.integer_list("ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = post.integer_list("ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class waitinglist_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        title = _("Add waiting list", l)
        s = html.header(title, session, "waitinglist_new.js")
        c = html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_WAITING_LIST)
        dbo = session.dbo
        post = utils.PostedData(web.input(), session.locale)
        return str(extwaitinglist.insert_waitinglist_from_form(dbo, post, session.user))

class waitinglist_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        urgencies = extlookups.get_urgencies(dbo)
        lowest_priority = len(urgencies)
        post = utils.PostedData(web.input(priorityfloor = lowest_priority, includeremoved = 0, species = -1, size = -1, 
            namecontains = "", addresscontains = "", descriptioncontains = ""), session.locale)
        rows = extwaitinglist.get_waitinglist(dbo, post.integer("priorityfloor"), post.integer("species"), post.integer("size"),
            post["addresscontains"], post.integer("includeremoved"), post["namecontains"], post["descriptioncontains"])
        title = _("Waiting List", l)
        al.debug("found %d results" % (len(rows)), "code.waitinglist_results", dbo)
        s = html.header(title, session, "waitinglist_results.js")
        c = html.controller_json("rows", rows)
        c += html.controller_str("seladdresscontains", post["addresscontains"])
        c += html.controller_str("seldescriptioncontains", post["descriptioncontains"])
        c += html.controller_int("selincluderemoved", post.integer("includeremoved"))
        c += html.controller_str("selnamecontains", post["namecontains"])
        c += html.controller_int("selpriorityfloor", post.integer("priorityfloor"))
        c += html.controller_int("selspecies", post.integer("species"))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("urgencies", urgencies)
        c += html.controller_json("yesno", extlookups.get_yesno(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "delete":
            users.check_permission(session, users.DELETE_WAITING_LIST)
            for wid in post.integer_list("ids"):
                extwaitinglist.delete_waitinglist(session.dbo, session.user, wid)
        elif mode == "complete":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            for wid in post.integer_list("ids"):
                extwaitinglist.update_waitinglist_remove(session.dbo, session.user, wid)
        elif mode == "highlight":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            for wid in post.integer_list("ids"):
                extwaitinglist.update_waitinglist_highlight(session.dbo, wid, post["himode"])

if __name__ == "__main__":
    app.run()

