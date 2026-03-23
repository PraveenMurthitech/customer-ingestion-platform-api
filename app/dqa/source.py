# app/dqa/source.py

# 🔹 Dummy DB (in-memory)
SOURCES_DB = [
    {
        "config_id": "uuid1",
        "customer_id": 101,
        "source_name": "zoho_crm",
        "version": 2,
        "config": {"client_id": "xxx"},
        "checksum": "abc123",
        "is_active": True,
        "created_at": "2026-03-21T12:00:00Z",
        "updated_at": "2026-03-21T12:30:00Z"
    },
    {
        "config_id": "uuid2",
        "customer_id": 101,
        "source_name": "tally",
        "version": 1,
        "config": {"host": "localhost"},
        "checksum": "def456",
        "is_active": True,
        "created_at": "2026-03-21T12:00:00Z",
        "updated_at": "2026-03-21T12:30:00Z"
    },
    {
        "config_id": "uuid3",
        "customer_id": 102,
        "source_name": "zoho_crm",
        "version": 1,
        "config": {},
        "checksum": "ghi789",
        "is_active": False,
        "created_at": "2026-03-21T12:00:00Z",
        "updated_at": "2026-03-21T12:30:00Z"
    }
]


# 🔹 helper: check customer existence
def _customer_exists(customer_id: int):
    return any(s["customer_id"] == customer_id for s in SOURCES_DB)


# 🔹 get all sources
def get_all_sources(customer_id: int):
    if not _customer_exists(customer_id):
        return {"error": "CUSTOMER_NOT_FOUND"}

    data = [s for s in SOURCES_DB if s["customer_id"] == customer_id]

    if not data:
        return {"error": "NO_SOURCES_FOUND"}

    return {"data": data}


# 🔹 get single source
def get_single_source(customer_id: int, source_name: str):
    if not _customer_exists(customer_id):
        return {"error": "CUSTOMER_NOT_FOUND"}

    for s in SOURCES_DB:
        if s["customer_id"] == customer_id and s["source_name"] == source_name:
            return {"data": s}

    return {"error": "SOURCE_NOT_FOUND"}


# 🔹 activate source
def activate_source(customer_id: int, source_name: str):
    if not _customer_exists(customer_id):
        return {"error": "CUSTOMER_NOT_FOUND"}

    for s in SOURCES_DB:
        if s["customer_id"] == customer_id and s["source_name"] == source_name:
            s["is_active"] = True
            return {"data": True}

    return {"error": "SOURCE_NOT_FOUND"}


# 🔹 deactivate source
def deactivate_source(customer_id: int, source_name: str):
    if not _customer_exists(customer_id):
        return {"error": "CUSTOMER_NOT_FOUND"}

    for s in SOURCES_DB:
        if s["customer_id"] == customer_id and s["source_name"] == source_name:
            s["is_active"] = False
            return {"data": True}

    return {"error": "SOURCE_NOT_FOUND"}