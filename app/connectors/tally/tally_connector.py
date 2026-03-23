from app.connectors.base.base_connector import BaseConnector


class TallyConnector(BaseConnector):

    def test_connection(self, config: dict):
        return {
            "source_name": "tally",
            "connection_status": "success",
            "details": "Connection established successfully"
        }