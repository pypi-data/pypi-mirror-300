"""Stream type classes for tap-brevo."""

from __future__ import annotations
from typing import Optional
from importlib import resources
from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_brevo.client import brevoStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ListsStream(brevoStream):
    """Define custom stream."""

    name = "lists"
    path = "/contacts/lists"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("totalBlacklisted", th.IntegerType),
        th.Property("totalSubscribers", th.IntegerType),
        th.Property("uniqueSubscribers", th.IntegerType),
        th.Property("folderId", th.IntegerType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class CampaignsStream(brevoStream):
    """Define custom stream."""

    name = "campaigns"
    path = "/emailCampaigns"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.campaigns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("subject", th.StringType),
        th.Property("type", th.StringType),
        th.Property("status", th.StringType),
        th.Property("scheduledAt", th.StringType),
        th.Property("testSent", th.BooleanType),
        th.Property("header", th.StringType),
        th.Property("footer", th.StringType),
        th.Property(
            "sender",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("replyTo", th.StringType),
        th.Property("toField", th.StringType),
        th.Property("shareLink", th.StringType),
        th.Property("tag", th.StringType),
        th.Property("createdAt", th.StringType),
        th.Property("modifiedAt", th.StringType),
        th.Property("inlineImageActivation", th.BooleanType),
        th.Property("mirrorActive", th.BooleanType),
        th.Property("recurring", th.BooleanType),
        th.Property(
            "recipients",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("statistics", th.ObjectType(additional_properties=True)),
    ).to_dict()


class SMSCampaignsStream(brevoStream):
    """Define custom stream."""

    name = "sms_campaigns"
    path = "/smsCampaigns"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.campaigns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("status", th.StringType),
        th.Property("content", th.StringType),
        th.Property("scheduledAt", th.StringType),
        th.Property("testSent", th.BooleanType),
        th.Property("sender", th.StringType),
        th.Property("createdAt", th.StringType),
        th.Property("modifiedAt", th.StringType),
        th.Property("recipients", th.ObjectType()),
        th.Property("statistics", th.ObjectType()),
    ).to_dict()
