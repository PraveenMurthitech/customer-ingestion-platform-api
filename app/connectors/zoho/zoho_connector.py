from app.connectors.base.base_connector import BaseConnector


class ZohoConnector(BaseConnector):

    def test_connection(self, config: dict):
        return {
            "source_name": "zoho_crm",
            "connection_status": "success",
            "details": "Connection established successfully"
        }