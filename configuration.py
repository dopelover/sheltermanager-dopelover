#!/usr/bin/python

import audit
import db
import i18n
import time
from sitedefs import LOCALE, TIMEZONE

QUICKLINKS_SET = {
    1: ("animal_find", "asm-icon-animal-find", i18n._("Find animal")),
    2: ("animal_new", "asm-icon-animal-add", i18n._("Add a new animal")),
    3: ("log_new", "asm-icon-log", i18n._("Add a log entry")),
    4: ("litters", "asm-icon-litter", i18n._("Edit litters")),
    5: ("person_find", "asm-icon-person-find", i18n._("Find person")),
    6: ("person_new", "asm-icon-person-add", i18n._("Add a new person")),
    7: ("lostanimal_find", "asm-icon-animal-lost-find", i18n._("Find a lost animal")),
    8: ("foundanimal_find", "asm-icon-animal-found-find", i18n._("Find a found animal")),
    9: ("lostanimal_new", "asm-icon-animal-lost-add", i18n._("Add a lost animal")),
    10: ("foundanimal_new", "asm-icon-animal-found-add", i18n._("Add a found animal")),
    11: ("lostfound_match", "asm-icon-match", i18n._("Match lost and found animals")),
    12: ("diary_edit_my?newnote=1", "asm-icon-diary", i18n._("Add a diary note")),
    13: ("diary_edit_my", "asm-icon-diary", i18n._("My diary notes")),
    14: ("diary_edit", "asm-icon-diary", i18n._("All diary notes")),
    15: ("diarytasks", "asm-icon-diary-task", i18n._("Edit diary tasks")),
    16: ("waitinglist_new", "asm-icon-waitinglist", i18n._("Add an animal to the waiting list")),
    17: ("waitinglist_results", "asm-icon-waitinglist", i18n._("Edit the current waiting list")),
    18: ("move_reserve", "asm-icon-reservation", i18n._("Reserve an animal")),
    19: ("move_foster", "", i18n._("Foster an animal")),
    20: ("move_adopt", "asm-icon-person", i18n._("Adopt an animal")),
    21: ("move_deceased", "asm-icon-death", i18n._("Mark an animal deceased")),
    22: ("move_book_recent_adoption", "", i18n._("Return an animal from adoption")),
    23: ("move_book_recent_other", "", i18n._("Return an animal from another movement")),
    24: ("move_book_reservation", "asm-icon-reservation", i18n._("Reservation book")),
    25: ("move_book_foster", "asm-icon-book", i18n._("Foster book")),
    26: ("move_book_retailer", "asm-icon-book", i18n._("Retailer book")),
    27: ("vaccination?newvacc=1", "", i18n._("Add a vaccination")),
    28: ("vaccination", "asm-icon-vaccination", i18n._("Vaccination book")),
    29: ("medical?newmed=1", "", i18n._("Add a medical regimen")),
    30: ("medical", "asm-icon-medical", i18n._("Medical book")),
    32: ("publish_options", "asm-icon-settings", i18n._("Set publishing options")),
    31: ("search?q=forpublish", "asm-icon-animal", i18n._("Up for adoption")),
    33: ("search?q=deceased", "asm-icon-death", i18n._("Recently deceased")),
    34: ("search?q=notforadoption", "", i18n._("Not for adoption")),
    35: ("search?q=onshelter", "asm-icon-animal", i18n._("Shelter animals")),
    36: ("accounts", "asm-icon-accounts", i18n._("Accounts")),
    37: ("donation_receive", "asm-icon-donation", i18n._("Receive a donation")),
    38: ("move_transfer", "", i18n._("Transfer an animal")),
    39: ("medicalprofile", "", i18n._("Medical profiles")),
    40: ("shelterview", "asm-icon-location", i18n._("Shelter view")),
    41: ("move_book_trial_adoption", "asm-icon-trial", i18n._("Trial adoption book")),
    42: ("incident_new", "asm-icon-call", i18n._("Report a new incident")),
    43: ("incident_find", "asm-icon-call", i18n._("Find an incident")),
    44: ("incident_map", "asm-icon-map", i18n._("Map of active incidents")),
    45: ("traploan?filter=active", "asm-icon-traploan", i18n._("Trap loans")),
    46: ("calendarview", "asm-icon-calendar", i18n._("Calendar view")),
    47: ("calendarview?ev=d", "asm-icon-calendar", i18n._("Diary calendar")),
    48: ("calendarview?ev=vmt", "asm-icon-calendar", i18n._("Medical calendar")),
    49: ("calendarview?ev=p", "asm-icon-calendar", i18n._("Payment calendar")),
    50: ("calendarview?ev=ol", "asm-icon-calendar", i18n._("Animal control calendar")),
    51: ("stocklevel", "asm-icon-stock", i18n._("Stock Levels"))
}

# Default configuration values for unset items. This is so they
# still get shown correctly in the options screens.
DEFAULTS = {
    "AdvancedFindAnimalOnShelter": "Yes",
    "AgeGroup1": "0.5",
    "AgeGroup1Name": "Baby",
    "AgeGroup2": "2",
    "AgeGroup2Name": "Young Adult",
    "AgeGroup3": "7",
    "AgeGroup3Name": "Adult",
    "AgeGroup4": "50",
    "AgeGroup4Name": "Senior",
    "AllowDuplicateMicrochip": "No",
    "AllowNonANMicrochip": "No",
    "AnimalFiguresSplitEntryReason": "No",
    "AnnualFiguresShowBabies": "Yes",
    "AnnualFiguresShowBabiesType": "Yes",
    "AnnualFiguresBabyMonths" : "6",
    "AutoCancelReservesDays": "14",
    "AutoDefaultShelterCode": "Yes",
    "AutoInsuranceStart": "0",
    "AutoInsuranceEnd": "0",
    "AutoInsuranceNext": "0",
    "AutoRemoveHoldDays": "0",
    "AutoRemoveIncomingFormsDays": "14",
    "AFDefaultBreed": "221",
    "AFDefaultCoatType": "0",
    "AFDefaultColour": "1",
    "AFDefaultDeathReason": "1",
    "AFDefaultDonationType": "1",
    "AFDefaultEntryReason": "4",
    "AFDefaultLocation": "1",
    "AFDefaultLogFilter": "-1",
    "AFDefaultReturnReason": "4",
    "AFDefaultSize": "1",
    "AFDefaultSpecies": "2",
    "AFDefaultType": "11",
    "AFDefaultTestType": "1",
    "AFDefaultVaccinationType": "1",
    "AFNonShelterType": "40",
    "BoardingCostType": "1",
    "CancelReservesOnAdoption": "Yes",
    "CreateBoardingCostOnAdoption": "Yes",
    "CreateDonationTrx": "Yes",
    "CodingFormat": "TYYYNNN",
    "ShortCodingFormat": "NNT",
    "DefaultDailyBoardingCost": "2000",
    "DefaultDateBroughtIn": "Yes",
    "DefaultIncidentType": "1",
    "DefaultMediaNotesFromFile": "Yes",
    "DisableAnimalControl": "No",
    "DisableStockControl": "No",
    "DisableTrapLoan": "No",
    "DisableAsilomar": "No",
    "DisableDocumentRepo": "No",
    "DisableOnlineForms": "No",
    "DisableRetailer": "No",
    "DocumentWordProcessor": "HTML",
    "DonationTrxOverride": "No",
    "DontShowCombi": "Yes",
    "DontShowHeartworm": "Yes",
    "EmailDiaryNotes": "Yes", 
    "EmailMessages": "Yes", 
    "EmblemAlwaysLocation": "No",
    "EmblemCrueltyCase": "Yes",
    "EmblemDeceased": "Yes",
    "EmblemHold": "Yes",
    "EmblemNonShelter": "Yes",
    "EmblemNotForAdoption": "Yes",
    "EmblemQuarantine": "Yes",
    "EmblemReserved": "Yes",
    "EmblemTrialAdoption": "Yes",
    "EmblemUnneutered": "Yes",
    "FacebookEnabled": "Yes",
    "FacebookTemplate": "$$ANIMALNAME$$, $$SEX$$ $$SPECIESNAME$$ aged $$DISPLAYAGE$$. $$ANIMALCOMMENTS$$",
    "FacebookLog": "No",
    "FacebookLogType": "3",
    "FacebookPostAs": "me",
    "FacebookPageName": "",
    "FancyTooltips": "No",
    "FosterOnShelter": "Yes",
    "IncomingMediaScaling": "640x640",
    "GenerateDocumentLog": "No",
    "GenerateDocumentLogType": "5",
    "InactivityTimer": "No",
    "InactivityTimeout": "20", 
    "IncludeOffShelterMedical": "No",
    "IncludeIncompleteMedicalDoc": "Yes",
    "Locale": "en",
    "LocationChangeLog": "Yes",
    "LocationChangeLogType": "3",
    "MainScreenAnimalLinkMode": "recentlychanged",
    "MainScreenAnimalLinkMax": "9",
    "ManualCodes": "No",
    "MatchSpecies": "5",
    "MatchBreed": "5",
    "MatchAge": "5",
    "MatchSex": "5",
    "MatchAreaLost": "5",
    "MatchFeatures": "5",
    "MatchPostcode": "5",
    "MatchColour": "5",
    "MatchIncludeShelter": "Yes",
    "MatchWithin2Weeks": "5",
    "MatchPointFloor": "20",
    "MaxMediaFileSize": "1000",
    "MeetAPetBaseURL": "http://meetapet.com/api_crud/",
    "MeetAPetKey" : "haRQPthLgW",
    "MovementDonationsDefaultDue": "No",
    "MovementNumberOverride": "No",
    "JSWindowPrint": "Yes",
    "OwnerAddressCheck": "Yes",
    "OwnerNameCheck": "Yes",
    "OwnerNameFormat": "{ownername}",
    "OwnerSearchColumns": "OwnerCode,OwnerName,OwnerSurname," \
        "MembershipNumber,IsBanned,IDCheck,OwnerAddress," \
        "OwnerTown,OwnerCounty,OwnerPostcode,HomeTelephone,WorkTelephone," \
        "MobileTelephone,EmailAddress",
    "PicturesInBooks": "Yes",
    "PDFInline": "Yes",
    "PublisherUseComments": "Yes",
    "PublisherIgnoreFTPOverride": "No",
    "QuicklinksID": "40,46,25,31,34,19,20",
    "QuicklinksHomeScreen": "Yes",
    "QuicklinksAllScreens": "No",
    "RecordSearchLimit": "1000",
    "RetailerOnShelter": "Yes",
    "ReturnFostersOnAdoption": "Yes",
    "ScalePDFs": "Yes", 
    "SearchColumns": "AnimalName,Image,ShelterCode,ShelterLocation,SpeciesID,BreedName," \
        "Sex, AnimalAge, Size, BaseColourID, Markings, IdentichipNumber, DateBroughtIn",
    "SearchSort": "3",
    "SecondDonationOnMove": "No",
    "ShelterViewDefault": "location",
    "ShelterViewShowCodes": "No",
    "ShowCostAmount": "Yes",
    "ShowCostPaid": "No",
    "ShowAlertsHomePage": "Yes", 
    "ShowStatsHomePage": "thismonth", 
    "ShowFirstTime": "Yes",
    "ShowILOffShelter": "Yes",
    "ShowPersonMiniMap": "Yes",
    "ShowSearchGo": "No", 
    "SystemTheme": "smoothness",
    "Timezone": "-5",
    "TrialAdoptions": "No",
    "TrialOnShelter": "No",
    "UseAutoInsurance": "No",
    "UseShortShelterCodes": "Yes", 
    "WaitingListViewColumns": "Rank,OwnerName,OwnerAddress," \
        "HomeTelephone,EmailAddress,DatePutOnList,TimeOnList," \
        "DateRemovedFromList,Urgency,SpeciesID,Size,AnimalDescription",
    "WaitingListDefaultUrgency": "3",
    "WaitingListUrgencyUpdatePeriod": "14",
    "WaitingListUseMultipleHighlights": "No",
    "WarnACTypeChange": "Yes",
    "WarnBroughtIn": "Yes",
    "WarnMultipleReserves": "Yes", 
    "WarnNoPendingVacc": "Yes",
    "WarnNoHomeCheck": "Yes",
    "WarnBannedOwner": "Yes",
    "WarnOOPostcode": "Yes",
    "WarnSimilarAnimalName": "Yes"
}

def cstring(dbo, key, default = ""):
    try:
        rows = db.query(dbo, "SELECT ITEMVALUE FROM configuration WHERE ITEMNAME LIKE '%s'" % key)
        if len(rows) == 0: return default
        v = rows[0]["ITEMVALUE"]
        if v == "": return default
        return v
    except:
        return default
    return default

def cboolean(dbo, key, default = False):
    defstring = "No"
    if default: defstring = "Yes"
    v = cstring(dbo, key, defstring)
    return v == "Yes" or v == "True"

def cint(dbo, key, default = 0):
    defstring = str(default)
    v = cstring(dbo, key, defstring)
    try:
        return int(v)
    except:
        return int(0)

def cfloat(dbo, key, default = 0.0):
    defstring = str(default)
    v = cstring(dbo, key, defstring)
    try:
        return float(v)
    except:
        return float(0)

def cset(dbo, key, value = "", ignoreDBLock = False):
    """
    Update a configuration item in the table.
    """
    # MySQL returns wrong affected value (AFFECTED_ROWS switch in newer), delete before insert
    if dbo.dbtype == "MYSQL":
        db.execute(dbo, "DELETE FROM configuration WHERE ItemName LIKE %s" % db.ds(key), ignoreDBLock)
        db.execute(dbo, "INSERT INTO configuration (ItemName, ItemValue) VALUES (%s, %s)" % (db.ds(key), db.ds(value)), ignoreDBLock)
    else:
        # Otherwise, attempt the update and if no rows matched, do the insert
        affected = db.execute(dbo, "UPDATE configuration SET ItemValue = %s WHERE ItemName LIKE %s" % (db.ds(value), db.ds(key)))
        if affected == 0:
            db.execute(dbo, "INSERT INTO configuration VALUES (%s, %s)" % ( db.ds(key), db.ds(value) ), ignoreDBLock)

def cset_db(dbo, key, value = ""):
    """
    Updates a configuration entry that could take place during a
    database update, so needs to ignore the locked flag.
    """
    cset(dbo, key, value, True)

def csave(dbo, username, post):
    """
    Takes configuration data passed as a web post and saves it to the
    database.
    """
    def valid_code(s):
        """
        Returns True if s has a valid code portion in it
        """
        VALID_CODES = ("NN", "NNN", "UUUU", "UUUUUUUUUU")
        for v in VALID_CODES:
            if s.find(v) != -1:
                return True
        return False

    for k in post.data.iterkeys():
        v = post[k]
        if k == "mode":
            pass
        elif k == "CodingFormat":
            # If there's no valid N or U tokens in there, it's not valid so reset to
            # the default.
            if not valid_code(v):
                cset(dbo, k, "TYYYYNNN")
            else:
                cset(dbo, k, v)
        elif k == "ShortCodingFormat":
            # If there's no N or U in there, it's not valid so reset to
            # the default.
            if not valid_code(v):
                cset(dbo, k, "NNT")
            else:
                cset(dbo, k, v)
        elif k == "DefaultDailyBoardingCost":
            # Need to handle currency fields differently
            cset(dbo, k, post.db_integer(k))
        elif k.startswith("rc:"):
            # It's a NOT check
            if v == "checked": v = "No"
            if v == "off": v = "Yes"
            cset(dbo, k[3:], v)
        elif v == "checked" or v == "off":
            # It's a checkbox
            if v == "checked": v = "Yes"
            if v == "off": v = "No"
            cset(dbo, k, v)
        else:
            # Must be a string
            cset(dbo, k, v)
    audit.edit(dbo, username, "configuration", str(post.data))

def account_period_totals(dbo):
    return cboolean(dbo, "AccountPeriodTotals")

def accounting_period(dbo):
    return cstring(dbo, "AccountingPeriod")

def adoptapet_user(dbo):
    return cstring(dbo, "SaveAPetFTPUser")

def adoptapet_password(dbo):
    return cstring(dbo, "SaveAPetFTPPassword")

def advanced_find_animal(dbo):
    return cboolean(dbo, "AdvancedFindAnimal")

def advanced_find_animal_on_shelter(dbo):
    return cboolean(dbo, "AdvancedFindAnimalOnShelter", DEFAULTS["AdvancedFindAnimalOnShelter"] == "Yes")

def age_group(dbo, band):
    return cfloat(dbo, "AgeGroup%d" % band)

def age_groups(dbo):
    groups = []
    for i in range(1, 9):
        groupname = cstring(dbo, "AgeGroup%dName" % i)
        if groupname != "":
            groups.append(groupname)
    return groups

def age_group_name(dbo, band):
    return cstring(dbo, "AgeGroup%dName" % band)

def all_diary_home_page(dbo):
    return cboolean(dbo, "AllDiaryHomePage")

def allow_duplicate_microchip(dbo):
    return cboolean(dbo, "AllowDuplicateMicrochip", DEFAULTS["AllowDuplicateMicrochip"] == "Yes")

def animal_figures_split_entryreason(dbo):
    return cboolean(dbo, "AnimalFiguresSplitEntryReason", DEFAULTS["AnimalFiguresSplitEntryReason"] == "Yes")

def animal_search_columns(dbo):
    return cstring(dbo, "SearchColumns", DEFAULTS["SearchColumns"])

def annual_figures_show_babies(dbo):
    return cboolean(dbo, "AnnualFiguresShowBabies", DEFAULTS["AnnualFiguresShowBabies"] == "Yes")

def annual_figures_show_babies_type(dbo):
    return cboolean(dbo, "AnnualFiguresShowBabiesType", DEFAULTS["AnnualFiguresShowBabiesType"] == "Yes")

def annual_figures_baby_months(dbo):
    return cint(dbo, "AnnualFiguresBabyMonths", int(DEFAULTS["AnnualFiguresBabyMonths"]))

def auto_cancel_reserves_days(dbo):
    return cint(dbo, "AutoCancelReservesDays", int(DEFAULTS["AutoCancelReservesDays"]))

def auto_cancel_hold_days(dbo):
    return cint(dbo, "AutoCancelHoldDays", int(DEFAULTS["AutoCancelHoldDays"]))

def auto_insurance_next(dbo, newins = 0):
    if newins == 0:
        return cint(dbo, "AutoInsuranceNext")
    else:
        cset(dbo, "AutoInsuranceNext", str(newins))

def auto_media_notes(dbo):
    return cboolean(dbo, "AutoMediaNotes")

def auto_not_for_adoption(dbo):
    return cboolean(dbo, "AutoNotForAdoption")

def auto_remove_incoming_forms_days(dbo):
    return cint(dbo, "AutoRemoveIncomingFormsDays", int(DEFAULTS["AutoRemoveIncomingFormsDays"]))

def avid_org_postcode(dbo):
    return cstring(dbo, "AvidOrgPostcode")

def avid_org_name(dbo):
    return cstring(dbo, "AvidOrgName")

def avid_org_serial(dbo):
    return cstring(dbo, "AvidOrgSerial")

def avid_org_password(dbo):
    return cstring(dbo, "AvidOrgPassword")

def cancel_reserves_on_adoption(dbo):
    return cboolean(dbo, "CancelReservesOnAdoption", DEFAULTS["CancelReservesOnAdoption"] == "Yes")

def coding_format(dbo):
    return cstring(dbo, "CodingFormat", DEFAULTS["CodingFormat"])

def coding_format_short(dbo):
    return cstring(dbo, "ShortCodingFormat", DEFAULTS["ShortCodingFormat"])

def create_donation_trx(dbo):
    return cboolean(dbo, "CreateDonationTrx")

def dbv(dbo, v = None):
    if v is None:
        return cstring(dbo, "DBV", "2870")
    else:
        cset_db(dbo, "DBV", v)

def db_lock(dbo):
    """
    Locks the database for updates, returns True if the lock was
    successful.
    """
    if cboolean(dbo, "DBLock"): return False
    cset_db(dbo, "DBLock", "Yes")
    return True

def db_unlock(dbo):
    """
    Marks the database as unlocked for updates
    """
    cset_db(dbo, "DBLock", "No")

def db_view_seq_version(dbo, newval = ""):
    if newval == "":
        return cstring(dbo, "DBViewSeqVersion")
    else:
        cset(dbo, "DBViewSeqVersion", newval)

def default_account_view_period(dbo):
    return cint(dbo, "DefaultAccountViewPeriod")

def default_breed(dbo):
    return cint(dbo, "AFDefaultBreed", 1)

def default_broughtinby(dbo):
    return cint(dbo, "DefaultBroughtInBy", 0)

def default_coattype(dbo):
    return cint(dbo, "AFDefaultCoatType", 1)

def default_colour(dbo):
    return cint(dbo, "AFDefaultColour", 1)

def default_daily_boarding_cost(dbo):
    return cint(dbo, "DefaultDailyBoardingCost", int(DEFAULTS["DefaultDailyBoardingCost"]))

def default_death_reason(dbo):
    return cint(dbo, "AFDefaultDeathReason", 1)

def default_donation_type(dbo):
    return cint(dbo, "AFDefaultDonationType", 1)

def default_entry_reason(dbo):
    return cint(dbo, "AFDefaultEntryReason", 4)

def default_incident(dbo):
    return cint(dbo, "DefaultIncidentType", 1)

def default_location(dbo):
    return cint(dbo, "AFDefaultLocation", 1)

def default_log_filter(dbo):
    return cint(dbo, "AFDefaultLogFilter", 0)

def default_media_notes_from_file(dbo):
    return cboolean(dbo, "DefaultMediaNotesFromFile", DEFAULTS["DefaultMediaNotesFromFile"] == "Yes")

def default_nonsheltertype(dbo):
    return cint(dbo, "AFNonShelterType", 40)

def default_return_reason(dbo):
    return cint(dbo, "AFDefaultReturnReason", 4)

def default_size(dbo):
    return cint(dbo, "AFDefaultSize", 1)

def default_species(dbo):
    return cint(dbo, "AFDefaultSpecies", 2)

def default_type(dbo):
    return cint(dbo, "AFDefaultType", 11)

def default_vaccination_type(dbo):
    return cint(dbo, "AFDefaultVaccinationType", 1)

def disable_asilomar(dbo):
    return cboolean(dbo, "DisableAsilomar", DEFAULTS["DisableAsilomar"] == "Yes")

def disable_investigation(dbo):
    return cboolean(dbo, "DisableInvestigation", DEFAULTS["DisableInvestigation"] == "Yes")

def donation_target_account(dbo):
    return cint(dbo, "DonationTargetAccount", 0)

def donation_account_mappings(dbo):
    m = {}
    cm = cstring(dbo, "DonationAccountMappings")
    sm = cm.split(",")
    for x in sm:
        if x.find("=") != -1:
            bt = x.split("=")
            donationtypeid = bt[0]
            accountid = bt[1]
            m[donationtypeid] = accountid
    return m

def donation_trx_override(dbo):
    return cboolean(dbo, "DonationTrxOverride", DEFAULTS["DonationTrxOverride"] == "Yes")

def email(dbo):
    return cstring(dbo, "EmailAddress")

def email_diary_notes(dbo):
    return cboolean(dbo, "EmailDiaryNotes", DEFAULTS["EmailDiaryNotes"] == "Yes")

def email_messages(dbo):
    return cboolean(dbo, "EmailMessages", DEFAULTS["EmailMessages"] == "Yes")

def facebook_enabled(dbo):
    return cboolean(dbo, "FacebookEnabled", DEFAULTS["FacebookEnabled"] == "Yes")

def facebook_log(dbo):
    return cboolean(dbo, "FacebookLog", DEFAULTS["FacebookLog"] == "Yes")

def facebook_log_type(dbo):
    return cint(dbo, "FacebookLogType", DEFAULTS["FacebookLogType"])

def facebook_pagename(dbo):
    return cstring(dbo, "FacebookPageName", DEFAULTS["FacebookPageName"])

def facebook_post_as(dbo):
    return cstring(dbo, "FacebookPostAs", DEFAULTS["FacebookPostAs"])

def facebook_template(dbo):
    return cstring(dbo, "FacebookTemplate", DEFAULTS["FacebookTemplate"])

def foster_on_shelter(dbo):
    return cboolean(dbo, "FosterOnShelter", DEFAULTS["FosterOnShelter"] == "Yes")

def ftp_host(dbo):
    return cstring(dbo, "FTPURL")

def ftp_user(dbo):
    return cstring(dbo, "FTPUser")

def ftp_passive(dbo):
    return cboolean(dbo, "FTPPassive", True)

def ftp_password(dbo):
    return cstring(dbo, "FTPPassword")

def ftp_port(dbo):
    return cint(dbo, "FTPPort", 21)

def ftp_root(dbo):
    return cstring(dbo, "FTPRootDirectory")

def generate_document_log(dbo):
    return cboolean(dbo, "GenerateDocumentLog", False)

def generate_document_log_type(dbo):
    return cint(dbo, "GenerateDocumentLogType", 0)

def geo_provider_override(dbo):
    return cstring(dbo, "GeoProviderOverride")

def geo_provider_key_override(dbo):
    return cstring(dbo, "GeoProviderKeyOverride")

def get_map(dbo):
    def escape(s):
        if s is None: return ""
        s = str(s)
        return s.replace("\"", "\\\"")
    rows = db.query(dbo, "SELECT ITEMNAME, ITEMVALUE FROM configuration ORDER BY ITEMNAME")
    cmap = DEFAULTS.copy()
    for r in rows:
        cmap[r["ITEMNAME"]] = escape(r["ITEMVALUE"])
    return cmap

def include_incomplete_medical_doc(dbo):
    return cboolean(dbo, "IncludeIncompleteMedicalDoc", DEFAULTS["IncludeIncompleteMedicalDoc"] == "Yes")

def include_off_shelter_medical(dbo):
    return cboolean(dbo, "IncludeOffShelterMedical", DEFAULTS["IncludeOffShelterMedical"] == "Yes")

def incoming_media_scaling(dbo):
    return cstring(dbo, "IncomingMediaScaling", DEFAULTS["IncomingMediaScaling"])

def js_window_print(dbo):
    return cboolean(dbo, "JSWindowPrint", DEFAULTS["JSWindowPrint"] == "Yes")

def locale(dbo):
    return cstring(dbo, "Locale", LOCALE)

def location_change_log(dbo):
    return cboolean(dbo, "LocationChangeLog", DEFAULTS["LocationChangeLog"] == "Yes")

def location_change_log_type(dbo):
    return cint(dbo, "LocationChangeLogType", DEFAULTS["LocationChangeLogType"])

def lookingfor_last_match_count(dbo, newcount = -1):
    if newcount == -1:
        return cint(dbo, "LookingForLastMatchCount", 0)
    else:
        cset(dbo, "LookingForLastMatchCount", "%d" % newcount)

def main_screen_animal_link_mode(dbo):
    return cstring(dbo, "MainScreenAnimalLinkMode", DEFAULTS["MainScreenAnimalLinkMode"])

def main_screen_animal_link_max(dbo):
    return cint(dbo, "MainScreenAnimalLinkMax", int(DEFAULTS["MainScreenAnimalLinkMax"]))

def manual_codes(dbo):
    return cboolean(dbo, "ManualCodes", DEFAULTS["ManualCodes"] == "Yes")

def map_link_override(dbo):
    return cstring(dbo, "MapLinkOverride")

def map_provider_override(dbo):
    return cstring(dbo, "MapProviderOverride")

def match_species(dbo):
    return cint(dbo, "MatchSpecies", 5)

def match_breed(dbo):
    return cint(dbo, "MatchBreed", 5)

def match_age(dbo):
    return cint(dbo, "MatchAge", 5)

def match_sex(dbo):
    return cint(dbo, "MatchSex", 5)

def match_area_lost(dbo):
    return cint(dbo, "MatchAreaLost", 5)

def match_features(dbo):
    return cint(dbo, "MatchFeatures", 5)

def match_postcode(dbo):
    return cint(dbo, "MatchPostcode", 5)

def match_colour(dbo):
    return cint(dbo, "MatchColour", 5)

def match_include_shelter(dbo):
    return cboolean(dbo, "MatchIncludeShelter", True)

def match_within2weeks(dbo):
    return cint(dbo, "MatchWithin2Weeks", 5)

def match_point_floor(dbo):
    return cint(dbo, "MatchPointFloor", 20)

def meetapet_key(dbo):
    return cstring(dbo, "MeetAPetKey", DEFAULTS["MeetAPetKey"])

def meetapet_secret(dbo):
    return cstring(dbo, "MeetAPetSecret")

def meetapet_userkey(dbo):
    return cstring(dbo, "MeetAPetUserKey")

def movement_donations_default_due(dbo):
    return cboolean(dbo, "MovementDonationsDefaultDue", DEFAULTS["MovementDonationsDefaultDue"] == "Yes")

def non_shelter_type(dbo):
    return cint(dbo, "AFNonShelterType", 40)

def organisation(dbo):
    return cstring(dbo, "Organisation", "")

def organisation_address(dbo):
    return cstring(dbo, "OrganisationAddress")

def organisation_telephone(dbo):
    return cstring(dbo, "OrganisationTelephone")

def pdf_inline(dbo):
    return cboolean(dbo, "PDFInline", DEFAULTS["PDFInline"] == "Yes")

def person_search_columns(dbo):
    return cstring(dbo, "OwnerSearchColumns", DEFAULTS["OwnerSearchColumns"])

def petfinder_user(dbo):
    return cstring(dbo, "PetFinderFTPUser")

def petfinder_password(dbo):
    return cstring(dbo, "PetFinderFTPPassword")

def helpinglostpets_orgid(dbo):
    return cstring(dbo, "HelpingLostPetsOrgID")

def helpinglostpets_user(dbo):
    return cstring(dbo, "HelpingLostPetsFTPUser")

def helpinglostpets_password(dbo):
    return cstring(dbo, "HelpingLostPetsFTPPassword")

def helpinglostpets_postal(dbo):
    return cstring(dbo, "HelpingLostPetsPostal")

def petlink_email(dbo):
    return cstring(dbo, "PetLinkEmail")

def petlink_password(dbo):
    return cstring(dbo, "PetLinkPassword")

def petlink_chippassword(dbo):
    return cstring(dbo, "PetLinkChipPassword")

def petrescue_user(dbo):
    return cstring(dbo, "PetRescueFTPUser")

def petrescue_password(dbo):
    return cstring(dbo, "PetRescueFTPPassword")

def pets911_user(dbo):
    return cstring(dbo, "Pets911FTPUser")

def pets911_password(dbo):
    return cstring(dbo, "Pets911FTPPassword")

def pets911_source(dbo):
    return cstring(dbo, "Pets911FTPSourceID")

def publisher_use_comments(dbo):
    return cboolean(dbo, "PublisherUseComments", DEFAULTS["PublisherUseComments"] == "Yes")

def publisher_executing(dbo, publishername = "", publisherprogress = 0):
    if publishername == "" and publisherprogress == 0:
        return cstring(dbo, "PublisherExecuting", "NONE|0")
    else:
        cset(dbo, "PublisherExecuting", "%s|%d" % (publishername, publisherprogress))

def publisher_last_error(dbo, lasterror = "***"):
    if lasterror == "***":
        return cstring(dbo, "PublisherLastError", "")
    else:
        cset(dbo, "PublisherLastError", lasterror)

def publisher_stop(dbo, stop = ""):
    if stop == "":
        return cboolean(dbo, "PublisherStop")
    else:
        cset(dbo, "PublisherStop", stop)
        
def record_search_limit(dbo):
    return cint(dbo, "RecordSearchLimit", 1000)

def return_fosters_on_adoption(dbo):
    return cboolean(dbo, "ReturnFostersOnAdoption", DEFAULTS["ReturnFostersOnAdoption"] == "Yes")

def smarttag_accountid(dbo):
    return cstring(dbo, "SmartTagFTPUser")

def publisher_presets(dbo):
    return cstring(dbo, "PublisherPresets")

def publisher_ignore_ftp_override(dbo):
    return cboolean(dbo, "PublisherIgnoreFTPOverride", DEFAULTS["PublisherIgnoreFTPOverride"] == "Yes")

def publishers_enabled(dbo):
    return cstring(dbo, "PublishersEnabled")

def quicklinks_id(dbo, newval = ""):
    if newval == "":
        return cstring(dbo, "QuicklinksID", DEFAULTS["QuicklinksID"])
    else:
        cset(dbo, "QuicklinksID", newval)

def rescuegroups_user(dbo):
    return cstring(dbo, "RescueGroupsFTPUser")

def rescuegroups_password(dbo):
    return cstring(dbo, "RescueGroupsFTPPassword")

def retailer_on_shelter(dbo):
    return cboolean(dbo, "RetailerOnShelter", DEFAULTS["RetailerOnShelter"] == "Yes")

def scale_pdfs(dbo):
    return cboolean(dbo, "ScalePDFs", DEFAULTS["ScalePDFs"] == "Yes")

def search_sort(dbo):
    return cint(dbo, "SearchSort", 3)

def set_variable_data_updated_blank(dbo):
    cset_db(dbo, "VariableAnimalDataUpdated", "")

def set_variable_data_updated_today(dbo):
    cset_db(dbo, "VariableAnimalDataUpdated", time.strftime("%Y%m%d", i18n.now().timetuple()))

def show_first_time_screen(dbo, change = False, newvalue = False):
    if not change:
        return cboolean(dbo, "ShowFirstTime", DEFAULTS["ShowFirstTime"] == "Yes")
    else:
        cset(dbo, "ShowFirstTime", newvalue and "Yes" or "No")

def show_alerts_home_page(dbo):
    return cboolean(dbo, "ShowAlertsHomePage", DEFAULTS["ShowAlertsHomePage"] == "Yes")

def show_stats_home_page(dbo):
    return cstring(dbo, "ShowStatsHomePage", DEFAULTS["ShowStatsHomePage"])

def smdb_locked(dbo):
    return cboolean(dbo, "SMDBLocked")

def smtp_server(dbo):
    return cstring(dbo, "SMTPServer")

def smtp_server_username(dbo):
    return cstring(dbo, "SMTPServerUsername")

def smtp_server_password(dbo):
    return cstring(dbo, "SMTPServerPassword")

def smtp_server_tls(dbo):
    return cboolean(dbo, "SMTPServerUseTLS")

def system_theme(dbo):
    return cstring(dbo, "SystemTheme", "smoothness")

def use_short_shelter_codes(dbo):
    return cboolean(dbo, "UseShortShelterCodes")

def third_party_publisher_sig(dbo):
    return cstring(dbo, "TPPublisherSig")

def timezone(dbo):
    return cint(dbo, "Timezone", TIMEZONE)

def trial_adoptions(dbo):
    return cboolean(dbo, "TrialAdoptions", DEFAULTS["TrialAdoptions"] == "Yes")

def trial_on_shelter(dbo):
    return cboolean(dbo, "TrialOnShelter", DEFAULTS["TrialOnShelter"] == "Yes")

def variable_data_updated_today(dbo):
    todaystr = time.strftime("%Y%m%d", i18n.now().timetuple())
    return todaystr == cstring(dbo, "VariableAnimalDataUpdated")

def vetenvoy_user_id(dbo):
    return cstring(dbo, "VetEnvoyUserId")

def vetenvoy_user_password(dbo):
    return cstring(dbo, "VetEnvoyUserPassword")

def waiting_list_default_urgency(dbo):
    return cint(dbo, "WaitingListDefaultUrgency")

def waiting_list_rank_by_species(dbo):
    return cboolean(dbo, "WaitingListRankBySpecies")

def waiting_list_highlights(dbo, newhighlights = "READ"):
    if newhighlights == "READ":
        return cstring(dbo, "WaitingListHighlights")
    else:
        cset(dbo, "WaitingListHighlights", newhighlights + " ")

def waiting_list_view_columns(dbo):
    return cstring(dbo, "WaitingListViewColumns", DEFAULTS["WaitingListViewColumns"])

def waiting_list_urgency_update_period(dbo):
    return cint(dbo, "WaitingListUrgencyUpdatePeriod", 14)

def warn_no_homecheck(dbo):
    return cboolean(dbo, "WarnNoHomeCheck", DEFAULTS["WarnNoHomeCheck"] == "Yes")

