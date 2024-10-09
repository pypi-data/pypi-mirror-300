""" Module for billing APIs """
import logging
from typing import List

from ..entities.billing import BillingReport
from ..Request import _Request

logger = logging.getLogger("BillingAPI")


# pylint: disable=protected-access
class BillingAPI:
    """Class for billing APIs"""

    def __init__(self, request: _Request):
        self.request = request

    def generate_report(self, params=None):
        return self.request._make_request("POST", "/billing/report", params=params)

    def get_billing_reports(self) -> List[BillingReport]:
        res = self.request._make_request("GET", "/billing/reports", list=True)
        if not res:
            raise Exception("No response")
        return [BillingReport(**r) for r in res]

    def get_billing_report(self, report_id: int) -> BillingReport:
        res = self.request._make_request("GET", f"/billing/reports/{report_id}")
        if not res:
            raise Exception("No response")
        return BillingReport(**res)

    def get_billing_report_download_url(self, report_id: int) -> str:
        res = self.request._make_request("GET", f"/billing/reports/{report_id}/download")
        if not res:
            raise Exception("No response")
        return res["url"]
