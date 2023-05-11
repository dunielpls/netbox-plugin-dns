import ipaddress

from django.db.models import (
    ForeignKey,
    CharField,
    BooleanField,
    PositiveIntegerField,
    BigIntegerField,
    CASCADE
)
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)

from netbox.models import NetboxModel
from netbox.utilities.querysets import RestrictedQuerySet
from netbox.utilities.choices import ChoiceSet

class ZoneType(ChoiceSet):
    key = "Zone.type"

    PRIMARY = "primary"
    SECONDARY = "secondary"
    STUB = "stub"
    FORWARD = "forward"
    DISABLED = "disabled"

    # For now - only support primary zones.
    CHOICES = [
        (PRIMARY, "Primary", "green"),
        #(SECONDARY, "Secondary", "blue"),
        #(STUB, "Stub", "orange"),
        #(FORWARD, "Forward", "purple"),
        (DISABLED, "Disabled", "grey")
    ]

class ZoneStatus(ChoiceSet):
    key = "Zone.status"

    ACTIVE = True
    DISABLED = False

    CHOICES = [
        (ACTIVE, "Active", "green"),
        (DISABLED, "Disabled", "grey")
    ]

class Zone(NetboxModel):
    name = CharField(
        max_length=253,
        null=False,
        blank=False,
        verbose_name="Zone name"
    )
    default_ttl = PositiveIntegerField(
        default=3600,
        null=False,
        blank=True,
        verbose_name="Default time-to-live",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(604800)
        ]
    )
    soa_ttl = PositiveIntegerField(
        default=3600,
        null=False,
        blank=True,
        verbose_name="SOA time-to-live"
    )
    soa_mname = CharField(
        max_length=255,
        null=False,
        blank=True,
        verbose_name="SOA master nameserver",
    )
    soa_rname = CharField(
        max_length=255,
        null=False,
        blank=True,
        verbose_name="SOA responsible party"
    )
    soa_serial = PositiveIntegerField(
        default=1,
        null=False,
        blank=True,
        verbose_name="SOA serial",
        validators=[
            MinValueValidator(1),
            # 2 ** 32 - 1
            MaxValueValidator(0xFFFFFFFF),
        ]
    )
    soa_refresh = PositiveIntegerField(
        default=3600,
        null=False,
        blank=True,
        verbose_name="SOA refresh",
        validators=[MinValueValidator(1)]
    )
    soa_retry = PositiveIntegerField(
        default=900,
        null=False,
        blank=True,
        verbose_name="SOA retry",
        validators=[MinValueValidator(1)]
    )
    soa_expire = PositiveIntegerField(
        default=604800,
        null=False,
        blank=True,
        verbose_name="SOA expire",
        validators=[MinValueValidator(1)]
    )
    soa_minimum = PositiveIntegerField(
        default=3600,
        null=False,
        blank=True,
        verbose_name="SOA minimum",
        validators=[MinValueValidator(1)]
    )
    # Metadata
    type = CharField(
        choices=ZoneType,
        default=ZoneType.PRIMARY,
        null=False,
        blank=False,
        verbose_name="Zone type"
    )
    status = BooleanField(
        choices=ZoneStatus,
        default=ZoneStatus.ACTIVE,
        null=False,
        blank=False,
        verbose_name="Zone status"
    )
    description = CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Description"
    )
    auto_serial = BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name="Automatically generate SOA serial"
    )

class RecordType(ChoiceSet):
    KEY = "Record.type"

    # Only a subset for now
    A = 1
    AAAA = 28
    CNAME = 5
    TXT = 16
    SRV = 33
    PTR = 12

    CHOICES = [
        (A, "IP address", "default"),
        (AAAA, "IPv6 address", "green"),
        (CNAME, "Canonical name", "blue"),
        (TXT, "Text", "red"),
        (SRV, "Service", "indigo"),
        (PTR, "Pointer", "orange")
    ]

class RecordStatus(ChoiceSet):
    key = "Record.status"

    ACTIVE = True
    DISABLED = False

    CHOICES = [
        (ACTIVE, "Active", "green"),
        (DISABLED, "Disabled", "grey")
    ]

class Record(NetboxModel):
    zone = ForeignKey(
        Zone,
        on_delete=CASCADE
    )
    name = CharField(
        max_length=255,
        verbose_name="Record name"
    )
    type = PositiveIntegerField(
        choices=RecordType,
        verbose_name="Record type",
        validators=[
            MinValueValidator(1),
            # 2 octets
            MaxValueValidator(0xFFFF)
        ]
    )
    value = CharField(
        max_length=65535,
        verbose_name="Record value"
    )
    ttl = PositiveIntegerField(
        default=3600,
        null=False,
        blank=True,
        verbose_name="Record time-to-live",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(604800)
        ]
    )
    # Metadata
    status = BooleanField(
        choices=RecordStatus,
        default=RecordStatus.ACTIVE,
        null=False,
        blank=False,
        verbose_name="Record status"
    )
