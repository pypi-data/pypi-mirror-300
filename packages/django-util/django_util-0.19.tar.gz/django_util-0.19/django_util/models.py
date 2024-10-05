import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from django_util.choices import (
    FlatOrPercentChoices,
    PaymentMethodTypeChoices,
    PersonBloodChoices,
    PersonEyeColorChoices,
    PersonGenderChoices,
    PersonRaceChoices,
    TimeFrequencyChoices,
    TransactionEventTypeChoices,
    TransactionStateChoices,
    TransactionTypeChoices,
)
from django_util.fields import UpperTextField, complex_fields, related_fields


# abstract
class Profile(models.Model):
    """
    Profile model extend Django User model

    Reference
    ---------
    - https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Base(models.Model):
    """
    The ideal abstract base model

    Reference
    ---------
    - https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes
    - https://stackoverflow.com/a/16838663

    Metadata

    - https://dataedo.com/kb/data-glossary/what-is-metadata

    User tracker

    - https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/#models-and-request-user
    - https://stackoverflow.com/questions/5611410/related-name-argument-not-working-as-expected-in-django-model
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    # The field ConcreteModel.created_by was declared with a lazy reference to 'django_util.profile', but app 'django_util' doesn't provide model 'profile'.
    # The field ConcreteModel.updated_by was declared with a lazy reference to 'django_util.profile', but app 'django_util' doesn't provide model 'profile'.
    # created_by = models.ForeignKey(
    # updated_by = models.ForeignKey(
    #     Profile,
    #     editable=False,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name="%(class)s_created_by",
    # )
    note = UpperTextField(
        blank=True,
        default="",
    )
    is_admin_verified = models.BooleanField(
        default=False,
        editable=False,
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_base_meta_field_list() -> list:
        return sorted(
            [
                "created_at",
                "updated_at",
            ]
        )

    @staticmethod
    def get_extra_meta_field_list() -> list:
        return sorted(
            [
                # "created_by",
                # "updated_by",
                "note",
                "is_admin_verified",
            ]
        )

    @classmethod
    def get_field_list(cls):
        return sorted([field.name for field in cls._meta.get_fields()])

    @classmethod
    def get_field_list_without_extra_meta(cls):
        return sorted(
            list(set(cls.get_field_list()) - set(cls.get_extra_meta_field_list()))
        )

    @classmethod
    def get_field_list_without_meta(cls):
        return sorted(
            list(
                set(cls.get_field_list())
                - set(cls.get_base_meta_field_list())
                - set(cls.get_extra_meta_field_list())
            )
        )

    @classmethod
    def get_related_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, related_fields):
                field_list.append(field.name)
        return sorted(field_list)

    @classmethod
    def get_complex_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, complex_fields):
                field_list.append(field.name)
        return sorted(field_list)


class BasePublicContribute(Base):
    """
    Enhanced abstract base model, use if data can be edited by public
    """

    is_verified = models.BooleanField(
        default=False,
    )
    is_hidden = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_staff_only_field_list():
        return sorted(
            [
                "is_hidden",
                "is_verified",
            ]
        )


class EmailHttpRequest(models.Model):
    """
    Abstract model that stores email and HttpRequest fields
    """

    email = models.EmailField(
        db_index=True,
    )
    campaign = UpperTextField(
        blank=True,
        default="",
    )
    http_referrer = UpperTextField(
        blank=True,
        default="",
    )
    http_user_agent = UpperTextField(
        blank=True,
        default="",
    )
    remote_addr = models.GenericIPAddressField(
        blank=True,
        null=True,
    )
    remote_host = UpperTextField(
        blank=True,
        default="",
    )

    class Meta:
        abstract = True


class Person(models.Model):
    """
    Abstract Person model

    Reference
    ---------
    - https://schema.org/Person
    """

    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    english_first_name = UpperTextField(
        blank=True,
        default="",
    )
    english_middle_name = UpperTextField(
        blank=True,
        default="",
    )
    english_last_name = UpperTextField(
        blank=True,
        default="",
    )
    native_first_name = UpperTextField(
        blank=True,
        default="",
    )
    native_middle_name = UpperTextField(
        blank=True,
        default="",
    )
    native_last_name = UpperTextField(
        blank=True,
        default="",
    )
    alias = ArrayField(
        UpperTextField(),
        blank=True,
        null=True,
    )
    description = UpperTextField(
        blank=True,
        default="",
    )

    # biology
    birth_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    death_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    blood_type = UpperTextField(
        blank=True,
        choices=PersonBloodChoices.choices,
        default=PersonBloodChoices.DEFAULT,
    )
    eye_color = UpperTextField(
        blank=True,
        choices=PersonEyeColorChoices.choices,
        default=PersonEyeColorChoices.DEFAULT,
    )
    gender = UpperTextField(
        blank=True,
        choices=PersonGenderChoices.choices,
        default=PersonGenderChoices.DEFAULT,
    )
    race = UpperTextField(
        blank=True,
        choices=PersonRaceChoices.choices,
        default=PersonRaceChoices.DEFAULT,
    )
    height = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        abstract = True


class FullCalendarEventParseV6(models.Model):
    """
    FullCalendar Event

    Reference
    ---------
    - https://fullcalendar.io/docs/v6/event-parsing
    """

    group_id = models.TextField(
        blank=True,
        default="",
    )
    all_day = models.BooleanField(
        blank=True,
        null=True,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
    )
    end = models.DateTimeField(
        blank=True,
        null=True,
    )
    days_of_week = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    start_time = models.TimeField(
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
    )
    start_recur = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_recur = models.DateTimeField(
        blank=True,
        null=True,
    )
    title = models.TextField(
        blank=True,
        default="",
    )
    url = models.URLField(
        blank=True,
        default="",
    )
    interactive = models.BooleanField(
        blank=True,
        null=True,
    )
    class_name = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    editable = models.BooleanField(
        blank=True,
        null=True,
    )
    start_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    duration_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    resource_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    resource_id = models.TextField(
        blank=True,
        default="",
    )
    resource_ids = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    display = models.TextField(
        blank=True,
        default="",
    )
    overlap = models.BooleanField(
        blank=True,
        null=True,
    )
    constraint = models.BooleanField(
        blank=True,
        null=True,
    )
    color = models.BooleanField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class WiseWebhook(models.Model):
    """
    Wise Webhook

    Reference
    ---------
    - https://docs.wise.com/api-docs/api-reference/webhook
    """

    data = models.JSONField(
        blank=True,
        default=dict,
    )
    subscription_id = models.TextField(
        blank=True,
        default="",
    )
    event_type = models.TextField(
        blank=True,
        default="",
    )
    schema_version = models.TextField(
        blank=True,
        default="",
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Transaction(models.Model):
    """
    Records a monetary exchange related to a subscription (e.g., payment, refund). The transactions table records monetary exchanges related to subscriptions.

    Reference
    ---------
    Transaction Amount encompasses the total monetary value of a transaction. Includes the base price of the item(s), taxes, shipping fees, any additional charges, and potentially discounts or credits applied. Is the final figure paid or received.

    Transaction Price often refers more specifically to the base price of the item or service being exchanged. Excludes taxes, fees, and other charges. Can be considered the core value of the transaction.
    """

    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    currency = UpperTextField(
        max_length=3,
        blank=True,
    )
    choice_type = UpperTextField(
        blank=True,
        choices=TransactionTypeChoices.choices,
        default=TransactionTypeChoices.DEFAULT,
    )
    data = models.JSONField(
        blank=True,
        default=dict,
    )
    state = UpperTextField(
        blank=True,
        choices=TransactionStateChoices.choices,
        default=TransactionStateChoices.DEFAULT,
    )
    transaction_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    # Relation
    # payment_method = models.ForeignKey
    # subscription = models.ForeignKey

    class Meta:
        abstract = True


class TransactionEvent(models.Model):
    """
    Captures specific actions or changes within a transaction's lifecycle. The transaction_event table provides granular details about the transaction's lifecycle.
    """

    choice_type = UpperTextField(
        blank=True,
        choices=TransactionEventTypeChoices.choices,
        default=TransactionEventTypeChoices.DEFAULT,
    )
    description = UpperTextField(
        blank=True,
        default="",
    )
    data = models.JSONField(
        blank=True,
        default=dict,
    )

    # Relation
    # transaction = models.ForeignKey

    class Meta:
        abstract = True


class PaymentMethod(models.Model):
    """
    Abstract payment model
    """

    choice_type = UpperTextField(
        blank=True,
        choices=PaymentMethodTypeChoices.choices,
        default=PaymentMethodTypeChoices.DEFAULT,
    )
    billing_address = models.TextField(
        blank=True,
        default="",
    )

    # Relation
    # profile = models.ForeignKey

    class Meta:
        abstract = True


class CardPayment(PaymentMethod):
    """
    Card payment inherit PayMethod abstract model
    """

    card_number = models.TextField(
        blank=True,
        default="",
    )
    card_expiry = models.DateTimeField(
        blank=True,
        null=True,
    )
    card_cvv = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        abstract = True


class Coupon(models.Model):
    """
    Coupon discount
    """

    code = models.TextField(
        blank=True,
        default="",
    )
    discount_type = UpperTextField(
        blank=True,
        choices=FlatOrPercentChoices.choices,
        default=FlatOrPercentChoices.DEFAULT,
    )
    discount_value = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    usage_limit = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Plan(models.Model):
    """
    Plan: Defines the features, price, and billing cycle of a subscription.
    """

    name = UpperTextField(
        blank=True,
        default="",
    )
    description = UpperTextField(
        blank=True,
        default="",
    )
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    currency = UpperTextField(
        max_length=3,
        blank=True,
    )
    billing_cycle = UpperTextField(
        blank=True,
        choices=TimeFrequencyChoices.choices,
        default=TimeFrequencyChoices.DEFAULT,
    )
    feature = ArrayField(
        UpperTextField(),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class PlanPlus(Plan):
    """
    Enhanced Plan
    """

    trial_period = models.IntegerField(
        blank=True,
        null=True,
    )
    discount_eligible = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class Subscription(models.Model):
    """
    Represents a customer's active subscription to a plan. The subscriptions table tracks the active state of a customer's subscription, including its start and end dates.
    """

    start_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    next_billing_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    prorated_amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    is_active = models.BooleanField(
        default=False,
    )

    # Relation
    # coupon = models.ForeignKey
    # plan = models.ForeignKey
    # profile = models.ForeignKey

    class Meta:
        abstract = True
