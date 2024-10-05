"""
Monkeypatches for pycsw.core.repository module
"""

import logging

import pycsw.core.repository
import requests
from sqlalchemy.sql import text

LOGGER = logging.getLogger(__name__)


def get_column_name(context, model_name):
    """
    Lookup function to get column name from mapping configuration (context)
    """
    return context.md_core_model["mappings"][model_name]


def execute_transaction_webhook(context, transaction_type, records):
    """
    Sends POST request o web hook URL (specified in config) with body
    containing summary about transaction executed
    """

    if (
        hasattr(context, "transactions_webhook_url")
        and context.transactions_webhook_url
    ):
        transactions = []

        for record in records:
            transaction = {
                "transaction_type": transaction_type,
                "record_id": getattr(
                    record, get_column_name(context, "pycsw:Identifier")
                ),
                "resource_type": getattr(
                    record, get_column_name(context, "pycsw:Type")
                ),
            }
            if transaction_type == "insert":
                transaction["record"] = getattr(
                    record, get_column_name(context, "pycsw:XML")
                )

            transactions.append(transaction)

        try:
            r = requests.post(
                context.transactions_webhook_url, json=transactions, timeout=10
            )
            r.raise_for_status()
        # pylint: disable=broad-exception-caught
        except Exception as e:
            LOGGER.warning("Notification to transactions web hook failed")
            LOGGER.warning(e)
    else:
        LOGGER.debug("Transactions web hook url not set, notification will not be send")


delete = pycsw.core.repository.Repository.delete
insert = pycsw.core.repository.Repository.insert


def rpi_insert(self, record, source, insert_date):
    """
    Patched version of pycsw.core.repository.insert function
    """

    # call original insert method
    insert(self, record, source, insert_date)

    # no exception has been raised, webhook may be called
    execute_transaction_webhook(self.context, "insert", [record])


def rpi_delete(self, constraint):
    """
    Patched version of pycsw.core.repository.delete function
    """

    # pylint: disable=protected-access
    records = (
        self._get_repo_filter(self.session.query(self.dataset))
        .filter(text(constraint["where"]))
        .params(self._create_values(constraint["values"]))
        .all()
    )

    # extend records with child records if any

    records.extend(
        self._get_repo_filter(self.session.query(self.dataset))
        .filter(
            getattr(
                self.dataset, get_column_name(self.context, "pycsw:ParentIdentifier")
            ).in_(
                [
                    getattr(record, get_column_name(self.context, "pycsw:Identifier"))
                    for record in records
                ]
            )
        )
        .all()
    )

    deleted = delete(self, constraint)

    # no exception has been raised, webhook may be called
    execute_transaction_webhook(self.context, "delete", records)

    return deleted


pycsw.core.repository.Repository.delete = rpi_delete
pycsw.core.repository.Repository.insert = rpi_insert
