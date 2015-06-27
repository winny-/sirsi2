from dexml import Model
from dexml.fields import Boolean, String, List, Integer
from dexml.fields import Model as ModelField

SYMPHONYWS_NS_TEMPLATE = 'http://schemas.sirsidynix.com/symws/{}'

SYMPHONYWS_STANDARD_NS = SYMPHONYWS_NS_TEMPLATE.format('standard')
SYMPHONYWS_ADMIN_NS = SYMPHONYWS_NS_TEMPLATE.format('admin')
SYMPHONYWS_SECURITY_NS = SYMPHONYWS_NS_TEMPLATE.format('security')
SYMPHONYWS_PATRON_NS = SYMPHONYWS_NS_TEMPLATE.format('patron')

########################################
# Version models
########################################

class Version(Model):
    class meta():
        tagname = 'version'
        namespace = SYMPHONYWS_STANDARD_NS

    product = String(tagname='product')
    version = String(tagname='version')

class VersionResponse(Model):
    class meta():
        namespace = SYMPHONYWS_STANDARD_NS

    versions = List(Version)

########################################
# ILS Configuration models
########################################

class ConfigInfo(Model):
    class meta():
        namespace = SYMPHONYWS_ADMIN_NS
        tagname = 'configInfo'

    name = String(tagname='name')
    value = String(tagname='value')

class LookupILSConfigurationResponse(Model):
    class meta():
        namespace = SYMPHONYWS_ADMIN_NS

    config_infos = List(ConfigInfo)

########################################

class LoginUserResponse(Model):
    class meta():
        namespace = SYMPHONYWS_SECURITY_NS

    userID = String(tagname='userID')
    sessionToken = String(tagname='sessionToken')

########################################
# Lookup My Account Info
########################################

class PatronInfo(Model):
    class meta():
        tagname = 'patronInfo'
        namespace = SYMPHONYWS_PATRON_NS

    userKey = String(tagname='userKey')
    userID = String(tagname='userID')
    alternativeID = String(tagname='alternativeID')
    webAuthID = String(tagname='webAuthID')
    groupID = String(tagname='groupID')
    birthDate = String(tagname='birthDate')
    patronLibraryID = String(tagname='patronLibraryID')
    department = String(tagname='department')
    preferredLanguage = String(tagname='preferredLanguage')

class PatronCirculationInfo(Model):
    class meta():
        tagname = 'patronCirculationInfo'
        namespace = SYMPHONYWS_PATRON_NS

    numberOfCheckouts = Integer(tagname='numberOfCheckouts')
    numberOfClaimsReturned = Integer(tagname='numberOfClaimsReturned')
    numberOfBookings = Integer(tagname='numberOfBookings')
    numberOfRequests = Integer(tagname='numberOfRequests')
    numberOfUnansweredRequests = Integer(tagname='numberOfUnansweredRequests')
    numberOfHolds = Integer(tagname='numberOfHolds')
    numberOfAvailableHolds = Integer(tagname='numberOfAvailableHolds')
    numberOfFees = Integer(tagname='numberOfFees')
    estimatedFines = String(tagname='estimatedFines')
    estimatedOverdues = Integer(tagname='estimatedOverdues')
    numberOfCheckoutsAllowedUnlimited = Boolean(tagname='numberOfCheckoutsAllowedUnlimited')

class PatronCheckoutInfo(Model):
    class meta():
        tagname = 'patronCheckoutInfo'
        namespace = SYMPHONYWS_PATRON_NS
        order_sensitive = False

    titleKey = String(tagname='titleKey')
    itemID = String(tagname='itemID')
    callNumber = String(tagname='callNumber')
    copyNumber = String(tagname='copyNumber')
    pieces = Integer(tagname='pieces')
    title = String(tagname='title')
    author = String(tagname='author')
    checkoutLibraryID = String(tagname='checkoutLibraryID')
    checkoutLibraryDescription = String(tagname='checkoutLibraryDescription')
    itemLibraryID = String(tagname='itemLibraryID')
    itemLibraryDescription = String(tagname='itemLibraryDescription')
    itemTypeID = String(tagname='itemTypeID')
    itemTypeDescription = String(tagname='itemTypeDescription')
    checkoutDate = String(tagname='checkoutDate')
    dueDate = String(tagname='dueDate')
    recallNoticesSent = Integer(tagname='recallNoticesSent')
    lastRenewedDate = String(tagname='lastRenewedDate', required=False)
    renewals = Integer(tagname='renewals')
    renewalsRemaining = Integer(tagname='renewalsRemaining')
    unseenRenewals = Integer(tagname='unseenRenewals')
    overdue = Boolean(tagname='overdue')
    overdueNoticesSent = Integer(tagname='overdueNoticesSent')

class FeeItemInfo(Model):
    class meta():
        tagname = 'feeItemInfo'
        namespace = SYMPHONYWS_PATRON_NS


class FeeInfo(Model):
    class meta():
        tagname = 'feeInfo'
        namespace = SYMPHONYWS_PATRON_NS

    feeInfo = ModelField(FeeItemInfo)

class LookupMyAccountInfoResponse(Model):
    class meta():
        namespace = SYMPHONYWS_PATRON_NS

    patronInfo = ModelField(PatronInfo)
    patronCirculationInfo = ModelField(PatronCirculationInfo)
    patronCheckoutInfos = List(PatronCheckoutInfo)
    feeInfo = ModelField(FeeInfo)

########################################

class RenewMyCheckoutResponse(Model):
    class meta():
        namespace = SYMPHONYWS_PATRON_NS

    message = String(tagname='message')
    userID = String(tagname='userID')
    userName = String(tagname='userName')
    itemID = String(tagname='itemID')
    callNumber = String(tagname='callNumber')
    title = String(tagname='title')
    dueDate = String(tagname='dueDate')
