import json
import logging
import os

from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField

logger = logging.getLogger(__name__)
client = bigquery.Client(project='wellio-integration')


class BigQueryTable(object):

    def __init__(self):
        self._bq_schema = [SchemaField("full_name", "STRING", mode="REQUIRED"),
        SchemaField("item_1", "STRING", mode="REQUIRED"),
        SchemaField("item_2", "STRING", mode="REQUIRED"),
        SchemaField("item_3", "STRING", mode="REQUIRED"),
        SchemaField("item_4", "STRING", mode="REQUIRED"), 
        SchemaField("item_5", "STRING", mode="REQUIRED"),
        SchemaField("item_6", "STRING", mode="REQUIRED"), ]
        self._dataset = 'dataflow_pipeline'
        self._table_name = 'test_table'

        self._table = self._get_table(self._dataset, self._table_name, self._bq_schema)

    def _get_table(self, dataset_name, table_name, schema):
        """
        Retrieves a table in a dataset with the specified schema,
        and creates it if not found.
        Returns
        -------
        table: google.cloud.bigquery.table import Table
            created table
        """
        dataset_ref = client.dataset(dataset_name)
        try:
            client.get_dataset(dataset_ref)
        except NotFound:
            logger.info('Dataset {} not found. Creating.'.format(dataset_name))
            client.create_dataset(bigquery.Dataset(dataset_ref))

        table_ref = dataset_ref.table(table_name)
        try:
            table = client.get_table(table_ref)
        except NotFound:
            table = client.create_table(bigquery.Table(table_ref, schema=schema))

        # ensure schema conformance
        table_schema = table.schema[:]
        if table_schema != schema:
            logger.warning('Updating BQ schema for {}.{}'.format(self._dataset, self._table_name))
            table.schema = schema
            client.update_table(table, ['schema'])

        return table

BigQueryTable()