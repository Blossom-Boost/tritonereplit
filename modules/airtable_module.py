import os
from typing import Iterable

from airtable.airtable import Airtable

AIRTABLE_BASE = os.environ.get('AIRTABLE_BASE')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')


class AirtableModule:

  def __init__(self):
    self.airtableClient = Airtable(AIRTABLE_BASE, AIRTABLE_API_KEY)

  def create_record(self, table: str, record: dict):
    return self.airtableClient.create(table, record)

  def get_all_records(self, table: str):
    return self.airtableClient.get(table)

  def get(self,
          table: str,
          record_id: str | None,
          limit: int = 0,
          offset: int | None = None,
          filter_by_formula: str | None = None,
          view: str | None = None,
          max_records: int = 0,
          fields: Iterable[str] = iter([])):
    return self.airtableClient.get(table, record_id, limit, offset,
                                   filter_by_formula, view, max_records,
                                   fields)

  def get_iterate(self,
                  table: str,
                  limit: int = 0,
                  offset: int | None = None,
                  filter_by_formula: str | None = None,
                  max_records: int = 0,
                  fields: Iterable[str] = iter([])):
    return self.airtableClient.iterate(table, limit, offset, filter_by_formula,
                                       max_records, fields)
