from dexml import Model
from dexml.fields import Boolean, String, List, Integer

DIRECTORY_NS = 'http://schemas.sirsidynix.com/directory/messages/v4'

########################################
# BriefLibrary models
########################################

class BriefLibrary(Model):
    class meta():
        tagname = 'library'
        namespace = DIRECTORY_NS

    id = Integer(tagname='id')
    version = Integer(tagname='version')
    deleted = Boolean(tagname='deleted')
    searchable = Boolean(tagname='searchable')
    name = String(tagname='name', required=False)
    latitude = String(tagname='latitude')
    longitude = String(tagname='longitude')
    libraryUrl = String(tagname='libraryUrl', required=False)
    policyName = String(tagname='policyName', required=False)
    symphonyWsURL = String(tagname='symphonyWsURL')
    logoUrl = String(tagname='logoUrl', required=False)
    profileName = String(tagname='profileName')

class GetBriefLibrariesResponse(Model):
    class meta():
        namespace = DIRECTORY_NS

    libraries = List(BriefLibrary)  # XXX: Prevent __repr__ spam.

########################################
# Library models
########################################

class EnrichedContent(Model):
    class meta():
        tagname = 'enrichedContent'
        namespace = DIRECTORY_NS

    type = String(tagname='type')
    value = String(tagname='value')
    erichedContentId = Integer(tagname='erichedContentId')

class GetLibraryResponse(BriefLibrary):
    class meta():
        namespace = DIRECTORY_NS

    discoveryWsURL = String(tagname='discoveryWsURL')
    address1 = String(tagname='address1')
    address2 = String(tagname='address2')
    address3 = String(tagname='address3')
    city = String(tagname='city')
    countryCode = String(tagname='countryCode')
    enrichedContents = List(EnrichedContent)
    groupPolicy = String(tagname='groupPolicy')
    openHours = String(tagname='openHours')
    email = String(tagname='email')
    pickupLocationIds = String(tagname='pickupLocationIds')
    postalCode = String(tagname='postalCode')
    searchFilterName = String(tagname='searchFilterName')
    stateOrProvince = String(tagname='stateOrProvince')
    authenticationLabelCount = Integer(tagname='authenticationLabelCount')
    authenticationLabel1 = String(tagname='authenticationLabel1')
    authenticationLabel2 = String(tagname='authenticationLabel2')
    authenticationLabel3 = String(tagname='authenticationLabel3')
    displayHoldsQueue = Boolean(tagname='displayHoldsQueue')
    changePinAllowed = Boolean(tagname='changePinAllowed')
    holdRange = String(tagname='holdRange')
    holdsEnabled = Boolean(tagname='holdsEnabled')
    suggestedReadingEnabled = Boolean(tagname='suggestedReadingEnabled')
    myListEnabled = Boolean(tagname='myListEnabled')
    adminSiteName = String(tagname='adminSiteName')
    facebookEnabled = Boolean(tagname='facebookEnabled')
