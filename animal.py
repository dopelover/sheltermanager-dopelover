#!/usr/bin/python

import additional
import al
import animalname
import audit
import configuration
import datetime
import diary
import db
import dbfs
import log
import lookups
import media
import movement
import utils
from i18n import _, date_diff, date_diff_days, now, display2python, subtract_years, subtract_months, add_days, subtract_days, monday_of_week, first_of_month, last_of_month, first_of_year
from random import choice

ASCENDING = 0
DESCENDING = 1

def get_animal_query(dbo):
    """
    Returns a select for animal rows with resolved lookups
    """
    dummy = dbo
    return "SELECT DISTINCT a.*, " \
        "at.AnimalType AS AnimalTypeName, " \
        "ba1.AnimalName AS BondedAnimal1Name, " \
        "ba1.ShelterCode AS BondedAnimal1Code, " \
        "ba2.AnimalName AS BondedAnimal2Name, " \
        "ba2.ShelterCode AS BondedAnimal2Code, " \
        "bc.BaseColour AS BaseColourName, " \
        "sp.SpeciesName AS SpeciesName, " \
        "sp.PetFinderSpecies, " \
        "bd.BreedName AS BreedName1, "\
        "bd2.BreedName AS BreedName2, "\
        "bd.PetFinderBreed, " \
        "bd2.PetFinderBreed AS PetFinderBreed2, " \
        "ct.CoatType AS CoatTypeName, " \
        "sx.Sex AS SexName, " \
        "sz.Size AS SizeName, " \
        "ov.OwnerName AS OwnersVetName, " \
        "ov.OwnerAddress AS OwnersVetAddress, " \
        "ov.OwnerTown AS OwnersVetTown, " \
        "ov.OwnerCounty AS OwnersVetCounty, " \
        "ov.OwnerPostcode AS OwnersVetPostcode, " \
        "ov.WorkTelephone AS OwnersVetWorkTelephone, " \
        "cv.OwnerName AS CurrentVetName, " \
        "cv.OwnerAddress AS CurrentVetAddress, " \
        "cv.OwnerTown AS CurrentVetTown, " \
        "cv.OwnerCounty AS CurrentVetCounty, " \
        "cv.OwnerPostcode AS CurrentVetPostcode, " \
        "cv.WorkTelephone AS CurrentVetWorkTelephone, " \
        "oo.OwnerName AS OriginalOwnerName, " \
        "oo.OwnerAddress AS OriginalOwnerAddress, " \
        "oo.OwnerTown AS OriginalOwnerTown, " \
        "oo.OwnerCounty AS OriginalOwnerCounty, " \
        "oo.OwnerPostcode AS OriginalOwnerPostcode, " \
        "oo.HomeTelephone AS OriginalOwnerHomeTelephone, " \
        "oo.WorkTelephone AS OriginalOwnerWorkTelephone, " \
        "oo.MobileTelephone AS OriginalOwnerMobileTelephone, " \
        "oo.EmailAddress AS OriginalOwnerEmailAddress, " \
        "co.ID AS CurrentOwnerID, " \
        "co.OwnerName AS CurrentOwnerName, " \
        "co.OwnerTitle AS CurrentOwnerTitle, " \
        "co.OwnerInitials AS CurrentOwnerInitials, " \
        "co.OwnerForeNames AS CurrentOwnerForeNames, " \
        "co.OwnerSurname AS CurrentOwnerSurname, " \
        "co.OwnerAddress AS CurrentOwnerAddress, " \
        "co.OwnerTown AS CurrentOwnerTown, " \
        "co.OwnerCounty AS CurrentOwnerCounty, " \
        "co.OwnerPostcode AS CurrentOwnerPostcode, " \
        "co.HomeTelephone AS CurrentOwnerHomeTelephone, " \
        "co.WorkTelephone AS CurrentOwnerWorkTelephone, " \
        "co.MobileTelephone AS CurrentOwnerMobileTelephone, " \
        "co.EmailAddress AS CurrentOwnerEmailAddress, " \
        "bo.OwnerName AS BroughtInByOwnerName, " \
        "bo.OwnerAddress AS BroughtInByOwnerAddress, " \
        "bo.OwnerTown AS BroughtInByOwnerTown, " \
        "bo.OwnerCounty AS BroughtInByOwnerCounty, " \
        "bo.OwnerPostcode AS BroughtInByOwnerPostcode, " \
        "bo.HomeTelephone AS BroughtInByHomeTelephone, " \
        "bo.WorkTelephone AS BroughtInByWorkTelephone, " \
        "bo.MobileTelephone AS BroughtInByMobileTelephone, " \
        "bo.EmailAddress AS BroughtInByEmailAddress, " \
        "ro.ID AS ReservedOwnerID, " \
        "ro.OwnerName AS ReservedOwnerName, " \
        "ro.OwnerAddress AS ReservedOwnerAddress, " \
        "ro.OwnerTown AS ReservedOwnerTown, " \
        "ro.OwnerCounty AS ReservedOwnerCounty, " \
        "ro.OwnerPostcode AS ReservedOwnerPostcode, " \
        "ro.HomeTelephone AS ReservedOwnerHomeTelephone, " \
        "ro.WorkTelephone AS ReservedOwnerWorkTelephone, " \
        "ro.MobileTelephone AS ReservedOwnerMobileTelephone, " \
        "ro.EmailAddress AS ReservedOwnerEmailAddress, " \
        "er.ReasonName AS EntryReasonName, " \
        "dr.ReasonName AS PTSReasonName, " \
        "il.LocationName AS ShelterLocationName, " \
        "pl.LocationName AS PickupLocationName, " \
        "ac.ID AS AnimalControlIncidentID, " \
        "itn.IncidentName AS AnimalControlIncidentName, " \
        "ac.IncidentDateTime AS AnimalControlIncidentDate, " \
        "mt.MovementType AS ActiveMovementTypeName, " \
        "am.AdoptionNumber AS ActiveMovementAdoptionNumber, " \
        "am.ReturnDate AS ActiveMovementReturnDate, " \
        "am.InsuranceNumber AS ActiveMovementInsuranceNumber, " \
        "am.ReasonForReturn AS ActiveMovementReasonForReturn, " \
        "am.TrialEndDate AS ActiveMovementTrialEndDate, " \
        "am.Comments AS ActiveMovementComments, " \
        "am.ReservationDate AS ActiveMovementReservationDate, " \
        "am.Donation AS ActiveMovementDonation, " \
        "am.CreatedBy AS ActiveMovementCreatedBy, " \
        "au.RealName AS ActiveMovementCreatedByName, " \
        "am.CreatedDate AS ActiveMovementCreatedDate, " \
        "am.LastChangedBy AS ActiveMovementLastChangedBy, " \
        "am.LastChangedDate AS ActiveMovementLastChangedDate, " \
        "CASE " \
        "WHEN EXISTS(SELECT ItemValue FROM configuration WHERE ItemName Like 'UseShortShelterCodes' AND ItemValue = 'Yes') " \
        "THEN a.ShortCode ELSE a.ShelterCode " \
        "END AS Code, " \
        "CASE " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType = 1 AND a.HasTrialAdoption = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=11) " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType = 2 AND a.HasPermanentFoster = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=12) " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType IN (2, 8, 13) THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=a.ActiveMovementType) " \
        "WHEN a.Archived = 1 AND a.DeceasedDate Is Not Null THEN " \
        "(SELECT ReasonName FROM deathreason WHERE ID = a.PTSReasonID) " \
        "WHEN a.Archived = 1 AND a.DeceasedDate Is Null AND a.ActiveMovementID <> 0 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=a.ActiveMovementType) " \
        "ELSE " \
        "(SELECT LocationName FROM internallocation WHERE ID=a.ShelterLocation) " \
        "END AS DisplayLocationName, " \
        "CASE " \
        "WHEN a.Archived = 0 AND a.CrueltyCase = 1 THEN 'Cruelty Case' " \
        "WHEN a.Archived = 0 AND a.IsQuarantine = 1 THEN 'Quarantine' " \
        "WHEN a.Archived = 0 AND a.IsHold = 1 THEN 'Hold' " \
        "WHEN a.Archived = 0 AND a.HasActiveReserve = 1 THEN 'Reserved' " \
        "WHEN a.Archived = 0 AND a.HasPermanentFoster = 1 THEN 'Permanent Foster' " \
        "WHEN a.IsNotAvailableForAdoption = 0 AND a.Archived = 0 AND a.HasTrialAdoption = 0 THEN 'Adoptable' " \
        "ELSE 'Not For Adoption' END AS AdoptionStatus, " \
        "web.MediaName AS WebsiteMediaName, " \
        "web.Date AS WebsiteMediaDate, " \
        "web.MediaNotes AS WebsiteMediaNotes, " \
        "(SELECT COUNT(*) FROM media mtc WHERE LOWER(mtc.MediaName) LIKE '%%.jpg' AND mtc.LinkTypeID = 0 AND mtc.LinkID = a.ID) AS WebsiteImageCount, " \
        "doc.MediaName AS DocMediaName, " \
        "vid.MediaName AS WebsiteVideoURL, " \
        "vid.MediaNotes AS WebsiteVideoNotes, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.NonShelterAnimal) AS NonShelterAnimalName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CrueltyCase) AS CrueltyCaseName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CrossBreed) AS CrossBreedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.EstimatedDOB) AS EstimatedDOBName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Identichipped) AS IdentichippedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Tattoo) AS TattooName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Neutered) AS NeuteredName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CombiTested) AS CombiTestedName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.CombiTestResult) AS CombiTestResultName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HeartwormTested) AS HeartwormTestedName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.HeartwormTestResult) AS HeartwormTestResultName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.FLVResult) AS FLVResultName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Declawed) AS DeclawedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.PutToSleep) AS PutToSleepName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsDOA) AS IsDOAName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsTransfer) AS IsTransferName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsPickup) AS IsPickupName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithChildren) AS IsGoodWithChildrenName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithCats) AS IsGoodWithCatsName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithDogs) AS IsGoodWithDogsName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsHouseTrained) AS IsHouseTrainedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsNotAvailableForAdoption) AS IsNotAvailableForAdoptionName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasSpecialNeeds) AS HasSpecialNeedsName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.DiedOffShelter) AS DiedOffShelterName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasActiveReserve) AS HasActiveReserveName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasTrialAdoption) AS HasTrialAdoptionName " \
        "FROM animal a " \
        "LEFT OUTER JOIN animal ba1 ON ba1.ID = a.BondedAnimalID " \
        "LEFT OUTER JOIN animal ba2 ON ba2.ID = a.BondedAnimal2ID " \
        "LEFT OUTER JOIN animaltype at ON at.ID = a.AnimalTypeID " \
        "LEFT OUTER JOIN basecolour bc ON bc.ID = a.BaseColourID " \
        "LEFT OUTER JOIN species sp ON sp.ID = a.SpeciesID " \
        "LEFT OUTER JOIN lksex sx ON sx.ID = a.Sex " \
        "LEFT OUTER JOIN lksize sz ON sz.ID = a.Size " \
        "LEFT OUTER JOIN entryreason er ON er.ID = a.EntryReasonID " \
        "LEFT OUTER JOIN internallocation il ON il.ID = a.ShelterLocation " \
        "LEFT OUTER JOIN pickuplocation pl ON pl.ID = a.PickupLocationID " \
        "LEFT OUTER JOIN media web ON web.LinkID = a.ID AND web.LinkTypeID = 0 AND web.WebsitePhoto = 1 " \
        "LEFT OUTER JOIN media vid ON vid.LinkID = a.ID AND vid.LinkTypeID = 0 AND vid.WebsiteVideo = 1 " \
        "LEFT OUTER JOIN media doc ON doc.LinkID = a.ID AND doc.LinkTypeID = 0 AND doc.DocPhoto = 1 " \
        "LEFT OUTER JOIN breed bd ON bd.ID = a.BreedID " \
        "LEFT OUTER JOIN breed bd2 ON bd2.ID = a.Breed2ID " \
        "LEFT OUTER JOIN lkcoattype ct ON ct.ID = a.CoatType " \
        "LEFT OUTER JOIN deathreason dr ON dr.ID = a.PTSReasonID " \
        "LEFT OUTER JOIN lksmovementtype mt ON mt.ID = a.ActiveMovementType " \
        "LEFT OUTER JOIN owner ov ON ov.ID = a.OwnersVetID " \
        "LEFT OUTER JOIN owner cv ON cv.ID = a.CurrentVetID " \
        "LEFT OUTER JOIN owner oo ON oo.ID = a.OriginalOwnerID " \
        "LEFT OUTER JOIN owner bo ON bo.ID = a.BroughtInByOwnerID " \
        "LEFT OUTER JOIN adoption am ON am.ID = a.ActiveMovementID " \
        "LEFT OUTER JOIN users au ON au.UserName = am.CreatedBy " \
        "LEFT OUTER JOIN owner co ON co.ID = am.OwnerID " \
        "LEFT OUTER JOIN animalcontrol ac ON ac.AnimalID = a.ID AND ac.ID = (SELECT MAX(sac.ID) FROM animalcontrol sac WHERE sac.AnimalID = a.ID) " \
        "LEFT OUTER JOIN incidenttype itn ON itn.ID = ac.IncidentTypeID " \
        "LEFT OUTER JOIN adoption ar ON ar.AnimalID = a.ID AND ar.MovementType = 0 AND ar.MovementDate Is Null AND ar.ReservationDate Is Not Null AND ar.ReservationCancelledDate Is Null AND ar.ID = (SELECT MAX(sar.ID) FROM adoption sar WHERE sar.AnimalID = a.ID AND sar.MovementType = 0 AND sar.MovementDate Is Null AND sar.ReservationDate Is Not Null AND sar.ReservationCancelledDate Is Null) " \
        "LEFT OUTER JOIN owner ro ON ro.ID = ar.OwnerID"

def get_animal(dbo, animalid):
    """
    Returns a complete animal row by id, or None if not found
    (int) animalid: The animal to get
    """
    if animalid is None or animalid == 0: return None
    rows = db.query(dbo, get_animal_query(dbo) + " WHERE a.ID = %d" % animalid)
    if rows is None or len(rows) == 0:
        return None
    else:
        return rows[0]

def get_animals_brief(animals, locationfilter = ""):
    """
    For any method that returns a list of animals from the get_animal_query 
    selector, this will strip them down and return shorter records for passing
    as json to things like search, shelterview and animal links screens.
    If a locationfilter is set, it will throw away animal records
    who are not in those locations.
    """
    r = []
    for a in animals:
        if locationfilter != "":
            if str(a["SHELTERLOCATION"]) not in locationfilter.split(","):
                continue
        r.append({ 
            "ACTIVEMOVEMENTID": a["ACTIVEMOVEMENTID"],
            "ACTIVEMOVEMENTTYPE": a["ACTIVEMOVEMENTTYPE"],
            "ADOPTIONSTATUS": a["ADOPTIONSTATUS"],
            "ANIMALCOMMENTS": a["ANIMALCOMMENTS"],
            "ANIMALAGE": a["ANIMALAGE"],
            "ANIMALNAME" : a["ANIMALNAME"],
            "ANIMALTYPENAME" : a["ANIMALTYPENAME"],
            "ARCHIVED" : a["ARCHIVED"],
            "BREEDNAME": a["BREEDNAME"],
            "CODE": a["CODE"],
            "CRUELTYCASE": a["CRUELTYCASE"],
            "CURRENTOWNERID": a["CURRENTOWNERID"],
            "CURRENTOWNERNAME": a["CURRENTOWNERNAME"],
            "DECEASEDDATE": a["DECEASEDDATE"],
            "DISPLAYLOCATIONNAME": a["DISPLAYLOCATIONNAME"],
            "ENTRYREASONNAME": a["ENTRYREASONNAME"],
            "HASACTIVERESERVE": a["HASACTIVERESERVE"],
            "HASTRIALADOPTION": a["HASTRIALADOPTION"],
            "HASPERMANENTFOSTER": a["HASPERMANENTFOSTER"],
            "HIDDENANIMALDETAILS": a["HIDDENANIMALDETAILS"],
            "HOLDUNTILDATE": a["HOLDUNTILDATE"],
            "ID": a["ID"], 
            "ISHOLD": a["ISHOLD"],
            "ISNOTAVAILABLEFORADOPTION": a["ISNOTAVAILABLEFORADOPTION"],
            "ISQUARANTINE": a["ISQUARANTINE"],
            "LASTCHANGEDDATE": a["LASTCHANGEDDATE"],
            "LASTCHANGEDBY": a["LASTCHANGEDBY"],
            "MARKINGS": a["MARKINGS"],
            "MOSTRECENTENTRYDATE" : a["MOSTRECENTENTRYDATE"],
            "NEUTERED" : a["NEUTERED"],
            "NONSHELTERANIMAL": a["NONSHELTERANIMAL"],
            "ORIGINALOWNERID": a["ORIGINALOWNERID"],
            "ORIGINALOWNERNAME": a["ORIGINALOWNERNAME"],
            "SEXNAME" : a["SEXNAME"],
            "SHELTERCODE" : a["SHELTERCODE"],
            "SHELTERLOCATION": a["SHELTERLOCATION"],
            "SHELTERLOCATIONNAME": a["SHELTERLOCATIONNAME"],
            "SHELTERLOCATIONUNIT": a["SHELTERLOCATIONUNIT"],
            "SHORTCODE": a["SHORTCODE"],
            "SPECIESID": a["SPECIESID"],
            "SPECIESNAME": a["SPECIESNAME"],
            "WEBSITEMEDIANAME": a["WEBSITEMEDIANAME"],
            "WEBSITEMEDIADATE": a["WEBSITEMEDIADATE"] 
        })
    return r

def get_animal_find_simple(dbo, query, classfilter = "all", limit = 0, onlyindexed = False, locationfilter = ""):
    """
    Returns rows for simple animal searches.
    query: The search criteria
    classfilter: all, shelter, female
    onlyindexed: only search fields with indexes
    locationfilter: IN clause of locations to search
    """
    # If no query has been given and we have a filter of shelter or all, 
    # do an on-shelter search instead
    if query == "" and (classfilter == "all" or classfilter == "shelter"):
        if locationfilter != "": locationfilter = "AND a.ShelterLocation IN (%s)" % locationfilter
        sql = get_animal_query(dbo) + " WHERE a.Archived = 0 %s ORDER BY a.AnimalName" % locationfilter
        if limit > 0: sql += " LIMIT " + str(limit)
        return db.query(dbo, sql)
    ors = []
    query = query.replace("'", "`")
    def add(field):
        return utils.where_text_filter(dbo, field, query)
    ors.append(add("a.AnimalName"))
    ors.append(add("a.ShelterCode"))
    ors.append(add("a.ShortCode"))
    ors.append(add("a.AcceptanceNumber"))
    ors.append(add("a.BreedName"))
    ors.append(add("a.IdentichipNumber"))
    ors.append(add("a.TattooNumber"))
    ors.append(add("a.RabiesTag"))
    ors.append(add("a.ShelterLocationUnit"))
    if not onlyindexed: 
        ors.append(add("a.Markings"))
        ors.append(add("a.HiddenAnimalDetails"))
        ors.append(add("a.AnimalComments"))
        ors.append(add("a.ReasonNO"))
        ors.append(add("a.HealthProblems"))
        ors.append(add("a.PTSReason"))
        ors.append(add("oo.OwnerName"))
        ors.append(add("oo.OwnerAddress"))
        ors.append(add("oo.HomeTelephone"))
        ors.append(add("oo.WorkTelephone"))
        ors.append(add("oo.MobileTelephone"))
        ors.append(add("co.OwnerName"))
        ors.append(add("co.OwnerAddress"))
        ors.append(add("co.HomeTelephone"))
        ors.append(add("co.WorkTelephone"))
        ors.append(add("co.MobileTelephone"))
        ors.append(add("bo.OwnerName"))
        ors.append(add("bo.OwnerAddress"))
        ors.append(add("bo.HomeTelephone"))
        ors.append(add("bo.WorkTelephone"))
        ors.append(add("bo.MobileTelephone"))
        ors.append(add("ro.OwnerName"))
        ors.append(add("ro.OwnerAddress"))
        ors.append(add("ro.HomeTelephone"))
        ors.append(add("ro.WorkTelephone"))
        ors.append(add("ro.MobileTelephone"))
        ors.append(add("cv.OwnerName"))
        ors.append(add("cv.OwnerAddress"))
        ors.append(add("cv.WorkTelephone"))
        ors.append(add("at.AnimalType"))
        ors.append(add("sp.SpeciesName"))
        ors.append(add("sx.Sex"))
        ors.append(add("il.LocationName"))
        ors.append(add("sz.Size"))
        ors.append(add("bc.BaseColour"))
        ors.append(add("ct.CoatType"))
        ors.append(u"EXISTS(SELECT ad.Value FROM additional ad WHERE ad.LinkID=a.ID AND ad.LinkType IN (%s) AND LOWER(ad.Value) LIKE '%%%s%%')" % (additional.ANIMAL_IN, query.lower()))
    sql = unicode(get_animal_query(dbo)) + " WHERE "
    if classfilter == "shelter":
        sql += u" a.Archived = 0 AND "
    elif classfilter == "female":
        sql += u" a.Sex = 0 AND "
    if locationfilter != "":
        sql += u" a.ShelterLocation IN (%s) AND " % locationfilter
    sql += "(" + u" OR ".join(ors) + ") ORDER BY a.Archived, a.AnimalName"
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_animal_find_advanced(dbo, criteria, limit = 0, locationfilter = ""):
    """
    Returns rows for advanced animal searches.
    criteria: A dictionary of criteria
       animalname - string partial pattern
       sheltercode - string partial pattern
       litterid - string partial pattern
       animaltypeid - -1 for all or ID
       breedid - -1 for all or ID
       speciesid - -1 for all or ID
       shelterlocation - -1 for all internal locations or ID
       size - -1 for all sizes or ID
       colour - -1 for all colours or ID
       comments - string partial pattern
       sex - -1 for all sexes or ID
       hasactivereserve - "both" "reserved" "unreserved"
       logicallocation - "all" "onshelter" "adoptable" "adopted" 
            "fostered" "permanentfoster" "transferred" "escaped" "stolen" "releasedtowild" 
            "reclaimed" "retailer" "nonshelter" "deceased" "notforadoption",
            "hold", "quarantine"
       inbetweenfrom - date string in current locale display format
       inbetweento - date string in current locale display format
       features - partial word/string match
       outbetweenfrom - date string in current locale display format
       outbetweento - date string in current locale display format
       adoptionno - string partial pattern
       agedbetweenfrom - string containing floating point number
       agedbetweento - string containing floating point number
       agegroup - contains an agegroup name
       microchip - string partial pattern
       insuranceno - string partial pattern
       rabiestag - string partial pattern
       hiddencomments - partial word/string pattern
       originalowner - string partial pattern
       medianotes - partial word/string pattern
       showtransfersonly - present if true
       includedeceased - present if true
       includenonshelter - present if true
       goodwithchildren - present if true
       goodwithcats - present if true
       goodwithdogs - present if true
       housetrained - present if true
    locationfilter: IN clause of locations to search
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

    def addidpair(cfield, field, field2): 
        if hk(cfield) and int(crit(cfield)) != -1: 
            c.append("(%s = %s OR %s = %s)" % ( 
            field, crit(cfield), field2, crit(cfield)))

    def addstr(cfield, field): 
        if hk(cfield) and crit(cfield) != "": 
            c.append("(LOWER(%s) LIKE '%%%s%%' OR LOWER(%s) LIKE '%%%s%%')" % ( 
                field, crit(cfield).lower().replace("'", "`"),
                field, utils.decode_html(crit(cfield).lower().replace(";", "`").replace("'", "`")) 
            ))

    def adddate(cfieldfrom, cfieldto, field): 
        if hk(cfieldfrom) and hk(cfieldto): 
            c.append("%s >= %s AND %s <= %s" % ( 
            field, db.dd(display2python(l, crit(cfieldfrom))), 
            field, db.dd(display2python(l, crit(cfieldto)))))

    def addcheck(cfield, condition):
        if hk(cfield): c.append(condition)

    def addcomp(cfield, value, condition):
        if hk(cfield) and crit(cfield) == value: c.append(condition)

    def addwords(cfield, field):
        if hk(cfield) and crit(cfield) != "":
            words = crit(cfield).split(" ")
            for w in words:
                c.append("(LOWER(%s) LIKE '%%%s%%' OR LOWER(%s) LIKE '%%%s%%')" % (
                    field, w.lower(),
                    field, utils.decode_html(w.lower())
                ))

    addstr("animalname", "a.AnimalName")
    addid("animaltypeid", "a.AnimalTypeID")
    addid("speciesid", "a.SpeciesID")
    addidpair("breedid", "a.BreedID", "a.Breed2ID")
    addid("shelterlocation", "a.ShelterLocation")
    # If we have a location filter and no location has been given, use the filter
    if locationfilter != "" and (not hk("shelterlocation") or crit("shelterlocation") == "-1"):
        c.append("a.ShelterLocation IN (%s)" % locationfilter)
    addstr("microchip", "a.IdentichipNumber")
    addstr("rabiestag", "a.RabiesTag")
    addid("sex", "a.Sex")
    addid("size", "a.Size")
    addid("colour", "a.BaseColourID")
    addstr("sheltercode", "a.ShelterCode")
    addstr("litterid", "a.AcceptanceNumber")
    adddate("inbetweenfrom", "inbetweento", "a.MostRecentEntryDate")
    addcheck("goodwithchildren", "a.IsGoodWithChildren = 0")
    addcheck("goodwithdogs", "a.IsGoodWithDogs = 0")
    addcheck("goodwithcats", "a.IsGoodWithCats = 0")
    addcheck("housetrained", "a.IsHouseTrained = 0")
    addcheck("showtransfersonly", "a.IsTransfer = 1")
    addcheck("showpickupsonly", "a.IsPickup = 1")
    addcheck("showcrueltycaseonly", "a.CrueltyCase = 1")
    addcheck("showspecialneedsonly", "a.HasSpecialNeeds = 1")
    addwords("comments", "a.AnimalComments")
    addwords("hiddencomments", "a.HiddenAnimalDetails")
    addwords("features", "a.Markings")
    addstr("originalowner", "oo.OwnerName")
    if crit("agegroup") != "" and crit("agegroup") != "-1":
        addstr("agegroup", "a.AgeGroup")
    adddate("outbetweenfrom", "outbetweento", "a.ActiveMovementDate")
    addwords("medianotes", "web.MediaNotes")

    if not hk("includedeceased") and not crit("logicallocation") == "deceased":
        c.append("a.DeceasedDate Is Null")

    if crit("logicallocation") == "nonshelter":
        c.append("a.NonShelterAnimal = 1")
    elif not hk("includenonshelter"):
        c.append("a.NonShelterAnimal = 0")

    if hk("agedbetweenfrom") and hk("agedbetweento"):
        c.append("%s >= %s AND %s <= %s" % (
            "a.DateOfBirth", db.dd(subtract_years(now(), float(crit("agedbetweento")))),
            "a.DateOfBirth", db.dd(subtract_years(now(), float(crit("agedbetweenfrom"))))))

    if hk("insuranceno") and crit("insuranceno") != "":
        c.append("EXISTS (SELECT InsuranceNumber FROM adoption WHERE " \
            "LOWER(InsuranceNumber) LIKE '%%%s%%' AND AnimalID = a.ID)" % crit("insuranceno"))

    if hk("adoptionno") and crit("adoptionno") != "":
        c.append("EXISTS (SELECT AdoptionNumber FROM adoption WHERE " \
            "LOWER(AdoptionNumber) LIKE '%%%s%%' AND AnimalID = a.ID)" % crit("adoptionno"))

    addcomp("reserved", "reserved", "a.HasActiveReserve = 1")
    addcomp("reserved", "unreserved", "a.HasActiveReserve = 0")
    addcomp("logicallocation", "onshelter", "a.Archived = 0")
    addcomp("logicallocation", "adoptable", "a.Archived = 0 AND a.IsNotAvailableForAdoption = 0 AND a.HasTrialAdoption = 0")
    addcomp("logicallocation", "reserved", "a.Archived = 0 AND a.HasActiveReserve = 1 AND a.HasTrialAdoption = 0")
    addcomp("logicallocation", "notforadoption", "a.IsNotAvailableForAdoption = 1 AND a.Archived = 0")
    addcomp("logicallocation", "hold", "a.IsHold = 1 AND a.Archived = 0")
    addcomp("logicallocation", "quarantine", "a.IsQuarantine = 1 AND a.Archived = 0")
    addcomp("logicallocation", "fostered", "a.ActiveMovementType = %d" % movement.FOSTER)
    addcomp("logicallocation", "permanentfoster", "a.ActiveMovementType = %d AND a.HasPermanentFoster = 1" % movement.FOSTER)
    addcomp("logicallocation", "adopted", "a.ActiveMovementType = %d" % movement.ADOPTION)
    addcomp("logicallocation", "transferred", "a.ActiveMovementType = %d" % movement.TRANSFER)
    addcomp("logicallocation", "escaped", "a.ActiveMovementType = %d" % movement.ESCAPED)
    addcomp("logicallocation", "stolen", "a.ActiveMovementType = %d" % movement.STOLEN)
    addcomp("logicallocation", "releasedtowild", "a.ActiveMovementType = %d" % movement.RELEASED)
    addcomp("logicallocation", "reclaimed", "a.ActiveMovementType = %d" % movement.RECLAIMED)
    addcomp("logicallocation", "retailer", "a.ActiveMovementType = %d" % movement.RETAILER)
    addcomp("logicallocation", "deceased", "a.DeceasedDate Is Not Null")
    where = ""
    if len(c) > 0:
        where = " WHERE " + " AND ".join(c)
    sql = get_animal_query(dbo) + where + " ORDER BY a.AnimalName"
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_animals_not_for_adoption(dbo):
    """
    Returns all shelter animals who have the not for adoption flag set
    """
    return db.query(dbo, get_animal_query(dbo) + " WHERE a.IsNotAvailableForAdoption = 1 AND a.Archived = 0")

def get_animals_hold(dbo):
    """
    Returns all shelter animals who have the hold flag set
    """
    return db.query(dbo, get_animal_query(dbo) + " WHERE a.IsHold = 1 AND a.Archived = 0")

def get_animals_hold_today(dbo):
    """
    Returns all shelter animals who have the hold flag set and the hold ends today
    """
    return db.query(dbo, get_animal_query(dbo) + " WHERE a.IsHold = 1 AND a.HoldUntilDate = %s AND a.Archived = 0" % db.dd(now(dbo.timezone)))

def get_animals_quarantine(dbo):
    """
    Returns all shelter animals who have the quarantine flag set
    """
    return db.query(dbo, get_animal_query(dbo) + " WHERE a.IsQuarantine = 1 AND a.Archived = 0")

def get_animals_recently_deceased(dbo):
    """
    Returns all shelter animals who are recently deceased
    """
    recent = subtract_days(now(), 30)
    return db.query(dbo, get_animal_query(dbo) + " " \
        "WHERE a.DeceasedDate Is Not Null " \
        "AND (a.ActiveMovementType Is Null OR a.ActiveMovementType = 0 " \
        "OR a.ActiveMovementType = 2) " \
        "AND a.DeceasedDate > %s" % db.dd(recent))

def get_alerts(dbo, locationfilter = ""):
    """
    Returns the alert totals for the main screen.
    """
    futuremonth = db.dd(add_days(now(dbo.timezone), 31))
    onemonth = db.dd(subtract_days(now(dbo.timezone), 31))
    oneweek = db.dd(subtract_days(now(dbo.timezone), 7))
    today = db.dd(now(dbo.timezone))
    if locationfilter != "": locationfilter = " AND ShelterLocation IN (%s)" % locationfilter
    shelterfilter = ""
    if not configuration.include_off_shelter_medical(dbo):
        shelterfilter = " AND (Archived = 0 OR ActiveMovementType = 2)"
    sql = "SELECT " \
        "(SELECT COUNT(*) FROM animalvaccination INNER JOIN animal ON animal.ID = animalvaccination.AnimalID WHERE " \
            "DateOfVaccination Is Null AND DeceasedDate Is Null %(shelterfilter)s AND " \
            "DateRequired  >= %(onemonth)s AND DateRequired <= %(today)s %(locfilter)s) AS duevacc," \
        "(SELECT COUNT(*) FROM animalvaccination INNER JOIN animal ON animal.ID = animalvaccination.AnimalID WHERE " \
            "DateOfVaccination Is Not Null AND DeceasedDate Is Null %(shelterfilter)s AND " \
            "DateExpires  >= %(onemonth)s AND DateExpires <= %(today)s %(locfilter)s) AS expvacc," \
        "(SELECT COUNT(*) FROM animaltest INNER JOIN animal ON animal.ID = animaltest.AnimalID WHERE " \
            "DateOfTest Is Null AND DeceasedDate Is Null %(shelterfilter)s AND " \
            "DateRequired >= %(onemonth)s AND DateRequired <= %(today)s %(locfilter)s) AS duetest," \
        "(SELECT COUNT(*) FROM animalmedicaltreatment INNER JOIN animal ON animal.ID = animalmedicaltreatment.AnimalID " \
            "INNER JOIN animalmedical ON animalmedicaltreatment.AnimalMedicalID = animalmedical.ID WHERE " \
            "DateGiven Is Null AND DeceasedDate Is Null %(shelterfilter)s AND " \
            "Status = 0 AND DateRequired  >= %(onemonth)s AND DateRequired <= %(today)s %(locfilter)s) AS duemed," \
        "(SELECT COUNT(*) FROM animalwaitinglist INNER JOIN owner ON owner.ID = animalwaitinglist.OwnerID " \
            "WHERE Urgency = 1 AND DateRemovedFromList Is Null) AS urgentwl," \
        "(SELECT COUNT(*) FROM adoption INNER JOIN owner ON owner.ID = adoption.OwnerID WHERE " \
            "MovementType = 0 AND ReservationDate Is Not Null AND ReservationCancelledDate Is Null AND IDCheck = 0) AS rsvhck," \
        "(SELECT COUNT(DISTINCT OwnerID) FROM ownerdonation WHERE DateDue <= %(today)s AND Date Is Null) AS duedon," \
        "(SELECT COUNT(*) FROM adoption WHERE IsTrial = 1 AND MovementType = 1 AND TrialEndDate <= %(oneweek)s) AS endtrial," \
        "(SELECT COUNT(*) FROM adoption INNER JOIN animal ON adoption.AnimalID = animal.ID WHERE " \
            "Archived = 0 AND DeceasedDate Is Null AND ReservationDate Is Not Null AND ReservationDate <= %(oneweek)s " \
            "AND ReservationCancelledDate Is Null AND MovementType = 0 AND MovementDate Is Null) AS longrsv," \
        "(SELECT COUNT(*) FROM animal WHERE Neutered = 0 AND ActiveMovementType = 1 AND " \
            "ActiveMovementDate > %(onemonth)s %(locfilter)s) AS notneu," \
        "(SELECT COUNT(*) FROM animal WHERE IsNotAvailableForAdoption = 1 " \
            "AND Archived = 0 %(locfilter)s) AS notadopt, " \
        "(SELECT COUNT(*) FROM animal WHERE IsHold = 1 AND HoldUntilDate = %(today)s AND Archived = 0) AS holdtoday, " \
        "(SELECT COUNT(DISTINCT CollationID) FROM onlineformincoming) AS inform, " \
        "(SELECT COUNT(*) FROM ownercitation WHERE FineDueDate Is Not Null AND FineDueDate <= %(today)s AND FinePaidDate Is Null) AS acunfine, " \
        "(SELECT COUNT(*) FROM animalcontrol WHERE CompletedDate Is Null AND DispatchDateTime Is Null AND CallDateTime Is Not Null) AS acundisp, " \
        "(SELECT COUNT(*) FROM animalcontrol WHERE CompletedDate Is Null) AS acuncomp, " \
        "(SELECT COUNT(*) FROM animalcontrol WHERE (CompletedDate Is Null AND " \
            "(FollowupDateTime Is Not Null AND FollowupDateTime <= %(today)s) OR " \
            "(FollowupDateTime2 Is Not Null AND FollowupDateTime2 <= %(today)s) OR " \
            "(FollowupDateTime3 Is Not Null AND FollowupDateTime3 <= %(today)s))) AS acfoll, " \
        "(SELECT COUNT(*) FROM ownertraploan WHERE ReturnDueDate Is Not Null AND ReturnDueDate <= %(today)s AND ReturnDate Is Null) AS tlover, " \
        "(SELECT COUNT(*) FROM stocklevel WHERE Balance > 0 AND Expiry Is Not Null AND Expiry > %(today)s AND Expiry <= %(futuremonth)s) AS stexpsoon, " \
        "(SELECT COUNT(*) FROM stocklevel WHERE Balance > 0 AND Expiry Is Not Null AND Expiry <= %(today)s) AS stexp " \
        "FROM animal LIMIT 1" \
            % { "today": today, "oneweek": oneweek, "onemonth": onemonth, "futuremonth": futuremonth, "locfilter": locationfilter, "shelterfilter": shelterfilter }
    return db.query_cache(dbo, sql)

def get_stats(dbo):
    """
    Returns the stats figures for the main screen.
    """
    statperiod = configuration.show_stats_home_page(dbo)
    statdate = now(dbo.timezone) # defaulting to today
    if statperiod == "thisweek": statdate = monday_of_week(statdate)
    if statperiod == "thismonth": statdate = first_of_month(statdate)
    if statperiod == "thisyear": statdate = first_of_year(statdate)
    if statperiod == "alltime": statdate = datetime.datetime(1900, 1, 1)
    countfrom = db.dd(statdate)
    sql = "SELECT " \
        "(SELECT COUNT(*) FROM animal WHERE NonShelterAnimal = 0 AND DateBroughtIn >= %(from)s) AS Entered," \
        "(SELECT COUNT(*) FROM animal WHERE ActiveMovementDate >= %(from)s AND ActiveMovementType = %(adoption)d) AS Adopted," \
        "(SELECT COUNT(*) FROM animal WHERE ActiveMovementDate >= %(from)s AND ActiveMovementType = %(reclaimed)d) AS Reclaimed, " \
        "(SELECT COUNT(*) FROM animal WHERE ActiveMovementDate >= %(from)s AND ActiveMovementType = %(transfer)d) AS Transferred, " \
        "(SELECT COUNT(*) FROM animal WHERE NonShelterAnimal = 0 AND DeceasedDate >= %(from)s AND PutToSleep = 1) AS PTS, " \
        "(SELECT COUNT(*) FROM animal WHERE NonShelterAnimal = 0 AND DeceasedDate >= %(from)s AND PutToSleep = 0) AS Died, " \
        "(SELECT SUM(Donation) FROM ownerdonation WHERE Date >= %(from)s) AS Donations, " \
        "(SELECT SUM(CostAmount) FROM animalcost WHERE CostDate >= %(from)s) + " \
            "(SELECT SUM(Cost) FROM animalvaccination WHERE DateOfVaccination >= %(from)s) + " \
            "(SELECT SUM(Cost) FROM animaltest WHERE DateOfTest >= %(from)s) + " \
            "(SELECT SUM(Cost) FROM animalmedical WHERE StartDate >= %(from)s) AS Costs " \
        "FROM animal LIMIT 1" \
        % { "from": countfrom, "adoption": movement.ADOPTION, "reclaimed": movement.RECLAIMED, "transfer": movement.TRANSFER }
    return db.query_cache(dbo, sql, 120)

def calc_most_recent_entry(dbo, animalid, a = None):
    """
    Returns the date the animal last entered the shelter
    (int) animalid: The animal to find the most recent entry date for
    """
    s = "SELECT MovementType, IsTrial, ReturnDate FROM adoption "
    s += "WHERE AnimalID = %d AND ReturnDate Is Not Null " % animalid
    s += "ORDER BY ReturnDate DESC"
    rows = db.query(dbo, s)

    # If there were no movement records, return the brought in date
    if len(rows) == 0:
        if a is not None:
            return a["DATEBROUGHTIN"]
        else:
            return get_date_brought_in(dbo, animalid)

    for r in rows:
        # Are we treating foster as on shelter? If so, skip
        # to the next movement instead
        if configuration.foster_on_shelter(dbo) and r["MOVEMENTTYPE"] == movement.FOSTER:
            continue

        # Are we treating retailers as on shelter? If so, skip
        # to the next movement instead
        if configuration.retailer_on_shelter(dbo) and r["MOVEMENTTYPE"] == movement.RETAILER:
            continue

        # Are we treating trial adoptions as on shelter? If so, skip
        # to the next movement instead
        if configuration.trial_on_shelter(dbo) and r["MOVEMENTTYPE"] == movement.ADOPTION and r["ISTRIAL"] == 1:
            continue

        # Otherwise, this will be the latest return date
        return r["RETURNDATE"]

    # If we got here, there was only foster movements
    if a is not None:
        return a["DATEBROUGHTIN"]
    else:
        return get_date_brought_in(dbo, animalid)

def calc_time_on_shelter(dbo, animalid, a = None):
    """
    Returns the length of time the animal has been on the shelter as a 
    formatted string, eg: "6 weeks and 3 days"
    (int) animalid: The animal to calculate time on shelter for
    """
    l = dbo.locale
    mre = calc_most_recent_entry(dbo, animalid, a)
    stop = now()
    if a is None:
        a = db.query(dbo, "SELECT Archived, DeceasedDate, ActiveMovementDate FROM animal WHERE ID = %d" % animalid)[0]

    # If the animal is dead, use that as our cutoff
    if a["DECEASEDDATE"] is not None:
        stop = a["DECEASEDDATE"]

    # If the animal has left the shelter, use that as our stop date
    elif a["ACTIVEMOVEMENTDATE"] is not None and a["ARCHIVED"] == 1:
        stop = a["ACTIVEMOVEMENTDATE"]

    # Format it as time period
    return date_diff(l, mre, stop)

def calc_days_on_shelter(dbo, animalid, a = None):
    """
    Returns the number of days an animal has been on the shelter as an int
    (int) animalid: The animal to get the number of days on shelter for
    """
    mre = calc_most_recent_entry(dbo, animalid, a)
    stop = now()
    if a is None:
        a = db.query(dbo, "SELECT DeceasedDate, ActiveMovementDate FROM animal WHERE ID = %d" % animalid)[0]

    # If the animal is dead, or has left the shelter
    # use that date as our cutoff instead
    if a["DECEASEDDATE"] is not None:
        stop = a["DECEASEDDATE"]
    elif a["ACTIVEMOVEMENTDATE"] is not None:
        stop = a["ACTIVEMOVEMENTDATE"]

    return date_diff_days(mre, stop)

def calc_age_group(dbo, animalid, a = None):
    """
    Returns the age group the animal fits into based on its
    date of birth.
    (int) animalid: The animal to calculate the age group for
    """

    # Calculate animal's age in days
    dob = None
    if a is None:
        dob = get_date_of_birth(dbo, animalid)
    else:
        dob = a["DATEOFBIRTH"]

    days = date_diff_days(dob, now())

    i = 1
    band = 0

    while True:

        # Get the next age group band
        band = configuration.age_group(dbo, i)
        if band == 0:
            break

        # The band figure is expressed in years, convert it to days
        band *= 365

        # Does the animal's current age fall into this band?
        if days <= band:
            return configuration.age_group_name(dbo, i)

        i += 1

    # Out of bands and none matched
    return ""

def calc_age(dbo, animalid, a = None):
    """
    Returns an animal's age as a readable string
     (int) animalid: The animal to calculate time on shelter for
    """
    l = dbo.locale
    dob = None
    deceased = None
    if a is not None:
        dob = a["DATEOFBIRTH"]
        deceased = a["DECEASEDDATE"]
    else:
        dob = get_date_of_birth(dbo, animalid)
        deceased = get_deceased_date(dbo, animalid)
    stop = now()

    # If the animal is dead, stop there
    if deceased is not None:
        stop = deceased

    # Format it as time period
    return date_diff(l, dob, stop)

def calc_shelter_code(dbo, animaltypeid, entryreasonid, speciesid, datebroughtin):
    """
    Creates a new shelter code using the configured format
    animaltypeid: The integer animal type id to use when creating the code
    datebroughtin: The date the animal was brought in as a python date
    Returns a tuple of sheltercode, shortcode, unique and year for an animal record
    Format tokens include:
        T - First char of animal type
        TT - First two chars of animal type
        E - First char of entry category
        EE - First two chars of entry category
        S - First char of species
        SS - First two chars of species
        YYYY - 4 digit brought in year
        YY - 2 digit brought in year
        MM - 2 digit brought in month
        DD - 2 digit brought in day
        UUUUUUUUUU - 10 digit padded code for next animal of all time
        UUUU - 4 digit padded code for next animal of all time
        XXX - 3 digit padded code for next animal for year
        XX - unpadded code for next animal for year
        NNN - 3 digit padded code for next animal of type for year
        NN - unpadded code for next animal of type for year
    """
    al.debug("sheltercode: generating for type %d, entry %d, species %d, datebroughtin %s" % \
        (int(animaltypeid), int(entryreasonid), int(speciesid), datebroughtin),
        "animal.calc_shelter_code", dbo)

    def clean_lookup(s):
        """ Removes whitespace and punctuation from the beginning of a lookup name """
        s = s.replace("(", "").replace("[", "").replace("{", "")
        s = s.replace(".", "").replace(",", "").replace("!", "")
        s = s.replace("\"", "").replace("'", "").replace("`", "")
        s = s.strip()
        return s

    def substitute_tokens(fmt, year, tyear, ever, datebroughtin, animaltype, species, entryreason):
        code = fmt
        code = code.replace("YYYY", "%04d" % datebroughtin.year)
        code = code.replace("YY", "%02d" % (int(datebroughtin.year) - 2000))
        code = code.replace("MM", "%02d" % datebroughtin.month)
        code = code.replace("DD", "%02d" % datebroughtin.day)
        code = code.replace("UUUUUUUUUU", "%010d" % ever)
        code = code.replace("UUUU", "%04d" % ever)
        code = code.replace("NNN", "%03d" % tyear)
        code = code.replace("NN", str(tyear))
        code = code.replace("XXX", "%03d" % year)
        code = code.replace("XX", str(year))
        # The following tokens all substitute to letters that could
        # then be substituted themselves - wrap delimiters around
        # those tokens before substituting them so that doesn't happen
        code = code.replace("TT", "{YY}")
        code = code.replace("T", "{T}")
        code = code.replace("SS", "{PP}")
        code = code.replace("S", "{S}")
        code = code.replace("EE", "{NN}")
        code = code.replace("E", "{E}")
        code = code.replace("{YY}", utils.substring(animaltype, 0, 2))
        code = code.replace("{T}", utils.substring(animaltype, 0, 1))
        code = code.replace("{PP}", utils.substring(species, 0, 2))
        code = code.replace("{S}", utils.substring(species, 0, 1))
        code = code.replace("{NN}", utils.substring(entryreason, 0, 2))
        code = code.replace("{E}", utils.substring(entryreason, 0, 1))
        return code

    if datebroughtin is None:
        datebroughtin = now()

    codeformat = configuration.coding_format(dbo)
    shortformat = configuration.coding_format_short(dbo)
    animaltype = clean_lookup(lookups.get_animaltype_name(dbo, animaltypeid))
    entryreason = clean_lookup(lookups.get_entryreason_name(dbo, entryreasonid))
    species = clean_lookup(lookups.get_species_name(dbo, speciesid))
    beginningofyear = datetime.datetime(datebroughtin.year, 1, 1, 0, 0, 0)
    endofyear = datetime.datetime(datebroughtin.year, 12, 31, 23, 59, 59)
    oneyearago = subtract_years(now(), 1.0)
    highesttyear = 0
    highestyear = 0
    highestever = 0

    # If our code uses N, calculate the highest code seen for this type this year
    if codeformat.find("N") != -1 or shortformat.find("N") != -1:
        highesttyear = db.query_int(dbo, "SELECT MAX(YearCodeID) FROM animal WHERE " \
            "DateBroughtIn >= " + db.dd(beginningofyear) + " AND " \
            "DateBroughtIn <= " + db.dd(endofyear) + " AND " \
            "AnimalTypeID = " + db.di(animaltypeid))
        highesttyear += 1

    # If our code uses X, calculate the highest code seen this year
    if codeformat.find("N") != -1 or shortformat.find("N") != -1:
        highestyear = db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE " \
            "DateBroughtIn >= " + db.dd(beginningofyear) + " AND " \
            "DateBroughtIn <= " + db.dd(endofyear))
        highestyear += 1

    # If our code uses U, calculate the highest code ever seen
    if codeformat.find("U") != -1 or shortformat.find("U") != -1:
        highestever = db.query_int(dbo, "SELECT MAX(UniqueCodeID) FROM animal WHERE " \
            "CreatedDate >= " + db.dd(oneyearago))
        highestever += 1

    unique = False
    code = ""
    shortcode = ""
    while not unique:

        # Generate the codes
        code = substitute_tokens(codeformat, highestyear, highesttyear, highestever, datebroughtin, animaltype, species, entryreason)
        shortcode = substitute_tokens(shortformat, highestyear, highesttyear, highestever, datebroughtin, animaltype, species, entryreason)

        # Verify the code is unique
        unique = 0 == db.query_int(dbo, "SELECT COUNT(*) FROM animal WHERE ShelterCode LIKE '%s'" % code)

        # If it's not, increment and try again
        if not unique:
            if codeformat.find("U") != -1: highestever += 1
            if codeformat.find("N") != -1: highesttyear += 1
            if codeformat.find("X") != -1: highestyear += 1

    al.debug("sheltercode: code=%s, short=%s for type %s, entry %s, species %s, datebroughtin %s" % \
        (code, shortcode, animaltype, entryreason, species, datebroughtin),
        "animal.calc_shelter_code", dbo)
    return (code, shortcode, highestever, highesttyear)

def get_latest_movement(dbo, animalid):
    """
    Returns the latest movement for an animal. The return
    value is a resultset of the movement itself or None
    if the animal has no movements.
    """
    l = dbo.locale
    reserve = db.query(dbo, "SELECT ad.*, o.ID AS CurrentOwnerID, o.OwnerName AS CurrentOwnerName, " \
        "%s AS MovementTypeName FROM adoption ad " \
        "INNER JOIN owner o ON o.ID = ad.OwnerID " \
        "WHERE ad.AnimalID = %d AND ad.ReservationDate Is Not Null " \
        "ORDER BY ad.ReservationDate DESC" % (db.ds(_("Reserved", l)), animalid))
    move = db.query(dbo, "SELECT ad.*, o.ID AS CurrentOwnerID, o.OwnerName AS CurrentOwnerName, " \
        "mt.MovementType AS MovementTypeName FROM adoption ad " \
        "INNER JOIN lksmovementtype mt ON mt.ID = ad.MovementType " \
        "LEFT OUTER JOIN owner o ON o.ID = ad.OwnerID " \
        "WHERE ad.AnimalID = %d AND ad.MovementDate Is Not Null AND " \
        "(ad.ReturnDate Is Null OR ad.ReturnDate > %s) " \
        "ORDER BY ad.MovementDate DESC" % (animalid, db.dd(now(dbo.timezone))))

    # If we don't have any movements, use the latest reservation
    if len(move) == 0: 
        if len(reserve) > 0:
            return reserve[0]
        else:
            return None
    else:
        # Use the latest movement
        return move[0]

def get_is_on_shelter(dbo, animalid):
    """
    Returns true if the animal is on shelter
    """
    return 0 == db.query_int(dbo, "SELECT Archived FROM animal WHERE ID = %d" % animalid)

def get_comments(dbo, animalid):
    """
    Returns an animal's comments
    (int) animalid: The animal to get the comments from
    """
    return db.query_string(dbo, "SELECT AnimalComments FROM animal WHERE ID = %d" % animalid)

def get_date_of_birth(dbo, animalid):
    """
    Returns an animal's date of birth
    (int) animalid: The animal to get the dob
    """
    return db.query_date(dbo, "SELECT DateOfBirth FROM animal WHERE ID = %d" % animalid)

def get_days_on_shelter(dbo, animalid):
    """
    Returns the number of days on the shelter
    """
    return db.query_int(dbo, "SELECT DaysOnShelter FROM animal WHERE ID = %d" % animalid)

def get_daily_boarding_cost(dbo, animalid):
    """
    Returns the daily boarding cost
    """
    return db.query_int(dbo, "SELECT DailyBoardingCost FROM animal WHERE ID = %d" % animalid)

def get_deceased_date(dbo, animalid):
    """
    Returns an animal's deceased date
    (int) animalid: The animal to get the deceased date
    """
    return db.query_date(dbo, "SELECT DeceasedDate FROM animal WHERE ID = %d" % animalid)

def get_date_brought_in(dbo, animalid):
    """
    Returns the date an animal was brought in
    (int) animalid: The animal to get the brought in date from
    """
    return db.query_date(dbo, "SELECT DateBroughtIn FROM animal WHERE ID = %d" % animalid)

def get_code(dbo, animalid):
    """
    Returns the appropriate animal code for display
    """
    rv = ""
    if configuration.use_short_shelter_codes(dbo):
        rv = get_short_code(dbo, animalid)
    else:
        rv = get_shelter_code(dbo, animalid)
    return rv

def get_short_code(dbo, animalid):
    """
    Returns the short code for animalid
    """
    return db.query_string(dbo, "SELECT ShortCode FROM animal WHERE ID = %d" % animalid)

def get_shelter_code(dbo, animalid):
    """
    Returns the shelter code for animalid
    """
    return db.query_string(dbo, "SELECT ShelterCode FROM animal WHERE ID = %d" % animalid)

def get_animal_namecode(dbo, animalid):
    """
    Returns an animal's name and code or an empty
    string if the id is not valid.
    """
    r = db.query(dbo, "SELECT AnimalName, ShelterCode, ShortCode " \
        "FROM animal WHERE ID = %d" % utils.cint(animalid))
    if len(r) == 0:
        return ""
    if configuration.use_short_shelter_codes(dbo):
        rv = r[0]["SHORTCODE"] + " - " + r[0]["ANIMALNAME"]
    else:
        rv = r[0]["SHELTERCODE"] + " - " + r[0]["ANIMALNAME"]
    return rv

def get_animals_namecode(dbo):
    """
    Returns a resultset containing the ID, name and code
    of all animals.
    """
    return db.query(dbo, "SELECT ID, AnimalName, ShelterCode, ShortCode " \
        "FROM animal ORDER BY AnimalName, ShelterCode")

def get_animals_on_shelter_namecode(dbo):
    """
    Returns a resultset containing the ID, name and code
    of all on shelter animals.
    """
    return db.query(dbo, "SELECT ID, AnimalName, ShelterCode, ShortCode, " \
        "CASE WHEN EXISTS(SELECT ItemValue FROM configuration WHERE ItemName Like 'UseShortShelterCodes' AND ItemValue = 'Yes') " \
        "THEN ShortCode ELSE ShelterCode END AS Code " \
        "FROM animal WHERE Archived = 0 ORDER BY AnimalName, ShelterCode")

def get_animals_on_shelter_foster_namecode(dbo):
    """
    Returns a resultset containing the ID, name and code
    of all on shelter and foster animals.
    """
    return db.query(dbo, "SELECT ID, AnimalName, ShelterCode, ShortCode, " \
        "CASE WHEN EXISTS(SELECT ItemValue FROM configuration WHERE ItemName Like 'UseShortShelterCodes' AND ItemValue = 'Yes') " \
        "THEN ShortCode ELSE ShelterCode END AS Code " \
        "FROM animal WHERE (Archived = 0 OR ActiveMovementType = 2) ORDER BY AnimalName, ShelterCode")

def get_breedname(dbo, breed1id, breed2id):
    """
    Returns the name of a breed from the primary and secondary breed
    breed1id: The first breed
    breed2id: The second breed
    """
    if breed1id == 0 or breed2id == 0: return ""
    if breed1id == breed2id:
        return lookups.get_breed_name(dbo, breed1id)
    return lookups.get_breed_name(dbo, breed1id) + "/" + lookups.get_breed_name(dbo, breed2id)

def get_costs(dbo, animalid, sort = ASCENDING):
    """
    Returns cost records for the given animal:
    COSTTYPEID, COSTTYPENAME, COSTDATE, DESCRIPTION
    """
    sql = "SELECT a.ID, a.CostTypeID, a.CostAmount, a.CostDate, a.CostPaidDate, c.CostTypeName, a.Description " \
        "FROM animalcost a INNER JOIN costtype c ON c.ID = a.CostTypeID " \
        "WHERE a.AnimalID = %d" % animalid
    if sort == ASCENDING:
        sql += " ORDER BY a.CostDate"
    else:
        sql += " ORDER BY a.CostDate DESC"
    return db.query(dbo, sql)

def get_cost_totals(dbo, animalid):
    """
    Returns a resultset containing totals of all cost values for an animal.
    DAILYBOARDINGCOST, DAYSONSHELTER, TV, TM, TC, TD
    """
    q = "SELECT DailyBoardingCost, DaysOnShelter, " \
        "(SELECT SUM(Cost) FROM animalvaccination WHERE AnimalID = animal.ID AND DateOfVaccination Is Not Null) AS tv, " \
        "(SELECT SUM(Cost) FROM animaltest WHERE AnimalID = animal.ID AND DateOfTest Is Not Null) AS tt, " \
        "(SELECT SUM(Cost) FROM animalmedical WHERE AnimalID = animal.ID) AS tm, " \
        "(SELECT SUM(CostAmount) FROM animalcost WHERE AnimalID = animal.ID) AS tc, " \
        "(SELECT SUM(Donation) FROM ownerdonation WHERE AnimalID = animal.ID) AS td " \
        "FROM animal WHERE ID = %d" % int(animalid)
    return db.query(dbo, q)[0]

def get_diets(dbo, animalid, sort = ASCENDING):
    """
    Returns diet records for the given animal:
    DIETNAME, DIETDESCRIPTION, DATESTARTED, COMMENTS
    """
    sql = "SELECT a.ID, a.DietID, d.DietName, d.DietDescription, a.DateStarted, a.Comments " \
        "FROM animaldiet a INNER JOIN diet d ON d.ID = a.DietID " \
        "WHERE a.AnimalID = %d" % animalid
    if sort == ASCENDING:
        sql += " ORDER BY a.DateStarted"
    else:
        sql += " ORDER BY a.DateStarted DESC"
    return db.query(dbo, sql)

def get_display_location(dbo, animalid):
    """ Returns an animal's current display location """
    return db.query_string(dbo, "SELECT DisplayLocation FROM animal WHERE ID = %d" % utils.cint(animalid))

def get_display_location_noq(dbo, animalid):
    """ Returns an animal's current display location without
        the :: qualifier if present """
    loc = db.query_string(dbo, "SELECT DisplayLocation FROM animal WHERE ID = %d" % utils.cint(animalid))
    if loc.find("::") != -1:
        loc = loc[0:loc.find("::")]
    return loc

def get_has_animals(dbo):
    """
    Returns True if there is at least one animal in the database
    """
    return db.query_int(dbo, "SELECT COUNT(ID) FROM animal") > 0

def get_has_animal_on_shelter(dbo):
    """
    Returns True if there is at least one animal on the shelter
    """
    return db.query_int(dbo, "SELECT COUNT(ID) FROM animal a WHERE a.Archived = 0") > 0

def get_links_ids(dbo, sort, q):
    """
    All links queries should be small, tight queries that return a
    list of animal IDs. We then do the full select on only those IDs. This
    improves performance when ORDER BY/LIMIT is slow.
    """
    init = db.query(dbo, q)
    aids = []
    for aid in init:
        aids.append(str(aid["ID"]))
    if len(aids) == 0: return aids # Return empty set if no results
    return db.query_cache(dbo, get_animal_query(dbo) + " WHERE a.ID IN (%s) ORDER BY %s" % (",".join(aids), sort), 120)

def get_links_recently_adopted(dbo, limit = 5, locationfilter = ""):
    """
    Returns link info for animals who were recently adopted
    """
    if locationfilter != "": locationfilter = "AND ShelterLocation IN (%s)" % locationfilter
    return get_links_ids(dbo, "a.ActiveMovementDate DESC", "SELECT ID FROM animal WHERE ActiveMovementType = 1 %s ORDER BY ActiveMovementDate DESC LIMIT %d" % (locationfilter, limit))

def get_links_recently_fostered(dbo, limit = 5, locationfilter = ""):
    """
    Returns link info for animals who were recently fostered
    """
    if locationfilter != "": locationfilter = "AND ShelterLocation IN (%s)" % locationfilter
    return get_links_ids(dbo, "a.ActiveMovementDate DESC", "SELECT ID FROM animal WHERE ActiveMovementType = 2 %s ORDER BY ActiveMovementDate DESC LIMIT %d" % (locationfilter, limit))

def get_links_recently_changed(dbo, limit = 5, locationfilter = ""):
    """
    Returns link info for animals who have recently been changed.
    """
    if locationfilter != "": locationfilter = " WHERE ShelterLocation IN (%s)" % locationfilter
    return get_links_ids(dbo, "a.LastChangedDate DESC", "SELECT ID FROM animal %s ORDER BY LastChangedDate DESC LIMIT %d" % (locationfilter, limit))

def get_links_recently_entered(dbo, limit = 5, locationfilter = ""):
    """
    Returns link info for animals who recently entered the shelter.
    """
    if locationfilter != "": locationfilter = "AND ShelterLocation IN (%s)" % locationfilter
    return get_links_ids(dbo, "a.MostRecentEntryDate DESC", "SELECT ID FROM animal WHERE Archived = 0 %s ORDER BY MostRecentEntryDate DESC LIMIT %d" % (locationfilter, limit))

def get_links_longest_on_shelter(dbo, limit = 5, locationfilter = ""):
    """
    Returns link info for animals who have been on the shelter the longest
    """
    if locationfilter != "": locationfilter = "AND ShelterLocation IN (%s)" % locationfilter
    return get_links_ids(dbo, "a.MostRecentEntryDate", "SELECT ID FROM animal WHERE Archived = 0 %s ORDER BY MostRecentEntryDate LIMIT %d" % (locationfilter, limit))

def get_number_animals_on_file(dbo):
    """
    Returns the number of animals on the system
    """
    return db.query_int(dbo, "SELECT COUNT(ID) FROM animal")

def get_number_animals_on_shelter_now(dbo):
    """
    Returns the number of animals on shelter
    """
    return db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE Archived = 0")

def update_active_litters(dbo):
    """
    Goes through all litters on the system that haven't expired
    and recalculates the number of animals aged under six months
    left on the shelter. If it reaches zero, the litter is cancelled 
    with today's date. The field CachedAnimalsLeft is updated as well 
    if it differs.
    """
    active = db.query(dbo, "SELECT l.*, " \
        "(SELECT COUNT(*) FROM animal a WHERE a.Archived = 0 " \
        "AND a.AcceptanceNumber Like l.AcceptanceNumber AND a.DateOfBirth >= %s) AS dbcount " \
        "FROM animallitter l " \
        "WHERE l.CachedAnimalsLeft Is Not Null AND " \
        "(l.InvalidDate Is Null OR l.InvalidDate > %s) " % ( db.dd(subtract_months(now(), 6)), db.dd(now(dbo.timezone))))
    for a in active:
        remaining = a["CACHEDANIMALSLEFT"]
        newremaining = a["DBCOUNT"]
        if newremaining == 0 and remaining > 0:
            al.debug("litter '%s' has no animals left, expiring." % a["ACCEPTANCENUMBER"], "animal.update_active_litters", dbo)
            db.execute(dbo, "UPDATE animallitter SET InvalidDate=%s WHERE ID=%d" % (db.dd(now(dbo.timezone)), int(a["ID"])))
        if newremaining != remaining:
            db.execute(dbo, "UPDATE animallitter SET CachedAnimalsLeft=%d WHERE ID=%d" % (int(newremaining), int(a["ID"])))
            al.debug("litter '%s' has fewer animals, setting remaining to %d." % (a["ACCEPTANCENUMBER"], int(newremaining)), "animal.update_active_litters", dbo)

def get_active_litters(dbo, speciesid = -1):
    """
    Returns all active animal litters in descending order of age
    speciesid: A species filter or -1 for all
    """
    sql = "SELECT l.*, a.AnimalName AS MotherName, " \
        "a.ShelterCode AS Mothercode, s.SpeciesName AS SpeciesName " \
        "FROM animallitter l " \
        "LEFT OUTER JOIN animal a ON l.ParentAnimalID = a.ID " \
        "INNER JOIN species s ON l.SpeciesID = s.ID " \
        "WHERE InvalidDate < %s %s" \
        "ORDER BY l.Date DESC" 
    where = ""
    if speciesid != -1: where = "AND SpeciesID = %d " % int(speciesid)
    return db.query(dbo, sql % (db.dd(now(dbo.timezone)), where))

def get_litters(dbo):
    """
    Returns all animal litters in descending order of age. Litters
    over a year old are ignored.
    """
    return db.query(dbo, "SELECT l.*, a.AnimalName AS MotherName, " \
        "a.ShelterCode AS Mothercode, s.SpeciesName AS SpeciesName " \
        "FROM animallitter l " \
        "LEFT OUTER JOIN animal a ON l.ParentAnimalID = a.ID " \
        "INNER JOIN species s ON l.SpeciesID = s.ID " \
        "WHERE l.Date >= %s " \
        "ORDER BY l.Date DESC" % ( db.dd(subtract_years(now(), 1))))

def get_satellite_counts(dbo, animalid):
    """
    Returns a resultset containing the number of each type of satellite
    record that an animal has.
    """
    sql = "SELECT a.ID, " \
        "(SELECT COUNT(*) FROM animalvaccination av WHERE av.AnimalID = a.ID) AS vaccination, " \
        "(SELECT COUNT(*) FROM animaltest at WHERE at.AnimalID = a.ID) AS test, " \
        "(SELECT COUNT(*) FROM animalmedical am WHERE am.AnimalID = a.ID) AS medical, " \
        "(SELECT COUNT(*) FROM animaldiet ad WHERE ad.AnimalID = a.ID) AS diet, " \
        "(SELECT COUNT(*) FROM media me WHERE me.LinkID = a.ID AND me.LinkTypeID = %d) AS media, " \
        "(SELECT COUNT(*) FROM diary di WHERE di.LinkID = a.ID AND di.LinkType = %d) AS diary, " \
        "(SELECT COUNT(*) FROM adoption ad WHERE ad.AnimalID = a.ID) AS movements, " \
        "(SELECT COUNT(*) FROM log WHERE log.LinkID = a.ID AND log.LinkType = %d) AS logs, " \
        "(SELECT COUNT(*) FROM ownerdonation od WHERE od.AnimalID = a.ID) AS donations, " \
        "(SELECT COUNT(*) FROM ownerlicence ol WHERE ol.AnimalID = a.ID) AS licence, " \
        "(SELECT COUNT(*) FROM animalcost ac WHERE ac.AnimalID = a.ID) AS costs " \
        "FROM animal a WHERE a.ID = %d" \
        % (media.ANIMAL, diary.ANIMAL, log.ANIMAL, int(animalid))
    return db.query(dbo, sql)

def get_preferred_web_media_name(dbo, animalid):
    """
    Returns the name of the preferred media image for publishing to the
    web. If no preferred is found, returns the first image available for
    the animal. If the animal has no images, an empty string is returned.
    """
    mrec = db.query(dbo, "SELECT * FROM media WHERE LinkID = %d AND LinkTypeID = 0 AND (LOWER(MediaName) Like '%%.jpg' OR LOWER(MediaName) LIKE '%%.jpeg')" % animalid)
    for m in mrec:
        if m["WEBSITEPHOTO"] == 1:
            return m["MEDIANAME"]
    if len(mrec) > 0:
        return mrec[0]["MEDIANAME"]
    else:
        return ""

def get_random_name(dbo, sex = 0):
    """
    Returns a random animal name from the database. It will ignore names
    that end with numbers and try to prefer less well used names.
    sex: A sex from lksex - 0 = Female, 1 = Male, 2 = Unknown
    """
    names = db.query(dbo, "SELECT AnimalName, COUNT(AnimalName) AS Total " \
        "FROM animal " \
        "WHERE Sex = %d " \
        "AND AnimalName Not Like '%%0' "\
        "AND AnimalName Not Like '%%1' "\
        "AND AnimalName Not Like '%%2' "\
        "AND AnimalName Not Like '%%3' "\
        "AND AnimalName Not Like '%%4' "\
        "AND AnimalName Not Like '%%5' "\
        "AND AnimalName Not Like '%%6' "\
        "AND AnimalName Not Like '%%7' "\
        "AND AnimalName Not Like '%%8' "\
        "AND AnimalName Not Like '%%9' "\
        "GROUP BY AnimalName " \
        "ORDER BY COUNT(AnimalName)" % sex)
    # We have less than a hundred animals, use one of our random set
    if len(names) < 100: return animalname.get_random_name()
    # Build a separate list of the lesser used names
    leastused = []
    for n in names:
        if n["TOTAL"] < 3:
            leastused.append(n)
    # Choose whether we're going to use our set, one of the lesser
    # used or something from the overall pool. We prefer our set, then
    # the lesser used names, then anything
    decide = choice((1, 2, 3, 4, 5, 6))
    if decide < 4:
        return animalname.get_random_name()
    elif decide == 4 or decide == 5:
        return choice(leastused)["ANIMALNAME"]
    else:
        return choice(names)["ANIMALNAME"]

def get_recent_with_name(dbo, name):
    """
    Returns a list of animals who have a brought in date in the last 3 weeks
    with the name given.
    """
    return db.query(dbo, "SELECT ID, ID AS ANIMALID, SHELTERCODE, ANIMALNAME FROM animal " \
        "WHERE DateBroughtIn >= %s AND LOWER(ANIMALNAME) LIKE LOWER(%s)" % (db.dd(subtract_days(now(dbo.timezone), 21)), db.ds(name)))

def get_units_with_availability(dbo, locationid):
    """
    Returns a list of location units for location id
    each one has a pipe delimiter and 1 for free/available,
    0 for unavailable.
    """
    a = []
    units = db.query_string(dbo, "SELECT Units FROM internallocation WHERE ID = %d" % utils.cint(locationid)).split(",")
    for u in units:
        uname = u.strip()
        ainu = db.query_int(dbo, "SELECT COUNT(*) FROM animal WHERE Archived = 0 AND ShelterLocationUnit LIKE '%s'" % uname)
        a.append( "%s|%d" % (uname, ainu == 0 and 1 or 0 ))
    return a

def get_shelterview_animals(dbo, locationfilter = ""):
    """
    Returns all available animals for shelterview
    """
    if locationfilter != "": locationfilter = "AND a.ShelterLocation IN (%s)" % locationfilter
    return db.query_cache(dbo, get_animal_query(dbo) + " WHERE a.Archived = 0 %s ORDER BY a.AnimalName" % locationfilter)

def insert_animal_from_form(dbo, post, username):
    """
    Creates an animal record from the new animal screen
    data: The webpy data object containing form parameters
    Returns a tuple containing the newly created animal id and code
    """
    l = dbo.locale
    nextid = db.get_id(dbo, "animal")
    def c(field):
        return post.db_boolean(field)
    def t(field):
        return post.db_string(field)
    def s(field):
        return post.db_integer(field)
    def kd(field):
        return post.date(field)
    def ki(field):
        return post.integer(field)
    def kf(field):
        return post.floating(field)
    def ks(field):
        return post.string(field)

    if ks("dateofbirth") == "" or None == kd("dateofbirth"):
        estimateddob = 1
        dob = subtract_years(now(), kf("estimatedage"))
    else:
        estimateddob = 0
        dob = kd("dateofbirth")

    # Set brought in by date
    datebroughtin = kd("datebroughtin")
    if datebroughtin is None:
        datebroughtin = now()

    # Set the code manually if we were given a code, or the option was turned on
    if configuration.manual_codes(dbo) or ks("sheltercode") != "":
        sheltercode = ks("sheltercode")
        shortcode = ks("shortcode")
        unique = 0
        year = 0
        if sheltercode.strip() == "":
            raise utils.ASMValidationError(_("You must supply a code.", l))
        if 0 != db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE ShelterCode = '%s'" % sheltercode.replace("'", "`")):
            raise utils.ASMValidationError(_("This code has already been used.", l))
    else:
        # Generate a new code
        sheltercode, shortcode, unique, year = calc_shelter_code(dbo, ki("animaltype"), ki("entryreason"), ki("species"), datebroughtin)

    # Default good with
    goodwithcats = 2
    if post.has_key("goodwithcats"): goodwithcats = ki("goodwithcats")
    goodwithdogs = 2
    if post.has_key("goodwithdogs"): goodwithdogs = ki("goodwithdogs")
    goodwithkids = 2
    if post.has_key("goodwithkids"): goodwithkids = ki("goodwithkids")
    housetrained = 2
    if post.has_key("housetrained"): housetrained = ki("housetrained")
    unknown = 0

    # Validate form fields
    if ks("animalname") == "":
        raise utils.ASMValidationError(_("Name cannot be blank", l))
    if ks("microchipnumber").strip() != "" and not configuration.allow_duplicate_microchip(dbo):
        if db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE IdentichipNumber Like %s AND ID <> %d" % (post.db_string("microchipnumber"), ki("id"))) > 0:
            raise utils.ASMValidationError(_("Microchip number {0} has already been allocated to another animal.", l).format(ks("microchipnumber")))

    # Set default brought in by if we have one and none was set
    dbb = ki("broughtinby")
    if dbb == 0:
        dbb = configuration.default_broughtinby(dbo)

    # Set not for adoption if the option is on
    notforadoption = 0
    if post.has_key("notforadoption"):
        notforadoption = ki("notforadoption")
    elif configuration.auto_not_for_adoption(dbo):
        notforadoption = 1        

    sql = db.make_insert_user_sql(dbo, "animal", username, (
        ( "ID", db.di(nextid)),
        ( "AnimalName", t("animalname")),
        ( "ShelterCode", db.ds(sheltercode)),
        ( "ShortCode", db.ds(shortcode)),
        ( "UniqueCodeID", db.di(unique)),
        ( "YearCodeID", db.di(year)),
        ( "DateOfBirth", db.dd(dob)),
        ( "DailyBoardingCost", db.di(configuration.default_daily_boarding_cost(dbo))),
        ( "Sex", s("sex")),
        ( "AnimalTypeID", s("animaltype")),
        ( "SpeciesID", s("species")),
        ( "BreedID", s("breed1")),
        ( "Breed2ID", s("breed2")),
        ( "BreedName", db.ds(get_breedname(dbo, ki("breed1"), ki("breed2")))),
        ( "Crossbreed", c("crossbreed")),
        ( "AcceptanceNumber", t("litterid")),
        ( "BaseColourID", s("basecolour")),
        ( "ShelterLocation", s("internallocation")),
        ( "ShelterLocationUnit", t("unit")),
        ( "NonShelterAnimal", db.di(0)),
        ( "CrueltyCase", db.di(0)),
        ( "BondedAnimalID", db.di(0)),
        ( "BondedAnimal2ID", db.di(0)),
        ( "CoatType", db.di(configuration.default_coattype(dbo))),
        ( "EstimatedDOB", db.di(estimateddob)),
        ( "Fee", s("fee")),
        ( "Identichipped", s("microchipped")),
        ( "IdentichipNumber", t("microchipnumber")),
        ( "IdentichipDate", db.dd(kd("microchipdate"))),
        ( "Tattoo", db.di(0)),
        ( "TattooDate", db.dd(None)),
        ( "TattooNumber", db.ds("")),
        ( "SmartTag", db.di(0)),
        ( "SmartTagNumber", db.ds("")),
        ( "SmartTagType", db.di(0)),
        ( "Neutered", s("neutered")),
        ( "NeuteredDate", db.dd(kd("neutereddate"))),
        ( "Declawed", db.di(0)),
        # ASM2_COMPATIBILITY
        ( "HeartwormTested", db.di(0)),
        ( "HeartwormTestDate", db.dd(None)),
        ( "HeartwormTestResult", db.di(unknown)),
        ( "CombiTested", db.di(0)),
        ( "CombiTestDate", db.dd(None)),
        ( "CombiTestResult", db.di(unknown)),
        ( "FLVResult", db.di(unknown)),
        # ASM2_COMPATIBILITY
        ( "Markings", t("markings")),
        ( "HiddenAnimalDetails", t("hiddenanimaldetails")),
        ( "AnimalComments", t("comments")),
        ( "IsGoodWithCats", db.di(goodwithcats)),
        ( "IsGoodWithDogs", db.di(goodwithdogs)),
        ( "IsGoodWithChildren", db.di(goodwithkids)),
        ( "IsHouseTrained", db.di(housetrained)),
        ( "OriginalOwnerID", s("originalowner")),
        ( "BroughtInByOwnerID", db.di(dbb) ),
        ( "ReasonNO", db.ds("")),
        ( "ReasonForEntry", t("reasonforentry")),
        ( "EntryReasonID", s("entryreason")),
        ( "IsTransfer", db.di(0)),
        ( "IsPickup", db.di(0)),
        ( "IsHold", db.di(0)),
        ( "HoldUntilDate", db.dd(None)),
        ( "IsQuarantine", db.di(0)),
        ( "DateBroughtIn", db.dd(datebroughtin)),
        ( "AsilomarIntakeCategory", db.di(0)),
        ( "AsilomarIsTransferExternal", db.di(0)),
        ( "AsilomarOwnerRequestedEuthanasia", db.di(0)),
        ( "HealthProblems", t("healthproblems")),
        ( "HasSpecialNeeds", db.di(0)),
        ( "RabiesTag", db.ds("")),
        ( "CurrentVetID", db.di(0)),
        ( "OwnersVetID", db.di(0)),
        ( "DeceasedDate", db.dd(kd("deceaseddate"))),
        ( "PTSReasonID", db.di(configuration.default_death_reason(dbo))),
        ( "PutToSleep", db.di(0)),
        ( "IsDOA", db.di(0)),
        ( "DiedOffShelter", db.di(0)),
        ( "PTSReason", db.ds("")),
        ( "IsNotAvailableForAdoption", db.di(notforadoption)),
        ( "Size", s("size")),
        ( "Archived", db.di(0)),
        ( "ActiveMovementID", db.di(0)),
        ( "HasActiveReserve", db.di(0)),
        ( "MostRecentEntryDate", db.dd(now()))
    ))
    db.execute(dbo, sql)

    audit.create(dbo, username, "animal", sheltercode + " " + t("animalname"))

    # Update denormalised fields after the insert
    update_animal_check_bonds(dbo, nextid)
    update_animal_status(dbo, nextid)
    update_variable_animal_data(dbo, nextid)
    return (nextid, get_code(dbo, nextid))

def update_animal_from_form(dbo, post, username):
    """
    Updates an animal record from the edit animal screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    def c(field):
        return post.db_boolean(field)
    def t(field):
        return post.db_string(field)
    def s(field):
        return post.db_integer(field)
    def d(field):
        return post.db_date(field)
    def kd(field):
        return post.date(field)
    def ki(field):
        return post.integer(field)
    def ks(field):
        return post.string(field)

    # Validate form fields
    if ks("animalname") == "":
        raise utils.ASMValidationError(_("Name cannot be blank", l))
    if ks("dateofbirth") == "":
        raise utils.ASMValidationError(_("Date of birth cannot be blank", l))
    if kd("dateofbirth") is None:
        raise utils.ASMValidationError(_("Date of birth is not valid", l))
    if ks("datebroughtin") == "":
        raise utils.ASMValidationError(_("Date brought in cannot be blank", l))
    if kd("datebroughtin") is None:
        raise utils.ASMValidationError(_("Date brought in is not valid", l))
    if ks("sheltercode") == "":
        raise utils.ASMValidationError(_("Shelter code cannot be blank", l))
    if db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE ShelterCode Like '%s' AND ID <> %d" % (ks("sheltercode").replace("'", "`"), ki("id"))) > 0:
        raise utils.ASMValidationError(_("Shelter code {0} has already been allocated to another animal.", l).format(ks("sheltercode")))
    if ks("microchipnumber").strip() != "" and not configuration.allow_duplicate_microchip(dbo):
        if db.query_int(dbo, "SELECT COUNT(ID) FROM animal WHERE IdentichipNumber Like %s AND ID <> %d" % (post.db_string("microchipnumber"), ki("id"))) > 0:
            raise utils.ASMValidationError(_("Microchip number {0} has already been allocated to another animal.", l).format(ks("microchipnumber")))
    if ks("deceaseddate") != "":
        deceaseddate = d("deceaseddate")
        datebroughtin = d("datebroughtin")
        if deceaseddate is not None and datebroughtin != None and deceaseddate < datebroughtin:
            raise utils.ASMValidationError(_("Animal cannot be deceased before it was brought to the shelter", l))

    # If the option is on and the internal location has changed, log it
    oldlocid = db.query_int(dbo, "SELECT ShelterLocation FROM animal WHERE ID=%d" % ki("id"))
    if configuration.location_change_log(dbo) and ki("location") != oldlocid:
        oldlocation = db.query_string(dbo, "SELECT LocationName FROM internallocation WHERE ID = %d" % oldlocid)
        newlocation = db.query_string(dbo, "SELECT LocationName FROM internallocation WHERE ID = %d" % ki("location"))
        log.add_log(dbo, username, log.ANIMAL, ki("id"), configuration.location_change_log_type(dbo), 
            _("{0} {1}: Moved from {2} to {3}", l).format(ks("sheltercode"), ks("animalname"), oldlocation, newlocation))

    preaudit = db.query(dbo, "SELECT * FROM animal WHERE ID = %d" % ki("id"))
    db.execute(dbo, db.make_update_user_sql(dbo, "animal", username, "ID=%d" % ki("id"), (
        ( "NonShelterAnimal", c("nonshelter")),
        ( "IsNotAvailableForAdoption", c("notforadoption")),
        ( "IsHold", c("hold")),
        ( "HoldUntilDate", d("holduntil")),
        ( "IsQuarantine", c("quarantine")),
        ( "CrueltyCase", c("crueltycase")),
        ( "ShelterCode", t("sheltercode")),
        ( "ShortCode", t("shortcode")),
        ( "UniqueCodeID", s("uniquecode")),
        ( "YearCodeID", s("yearcode")),
        ( "AcceptanceNumber", t("litterid")),
        ( "AnimalName", t("animalname")),
        ( "Sex", s("sex")),
        ( "AnimalTypeID", s("animaltype")),
        ( "BaseColourID", s("basecolour")),
        ( "CoatType", s("coattype")),
        ( "Size", s("size")),
        ( "SpeciesID", s("species")),
        ( "BreedID", s("breed1")),
        ( "Breed2ID", s("breed2")),
        ( "BreedName", db.ds(get_breedname(dbo, ki("breed1"), ki("breed2")))),
        ( "Crossbreed", c("crossbreed")),
        ( "ShelterLocation", s("location")),
        ( "ShelterLocationUnit", t("unit")),
        ( "DateOfBirth", d("dateofbirth")),
        ( "EstimatedDOB", c("estimateddob")),
        ( "Fee", s("fee")),
        ( "Identichipped", c("microchipped")),
        ( "IdentichipDate", d("microchipdate")),
        ( "IdentichipNumber", t("microchipnumber")),
        ( "Tattoo", c("tattoo")),
        ( "TattooDate", d("tattoodate")),
        ( "TattooNumber", t("tattoonumber")),
        ( "SmartTag", c("smarttag")),
        ( "SmartTagNumber", t("smarttagnumber")),
        ( "SmartTagType", s("smarttagtype")),
        ( "Neutered", c("neutered")),
        ( "NeuteredDate", d("neutereddate")),
        ( "Declawed", c("declawed")),
        # ASM2_COMPATIBILITY
        ( "HeartwormTested", c("heartwormtested")),
        ( "HeartwormTestDate", d("heartwormtestdate")),
        ( "HeartwormTestResult", s("heartwormtestresult")),
        ( "CombiTested", c("fivltested")),
        ( "CombiTestDate", d("fivltestdate")),
        ( "CombiTestResult", s("fivresult")),
        ( "FLVResult", s("flvresult")),
        # ASM2_COMPATIBILITY
        ( "Markings", t("markings")),
        ( "HiddenAnimalDetails", t("hiddencomments")),
        ( "AnimalComments", t("comments")),
        ( "IsGoodWithCats", s("goodwithcats")),
        ( "IsGoodWithDogs", s("goodwithdogs")),
        ( "IsGoodWithChildren", s("goodwithkids")),
        ( "IsHouseTrained", s("housetrained")),
        ( "OriginalOwnerID", s("originalowner")),
        ( "BroughtInByOwnerID", s("broughtinby")),
        ( "BondedAnimalID", s("bonded1")),
        ( "BondedAnimal2ID", s("bonded2")),
        ( "ReasonNO", t("reasonnotfromowner")),
        ( "ReasonForEntry", t("reasonforentry")),
        ( "EntryReasonID", s("entryreason")),
        ( "IsTransfer", c("transferin")),
        ( "IsPickup", c("pickedup")),
        ( "PickupLocationID", s("pickuplocation")),
        ( "PickedUpByOwnerID", s("pickedupby")),
        ( "DateBroughtIn", d("datebroughtin")),
        ( "AsilomarIntakeCategory", s("asilomarintakecategory")),
        ( "AsilomarIsTransferExternal", c("asilomartransferexternal")),
        ( "AsilomarOwnerRequestedEuthanasia", c("asilomarownerrequested")),
        ( "HealthProblems", t("healthproblems")),
        ( "HasSpecialNeeds", c("specialneeds")),
        ( "RabiesTag", t("rabiestag")),
        ( "CurrentVetID", s("currentvet")),
        ( "OwnersVetID", s("ownersvet")),
        ( "DeceasedDate", d("deceaseddate")),
        ( "PTSReasonID", s("deathcategory")),
        ( "PutToSleep", c("puttosleep")),
        ( "IsDOA", c("deadonarrival")),
        ( "DiedOffShelter", c("diedoffshelter")),
        ( "PTSReason", t("ptsreason"))
    )))
    postaudit = db.query(dbo, "SELECT * FROM animal WHERE ID = %d" % ki("id"))
    audit.edit(dbo, username, "animal", audit.map_diff(preaudit, postaudit, [ "SHELTERCODE", "ANIMALNAME" ]))

    # Save any additional field values given
    additional.save_values_for_link(dbo, post, ki("id"), "animal")

    # Update denormalised fields after the change
    update_animal_check_bonds(dbo, ki("id"))
    update_animal_status(dbo, ki("id"))
    update_variable_animal_data(dbo, ki("id"))

def update_animals_from_form(dbo, post, username):
    """
    Batch updates multiple animal records from the bulk form
    """
    dummy = username # TODO: Not audited
    if len(post.integer_list("animals")) == 0: return 0
    if post["litterid"] != "":
        db.execute(dbo, "UPDATE animal SET AcceptanceNumber = %s WHERE ID IN (%s)" % (post.db_string("litterid"), post["animals"]))
    if post.integer("animaltype") != -1:
        db.execute(dbo, "UPDATE animal SET AnimalTypeID = %d WHERE ID IN (%s)" % (post.integer("animaltype"), post["animals"]))
    if post.integer("location") != -1:
        db.execute(dbo, "UPDATE animal SET ShelterLocation = %d WHERE ID IN (%s)" % (post.integer("location"), post["animals"]))
    if post.integer("fee") > 0:
        db.execute(dbo, "UPDATE animal SET Fee = %d WHERE ID IN (%s)" % (post.integer("fee"), post["animals"]))
    if post.integer("notforadoption") != -1:
        db.execute(dbo, "UPDATE animal SET IsNotAvailableForAdoption = %d WHERE ID IN (%s)" % (post.integer("notforadoption"), post["animals"]))
    if post.integer("goodwithcats") != -1:
        db.execute(dbo, "UPDATE animal SET IsGoodWithCats = %d WHERE ID IN (%s)" % (post.integer("goodwithcats"), post["animals"]))
    if post.integer("goodwithdogs") != -1:
        db.execute(dbo, "UPDATE animal SET IsGoodWithDogs = %d WHERE ID IN (%s)" % (post.integer("goodwithdogs"), post["animals"]))
    if post.integer("goodwithkids") != -1:
        db.execute(dbo, "UPDATE animal SET IsGoodWithChildren = %d WHERE ID IN (%s)" % (post.integer("goodwithkids"), post["animals"]))
    if post.integer("housetrained") != -1:
        db.execute(dbo, "UPDATE animal SET IsHouseTrained = %d WHERE ID IN (%s)" % (post.integer("housetrained"), post["animals"]))
    if post["neutereddate"] != "":
        db.execute(dbo, "UPDATE animal SET Neutered = 1, NeuteredDate = %s WHERE ID IN (%s)" % (post.db_date("neutereddate"), post["animals"]))
    return len(post.integer_list("animals"))

def update_deceased_from_form(dbo, username, post):
    """
    Sets an animal's deceased information from the move_deceased form
    """
    animalid = post.integer("animal")
    sql = db.make_update_user_sql(dbo, "animal", username, "ID=%s" % db.di(animalid), (
        ( "DeceasedDate", post.db_date("deceaseddate")),
        ( "PTSReasonID", post.db_integer("deathcategory")),
        ( "PutToSleep", post.db_boolean("puttosleep")),
        ( "IsDOA", post.db_boolean("deadonarrival")),
        ( "DiedOffShelter", post.db_boolean("diedoffshelter")),
        ( "PTSReason", post.db_string("ptsreason"))
    ))
    preaudit = db.query(dbo, "SELECT * FROM animal WHERE ID = %d" % animalid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animal WHERE ID = %d" % animalid)
    audit.edit(dbo, username, "animal", audit.map_diff(preaudit, postaudit, [ "ANIMALNAME", ]))
    # Update denormalised fields after the deceased change
    update_animal_status(dbo, animalid)
    update_variable_animal_data(dbo, animalid)

def update_location(dbo, username, animalid, locationid):
    """
    Updates the shelterlocation field of the animal given.
    """
    # If the option is on and the internal location has changed, log it
    l = dbo.locale
    a = db.query(dbo, "SELECT ShelterCode, AnimalName, ShelterLocation FROM animal WHERE ID=%d" % animalid)
    if len(a) == 0: return
    a = a[0]
    if configuration.location_change_log(dbo) and locationid != a["SHELTERLOCATION"]:
        oldlocation = db.query_string(dbo, "SELECT LocationName FROM internallocation WHERE ID = %d" % a["SHELTERLOCATION"])
        newlocation = db.query_string(dbo, "SELECT LocationName FROM internallocation WHERE ID = %d" % locationid)
        log.add_log(dbo, username, log.ANIMAL, animalid, configuration.location_change_log_type(dbo), 
            _("{0} {1}: Moved from {2} to {3}", l).format(a["SHELTERCODE"], a["ANIMALNAME"], oldlocation, newlocation))
    # Change the location
    db.execute(dbo, "UPDATE animal SET ShelterLocation = %d WHERE ID = %d" % (int(locationid), int(animalid)))

def clone_animal(dbo, username, animalid):
    """
    Clones an animal and its satellite records.
    """
    l = dbo.locale
    a = get_animal(dbo, animalid)
    nid = db.get_id(dbo, "animal")
    sheltercode, shortcode, unique, year = calc_shelter_code(dbo, a["ANIMALTYPEID"], a["ENTRYREASONID"], a["SPECIESID"], a["DATEBROUGHTIN"])
    sql = db.make_insert_user_sql(dbo, "animal", username, (
        ( "ID", db.di(nid) ),
        ( "AnimalTypeID", db.di(a["ANIMALTYPEID"]) ),
        ( "ShelterCode", db.ds(sheltercode)),
        ( "ShortCode", db.ds(shortcode)),
        ( "UniqueCodeID", db.di(unique)),
        ( "YearCodeID", db.di(year)),
        ( "AnimalName", db.ds( _("Copy of {0}", l).format(a["ANIMALNAME"]))),
        ( "NonShelterAnimal", db.di(a["NONSHELTERANIMAL"])),
        ( "CrueltyCase", db.di(a["CRUELTYCASE"])),
        ( "BaseColourID", db.di(a["BASECOLOURID"])),
        ( "SpeciesID", db.di(a["SPECIESID"])),
        ( "BreedID", db.di(a["BREEDID"])),
        ( "Breed2ID", db.di(a["BREED2ID"])),
        ( "BreedName", db.ds(a["BREEDNAME"])),
        ( "CrossBreed", db.di(a["CROSSBREED"])),
        ( "CoatType", db.di(a["COATTYPE"])),
        ( "Markings", db.ds(a["MARKINGS"])),
        ( "AcceptanceNumber", db.ds(a["ACCEPTANCENUMBER"])),
        ( "DateOfBirth", db.dd(a["DATEOFBIRTH"])),
        ( "EstimatedDOB", db.di(a["ESTIMATEDDOB"])),
        ( "Fee", db.di(a["FEE"])),
        ( "AgeGroup", db.ds(a["AGEGROUP"])),
        ( "DeceasedDate", db.dd(a["DECEASEDDATE"])),
        ( "Sex", db.di(a["SEX"])),
        ( "Identichipped", db.di(a["IDENTICHIPPED"])),
        ( "IdentichipNumber", db.ds("")),
        ( "Tattoo", db.di(a["TATTOO"])),
        ( "TattooNumber", db.ds("")),
        ( "Neutered", db.di(a["NEUTERED"])),
        ( "NeuteredDate", db.dd(a["NEUTEREDDATE"])),
        # ASM2_COMPATIBILITY
        ( "CombiTested", db.di(a["COMBITESTED"])),
        ( "CombiTestDate", db.dd(a["COMBITESTDATE"])),
        ( "CombiTestResult", db.di(a["COMBITESTRESULT"])),
        ( "HeartwormTested", db.di(a["HEARTWORMTESTED"])),
        ( "HeartwormTestDate", db.dd(a["HEARTWORMTESTDATE"])),
        ( "HeartwormTestResult", db.di(a["HEARTWORMTESTRESULT"])),
        ( "FLVResult", db.di(a["FLVRESULT"])),
        # ASM2_COMPATIBILITY
        ( "SmartTag", db.di(0)),
        ( "SmartTagNumber", db.ds("")),
        ( "SmartTagType", db.di(0)),
        ( "Declawed", db.di(a["DECLAWED"])),
        ( "HiddenAnimalDetails", db.ds(a["HIDDENANIMALDETAILS"])),
        ( "AnimalComments", db.ds(a["ANIMALCOMMENTS"])),
        ( "OwnersVetID", db.di(a["OWNERSVETID"])),
        ( "CurrentVetID",  db.di(a["CURRENTVETID"])),
        ( "OriginalOwnerID", db.di(a["ORIGINALOWNERID"])),
        ( "BroughtInByOwnerID", db.di(a["BROUGHTINBYOWNERID"])),
        ( "ReasonForEntry", db.ds(a["REASONFORENTRY"])),
        ( "ReasonNO", db.ds(a["REASONNO"])),
        ( "DateBroughtIn", db.dd(a["DATEBROUGHTIN"])),
        ( "EntryReasonID", db.di(a["ENTRYREASONID"])),
        ( "AsilomarIsTransferExternal", db.di(a["ASILOMARISTRANSFEREXTERNAL"])),
        ( "AsilomarIntakeCategory", db.di(a["ASILOMARINTAKECATEGORY"])),
        ( "AsilomarOwnerRequestedEuthanasia", db.di(a["ASILOMAROWNERREQUESTEDEUTHANASIA"])),
        ( "HealthProblems", db.ds(a["HEALTHPROBLEMS"])),
        ( "PutToSleep", db.di(a["PUTTOSLEEP"])),
        ( "PTSReason", db.ds(a["PTSREASON"])),
        ( "PTSReasonID", db.di(a["PTSREASONID"])),
        ( "IsDOA", db.di(a["ISDOA"])),
        ( "IsTransfer", db.di(a["ISTRANSFER"])),
        ( "IsGoodWithCats", db.di(a["ISGOODWITHCATS"])),
        ( "IsGoodWithDogs", db.di(a["ISGOODWITHDOGS"])),
        ( "IsGoodWithChildren", db.di(a["ISGOODWITHCHILDREN"])),
        ( "IsHouseTrained", db.di(a["ISHOUSETRAINED"])),
        ( "IsNotAvailableForAdoption", db.di(a["ISNOTAVAILABLEFORADOPTION"])),
        ( "IsHold", db.di(a["ISHOLD"])),
        ( "HoldUntilDate", db.dd(a["HOLDUNTILDATE"])),
        ( "IsQuarantine", db.di(a["ISQUARANTINE"])),
        ( "HasSpecialNeeds", db.di(a["HASSPECIALNEEDS"])),
        ( "ShelterLocation", db.di(a["SHELTERLOCATION"])),
        ( "ShelterLocationUnit", db.ds(a["SHELTERLOCATIONUNIT"])),
        ( "DiedOffShelter", db.di(a["DIEDOFFSHELTER"])),
        ( "Size", db.di(a["SIZE"])),
        ( "RabiesTag", db.ds(a["RABIESTAG"])),
        ( "BondedAnimalID", db.di(0)),
        ( "BondedAnimal2ID", db.di(0)),
        ( "Archived", db.di(0)),
        ( "ActiveMovementID", db.di(0)),
        ( "ActiveMovementType", db.di(0)),
        ( "HasActiveReserve", db.di(0)),
        ( "MostRecentEntryDate", db.dd(a["MOSTRECENTENTRYDATE"]))
        ))
    db.execute(dbo, sql)
    # Additional Fields
    for af in db.query(dbo, "SELECT * FROM additional WHERE LinkID = %d AND LinkType IN (%s)" % (int(animalid), additional.ANIMAL_IN)):
        sql = db.make_insert_sql("additional", (
            ( "LinkType", db.di(af["LINKTYPE"]) ),
            ( "LinkID", db.di(nid) ),
            ( "AdditionalFieldID", db.di(af["ADDITIONALFIELDID"]) ),
            ( "Value", db.ds(af["VALUE"])) ))
        db.execute(dbo, sql)
    # Vaccinations
    for v in db.query(dbo, "SELECT * FROM animalvaccination WHERE AnimalID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "animalvaccination", username, (
            ( "ID", db.di(db.get_id(dbo, "animalvaccination")) ),
            ( "AnimalID", db.di(nid) ),
            ( "VaccinationID", db.di(v["VACCINATIONID"]) ),
            ( "DateOfVaccination", db.dd(v["DATEOFVACCINATION"]) ),
            ( "DateRequired", db.dd(v["DATEREQUIRED"]) ),
            ( "Cost", db.di(v["COST"]) ),
            ( "Comments", db.ds(v["COMMENTS"]) )
            ))
        db.execute(dbo, sql)
    # Tests
    for t in db.query(dbo, "SELECT * FROM animaltest WHERE AnimalID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "animaltest", username, ( 
            ( "ID", db.di(db.get_id(dbo, "animaltest")) ),
            ( "AnimalID", db.di(nid)),
            ( "TestTypeID", db.di(t["TESTTYPEID"]) ),
            ( "TestResultID", db.di(t["TESTRESULTID"]) ),
            ( "DateOfTest", db.di(t["DATEOFTEST"]) ),
            ( "DateRequired", db.di(t["DATEREQUIRED"]) ),
            ( "Cost", db.di(t["COST"]) ),
            ( "Comments", db.ds(t["COMMENTS"]) )
            ))
    # Medical
    for am in db.query(dbo, "SELECT * FROM animalmedical WHERE AnimalID = %d" % int(animalid)):
        namid = db.get_id(dbo, "animalmedical")
        sql = db.make_insert_user_sql(dbo, "animalmedical", username, (
            ( "ID", db.di(namid)),
            ( "AnimalID", db.di(nid) ),
            ( "MedicalProfileID", db.di(am["MEDICALPROFILEID"]) ),
            ( "TreatmentName", db.ds(am["TREATMENTNAME"]) ),
            ( "StartDate", db.ds(am["STARTDATE"]) ),
            ( "Dosage", db.ds(am["DOSAGE"]) ),
            ( "Cost", db.di(am["COST"]) ),
            ( "TimingRule", db.di(am["TIMINGRULE"]) ),
            ( "TimingRuleFrequency", db.di(am["TIMINGRULEFREQUENCY"]) ),
            ( "TimingRuleNoFrequencies", db.di(am["TIMINGRULENOFREQUENCIES"]) ),
            ( "TreatmentRule", db.di(am["TREATMENTRULE"]) ),
            ( "TotalNumberOfTreatments", db.di(am["TOTALNUMBEROFTREATMENTS"]) ),
            ( "TreatmentsGiven", db.di(am["TREATMENTSGIVEN"]) ),
            ( "TreatmentsRemaining", db.di(am["TREATMENTSREMAINING"]) ),
            ( "Status", db.di(am["STATUS"]) ),
            ( "Comments", db.ds(am["COMMENTS"]) )
            ))
        db.execute(dbo, sql)
        for amt in db.query(dbo, "SELECT * FROM animalmedicaltreatment WHERE AnimalMedicalID = %d" % int(am["ID"])):
            sql = db.make_insert_user_sql(dbo, "animalmedicaltreatment", username, (
                ( "ID", db.di(db.get_id(dbo, "animalmedicaltreatment")) ),
                ( "AnimalID", db.di(nid) ),
                ( "AnimalMedicalID", db.di(namid) ),
                ( "DateRequired", db.dd(amt["DATEREQUIRED"])),
                ( "DateGiven", db.dd(amt["DATEGIVEN"])),
                ( "TreatmentNumber", db.di(amt["TREATMENTNUMBER"])),
                ( "TotalTreatments", db.di(amt["TOTALTREATMENTS"])),
                ( "GivenBy", db.ds(amt["GIVENBY"])),
                ( "Comments", db.ds(amt["COMMENTS"]))
                ))
            db.execute(dbo, sql)
    # Diet
    for d in db.query(dbo, "SELECT * FROM animaldiet WHERE AnimalID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "animaldiet", username, (
            ( "ID", db.di(db.get_id(dbo, "animaldiet")) ),
            ( "AnimalID", db.di(nid) ),
            ( "DietID", db.di(d["DIETID"]) ),
            ( "DateStarted", db.dd(d["DATESTARTED"])),
            ( "Comments", db.ds(d["COMMENTS"]))
        ))
        db.execute(dbo, sql)
    # Costs
    for c in db.query(dbo, "SELECT * FROM animalcost WHERE AnimalID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "animalcost", username, (
            ( "ID", db.di(db.get_id(dbo, "animalcost")) ),
            ( "AnimalID", db.di(nid) ),
            ( "CostTypeID", db.di(c["COSTTYPEID"])),
            ( "CostDate", db.dd(c["COSTDATE"])),
            ( "CostAmount", db.di(c["COSTAMOUNT"])),
            ( "Description", db.ds(c["DESCRIPTION"]))
        ))
        db.execute(dbo, sql)
    # Donations
    for dt in db.query(dbo, "SELECT * FROM ownerdonation WHERE AnimalID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "ownerdonation", username, (
            ( "ID", db.di(db.get_id(dbo, "ownerdonation")) ),
            ( "AnimalID", db.di(nid) ),
            ( "OwnerID", db.di(dt["OWNERID"])),
            ( "MovementID", db.di(0)),
            ( "DonationTypeID", db.di(dt["DONATIONTYPEID"])),
            ( "Date", db.dd(dt["DATE"])),
            ( "DateDue", db.dd(dt["DATEDUE"])),
            ( "Donation", db.di(dt["DONATION"])),
            ( "IsGiftAid", db.di(dt["ISGIFTAID"])),
            ( "Frequency", db.di(dt["FREQUENCY"])),
            ( "NextCreated", db.di(dt["NEXTCREATED"])),
            ( "Comments", db.ds(dt["COMMENTS"]))
        ))
        db.execute(dbo, sql)
    # Diary
    for di in db.query(dbo, "SELECT * FROM diary WHERE LinkType = 1 AND LinkID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "diary", username, (
            ( "ID", db.di(db.get_id(dbo, "diary")) ),
            ( "LinkID", db.di(nid) ),
            ( "LinkType", db.di(1) ),
            ( "DiaryDateTime", db.ddt(di["DIARYDATETIME"])),
            ( "DiaryForName", db.ds(di["DIARYFORNAME"])),
            ( "Subject", db.ds(di["SUBJECT"])),
            ( "Note", db.ds(di["NOTE"])),
            ( "DateCompleted", db.dd(di["DATECOMPLETED"])),
            ( "LinkInfo", db.ds(diary.get_link_info(dbo, 1, nid)))
        ))
        db.execute(dbo, sql)
    # Movements
    for mv in db.query(dbo, "SELECT * FROM adoption WHERE AnimalID = %d" % int(animalid)):
        nadid = db.get_id(dbo, "adoption")
        sql = db.make_insert_user_sql(dbo, "adoption", username, (
            ( "ID", db.di(nadid) ),
            ( "AnimalID", db.di(nid) ),
            ( "OwnerID", db.di(mv["OWNERID"])),
            ( "RetailerID", db.di(mv["RETAILERID"])),
            ( "AdoptionNumber", db.ds(utils.padleft(nadid, 6))),
            ( "OriginalRetailerMovementID", db.di(0)),
            ( "MovementDate", db.dd(mv["MOVEMENTDATE"])),
            ( "MovementType", db.di(mv["MOVEMENTTYPE"])),
            ( "ReturnDate", db.dd(mv["RETURNDATE"])),
            ( "ReturnedReasonID", db.di(mv["RETURNEDREASONID"])),
            ( "InsuranceNumber", db.ds(mv["INSURANCENUMBER"])),
            ( "ReasonForReturn", db.ds(mv["REASONFORRETURN"])),
            ( "ReservationDate", db.dd(mv["RESERVATIONDATE"])),
            ( "Donation", db.di(mv["DONATION"])),
            ( "ReservationCancelledDate", db.dd(mv["RESERVATIONCANCELLEDDATE"])),
            ( "Comments", db.ds(mv["COMMENTS"]))
        ))
        db.execute(dbo, sql)
    # Log
    for lo in db.query(dbo, "SELECT * FROM log WHERE LinkType = 0 AND LinkID = %d" % int(animalid)):
        sql = db.make_insert_user_sql(dbo, "log", username, (
            ( "ID", db.di(db.get_id(dbo, "log")) ),
            ( "LinkID", db.di(nid) ),
            ( "LinkType", db.di(0) ),
            ( "LogTypeID", db.di(lo["LOGTYPEID"])),
            ( "Date", db.dd(lo["DATE"])),
            ( "Comments", db.ds(lo["COMMENTS"]))
        ))
        db.execute(dbo, sql)
    audit.create(dbo, username, "animal", str(nid) + " cloned from " + str(a["ID"]))
    update_animal_status(dbo, nid)
    update_variable_animal_data(dbo, nid)
    return nid

def delete_animal(dbo, username, animalid):
    """
    Deletes an animal and all its satellite records.
    """
    l = dbo.locale
    if db.query_int(dbo, "SELECT COUNT(ID) FROM adoption WHERE AnimalID=%d" % animalid):
        raise utils.ASMValidationError(_("This animal has movements and cannot be removed.", l))
    audit.delete(dbo, username, "animal", str(db.query(dbo, "SELECT * FROM animal WHERE ID=%d" % animalid)))
    db.execute(dbo, "DELETE FROM media WHERE LinkID = %d AND LinkTypeID = %d" % (animalid, 0))
    db.execute(dbo, "DELETE FROM diary WHERE LinkID = %d AND LinkType = %d" % (animalid, 1))
    db.execute(dbo, "DELETE FROM log WHERE LinkID = %d AND LinkType = %d" % (animalid, 0))
    db.execute(dbo, "DELETE FROM additional WHERE LinkID = %d AND LinkType IN (%s)" % (animalid, additional.ANIMAL_IN))
    db.execute(dbo, "DELETE FROM adoption WHERE AnimalID = %d" % animalid)
    db.execute(dbo, "DELETE FROM animalcontrol WHERE AnimalID = %d" % animalid)
    db.execute(dbo, "DELETE FROM animalmedical WHERE AnimalID = %d" % animalid)
    db.execute(dbo, "DELETE FROM animalmedicaltreatment WHERE AnimalID = %d" % animalid)
    db.execute(dbo, "DELETE FROM animalvaccination WHERE AnimalID = %d" % animalid)
    dbfs.delete_path(dbo, "/animal/%d" % animalid)
    db.execute(dbo, "DELETE FROM animal WHERE ID = %d" % animalid)

def update_daily_boarding_cost(dbo, username, animalid, cost):
    """
    Updates the daily boarding cost amount for an animal. The
    cost parameter should have already been turned into an integer.
    """
    oldcost = db.query_string(dbo, "SELECT DailyBoardingCost FROM animal WHERE ID = %d" % int(animalid) )
    db.execute(dbo, "UPDATE animal SET DailyBoardingCost = %s WHERE ID = %d" % ( str(cost), int(animalid) ))
    audit.edit(dbo, username, "animal", "%s: DailyBoardingCost %s ==> %s" % ( str(animalid), oldcost, str(cost) ))

def update_preferred_web_media_notes(dbo, username, animalid, newnotes):
    """
    Updates the preferred web media notes for an animal.
    """
    mediaid = db.query_int(dbo, "SELECT ID FROM media WHERE " \
        "WebsitePhoto = 1 AND LinkID = %d AND LinkTypeID = %d" % \
        (int(animalid), media.ANIMAL))
    if mediaid > 0:
        db.execute(dbo, "UPDATE media SET MediaNotes = '%s', UpdatedSinceLastPublish = 1 WHERE " \
            "ID = %d" % (db.escape(newnotes), mediaid))
        audit.edit(dbo, username, "media", str(mediaid) + "notes => " + newnotes)
 
def insert_diet_from_form(dbo, username, post):
    """
    Creates a diet record from posted form data
    """
    ndietid = db.get_id(dbo, "animaldiet")
    sql = db.make_insert_user_sql(dbo, "animaldiet", username, ( 
        ( "ID", db.di(ndietid)),
        ( "AnimalID", post.db_integer("animalid")),
        ( "DietID", post.db_integer("type")),
        ( "DateStarted", post.db_date("startdate")),
        ( "Comments", post.db_string("comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animaldiet", str(ndietid))
    return ndietid

def update_diet_from_form(dbo, username, post):
    """
    Updates a diet record from posted form data
    """
    dietid = post.integer("dietid")
    sql = db.make_update_user_sql(dbo, "animaldiet", username, "ID=%d" % dietid, ( 
        ( "DietID", post.db_integer("type")),
        ( "DateStarted", post.db_date("startdate")),
        ( "Comments", post.db_string("comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animaldiet WHERE ID = %d" % dietid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animaldiet WHERE ID = %d" % dietid)
    audit.edit(dbo, username, "animaldiet", audit.map_diff(preaudit, postaudit))

def delete_diet(dbo, username, did):
    """
    Deletes the selected diet
    """
    audit.delete(dbo, username, "animaldiet", str(db.query(dbo, "SELECT * FROM animaldiet WHERE ID=%d" % int(did))))
    db.execute(dbo, "DELETE FROM animaldiet WHERE ID = %d" % int(did))

def insert_cost_from_form(dbo, username, post):
    """
    Creates a cost record from posted form data
    """
    l = dbo.locale
    ncostid = db.get_id(dbo, "animalcost")
    if post.date("costdate") is None:
        raise utils.ASMValidationError(_("Cost date must be a valid date", l))
    sql = db.make_insert_user_sql(dbo, "animalcost", username, ( 
        ( "ID", db.di(ncostid)),
        ( "AnimalID", post.db_integer("animalid")),
        ( "CostTypeID", post.db_integer("type")),
        ( "CostDate", post.db_date("costdate")),
        ( "CostPaidDate", post.db_date("costpaid")),
        ( "CostAmount", post.db_integer("cost")),
        ( "Description", post.db_string("description"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animalcost", str(ncostid))
    return ncostid

def update_cost_from_form(dbo, username, post):
    """
    Updates a cost record from posted form data
    """
    costid = post.integer("costid")
    sql = db.make_update_user_sql(dbo, "animalcost", username, "ID=%d" % costid, ( 
        ( "CostTypeID", post.db_integer("type")),
        ( "CostDate", post.db_date("costdate")),
        ( "CostPaidDate", post.db_date("costpaid")),
        ( "CostAmount", post.db_integer("cost")),
        ( "Description", post.db_string("description"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animalcost WHERE ID = %d" % costid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animalcost WHERE ID = %d" % costid)
    audit.edit(dbo, username, "animalcost", audit.map_diff(preaudit, postaudit))

def delete_cost(dbo, username, cid):
    """
    Deletes a cost record
    """
    audit.delete(dbo, username, "animalcost", str(db.query(dbo, "SELECT * FROM animalcost WHERE ID = %d" % cid)))
    db.execute(dbo, "DELETE FROM animalcost WHERE ID = %d" % cid)

def insert_litter_from_form(dbo, username, post):
    """
    Creates a litter record from posted form data
    """
    nid = db.get_id(dbo, "animallitter")
    sql = db.make_insert_sql("animallitter", ( 
        ( "ID", db.di(nid)),
        ( "ParentAnimalID", post.db_integer("animal")),
        ( "SpeciesID", post.db_integer("species")),
        ( "Date", post.db_date("startdate")),
        ( "AcceptanceNumber", post.db_string("litterref")),
        ( "CachedAnimalsLeft", db.di(0)),
        ( "InvalidDate", post.db_date("expirydate")),
        ( "NumberInLitter", post.db_integer("numberinlitter")),
        ( "Comments", post.db_string("comments")),
        ( "RecordVersion", db.di(0))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animallitter", str(nid))
    update_active_litters(dbo)
    return nid

def update_litter_from_form(dbo, username, post):
    """
    Updates a litter record from posted form data
    """
    litterid = post.integer("litterid")
    sql = db.make_update_sql("animallitter", "ID=%d" % litterid, ( 
        ( "ParentAnimalID", post.db_integer("animal")),
        ( "SpeciesID", post.db_integer("species")),
        ( "Date", post.db_date("startdate")),
        ( "AcceptanceNumber", post.db_string("litterref")),
        ( "CachedAnimalsLeft", db.di(0)),
        ( "InvalidDate", post.db_date("expirydate")),
        ( "NumberInLitter", post.db_integer("numberinlitter")),
        ( "Comments", post.db_string("comments")),
        ( "RecordVersion", db.di(0))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animallitter WHERE ID = %d" % litterid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animallitter WHERE ID = %d" % litterid)
    audit.edit(dbo, username, "animallitter", audit.map_diff(preaudit, postaudit))
    update_active_litters(dbo)

def delete_litter(dbo, username, lid):
    """
    Deletes the selected litter
    """
    audit.delete(dbo, username, "animallitter", str(db.query(dbo, "SELECT * FROM animallitter WHERE ID=%d" % int(lid))))
    db.execute(dbo, "DELETE FROM animallitter WHERE ID = %d" % int(lid))

def update_variable_animal_data(dbo, animalid, a = None, animalupdatebatch = None):
    """
    Updates the variable data animal fields,
    MostRecentEntryDate, TimeOnShelter, AgrGroup, AnimalAge
    and DaysOnShelter
    (int) animalid: The animal to update
    a: An animal result to use instead of looking it up from the id
    animalupdatebatch: A batch of update parameters
    """
    if animalupdatebatch is not None:
        animalupdatebatch.append((
            calc_most_recent_entry(dbo, animalid, a),
            calc_time_on_shelter(dbo, animalid, a),
            calc_age_group(dbo, animalid, a),
            calc_age(dbo, animalid, a),
            calc_days_on_shelter(dbo, animalid, a),
            animalid
        ))
    else:
        s = db.make_update_sql("animal", "ID = %d" % animalid, (
            ( "MostRecentEntryDate", db.dd(calc_most_recent_entry(dbo, animalid, a))),
            ( "TimeOnShelter", db.ds(calc_time_on_shelter(dbo, animalid, a))),
            ( "AgeGroup", db.ds(calc_age_group(dbo, animalid, a))),
            ( "AnimalAge", db.ds(calc_age(dbo, animalid, a))),
            ( "DaysOnShelter", db.di(calc_days_on_shelter(dbo, animalid, a))) 
        ))
        db.execute(dbo, s)

def update_all_variable_animal_data(dbo):
    """
    Updates variable animal data for all animals
    """
    l = dbo.locale
    # We only need to do this once a day, skip if it's already
    # been run
    if configuration.variable_data_updated_today(dbo):
        al.debug("already done today", "animal.update_all_variable_animal_data", dbo)
        return

    # Update variable data for each animal
    animalupdatebatch = []
    animals = db.query(dbo, "SELECT ID, DateBroughtIn, DeceasedDate, Archived, ActiveMovementDate, DateOfBirth FROM animal")
    for a in animals:
        update_variable_animal_data(dbo, int(a["ID"]), a, animalupdatebatch)

    db.execute_many(dbo, "UPDATE animal SET " \
        "MostRecentEntryDate = %s, " \
        "TimeOnShelter = %s, " \
        "AgeGroup = %s, " \
        "AnimalAge = %s, " \
        "DaysOnShelter = %s " \
        "WHERE ID = %s", animalupdatebatch)

    al.debug("updated variable data for %d animals (locale %s)" % (len(animals), l), "animal.update_all_variable_animal_data", dbo)

    # Mark the data as updated today
    configuration.set_variable_data_updated_today(dbo)

def update_all_animal_statuses(dbo):
    """
    Updates statuses for all animals
    """
    animals = db.query(dbo, get_animal_query(dbo))
    animalupdatebatch = []
    diaryupdatebatch = []

    for a in animals:
        update_animal_status(dbo, int(a["ID"]), a, animalupdatebatch, diaryupdatebatch)

    db.execute_many(dbo, "UPDATE animal SET " \
        "Archived = %s, " \
        "ActiveMovementID = %s, " \
        "ActiveMovementDate = %s, " \
        "ActiveMovementType = %s, " \
        "ActiveMovementReturn = %s, " \
        "DisplayLocation = %s, " \
        "HasActiveReserve = %s, " \
        "HasTrialAdoption = %s, " \
        "HasPermanentFoster = %s " \
        "WHERE ID = %s", animalupdatebatch)
    aff = db.execute_many(dbo, "UPDATE diary SET LinkInfo = %s WHERE LinkType = %s AND LinkID = %s", diaryupdatebatch)
    al.debug("updated %d animal statuses (%d)" % (aff, len(animals)), "animal.update_all_animal_statuses", dbo)

def update_foster_animal_statuses(dbo):
    """
    Updates statuses for all animals on foster
    """
    animals = db.query(dbo, get_animal_query(dbo) + " WHERE a.ActiveMovementType = 2")
    animalupdatebatch = []
    diaryupdatebatch = []

    for a in animals:
        update_animal_status(dbo, int(a["ID"]), a, animalupdatebatch, diaryupdatebatch)

    db.execute_many(dbo, "UPDATE animal SET " \
        "Archived = %s, " \
        "ActiveMovementID = %s, " \
        "ActiveMovementDate = %s, " \
        "ActiveMovementType = %s, " \
        "ActiveMovementReturn = %s, " \
        "DisplayLocation = %s, " \
        "HasActiveReserve = %s, " \
        "HasTrialAdoption = %s, " \
        "HasPermanentFoster = %s " \
        "WHERE ID = %s", animalupdatebatch)
    aff = db.execute_many(dbo, "UPDATE diary SET LinkInfo = %s WHERE LinkType = %s AND LinkID = %s", diaryupdatebatch)
    al.debug("updated %d fostered animal statuses (%d)" % (aff, len(animals)), "animal.update_foster_animal_statuses", dbo)

def update_on_shelter_animal_statuses(dbo):
    """
    Updates statuses for all animals on shelter
    """
    animals = db.query(dbo, get_animal_query(dbo) + " WHERE a.Archived = 0")
    animalupdatebatch = []
    diaryupdatebatch = []

    for a in animals:
        update_animal_status(dbo, int(a["ID"]), a, animalupdatebatch, diaryupdatebatch)

    db.execute_many(dbo, "UPDATE animal SET " \
        "Archived = %s, " \
        "ActiveMovementID = %s, " \
        "ActiveMovementDate = %s, " \
        "ActiveMovementType = %s, " \
        "ActiveMovementReturn = %s, " \
        "DisplayLocation = %s, " \
        "HasActiveReserve = %s, " \
        "HasTrialAdoption = %s, " \
        "HasPermanentFoster = %s " \
        "WHERE ID = %s", animalupdatebatch)
    aff = db.execute_many(dbo, "UPDATE diary SET LinkInfo = %s WHERE LinkType = %s AND LinkID = %s", diaryupdatebatch)
    al.debug("updated %d on shelter animal statuses (%d)" % (aff, len(animals)), "animal.update_on_shelter_animal_statuses", dbo)

def update_animal_check_bonds(dbo, animalid):
    """
    Checks the bonds on animalid and if necessary, creates
    links back to animalid from the bonded animals
    """

    def addbond(tanimalid, bondid):
        tbond = db.query(dbo, "SELECT BondedAnimalID, BondedAnimal2ID FROM animal WHERE ID = %d" % int(tanimalid))
        if len(tbond) == 0: return
        # If a bond already exists, don't do anything
        if tbond[0]["BONDEDANIMALID"] == bondid: return
        if tbond[0]["BONDEDANIMAL2ID"] == bondid: return
        # Add a bond if we have a free slot
        if tbond[0]["BONDEDANIMALID"] == 0:
            db.execute(dbo, "UPDATE animal SET BondedAnimalID = %d WHERE ID = %d" % ( int(bondid), int(tanimalid) ))
            return
        if tbond[0]["BONDEDANIMAL2ID"] == 0:
            db.execute(dbo, "UPDATE animal SET BondedAnimal2ID = %d WHERE ID = %d" % ( int(bondid), int(tanimalid) ))

    bonds = db.query(dbo, "SELECT BondedAnimalID, BondedAnimal2ID FROM animal WHERE ID = %d" % int(animalid))
    if len(bonds) == 0: return
    bond1 = bonds[0]["BONDEDANIMALID"]
    bond2 = bonds[0]["BONDEDANIMAL2ID"]
    if bond1 != 0: addbond(bond1, animalid)
    if bond2 != 0: addbond(bond2, animalid)

def update_animal_status(dbo, animalid, a = None, animalupdatebatch = None, diaryupdatebatch = None):
    """
    Updates the movement status fields on an animal record: 
        ActiveMovement*, HasActiveReserve, HasTrialAdoption, MostRecentEntryDate, Archived and DisplayLocation.

    a can be an already loaded animal record
    animalupdatebatch and diaryupdatebatch are lists of parameters that can be passed to
    db.execute_many to do all updates in one hit where necessary. If they are passed, we'll
    append our changes to them. If they aren't passed, then we do any database updates now.
    """

    l = dbo.locale
    on_shelter = True
    has_reserve = False
    has_trial = False
    has_permanent_foster = False
    last_return = None
    activemovementid = 0
    activemovementdate = None
    activemovementtype = None
    activemovementtypename = None
    activemovementreturn = None
    currentownerid = None
    currentownername = None
    b2i = lambda x: x and 1 or 0

    if a is None:
        a = get_animal(dbo, animalid)
        if a is None: return

    movements = db.query(dbo, "SELECT ID, MovementType, MovementDate, ReturnDate, " \
        "ReservationDate, ReservationCancelledDate, IsTrial, IsPermanentFoster FROM adoption " \
        "WHERE AnimalID = %d ORDER BY MovementDate DESC" % animalid)

    for m in movements:

        # If there's an open movement today, our animal can't be on the shelter
        if (m["MOVEMENTDATE"] is not None and m["MOVEMENTDATE"] <= now() and m["RETURNDATE"] is None) or \
            (m["MOVEMENTDATE"] is not None and m["MOVEMENTDATE"] <= now() and m["RETURNDATE"] > now()):
            on_shelter = False

        # Does it have an active reservation?
        if m["RETURNDATE"] is None and m["MOVEMENTTYPE"] == movement.NO_MOVEMENT \
            and m["MOVEMENTDATE"] is None and m["RESERVATIONCANCELLEDDATE"] == None and \
            m["RESERVATIONDATE"] is not None:
            has_reserve = True

        # Does it have a trial adoption?
        if m["MOVEMENTTYPE"] == movement.ADOPTION and m["ISTRIAL"] == 1:
            has_trial = True

        # A permanent foster?
        if m["MOVEMENTTYPE"] == movement.FOSTER and m["ISPERMANENTFOSTER"] == 1:
            has_permanent_foster = True

        # Update the last time the animal was returned
        if m["RETURNDATE"] is not None:
            if last_return is None: last_return = m["RETURNDATE"]
            if m["RETURNDATE"] > last_return: last_return = m["RETURNDATE"]


    # Override the other flags if the animal is dead
    if a["DECEASEDDATE"] is not None:
        on_shelter = False
        has_trial = False
        has_reserve = False

    # Override the on shelter flag if the animal is a non-shelter animal
    if a["NONSHELTERANIMAL"] == 1:
        on_shelter = False

    # Stamp our latest return date (or null if there isn't one)
    db.execute(dbo, "UPDATE animal SET ActiveMovementReturn = " + db.dd(last_return) + 
        " WHERE ID = %d" % animalid)

    # If the animal is on the shelter, or is a nonshelter animal then it has no active movement
    if not on_shelter and a["NONSHELTERANIMAL"] != 1:
        
        # Find the latest movement for our animal
        latest = get_latest_movement(dbo, animalid)

        # We got one, load some data for storing on our animal record
        if latest is not None:
            activemovementid = latest["ID"]
            activemovementdate = latest["MOVEMENTDATE"]
            activemovementtype = latest["MOVEMENTTYPE"]
            activemovementtypename = latest["MOVEMENTTYPENAME"]
            activemovementreturn = latest["RETURNDATE"]
            currentownerid = latest["CURRENTOWNERID"]
            currentownername = latest["CURRENTOWNERNAME"]

            # If the active movement is a foster and we're treating fosters
            # as on shelter, we should mark the animal as on shelter
            if latest["MOVEMENTTYPE"] == movement.FOSTER and configuration.foster_on_shelter(dbo) \
                and a["DECEASEDDATE"] is None:
                on_shelter = True

            # If the active movement is a retailer and we're treating retailers
            # as on shelter, we should mark the animal as on shelter
            if latest["MOVEMENTTYPE"] == movement.RETAILER and configuration.retailer_on_shelter(dbo) \
                and a["DECEASEDDATE"] is None:
                on_shelter = True

            # If the active movement is a trial adoption and we're treating
            # trial adoptions as on shelter, we should mark accordingly
            if latest["MOVEMENTTYPE"] == movement.ADOPTION and latest["ISTRIAL"] == 1 \
                and configuration.trial_on_shelter(dbo) and a["DECEASEDDATE"] is None:
                on_shelter = True

            # If the active movement is transport, we treat that as on shelter
            if latest["MOVEMENTTYPE"] == movement.TRANSPORT and a["DECEASEDDATE"] is None:
                on_shelter = True

    # Calculate location and qualified display location
    loc = ""
    qlocname = ""
    if a["DECEASEDDATE"] is not None:
        loc = _("Deceased", l)
        qlocname = loc
        if a["PUTTOSLEEP"] == 1:
            qlocname = "%s::%s" % (qlocname, a["PTSREASONNAME"])
    elif activemovementdate is not None:
        loc = activemovementtypename
        qlocname = loc
        if currentownerid is not None and currentownername is not None:
            qlocname = "%s::%s" % (loc, currentownername)
    else:
        loc = a["SHELTERLOCATIONNAME"]
        qlocname = loc

    # Has anything actually changed?
    if a["ARCHIVED"] == b2i(not on_shelter) and \
       a["ACTIVEMOVEMENTID"] == activemovementid and \
       a["ACTIVEMOVEMENTDATE"] == activemovementdate and \
       a["ACTIVEMOVEMENTTYPE"] == activemovementtype and \
       a["ACTIVEMOVEMENTRETURN"] == activemovementreturn and \
       a["HASACTIVERESERVE"] == b2i(has_reserve) and \
       a["HASTRIALADOPTION"] == b2i(has_trial) and \
       a["HASPERMANENTFOSTER"] == b2i(has_permanent_foster) and \
       a["DISPLAYLOCATION"] == qlocname:
        # No - don't do anything
        return

    # Update our in memory animal
    a["ARCHIVED"] = b2i(not on_shelter)
    a["ACTIVEMOVEMENTID"] = activemovementid
    a["ACTIVEMOVEMENTDATE"] = activemovementdate
    a["ACTIVEMOVEMENTTYPE"] = activemovementtype
    a["ACTIVEMOVEMENTRETURN"] = activemovementreturn
    a["HASACTIVERESERVE"] = b2i(has_reserve)
    a["HASTRIALADOPTION"] = b2i(has_trial)
    a["HASPERMANENTFOSTER"] = b2i(has_permanent_foster)
    a["DISPLAYLOCATION"] = qlocname

    # If we have an animal batch going, append to it
    if animalupdatebatch is not None:
        animalupdatebatch.append((
            b2i(not on_shelter),
            activemovementid,
            activemovementdate,
            activemovementtype,
            activemovementreturn,
            qlocname,
            b2i(has_reserve),
            b2i(has_trial),
            b2i(has_permanent_foster),
            animalid
        ))
    else:
        # Just do the DB update now
        db.execute(dbo, db.make_update_sql("animal", "ID=%d" % animalid, (
            ( "Archived", db.di(b2i(not on_shelter)) ),
            ( "ActiveMovementID", db.di(activemovementid) ),
            ( "ActiveMovementDate", db.dd(activemovementdate) ),
            ( "ActiveMovementType", db.di(activemovementtype) ),
            ( "ActiveMovementReturn", db.dd(activemovementreturn) ),
            ( "DisplayLocation", db.ds(qlocname) ),
            ( "HasActiveReserve", db.di(b2i(has_reserve)) ),
            ( "HasTrialAdoption", db.di(b2i(has_trial)) ),
            ( "HasPermanentFoster", db.di(b2i(has_permanent_foster)) )
            )))

    # Update the location on any diary notes for this animal
    diaryloc = "%s %s - %s" % ( a["SHELTERCODE"], a["ANIMALNAME"], loc)
    if diaryupdatebatch is not None:
        diaryupdatebatch.append( (diaryloc, diary.ANIMAL, animalid) )
    else:
        db.execute(dbo, "UPDATE diary SET LinkInfo = %s WHERE LinkType = %d AND LinkID = %d" % (
            db.ds(diaryloc), diary.ANIMAL, animalid ))
  
def get_number_animals_on_shelter(dbo, date, speciesid = 0, animaltypeid = 0, internallocationid = 0, ageselection = 0):
    """
    Returns the number of animals on shelter at a given date for a species, type,
    location and optionally for an ageselection - 0 = allages, 1 = under six months, 2 = over six months
    """
    sdate = db.dd(date)
    sixmonthsago = db.dd(subtract_days(date, 182))
    sql = "SELECT COUNT(ID) FROM animal WHERE "
    if speciesid != 0:
        sql += "SpeciesID = %d" % speciesid
    else:
        sql += "AnimalTypeID = %d" % animaltypeid
    sql += " AND DateBroughtIn <= %s AND NonShelterAnimal = 0" % sdate
    sql += " AND (DeceasedDate > %s OR DeceasedDate Is Null)" % sdate
    if internallocationid != 0:
        sql += " AND ShelterLocation = %d" % internallocationid
    if ageselection == 1:
        sql += " AND DateOfBirth >= %s" % sixmonthsago
    if ageselection == 2:
        sql += " AND DateOfBirth < %s" % sixmonthsago
    sql += " AND 0 = (SELECT COUNT(adoption.ID) FROM adoption " \
        "WHERE AnimalID = animal.ID AND MovementDate Is Not Null AND " \
        "MovementDate <= %s AND (ReturnDate Is Null OR ReturnDate > %s))" % (sdate, sdate)
    return db.query_int(dbo, sql)

def get_number_litters_on_shelter(dbo, date, speciesid = 0):
    """
    Returns the number of active litters at a given date, optionally
    for a single species.
    """
    sdate = db.dd(date)
    sql = "SELECT COUNT(a.ID) FROM animallitter a " \
        "WHERE a.Date <= %s " % sdate
    if speciesid != 0:
        sql += "AND SpeciesID = %d " % speciesid
    sql += "AND (InvalidDate Is Null OR InvalidDate > %s)" % sdate
    return db.query_int(dbo, sql)

def get_number_animals_on_foster(dbo, date, speciesid = 0, animaltypeid = 0):
    """
    Returns the number of animals on foster at a given date for a species or type
    """
    sdate = db.dd(date)
    sql = "SELECT COUNT(ID) FROM animal " \
        "WHERE "
    if speciesid != 0:
        sql += "SpeciesID = %d" % speciesid
    else:
        sql += "AnimalTypeID = %d" % animaltypeid
    sql += " AND DateBroughtIn <= %s" % sdate
    sql += " AND NonShelterAnimal = 0"
    sql += " AND (DeceasedDate > %s OR DeceasedDate Is Null)" % sdate
    sql += " AND EXISTS(SELECT AdoptionNumber FROM adoption WHERE "
    sql += " MovementType = %d" % movement.FOSTER
    sql += " AND MovementDate <= %s" % sdate
    sql += " AND AnimalID = animal.ID"
    sql += " AND (ReturnDate > %s OR ReturnDate Is Null))" % sdate
    return db.query_int(dbo, sql)

def update_animal_figures(dbo, month = 0, year = 0):
    """
    Updates the animal figures table for the month and year given.
    If month and year aren't given, defaults to this month, unless today is
    the first day of the month in which case we do last month.
    """

    batch = []
    nid = db._get_id_max(dbo, "animalfigures")

    def sql_days(sql):
        """ Returns a query with THEDATE and TOTAL as a dictionary for add_row """
        d = {}
        for i in xrange(1, 32):
            d["D%d" % i] = "0"
        rows = db.query(dbo, sql)
        for r in rows:
            dk = "D%d" % r["THEDATE"].day
            d[dk] = r["TOTAL"]
        return d

    def add_days(listdays):
        """ Adds up a list of day dictionaries """
        d = {}
        for i in xrange(1, 32):
            d["D%d" % i] = 0
        for cd in listdays:
            if not cd.has_key("D29"): cd["D29"] = 0
            if not cd.has_key("D30"): cd["D30"] = 0
            if not cd.has_key("D31"): cd["D31"] = 0
            for i in xrange(1, 32):
                dk = "D%d" % i
                if cd.has_key(dk):
                    d[dk] = int(d[dk]) + int(cd[dk])
        return d

    def is_zero_days(days):
        """ Returns true if a map of day counts is all zero """
        for i in xrange(1, 32):
            dk = "D%d" % i
            if days.has_key(dk) and int(days[dk]) > 0:
                return False
        return True

    def sub_days(initdic, subdic):
        """ Subtracts day dictionary subdic from initdic """
        d = initdic.copy()
        cd = subdic
        if not d.has_key("D29"): d["D29"] = 0
        if not d.has_key("D30"): d["D30"] = 0
        if not d.has_key("D31"): d["D31"] = 0
        if not cd.has_key("D29"): cd["D29"] = 0
        if not cd.has_key("D30"): cd["D30"] = 0
        if not cd.has_key("D31"): cd["D31"] = 0
        for i in xrange(1, 32):
            dk = "D%d" % i
            d[dk] = int(d[dk]) - int(cd[dk])
        return d

    def add_row(orderindex, code, animaltypeid, speciesid, maxdaysinmonth, heading, bold, calctotal, days):
        """ Adds a row to the animalfigures table """
        if not days.has_key("D29"): days["D29"] = 0
        if not days.has_key("D30"): days["D30"] = 0
        if not days.has_key("D31"): days["D31"] = 0
        avg = 0.0
        tot = 0
        total = ""
        for i in xrange(1, maxdaysinmonth + 1):
            avg += int(days["D%d" % i])
            tot += int(days["D%d" %i])
        avg = round(float(float(avg) / float(maxdaysinmonth)), 1)
        if calctotal: 
            total = str(tot)
        batch.append((
            nid + len(batch),
            month,
            year,
            orderindex,
            code,
            animaltypeid,
            speciesid,
            maxdaysinmonth,
            heading,
            bold,
            days["D1"],
            days["D2"],
            days["D3"],
            days["D4"],
            days["D5"],
            days["D6"],
            days["D7"],
            days["D8"],
            days["D9"],
            days["D10"],
            days["D11"],
            days["D12"],
            days["D13"],
            days["D14"],
            days["D15"],
            days["D16"],
            days["D17"],
            days["D18"],
            days["D19"],
            days["D20"],
            days["D21"],
            days["D22"],
            days["D23"],
            days["D24"],
            days["D25"],
            days["D26"],
            days["D27"],
            days["D28"],
            days["D29"],
            days["D30"],
            days["D31"],
            total,
            avg
        ))

    def update_db(month, year):
        """ Writes all of our figures to the database """
        db.execute(dbo, "DELETE FROM animalfigures WHERE Month = %d AND Year = %d" % (month, year))
        sql = "INSERT INTO animalfigures (ID, Month, Year, OrderIndex, Code, AnimalTypeID, " \
            "SpeciesID, MaxDaysInMonth, Heading, Bold, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, " \
            "D11, D12, D13, D14, D15, D16, D17, D18, D19, D20, D21, D22, D23, D24, D25, D26, " \
            "D27, D28, D29, D30, D31, Total, Average) VALUES (%s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s, %s)"
        db.execute_many(dbo, sql, batch)
        al.debug("wrote %d figures records" % len(batch), "animal.update_animal_figures", dbo)

    # If month and year are zero, figure out which one we're going
    # to generate for. We use this month, unless today is the first
    # of the month, in which case we do last month
    if month == 0 and year == 0:
        today = now()
        if today.day == 1: today = subtract_months(today, 1)
        month = today.month
        year = today.year
    al.debug("Generating animal figures for month=%d, year=%d" % (month, year), "animal.update_animal_figures", dbo)

    l = dbo.locale
    fom = datetime.datetime(year, month, 1)
    lom = last_of_month(fom)
    firstofmonth = db.dd(fom)
    lastofmonth = db.dd(lom)
    daysinmonth = lom.day
    loopdays = daysinmonth + 1

    # Species =====================================
    allspecies = lookups.get_species(dbo)
    for sp in allspecies:

        speciesid = int(sp["ID"])

        # If we never had anything for this species, skip it
        if 0 == db.query_int(dbo, "SELECT COUNT(*) FROM animal WHERE SpeciesID = %d" % speciesid):
            continue

        # On Shelter
        onshelter = {}
        for i in xrange(1, loopdays):
            d = datetime.datetime(year, month, i)
            dk = "D%d" % i
            onshelter[dk] = get_number_animals_on_shelter(dbo, d, speciesid)
        add_row(1, "SP_ONSHELTER", 0, speciesid, daysinmonth, _("On Shelter", l), 0, False, onshelter)

        # On Foster (if foster on shelter set)
        if configuration.foster_on_shelter(dbo):
            onfoster = {}
            for i in xrange(1, loopdays):
                d = datetime.datetime(year, month, i)
                dk = "D%d" % i
                onfoster[dk] = get_number_animals_on_foster(dbo, d, speciesid)
            add_row(2, "SP_ONFOSTER", 0, speciesid, daysinmonth, _("On Foster (in figures)", l), 0, False, onfoster)
            #sheltertotal = add_days((onshelter, onfoster)) double count
            sheltertotal = onshelter
        else:
            sheltertotal = onshelter

        # Litters
        litters = {}
        for i in xrange(1, loopdays):
            d = datetime.datetime(year, month, i)
            dk = "D%d" % i
            litters[dk] = get_number_litters_on_shelter(dbo, d, speciesid)
        add_row(3, "SP_LITTERS", 0, speciesid, daysinmonth, _("Litters", l), 0, False, litters)

        # Start of day total - handled at the end.

        # Brought In
        # If the config option is on, output a row for each entry
        # category or a single line for brought in.
        if configuration.animal_figures_split_entryreason(dbo):
            reasons = lookups.get_entryreasons(dbo)
            idx = 5
            broughtin = {}
            for er in reasons:
                erline = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
                    "SpeciesID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
                    "AND IsTransfer = 0 AND NonShelterAnimal = 0 AND EntryReasonID = %d " \
                    "GROUP BY DateBroughtIn" % (speciesid, firstofmonth, lastofmonth, er["ID"]))
                if not is_zero_days(erline):
                    add_row(idx, "SP_ER_%d" % er["ID"], 0, speciesid, daysinmonth, er["REASONNAME"], 0, True, erline)
                    idx += 1
                    broughtin = add_days((broughtin, erline))
        else:
            broughtin = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
                "SpeciesID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
                "AND IsTransfer = 0 AND NonShelterAnimal = 0 " \
                "GROUP BY DateBroughtIn" % (speciesid, firstofmonth, lastofmonth))
            add_row(5, "SP_BROUGHTIN", 0, speciesid, daysinmonth, _("Incoming", l), 0, True, broughtin)

        # Returned
        returned = sql_days("SELECT ReturnDate AS TheDate, COUNT(animal.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON adoption.AnimalID = animal.ID " \
            "WHERE SpeciesID = %d AND ReturnDate >= %s AND ReturnDate <= %s " \
            "AND MovementType = %d " \
            "GROUP BY ReturnDate" % (speciesid, firstofmonth, lastofmonth, movement.ADOPTION))
        add_row(106, "SP_RETURNED", 0, speciesid, daysinmonth, _("Returned", l), 0, True, returned)

        # Transferred In
        transferin = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
            "SpeciesID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
            "AND IsTransfer <> 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DateBroughtIn" % (speciesid, firstofmonth, lastofmonth))
        add_row(107, "SP_TRANSFERIN", 0, speciesid, daysinmonth, _("Transferred In", l), 0, True, transferin)

        # Returned From Fostering
        returnedfoster = sql_days("SELECT ReturnDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND ReturnDate >= %s AND ReturnDate <= %s " \
            "GROUP BY ReturnDate" % (speciesid, movement.FOSTER, firstofmonth, lastofmonth))
        add_row(108, "SP_RETURNEDFOSTER", 0, speciesid, daysinmonth, _("From Fostering", l), 0, True, returnedfoster)

        # Returned From Other
        returnedother = sql_days("SELECT ReturnDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType <> %d AND MovementType <> %d " \
            "AND ReturnDate >= %s AND ReturnDate <= %s " \
            "GROUP BY ReturnDate" % (speciesid, movement.FOSTER, movement.ADOPTION, firstofmonth, lastofmonth))
        add_row(109, "SP_RETURNEDOTHER", 0, speciesid, daysinmonth, _("From Other", l), 0, True, returnedother)

        # In subtotal
        insubtotal = add_days((broughtin, returned, transferin, returnedfoster, returnedother))
        add_row(110, "SP_INTOTAL", 0, speciesid, daysinmonth, _("In SubTotal", l), 1, False, insubtotal)

        # Adopted
        adopted = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.ADOPTION, firstofmonth, lastofmonth))
        add_row(111, "SP_ADOPTED", 0, speciesid, daysinmonth, _("Adopted", l), 0, True, adopted)

        # Reclaimed
        reclaimed = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.RECLAIMED, firstofmonth, lastofmonth))
        add_row(112, "SP_RECLAIMED", 0, speciesid, daysinmonth, _("Returned To Owner", l), 0, True, reclaimed)

        # Escaped
        escaped = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.ESCAPED, firstofmonth, lastofmonth))
        add_row(113, "SP_ESCAPED", 0, speciesid, daysinmonth, _("Escaped", l), 0, True, escaped)

        # Stolen
        stolen = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.STOLEN, firstofmonth, lastofmonth))
        add_row(114, "SP_STOLEN", 0, speciesid, daysinmonth, _("Stolen", l), 0, True, stolen)

        # Released
        released = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.RELEASED, firstofmonth, lastofmonth))
        add_row(115, "SP_RELEASED", 0, speciesid, daysinmonth, _("Released To Wild", l), 0, True, released)

        # Transferred
        transferred = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.TRANSFER, firstofmonth, lastofmonth))
        add_row(116, "SP_TRANSFERRED", 0, speciesid, daysinmonth, _("Transferred Out", l), 0, True, transferred)

        # Fostered
        fostered = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.FOSTER, firstofmonth, lastofmonth))
        add_row(117, "SP_FOSTERED", 0, speciesid, daysinmonth, _("To Fostering", l), 0, True, fostered)

        # Retailer
        retailer = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, movement.RETAILER, firstofmonth, lastofmonth))
        add_row(118, "SP_RETAILER", 0, speciesid, daysinmonth, _("To Retailer", l), 0, True, retailer)

        # Died
        died = sql_days("SELECT DeceasedDate AS TheDate, COUNT(animal.ID) AS Total FROM animal WHERE " \
            "SpeciesID = %d AND DeceasedDate >= %s AND DeceasedDate <= %s " \
            "AND PutToSleep = 0 AND DiedOffShelter = 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DeceasedDate" % (speciesid, firstofmonth, lastofmonth))
        add_row(119, "SP_DIED", 0, speciesid, daysinmonth, _("Died", l), 0, True, died)

        # PTS
        pts = sql_days("SELECT DeceasedDate AS TheDate, COUNT(animal.ID) AS Total FROM animal WHERE " \
            "SpeciesID = %d AND DeceasedDate >= %s AND DeceasedDate <= %s " \
            "AND PutToSleep <> 0 AND DiedOffShelter = 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DeceasedDate" % (speciesid, firstofmonth, lastofmonth))
        add_row(120, "SP_PTS", 0, speciesid, daysinmonth, _("Euthanized", l), 0, True, pts)

        # Other
        toother = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "SpeciesID = %d AND MovementType NOT IN (1, 2, 3, 4, 5, 6, 7, 8) " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (speciesid, firstofmonth, lastofmonth))
        add_row(121, "SP_OUTOTHER", 0, speciesid, daysinmonth, _("To Other", l), 0, True, toother)

        # Out subtotal
        outsubtotal = add_days((adopted, reclaimed, escaped, stolen, released, transferred, fostered, retailer, died, pts, toother))
        add_row(122, "SP_OUTTOTAL", 0, speciesid, daysinmonth, _("Out SubTotal", l), 1, False, outsubtotal)

        # Start of day total
        starttotal = sub_days(sheltertotal, insubtotal)
        starttotal = add_days((starttotal, outsubtotal))
        add_row(4, "SP_STARTTOTAL", 0, speciesid, daysinmonth, _("Start Of Day", l), 1, False, starttotal)

        # End of day
        add_row(123, "SP_TOTAL", 0, speciesid, daysinmonth, _("End Of Day", l), 1, False, sheltertotal)

    # Animal Types =====================================
    alltypes = lookups.get_animal_types(dbo)
    for at in alltypes:

        typeid = int(at["ID"])

        # If we never had anything for this type, skip it
        if 0 == db.query_int(dbo, "SELECT COUNT(*) FROM animal WHERE AnimalTypeID = %d" % typeid):
            continue

        # On Shelter
        onshelter = {}
        for i in xrange(1, loopdays):
            d = datetime.datetime(year, month, i)
            dk = "D%d" % i
            onshelter[dk] = get_number_animals_on_shelter(dbo, d, 0, typeid)
        add_row(1, "AT_ONSHELTER", typeid, 0, daysinmonth, _("On Shelter", l), 0, False, onshelter)

        # On Foster (if foster on shelter set)
        if configuration.foster_on_shelter(dbo):
            onfoster = {}
            for i in xrange(1, loopdays):
                d = datetime.datetime(year, month, i)
                dk = "D%d" % i
                onfoster[dk] = get_number_animals_on_foster(dbo, d, 0, typeid)
            add_row(2, "AT_ONFOSTER", typeid, 0, daysinmonth, _("On Foster (in figures)", l), 0, False, onfoster)
            #sheltertotal = add_days((onshelter, onfoster)) double count
            sheltertotal = onshelter
        else:
            sheltertotal = onshelter

        # Start of day - handled later

        # Brought In
        # If the config option is on, output a row for each entry
        # category or a single line for brought in.
        if configuration.animal_figures_split_entryreason(dbo):
            reasons = lookups.get_entryreasons(dbo)
            broughtin = {}
            idx = 5
            for er in reasons:
                erline = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
                    "AnimalTypeID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
                    "AND IsTransfer = 0 AND NonShelterAnimal = 0 AND EntryReasonID = %d " \
                    "GROUP BY DateBroughtIn" % (typeid, firstofmonth, lastofmonth, er["ID"]))
                if not is_zero_days(erline):
                    add_row(idx, "AT_ER_%d" % er["ID"], typeid, 0, daysinmonth, er["REASONNAME"], 0, True, erline)
                    broughtin = add_days((broughtin, erline))
                    idx += 1
        else:
            # Brought In
            broughtin = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
                "AnimalTypeID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
                "AND IsTransfer = 0 AND NonShelterAnimal = 0 " \
                "GROUP BY DateBroughtIn" % (typeid, firstofmonth, lastofmonth))
            add_row(5, "AT_BROUGHTIN", typeid, 0, daysinmonth, _("Incoming", l), 0, True, broughtin)

        # Returned
        returned = sql_days("SELECT ReturnDate AS TheDate, COUNT(animal.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON adoption.AnimalID = animal.ID " \
            "WHERE AnimalTypeID = %d AND ReturnDate >= %s AND ReturnDate <= %s " \
            "AND MovementType = %d " \
            "GROUP BY ReturnDate" % (typeid, firstofmonth, lastofmonth, movement.ADOPTION))
        add_row(6, "AT_RETURNED", typeid, 0, daysinmonth, _("Returned", l), 0, True, returned)

        # Transferred In
        transferin = sql_days("SELECT DateBroughtIn AS TheDate, COUNT(ID) AS Total FROM animal WHERE " \
            "AnimalTypeID = %d AND DateBroughtIn >= %s AND DateBroughtIn <= %s " \
            "AND IsTransfer <> 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DateBroughtIn" % (typeid, firstofmonth, lastofmonth))
        add_row(7, "AT_TRANSFERIN", typeid, 0, daysinmonth, _("Transferred In", l), 0, True, transferin)

        # Returned From Fostering
        returnedfoster = sql_days("SELECT ReturnDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND ReturnDate >= %s AND ReturnDate <= %s " \
            "GROUP BY ReturnDate" % (typeid, movement.FOSTER, firstofmonth, lastofmonth))
        add_row(8, "AT_RETURNEDFOSTER", typeid, 0, daysinmonth, _("From Fostering", l), 0, True, returnedfoster)

        # Returned From Other
        returnedother = sql_days("SELECT ReturnDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType <> %d AND MovementType <> %d " \
            "AND ReturnDate >= %s AND ReturnDate <= %s " \
            "GROUP BY ReturnDate" % (typeid, movement.FOSTER, movement.ADOPTION, firstofmonth, lastofmonth))
        add_row(9, "AT_RETURNEDOTHER", typeid, 0, daysinmonth, _("From Other", l), 0, True, returnedother)

        # In subtotal
        insubtotal = add_days((broughtin, returned, transferin, returnedfoster, returnedother))
        add_row(10, "AT_INTOTAL", typeid, 0, daysinmonth, _("SubTotal", l), 1, False, insubtotal)

        # Adopted
        adopted = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.ADOPTION, firstofmonth, lastofmonth))
        add_row(11, "AT_ADOPTED", typeid, 0, daysinmonth, _("Adopted", l), 0, True, adopted)

        # Reclaimed
        reclaimed = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.RECLAIMED, firstofmonth, lastofmonth))
        add_row(12, "AT_RECLAIMED", typeid, 0, daysinmonth, _("Returned To Owner", l), 0, True, reclaimed)

        # Escaped
        escaped = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.ESCAPED, firstofmonth, lastofmonth))
        add_row(13, "AT_ESCAPED", typeid, 0, daysinmonth, _("Escaped", l), 0, True, escaped)

        # Stolen
        stolen = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.STOLEN, firstofmonth, lastofmonth))
        add_row(14, "AT_STOLEN", typeid, 0, daysinmonth, _("Stolen", l), 0, True, stolen)

        # Released
        released = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.RELEASED, firstofmonth, lastofmonth))
        add_row(15, "AT_RELEASED", typeid, 0, daysinmonth, _("Released To Wild", l), 0, True, released)

        # Transferred
        transferred = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.TRANSFER, firstofmonth, lastofmonth))
        add_row(16, "AT_TRANSFERRED", typeid, 0, daysinmonth, _("Transferred Out", l), 0, True, transferred)

        # Fostered
        fostered = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.FOSTER, firstofmonth, lastofmonth))
        add_row(17, "AT_FOSTERED", typeid, 0, daysinmonth, _("To Fostering", l), 0, True, fostered)

        # Retailer
        retailer = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType = %d " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, movement.RETAILER, firstofmonth, lastofmonth))
        add_row(18, "AT_RETAILER", typeid, 0, daysinmonth, _("To Retailer", l), 0, True, retailer)

        # Died
        died = sql_days("SELECT DeceasedDate AS TheDate, COUNT(animal.ID) AS Total FROM animal WHERE " \
            "AnimalTypeID = %d AND DeceasedDate >= %s AND DeceasedDate <= %s " \
            "AND PutToSleep = 0 AND DiedOffShelter = 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DeceasedDate" % (typeid, firstofmonth, lastofmonth))
        add_row(19, "AT_DIED", typeid, 0, daysinmonth, _("Died", l), 0, True, died)

        # PTS
        pts = sql_days("SELECT DeceasedDate AS TheDate, COUNT(animal.ID) AS Total FROM animal WHERE " \
            "AnimalTypeID = %d AND DeceasedDate >= %s AND DeceasedDate <= %s " \
            "AND PutToSleep <> 0 AND DiedOffShelter = 0 AND NonShelterAnimal = 0 " \
            "GROUP BY DeceasedDate" % (typeid, firstofmonth, lastofmonth))
        add_row(20, "AT_PTS", typeid, 0, daysinmonth, _("Euthanized", l), 0, True, pts)

        # Other
        toother = sql_days("SELECT MovementDate AS TheDate, COUNT(adoption.ID) AS Total FROM adoption " \
            "INNER JOIN animal ON animal.ID = adoption.AnimalID WHERE " \
            "AnimalTypeID = %d AND MovementType NOT IN (1, 2, 3, 4, 5, 6, 7, 8) " \
            "AND MovementDate >= %s AND MovementDate <= %s " \
            "GROUP BY MovementDate" % (typeid, firstofmonth, lastofmonth))
        add_row(21, "AT_OUTOTHER", typeid, 0, daysinmonth, _("To Other", l), 0, True, toother)

        # Out subtotal
        outsubtotal = add_days((adopted, reclaimed, escaped, stolen, released, transferred, fostered, retailer, died, pts, toother))
        add_row(22, "AT_OUTTOTAL", typeid, 0, daysinmonth, _("SubTotal", l), 1, False, outsubtotal)

        # Start of day total
        starttotal = sub_days(sheltertotal, insubtotal)
        starttotal = add_days((starttotal, outsubtotal))
        add_row(4, "AT_STARTTOTAL", typeid, 0, daysinmonth, _("Start Of Day", l), 1, False, starttotal)

        # End of day
        add_row(50, "AT_TOTAL", typeid, 0, daysinmonth, _("End Of Day", l), 1, False, sheltertotal)

    # Write out our db changes
    update_db(month, year)

def update_animal_figures_annual(dbo, year = 0):
    """
    Updates the animal figures annual table for the year given.
    If year isn't given, defaults to this year, unless today is the
    first of the year in which case we do last year.
    """
    batch = []
    nid = db._get_id_max(dbo, "animalfiguresannual")

    def add_row(orderindex, code, animaltypeid, speciesid, group, heading, bold, months):
        """ Adds a row to the animalfiguresannual table, unless it's all 0 """
        if months[12] == 0: return
        batch.append((
            nid + len(batch),
            year,
            orderindex,
            code,
            animaltypeid,
            speciesid,
            group,
            heading,
            bold,
            months[0],
            months[1],
            months[2],
            months[3],
            months[4],
            months[5],
            months[6],
            months[7],
            months[8],
            months[9],
            months[10],
            months[11],
            months[12]
        ))

    def sql_months(sql, babysplit = False, babymonths = 4):
        """ 
            Executes a query and returns two sets of months based on the
            results. 
            Query should have three columns - THEDATE, DOB and TOTAL.
            If babysplit is True, then babymonths is used to figure out
            whether the animal was a baby at the date in the result and
            if so, returns it in the second set.
            It will calculate the horizontal totals as well.
        """
        d = [0] * 13
        d2 = [0] * 13
        rows = db.query(dbo, sql)
        for r in rows:
            dk = r["THEDATE"].month - 1
            if not babysplit:
                d[dk] += r["TOTAL"]
            else:
                if date_diff_days(r["DOB"], r["THEDATE"]) > (babymonths * 31):
                    d[dk] += r["TOTAL"]
                else:
                    d2[dk] += r["TOTAL"]
        total = 0
        for v in d:
            total += v
        d[12] = total
        total = 0
        for v in d2:
            total += v
        d2[12] = total
        return d, d2

    def species_line(sql, speciesid, speciesname, code, group, orderindex, showbabies, babymonths):
        """
        Adds a line for a particular species.
        sql: The query to run
        """
        babyname = ""
        if speciesid == 1: babyname = _("Puppies (under {0} months)", l).format(babymonths)
        if speciesid == 2: babyname = _("Kittens (under {0} months)", l).format(babymonths)
        babysplit = babyname != "" and showbabies
        lines = sql_months(sql, babysplit, babymonths)
        add_row(orderindex, code, 0, speciesid, group, speciesname, 0, lines[0])
        if babysplit: add_row(orderindex, code + "_BABY", 0, speciesid, group, babyname, 0, lines[1])

    def type_line(sql, typeid, typename, code, group, orderindex, showbabies, babymonths):
        """
        Adds a line for a particular type.
        sql: The query to run
        """
        babyname = _("{0} (under {1} months)", l).format(typename, babymonths)
        lines = sql_months(sql, showbabies, babymonths)
        add_row(orderindex, code, typeid, 0, group, typename, 0, lines[0])
        if showbabies: add_row(orderindex, code + "_BABY", typeid, 0, group, babyname, 0, lines[1])

    def update_db(year):
        """ Writes all of our figures to the database """
        db.execute(dbo, "DELETE FROM animalfiguresannual WHERE Year = %d" % year)
        sql = "INSERT INTO animalfiguresannual (ID, Year, OrderIndex, Code, AnimalTypeID, " \
            "SpeciesID, GroupHeading, Heading, Bold, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, " \
            "M11, M12, Total) VALUES (%s, %s, %s, %s, %s, " \
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
            "%s, %s, %s)"
        db.execute_many(dbo, sql, batch)
        al.debug("wrote %d annual figures records" % len(batch), "animal.update_animal_figures_annual", dbo)

    # If year is zero, figure out which one we're going
    # to generate for. We use this year, unless today is the first
    # of the year, in which case we do last year.
    l = dbo.locale
    if year == 0:
        today = now(dbo.timezone)
        if today.day == 1 and today.month == 1: today = subtract_years(today, 1)
        year = today.year
    al.debug("Generating animal figures annual for year=%d" % year, "animal.update_animal_figures_annual", dbo)

    # Work out the full year
    foy = datetime.datetime(year, 1, 1)
    loy = datetime.datetime(year, 12, 31)
    firstofyear = db.dd(foy)
    lastofyear = db.dd(loy)

    # Are we splitting between baby and adult animals?
    showbabies = configuration.annual_figures_show_babies(dbo)
    showbabiestype = configuration.annual_figures_show_babies_type(dbo)
    babymonths = configuration.annual_figures_baby_months(dbo)

    # Species =====================================
    allspecies = lookups.get_species(dbo)
    group = _("Intakes {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT a.DateBroughtIn AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.SpeciesID = %d AND a.DateBroughtIn >= %s AND a.DateBroughtIn <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DateBroughtIn, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear),
            sp["ID"], sp["SPECIESNAME"], "SP_BROUGHTIN", group, 1, showbabies, babymonths)

    group = _("Returns {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.ReturnDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.ReturnDate Is Not Null AND ad.ReturnDate >= %s AND ad.ReturnDate <= %s " \
            "AND a.NonShelterAnimal = 0 AND ad.MovementType = 1 " \
            "GROUP BY ad.ReturnDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear),
            sp["ID"], sp["SPECIESNAME"], "SP_RETURN", group, 2, showbabies, babymonths)

    group = _("Adoptions {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.ADOPTION),
            sp["ID"], sp["SPECIESNAME"], "SP_ADOPTED", group, 3, showbabies, babymonths)

    group = _("Euthanized {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT a.DeceasedDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.SpeciesID = %d AND a.DeceasedDate >= %s AND a.DeceasedDate <= %s " \
            "AND a.PutToSleep = 1 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DeceasedDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear),
            sp["ID"], sp["SPECIESNAME"], "SP_EUTHANIZED", group, 4, showbabies, babymonths)

    group = _("Died {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT a.DeceasedDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.SpeciesID = %d AND a.DeceasedDate >= %s AND a.DeceasedDate <= %s " \
            "AND a.DiedOffShelter = 0 AND a.PutToSleep = 0 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DeceasedDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear),
            sp["ID"], sp["SPECIESNAME"], "SP_DIED", group, 5, showbabies, babymonths)

    group = _("Returned to Owner {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.RECLAIMED),
            sp["ID"], sp["SPECIESNAME"], "SP_RECLAIMED", group, 6, showbabies, babymonths)

    group = _("Transferred Out {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.TRANSFER),
            sp["ID"], sp["SPECIESNAME"], "SP_TRANSFEROUT", group, 7, showbabies, babymonths)

    group = _("Escaped {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.ESCAPED),
            sp["ID"], sp["SPECIESNAME"], "SP_ESCAPED", group, 8, showbabies, babymonths)

    group = _("Stolen {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.STOLEN),
            sp["ID"], sp["SPECIESNAME"], "SP_STOLEN", group, 9, showbabies, babymonths)

    group = _("Released To Wild {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.RELEASED),
            sp["ID"], sp["SPECIESNAME"], "SP_STOLEN", group, 10, showbabies, babymonths)

    group = _("Transferred In {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT a.DateBroughtIn AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.SpeciesID = %d AND a.DateBroughtIn >= %s AND a.DateBroughtIn <= %s " \
            "AND a.IsTransfer = 1 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DateBroughtIn, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear),
            sp["ID"], sp["SPECIESNAME"], "SP_TRANSFERIN", group, 11, showbabies, babymonths)

    group = _("Adopted Transferred In {0}", l).format(year)
    for sp in allspecies:
        species_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.SpeciesID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 1 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(sp["ID"]), firstofyear, lastofyear, movement.ADOPTION),
            sp["ID"], sp["SPECIESNAME"], "SP_TRANSFERINADOPTED", group, 12, showbabies, babymonths)

    # Types =====================================
    alltypes = lookups.get_animal_types(dbo)
    for at in alltypes:
        # Find the last species this type referred to. If it was a dog or cat
        # species and we're splitting types for puppies/kittens, then mark the
        # type as appropriate for splitting.
        at["SPECIESID"] = db.query_int(dbo, "SELECT SpeciesID FROM animal WHERE AnimalTypeID = %d ORDER BY ID DESC LIMIT 1" % at["ID"])
        at["SHOWSPLIT"] = False
        if showbabiestype and (at["SPECIESID"] == 1 or at["SPECIESID"] == 2):
            at["SHOWSPLIT"] = True
    group = _("Intakes {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT a.DateBroughtIn AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.AnimalTypeID = %d AND a.DateBroughtIn >= %s AND a.DateBroughtIn <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DateBroughtIn, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear),
            at["ID"], at["ANIMALTYPE"], "AT_BROUGHTIN", group, 1, at["SHOWSPLIT"], babymonths)

    group = _("Returns {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.ReturnDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.ReturnDate Is Not Null AND ad.ReturnDate >= %s AND ad.ReturnDate <= %s " \
            "AND a.NonShelterAnimal = 0 AND ad.MovementType = 1 " \
            "GROUP BY ad.ReturnDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear),
            at["ID"], at["ANIMALTYPE"], "AT_RETURN", group, 2, at["SHOWSPLIT"], babymonths)

    group = _("Adoptions {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.ADOPTION),
            at["ID"], at["ANIMALTYPE"], "AT_ADOPTED", group, 3, at["SHOWSPLIT"], babymonths)

    group = _("Euthanized {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT a.DeceasedDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.AnimalTypeID = %d AND a.DeceasedDate >= %s AND a.DeceasedDate <= %s " \
            "AND a.PutToSleep = 1 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DeceasedDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear),
            at["ID"], at["ANIMALTYPE"], "AT_EUTHANIZED", group, 4, at["SHOWSPLIT"], babymonths)

    group = _("Died {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT a.DeceasedDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.AnimalTypeID = %d AND a.DeceasedDate >= %s AND a.DeceasedDate <= %s " \
            "AND a.PutToSleep = 0 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DeceasedDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear),
            at["ID"], at["ANIMALTYPE"], "AT_DIED", group, 5, at["SHOWSPLIT"], babymonths)

    group = _("Returned to Owner {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.RECLAIMED),
            at["ID"], at["ANIMALTYPE"], "AT_RECLAIMED", group, 6, at["SHOWSPLIT"], babymonths)

    group = _("Transferred Out {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.TRANSFER),
            at["ID"], at["ANIMALTYPE"], "AT_TRANSFEROUT", group, 7, at["SHOWSPLIT"], babymonths)

    group = _("Escaped {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.ESCAPED),
            at["ID"], at["ANIMALTYPE"], "AT_ESCAPED", group, 8, at["SHOWSPLIT"], babymonths)

    group = _("Stolen {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.STOLEN),
            at["ID"], at["ANIMALTYPE"], "AT_STOLEN", group, 9, at["SHOWSPLIT"], babymonths)

    group = _("Released To Wild {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 0 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.RELEASED),
            at["ID"], at["ANIMALTYPE"], "AT_STOLEN", group, 10, at["SHOWSPLIT"], babymonths)

    group = _("Transferred In {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT a.DateBroughtIn AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(a.ID) AS Total FROM animal a WHERE " \
            "a.AnimalTypeID = %d AND a.DateBroughtIn >= %s AND a.DateBroughtIn <= %s " \
            "AND a.IsTransfer = 1 AND a.NonShelterAnimal = 0 " \
            "GROUP BY a.DateBroughtIn, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear),
            at["ID"], at["ANIMALTYPE"], "AT_TRANSFERIN", group, 11, at["SHOWSPLIT"], babymonths)

    group = _("Adopted Transferred In {0}", l).format(year)
    for at in alltypes:
        type_line("SELECT ad.MovementDate AS TheDate, a.DateOfBirth AS DOB, " \
            "COUNT(ad.ID) AS Total FROM animal a INNER JOIN adoption ad ON ad.AnimalID = a.ID WHERE " \
            "a.AnimalTypeID = %d AND ad.MovementDate >= %s AND ad.MovementDate <= %s " \
            "AND a.IsTransfer = 1 AND a.NonShelterAnimal = 0 AND ad.MovementType = %d " \
            "GROUP BY ad.MovementDate, a.DateOfBirth" % (int(at["ID"]), firstofyear, lastofyear, movement.ADOPTION),
            at["ID"], at["ANIMALTYPE"], "AT_TRANSFERINADOPTED", group, 12, at["SHOWSPLIT"], babymonths)

    # Write out all our changes in one go
    update_db(year)

def update_animal_figures_asilomar(dbo, year = 0):
    """
    Updates the animal figures asilomar table for the year given.
    If year isn't given, defaults to this year, unless today is the
    first of the year in which case we do last year.
    """
    batch = []
    asrows = {}
    nid = db._get_id_max(dbo, "animalfiguresasilomar")

    def getcategory(catidx):
        if catidx == 0: return "Healthy"
        if catidx == 1: return "Treatable - Rehabilitatable"
        if catidx == 2: return "Treatable - Manageable"
        return "Unhealthy and Untreatable"

    def add_row(code, heading, bold, cat, dog):
        """ Adds a row to the animalfiguresasilomar table """
        total = -1
        if cat != -1 and dog != -1:
            total = cat + dog
        batch.append((
            nid + len(batch),
            year,
            nid + len(batch),
            code,
            heading,
            bold,
            cat,
            dog, 
            total
        ))

    def add_section(sql, headingtext, footertext, footercode):
        """ 
            Executes a query and calls add_row appropriately. The query
            should have 3 columns, CATEGORY, SPECIESID, TOTAL.
            (0 = healthy, 1 = rehabilitatable, 2 = manageable, 3 = unhealthy),
            the second and third are the totals for dog, then cat for
            the query.
            A heading of headingtext is sent first and a subtotal is
            calculated and sent afterwards with a bold line.
        """
        rows = db.query(dbo, sql)
        add_row("", headingtext, 0, -1, -1)
        section = [
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 }
        ]
        catsub = 0
        dogsub = 0
        for r in rows:
            if r["ASILOMARINTAKECATEGORY"] is None: r["ASILOMARINTAKECATEGORY"] = 0
            if r["SPECIESID"] == 1:
                section[r["ASILOMARINTAKECATEGORY"]]["dog"] = r["TOTAL"]
            elif r["SPECIESID"] == 2:
                section[r["ASILOMARINTAKECATEGORY"]]["cat"] = r["TOTAL"]
        for i, s in enumerate(section):
            add_row("", getcategory(i), 0, s["cat"], s["dog"])
            catsub += s["cat"]
            dogsub += s["dog"]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def add_subtotal(sql, footertext, footercode):
        """ 
            Executes a subtotal query and calls add_row appropriately. The query
            should have 2 columns, SPECIESID and TOTAL.
            The subtotal is calculated and added with a bold line.
        """
        rows = db.query(dbo, sql)
        catsub = 0
        dogsub = 0
        for r in rows:
            if r["SPECIESID"] == 1:
                dogsub = r["TOTAL"]
            elif r["SPECIESID"] == 2:
                catsub = r["TOTAL"]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def add_total(selrows, footertext, footercode):
        """
        Adds up any letters in selrows as a string and adds a new row
        """
        catsub = 0
        dogsub = 0
        for l in selrows:
            if asrows.has_key(l):
                cur = asrows[l]
                catsub += cur[0]
                dogsub += cur[1]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def update_db(year):
        """ Writes all of our figures to the database """
        db.execute(dbo, "DELETE FROM animalfiguresasilomar WHERE Year = %d" % year)
        sql = "INSERT INTO animalfiguresasilomar (ID, Year, OrderIndex, Code, Heading, " \
            "Bold, Cat, Dog, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db.execute_many(dbo, sql, batch)
        al.debug("wrote %d asilomar figures records" % len(batch), "animal.update_animal_figures_asilomar", dbo)

    # Is this not a US locale, or is the option turned off? Bail out.
    if dbo.locale != "en" or configuration.disable_asilomar(dbo):
        al.debug("Not a US locale, or asilomar is disabled", "animal.update_animal_figures_asilomar", dbo)
        return

    # If year is zero, figure out which one we're going
    # to generate for. We use this year, unless today is the first
    # of the year, in which case we do last year.
    if year == 0:
        today = now(dbo.timezone)
        if today.day == 1 and today.month == 1: today = subtract_years(today, 1)
        year = today.year
    al.debug("Generating asilomar figures annual for year=%d" % year, "animal.update_animal_figures_asilomar", dbo)

    # Work out the full year
    foy = datetime.datetime(year, 1, 1)
    loy = datetime.datetime(year, 12, 31)
    firstofyear = db.dd(foy)
    lastofyear = db.dd(loy)

    # A Beginning of year shelter count
    dogsub = get_number_animals_on_shelter(dbo, foy, 1)
    catsub = get_number_animals_on_shelter(dbo, foy, 2)
    add_row("A", "BEGINNING SHELTER COUNT", 1, catsub, dogsub)

    # B Intake from the public
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 0 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "INTAKE (Live Dogs and Cats Only)", "Subtotal Intake from the Public", "B")

    # C Incoming transfers from community
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 0 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "Incoming Transfers from within Target Community", "Subtotal Intake from Incoming Transfers from Orgs within Community/Coalition", "C")

    # D Incoming transfers from outside community
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 1 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "Incoming Transfers from outside Target Community", "Subtotal Intake from Incoming Transfers from Orgs outside Community/Coalition", "D")

    # E Owners requesting euthanasia
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 1 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "From Owners/Guardians Requesting Euthanasia", "Subtotal Intake from Owners/Guardians Requesting Euthanasia", "E")

    # F Total Intake
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Total Intake [B + C + D + E]", "F")

    # G Unhealthy owner requesting euthanasia
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND AsilomarIntakeCategory = 3 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Owner/Guardian Requested Euthanasia (Unhealthy and Untreatable Only)", "G")

    # H Adjusted intake
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND AsilomarIntakeCategory <> 3 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Adjusted Total Intake [F minus G]", "H")

    # I Total Adoptions
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 1 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "Adoptions (Only Dogs and Cats Adopted by the Public)", "Total Adoptions", "I")

    # J Total Outgoing Transfers (to orgs within community)
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 3 AND a.AsilomarIsTransferExternal = 0 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "Outgoing Transfers to target community", "Total Outgoing Transfers (to Orgs within Community/Coalition)", "J")

    # K Total Outgoing Transfers (to orgs outside community)
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 3 AND a.AsilomarIsTransferExternal = 1 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofyear, lastofyear)
    add_section(sql, "Outgoing Transfers outside target community", "Total Outgoing Transfers (to Orgs outside Community/Coalition)", "K")

    # L Return to Owner/Guardian
    sql = "SELECT a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 5 " \
        "GROUP BY a.SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Return to Owner/Guardian", "L")

    add_row("", "Dogs and Cats Euthanized", 0, -1, -1)

    # M Healthy
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 0 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Healthy (Includes Owner/Guardian Requested Euthanasia)", "M")

    # N Rehabilitatable
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 1 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Treatable - Rehabilitatable (Includes Owner/Guardian Requested Euthanasia)", "N")

    # O Manageable
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 2 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Treatable - Manageable (Includes Owner/Guardian Requested Euthanasia)", "O")

    # P Unhealthy
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 3 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Unhealthy and Untreatable (Includes Owner/Guardian Requested Euthanasia)", "P")

    # Q Total Euthanasia 
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Total Euthanasia [M + N + O + P]", "Q")

    # R Unhealthy owner requesting euthanasia
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "AND AsilomarIntakeCategory = 3 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Owner/Guardian Requested Euthanasia (Unhealthy and Untreatable Only)", "R")

    # S Adjusted Total Euthanasia 
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "AND AsilomarIntakeCategory <> 3 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Adjusted Total Euthanasia [Q minus R]", "S")

    # T Subtotal Outcomes
    add_total("IJKLS", "Subtotal Outcomes [I + J + K + L + S]", "T")
   
    # U Died Or Lost in Shelter/Care
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 0 " \
        "GROUP BY SpeciesID" % (firstofyear, lastofyear)
    add_subtotal(sql, "Died Or Lost in Shelter/Care", "U")

    # V Total Outcomes
    add_total("TU", "Total Outcomes [T + U]", "V")

    # W End of year shelter count
    dogsub = get_number_animals_on_shelter(dbo, loy, 1)
    catsub = get_number_animals_on_shelter(dbo, loy, 2)
    add_row("W", "ENDING SHELTER COUNT", 1, catsub, dogsub)

    # Write out all our changes in one go
    update_db(year)

def update_animal_figures_monthly_asilomar(dbo, month = 0, year = 0):
    """
    Updates the animal figures asilomar table for the year given.
    If year isn't given, defaults to this year, unless today is the
    first of the year in which case we do last year.
    """
    batch = []
    asrows = {}
    nid = db._get_id_max(dbo, "animalfiguresmonthlyasilomar")

    def getcategory(catidx):
        if catidx == 0: return "Healthy"
        if catidx == 1: return "Treatable - Rehabilitatable"
        if catidx == 2: return "Treatable - Manageable"
        return "Unhealthy and Untreatable"

    def add_row(code, heading, bold, cat, dog):
        """ Adds a row to the animalfiguresmonthlyasilomar table """
        total = -1
        if cat != -1 and dog != -1:
            total = cat + dog
        batch.append((
            nid + len(batch),
            month,
            year,
            nid + len(batch),
            code,
            heading,
            bold,
            cat,
            dog, 
            total
        ))

    def add_section(sql, headingtext, footertext, footercode):
        """ 
            Executes a query and calls add_row appropriately. The query
            should have 3 columns, CATEGORY, SPECIESID, TOTAL.
            (0 = healthy, 1 = rehabilitatable, 2 = manageable, 3 = unhealthy),
            the second and third are the totals for dog, then cat for
            the query.
            A heading of headingtext is sent first and a subtotal is
            calculated and sent afterwards with a bold line.
        """
        rows = db.query(dbo, sql)
        add_row("", headingtext, 0, -1, -1)
        section = [
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 },
            { "cat" : 0, "dog": 0 }
        ]
        catsub = 0
        dogsub = 0
        for r in rows:
            if r["ASILOMARINTAKECATEGORY"] is None: r["ASILOMARINTAKECATEGORY"] = 0
            if r["SPECIESID"] == 1:
                section[r["ASILOMARINTAKECATEGORY"]]["dog"] = r["TOTAL"]
            elif r["SPECIESID"] == 2:
                section[r["ASILOMARINTAKECATEGORY"]]["cat"] = r["TOTAL"]
        for i, s in enumerate(section):
            add_row("", getcategory(i), 0, s["cat"], s["dog"])
            catsub += s["cat"]
            dogsub += s["dog"]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def add_subtotal(sql, footertext, footercode):
        """ 
            Executes a subtotal query and calls add_row appropriately. The query
            should have 2 columns, SPECIESID and TOTAL.
            The subtotal is calculated and added with a bold line.
        """
        rows = db.query(dbo, sql)
        catsub = 0
        dogsub = 0
        for r in rows:
            if r["SPECIESID"] == 1:
                dogsub = r["TOTAL"]
            elif r["SPECIESID"] == 2:
                catsub = r["TOTAL"]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def add_total(selrows, footertext, footercode):
        """
        Adds up any letters in selrows as a string and adds a new row
        """
        catsub = 0
        dogsub = 0
        for l in selrows:
            if asrows.has_key(l):
                cur = asrows[l]
                catsub += cur[0]
                dogsub += cur[1]
        add_row(footercode, footertext, 1, catsub, dogsub)
        asrows[footercode] = (catsub, dogsub)

    def update_db(month, year):
        """ Writes all of our figures to the database """
        db.execute(dbo, "DELETE FROM animalfiguresmonthlyasilomar WHERE Month = %d AND Year = %d" % (month, year))
        sql = "INSERT INTO animalfiguresmonthlyasilomar (ID, Month, Year, OrderIndex, Code, Heading, " \
            "Bold, Cat, Dog, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db.execute_many(dbo, sql, batch)
        al.debug("wrote %d asilomar figures records" % len(batch), "animal.update_animal_figures_monthly_asilomar", dbo)

    # Is this not a US locale, or is the option turned off? Bail out.
    if dbo.locale != "en" or configuration.disable_asilomar(dbo):
        al.debug("Not a US locale, or asilomar is disabled", "animal.update_animal_figures_monthly_asilomar", dbo)
        return

    # If month and year are zero, figure out which one we're going
    # to generate for. We use this month, unless today is the first
    # of the month, in which case we do last month
    if month == 0 and year == 0:
        today = now()
        if today.day == 1: today = subtract_months(today, 1)
        month = today.month
        year = today.year
    al.debug("Generating asilomar monthly figures for month=%d, year=%d" % (month, year), "animal.update_animal_figures_monthly_asilomar", dbo)

    fom = datetime.datetime(year, month, 1)
    lom = last_of_month(fom)
    firstofmonth = db.dd(fom)
    lastofmonth = db.dd(lom)

    # A Beginning of year shelter count
    dogsub = get_number_animals_on_shelter(dbo, fom, 1)
    catsub = get_number_animals_on_shelter(dbo, fom, 2)
    add_row("A", "BEGINNING SHELTER COUNT", 1, catsub, dogsub)

    # B Intake from the public
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 0 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "INTAKE (Live Dogs and Cats Only)", "Subtotal Intake from the Public", "B")

    # C Incoming transfers from community
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 0 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "Incoming Transfers from within Target Community", "Subtotal Intake from Incoming Transfers from Orgs within Community/Coalition", "C")

    # D Incoming transfers from outside community
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 1 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "Incoming Transfers from outside Target Community", "Subtotal Intake from Incoming Transfers from Orgs outside Community/Coalition", "D")

    # E Owners requesting euthanasia
    sql = "SELECT AsilomarIntakeCategory, SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND IsTransfer = 1 AND AsilomarIsTransferExternal = 1 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY AsilomarIntakeCategory, SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "From Owners/Guardians Requesting Euthanasia", "Subtotal Intake from Owners/Guardians Requesting Euthanasia", "E")

    # F Total Intake
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Total Intake [B + C + D + E]", "F")

    # G Unhealthy owner requesting euthanasia
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND AsilomarIntakeCategory = 3 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Owner/Guardian Requested Euthanasia (Unhealthy and Untreatable Only)", "G")

    # H Adjusted intake
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND AsilomarIntakeCategory <> 3 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Adjusted Total Intake [F minus G]", "H")

    # I Total Adoptions
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 1 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "Adoptions (Only Dogs and Cats Adopted by the Public)", "Total Adoptions", "I")

    # J Total Outgoing Transfers (to orgs within community)
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 3 AND a.AsilomarIsTransferExternal = 0 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "Outgoing Transfers to target community", "Total Outgoing Transfers (to Orgs within Community/Coalition)", "J")

    # K Total Outgoing Transfers (to orgs outside community)
    sql = "SELECT a.AsilomarIntakeCategory, a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 3 AND a.AsilomarIsTransferExternal = 1 " \
        "GROUP BY a.AsilomarIntakeCategory, a.SpeciesID" % (firstofmonth, lastofmonth)
    add_section(sql, "Outgoing Transfers outside target community", "Total Outgoing Transfers (to Orgs outside Community/Coalition)", "K")

    # L Return to Owner/Guardian
    sql = "SELECT a.SpeciesID, COUNT(a.ID) AS Total FROM animal a " \
        "INNER JOIN adoption m ON m.AnimalID = a.ID " \
        "WHERE m.MovementDate >= %s AND m.MovementDate <= %s AND m.MovementType = 5 " \
        "GROUP BY a.SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Return to Owner/Guardian", "L")

    add_row("", "Dogs and Cats Euthanized", 0, -1, -1)

    # M Healthy
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 0 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Healthy (Includes Owner/Guardian Requested Euthanasia)", "M")

    # N Rehabilitatable
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 1 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Treatable - Rehabilitatable (Includes Owner/Guardian Requested Euthanasia)", "N")

    # O Manageable
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 2 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Treatable - Manageable (Includes Owner/Guardian Requested Euthanasia)", "O")

    # P Unhealthy
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 AND AsilomarIntakeCategory = 3 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Unhealthy and Untreatable (Includes Owner/Guardian Requested Euthanasia)", "P")

    # Q Total Euthanasia 
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Total Euthanasia [M + N + O + P]", "Q")

    # R Unhealthy owner requesting euthanasia
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "AND AsilomarIntakeCategory = 3 AND AsilomarOwnerRequestedEuthanasia = 1 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Owner/Guardian Requested Euthanasia (Unhealthy and Untreatable Only)", "R")

    # S Adjusted Total Euthanasia 
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 1 " \
        "AND AsilomarIntakeCategory <> 3 AND AsilomarOwnerRequestedEuthanasia = 0 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Adjusted Total Euthanasia [Q minus R]", "S")

    # T Subtotal Outcomes
    add_total("IJKLS", "Subtotal Outcomes [I + J + K + L + S]", "T")
   
    # U Died Or Lost in Shelter/Care
    sql = "SELECT SpeciesID, COUNT(ID) AS Total FROM animal " \
        "WHERE DateBroughtIn >= %s AND DateBroughtIn <= %s AND DeceasedDate Is Not Null AND PutToSleep = 0 " \
        "GROUP BY SpeciesID" % (firstofmonth, lastofmonth)
    add_subtotal(sql, "Died Or Lost in Shelter/Care", "U")

    # V Total Outcomes
    add_total("TU", "Total Outcomes [T + U]", "V")

    # W End of year shelter count
    dogsub = get_number_animals_on_shelter(dbo, lom, 1)
    catsub = get_number_animals_on_shelter(dbo, lom, 2)
    add_row("W", "ENDING SHELTER COUNT", 1, catsub, dogsub)

    # Write out all our changes in one go
    update_db(month, year)

def auto_cancel_holds(dbo):
    """
    Automatically cancels holds after the hold until date value set
    """
    sql = "UPDATE animal SET IsHold = 0 WHERE IsHold = 1 AND " \
        "HoldUntilDate Is Not Null AND " \
        "HoldUntilDate < %s" % db.dd(now(dbo.timezone))
    count = db.execute(dbo, sql)
    al.debug("cancelled %d holds" % (count), "animal.auto_cancel_holds", dbo)

def maintenance_reassign_all_codes(dbo):
    """
    Goes through all animals in the system and regenerates their 
    shelter codes.
    """
    db.execute(dbo, "UPDATE animal SET YearCodeID = 0, UniqueCodeID = 0, " \
        "ShelterCode = ID, ShortCode = ID")
    animals = db.query(dbo, "SELECT ID, AnimalTypeID, DateBroughtIn, AnimalName " \
        "FROM animal ORDER BY ID")
    for a in animals:
        sheltercode, shortcode, unique, year = calc_shelter_code(dbo, a["ANIMALTYPEID"], a["ENTRYREASONID"], a["SPECIESID"], a["DATEBROUGHTIN"])
        sql = "UPDATE animal SET ShelterCode = '%s', ShortCode = '%s', " \
            "UniqueCodeID = %d, YearCodeID = %d WHERE ID = %d" % ( \
            sheltercode, shortcode, unique, year, a["ID"])
        al.debug("RECODE: %s -> %s" % (a["ANIMALNAME"], sheltercode), "animal.maintenance_reassign_all_codes", dbo)
        db.execute(dbo, sql)

def maintenance_reassign_shelter_codes(dbo):
    """
    Goes through all animals on the shelter and regenerates their 
    shelter codes.
    """
    db.execute(dbo, "UPDATE animal SET YearCodeID = 0, UniqueCodeID = 0, " \
        "ShelterCode = ID, ShortCode = ID WHERE Archived = 0 ORDER BY ID")
    animals = db.query(dbo, "SELECT ID, AnimalTypeID, DateBroughtIn, AnimalName " \
        "FROM animal WHERE Archived = 0")
    for a in animals:
        sheltercode, shortcode, unique, year = calc_shelter_code(dbo, a["ANIMALTYPEID"], a["ENTRYREASONID"], a["SPECIESID"], a["DATEBROUGHTIN"])
        sql = "UPDATE animal SET ShelterCode = '%s', ShortCode = '%s', " \
            "UniqueCodeID = %d, YearCodeID = %d WHERE ID = %d" % ( \
            sheltercode, shortcode, unique, year, a["ID"])
        al.debug("RECODE: %s -> %s" % (a["ANIMALNAME"], sheltercode), "animal.maintenance_reassign_shelter_codes", dbo)
        db.execute(dbo, sql)

def maintenance_animal_figures(dbo, includeMonths = True, includeAnnual = True):
    """
    Finds all months/years the system has animal data for and generates 
    figures reporting data for them.
    """
    if dbo.dbtype == "POSTGRESQL":
        monthsyears = db.query(dbo, "SELECT DISTINCT CAST(EXTRACT(YEAR FROM DATEBROUGHTIN) AS INTEGER) AS TheYear, CAST(EXTRACT(MONTH FROM DATEBROUGHTIN) AS INTEGER) AS TheMonth FROM animal")
        years = db.query(dbo, "SELECT DISTINCT CAST(EXTRACT(YEAR FROM DATEBROUGHTIN) AS INTEGER) AS TheYear FROM animal")
    else:
        monthsyears = db.query(dbo, "SELECT DISTINCT MONTH(DateBroughtIn) AS TheMonth, YEAR(DateBroughtIn) AS TheYear FROM animal")
        years = db.query(dbo, "SELECT DISTINCT YEAR(DateBroughtIn) FROM animal")
    if includeMonths:
        for my in monthsyears:
            al.debug("update_animal_figures: month=%d, year=%d" % (my["THEMONTH"], my["THEYEAR"]), "animal.maintenance_animal_figures", dbo)
            update_animal_figures(dbo, int(my["THEMONTH"]), int(my["THEYEAR"]))
            al.debug("update_animal_figures_monthly_asilomar: month=%d, year=%d" % (my["THEMONTH"], my["THEYEAR"]), "animal.maintenance_animal_fitures", dbo)
            update_animal_figures_monthly_asilomar(dbo, int(my["THEMONTH"]), int(my["THEYEAR"]))
    if includeAnnual:
        for y in years:
            al.debug("update_animal_figures_annual: year=%d" % y["THEYEAR"], "animal.maintenance_animal_figures", dbo)
            update_animal_figures_annual(dbo, int(y["THEYEAR"]))
            al.debug("update_animal_figures_asilomar: year=%d" % y["THEYEAR"], "animal.maintenance_animal_figures", dbo)
            update_animal_figures_asilomar(dbo, int(y["THEYEAR"]))

