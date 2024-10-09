"""Stream type classes for tap-shopify."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_shopify.client import shopifyStream


class OrdersStream(shopifyStream):
    """Orders stream."""

    name = "orders"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "createdAt"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("referrerUrl", th.StringType),
        th.Property("landingPageUrl", th.StringType),
        th.Property("landingPageDisplayText", th.StringType),
        th.Property("totalRefunded", th.StringType),
        th.Property("totalTipReceived", th.ObjectType(
            th.Property("amount", th.StringType)
        )),
        th.Property("discountCodes", th.ArrayType(th.StringType), required=False),
        th.Property(
            "channel", th.ObjectType(th.Property("name", th.StringType)), required=False
        ),
        th.Property(
            "currentTotalPriceSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalTaxSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalDiscountsSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalShippingPriceSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "shippingAddress",
            th.ObjectType(
                th.Property("address1", th.StringType),
                th.Property("address2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("country", th.StringType),
                th.Property("province", th.StringType),
                th.Property("zip", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("displayName", th.StringType),
                th.Property("email", th.StringType),
                th.Property("phone", th.StringType),
            ),
        ),
        th.Property(
            "taxLines",
            th.ArrayType(th.ObjectType(th.Property("rate", th.NumberType, required=False))),
            required=False,
        )
    ).to_dict()

    @property
    def query(self) -> str:
        """Return the GraphQL query to be executed."""
        start_date = self.config.get("start_date")

        return f"""
        query {{
            orders (first: 250, query: "created_at:>={start_date}") {{
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
                edges {{
                    cursor
                    node {{
                        id
                        name
                        createdAt
                        referrerUrl
                        landingPageUrl
                        landingPageDisplayText
                        channel {{
                            name
                        }}
                        totalRefunded
                        discountCodes
                        totalTipReceived {{
                            amount
                        }}
                        currentTotalPriceSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalTaxSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalDiscountsSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalShippingPriceSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        shippingAddress {{
                            address1
                            address2
                            city
                            country
                            province
                            zip
                        }}
                        customer {{
                            displayName
                            email
                            phone
                        }}
                        taxLines {{
                            rate
                        }}
                    }}
                }}
            }}
        }}
        """
