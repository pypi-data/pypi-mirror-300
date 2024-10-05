from django.db import models
from django.utils.translation import gettext_lazy as _

TRUE_FALSE_CHOICES = [
    ("", "---"),
    (True, "True"),
    (False, "False"),
]


# Generic
class FlatOrPercentChoices(models.TextChoices):
    """
    Flat or percent enumeration
    """

    DEFAULT = "", _("---")
    FLAT = "FLAT", _("Flat")
    PERCENT = "PERCENT", _("Percent")


class TimeFrequencyChoices(models.TextChoices):
    """
    Time frequency enumeration
    """

    DEFAULT = "", _("---")
    HOURLY = "HOURLY", _("Hourly")
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    QUARTERLY = "QUARTERLY", _("Quarterly")
    ANNUALLY = "ANNUALLY", _("Annually")


# Person
class PersonBloodChoices(models.TextChoices):
    """
    Person blood enumeration
    """

    DEFAULT = "", _("---")
    A = "A", _("A")
    B = "B", _("B")
    AB = "AB", _("AB")
    O = "O", _("O")
    OTHERS = "OTHERS", _("Others")


class PersonEducationLevelChoices(models.TextChoices):
    """
    Person education level enumeration

    Reference
    ---------
    - https://study.com/different_degrees.html
    """

    DEFAULT = "", _("---")
    HIGH_SCHOOL = "HIGH_SCHOOL", _("High School")
    ASSOCIATE = "ASSOCIATE", _("Associate Degree")
    BACHELOR = "BACHELOR", _("Bachelor's Degree")
    MASTER = "MASTER", _("Master's Degree")
    DOCTORAL = "DOCTORAL", _("Doctoral Degree")
    OTHERS = "OTHERS", _("Others")


class PersonEyeColorChoices(models.TextChoices):
    """
    Person eye color enumeration

    Reference
    ---------
    - https://en.wikipedia.org/wiki/Eye_color#Eye_color_chart_(Martin_scale)
    """

    DEFAULT = "", _("---")
    AMBER = "AMBER", _("Amber")
    BLUE = "BLUE", _("Blue")
    BROWN = "BROWN", _("Brown")
    GREEN = "GREEN", _("Green")
    GREY = "GREY", _("Grey")
    HAZEL = "HAZEL", _("Hazel")
    RED = "RED", _("Red")
    OTHERS = "OTHERS", _("Others")


class PersonGenderChoices(models.TextChoices):
    """
    Person gender enumeration
    """

    DEFAULT = "", _("---")
    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    OTHERS = "OTHERS", _("Others")


class PersonRaceChoices(models.TextChoices):
    """
    Person race enumeration

    Reference
    ---------
    - https://grants.nih.gov/grants/guide/notice-files/not-od-15-089.html
    """

    DEFAULT = "", _("---")
    ASIAN = "ASIAN", _("Asian")
    BLACK = "BLACK", _("Black Or African American")
    HISPANIC = "HISPANIC", _("Hispanic Or Latino")
    INDIAN = "INDIAN", _("American Indian Or Alaska Native")
    ISLANDER = "ISLANDER", _("Native Hawaiian Or Other Pacific Islander")
    WHITE = "WHITE", _("White")
    OTHERS = "OTHERS", _("Others")


# Payment / Transaction
class PaymentMethodTypeChoices(models.TextChoices):
    """
    Payment method type enumeration
    """

    DEFAULT = "", _("---")
    CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
    DEBIT_CARD = "DEBIT_CARD", _("Debit Card")
    ELECTRONIC_BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")
    PAYPAL = "PAYPAL", _("Paypal")
    APPLE_PAY = "APPLE_PAY", _("Apple Pay")
    GOOGLE_PAY = "GOOGLE_PAY", _("Google Pay")


class TransactionGatewayChoices(models.TextChoices):
    """
    Transaction gateway enumeration
    """

    DEFAULT = "", _("---")
    ADYEN = "ADYEN", _("Adyen")
    ALIPAY = "ALIPAY", _("Alipay")
    AMAZON = "AMAZON", _("Amazon")
    AUTHORIZE = "AUTHORIZE", _("Authorize")
    BRAINTREE = "BRAINTREE", _("Braintree")
    CYBERSOURCE = "CYBERSOURCE", _("Cybersource")
    INGENICO = "INGENICO", _("Ingenico")
    PAYPAL = "PAYPAL", _("Paypal")
    SQUARE = "SQUARE", _("Square")
    STRIPE = "STRIPE", _("Stripe")
    WEPAY = "WEPAY", _("Wepay")
    WORLDPAY = "WORLDPAY", _("Worldpay")


class TransactionStateChoices(models.TextChoices):
    """
    Transaction state enumeration

    Reference
    ---------
    - https://stripe.com/docs/payments/intents#intent-statuses
    """

    DEFAULT = "", _("---")
    REQUIRES_PAYMENT_METHOD = "REQUIRES_PAYMENT_METHOD", _("Requires Payment Method")
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION", _("Requires Confirmation")
    REQUIRES_ACTION = "REQUIRES_ACTION", _("Requires Action")
    PROCESSING = "PROCESSING", _("Processing")
    CANCEL = "CANCEL", _("Cancel")
    SUCCESS = "SUCCESS", _("Success")


class TransactionTypeChoices(models.TextChoices):
    """
    Transaction type enumeration
    """

    DEFAULT = "", _("---")
    PAYMENT = "PAYMENT", _("Payment")
    REFUND = "REFUND", _("Refund")
    ADJUSTMENT = "ADJUSTMENT", _("Adjustment")
    COUPON = "COUPON", _("Coupon")
    PRORATION = "PRORATION", _("Proration")


class TransactionEventTypeChoices(models.TextChoices):
    """
    Transaction event type enumeration
    """

    DEFAULT = "", _("---")
    CREATED = "CREATED", _("Created")
    AUTHORIZED = "AUTHORIZED", _("Authorized")
    CAPTURED = "CAPTURED", _("Captured")
    REFUNDED = "REFUNDED", _("Refunded")
    FAILED = "FAILED", _("Failed")
