LOGIN = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
        },
        "password": {
            "type": "string",
        }
    },
    "required": ["username", "password"],
}

LOGOUT = {
    "type": "object",
    "properties": {
        "userid": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        }
    },
    "required": ["userid", "ts"],
}

TRIPINFO = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
    },
    "required": ["trip_id", "ts"],
}

TRIP_START_COMPLETE = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        }
    },
    "required": ["trip_id", "ts"],
}

TRIP_CANCEL = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
        "reason": {
            "type": "string",
        }
    },
    "required": ["trip_id", "ts", "reason"],
}

MEET_START_REACH = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
        "customer_d": {
            "type": "number",
        }
    },
    "required": ["trip_id", "ts", "customer_d"],
}

MEETCANCEL = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
        "customer_d": {
            "type": "number",
        },
        "reason": {
            "type": "string",
        }
    },
    "required": ["trip_id", "ts", "customer_d", "reason"],
}

MEETCOMPLETE = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "pictures": {
            "type": "multipart",
        },
        "customer_d": {
            "type": "number",
        },
        "note": {
            "type": "string",
        },
        "ts": {
            "type": "number",
        },
        "type": "object",
        "properties": {
            "type_id": {
                "type": "number",
            },
            "deadline": {
                "type": "date",
            },
            "summary": {
                "type": "string",
            },
            "note": {
                "type": "string",
            }
        },
    },
    "required": ["trip_id", "ts", "customer_d", "reason"],
}

LEADS_ACTIVITY = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
    },
    "required": ["trip_id", "ts"],
}

LEADS_INFO = {
    "type": "object",
    "properties": {
        "trip_id": {
            "type": "number",
        },
        "ts": {
            "type": "number",
        },
    },
    "required": ["trip_id", "ts"],
}
