from app.connectors.zoho.zoho_connector import ZohoConnector
from app.connectors.tally.tally_connector import TallyConnector


def get_connector(source_name: str):
    if source_name == "zoho_crm":
        return ZohoConnector()
    elif source_name == "tally":
        return TallyConnector()
    else:
        raise ValueError(f"Unsupported source: {source_name}")