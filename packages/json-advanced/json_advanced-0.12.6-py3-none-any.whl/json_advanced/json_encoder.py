import base64
import datetime
import json
import re
import uuid
from decimal import Decimal
from pathlib import Path

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None

try:
    from bson import Decimal128, ObjectId
except ImportError:
    Decimal128 = None
    ObjectId = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
except ImportError:
    pd = None


class JSONSerializer(json.JSONEncoder):
    def default(self, obj):
        # Text Type:	str
        # Numeric Types:	int, float, complex
        # Sequence Types:	list, tuple, range
        # Mapping Type:	dict
        # Set Types:	set, frozenset
        # Boolean Type:	bool
        # Binary Types:	bytes, bytearray, memoryview
        # None Type:	NoneType
        if isinstance(
            obj,
            (
                str,
                int,
                float,
                complex,
                list,
                tuple,
                range,
                dict,
                set,
                frozenset,
                bool,
                type(None),
            ),
        ):
            return obj
        if isinstance(obj, (bytes, bytearray, memoryview)):
            return f'b64:{base64.b64encode(bytes(obj)).decode("utf-8")}'
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S.%f")
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, Path):
            return str(obj)
        if hasattr(obj, "to_json"):
            return obj.to_json()
        if BaseModel and isinstance(obj, BaseModel):
            return obj.model_dump()
        if ObjectId and isinstance(obj, ObjectId):
            return str(obj)
        if Decimal128 and isinstance(obj, Decimal128):
            return str(obj)
        if isinstance(obj, Exception):
            return repr(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        if np and isinstance(obj, np.ndarray):
            return obj.tolist()
        if pd and isinstance(obj, pd.Series):
            return obj.to_dict()
        return super().default(obj)


def json_deserializer(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            # Base64 decoding
            if value.startswith("b64:"):
                base64_str = value[4:]  # Remove the 'b64:' prefix
                try:
                    dct[key] = base64.b64decode(base64_str)
                except (ValueError, TypeError):
                    pass

            # UUID conversion
            if re.match(
                r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
                value,
            ):
                try:
                    dct[key] = uuid.UUID(value)
                except ValueError:
                    pass

            # Datetime conversion
            datetime_patterns = [
                (
                    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$",
                    "%Y-%m-%dT%H:%M:%S.%f",
                    lambda dt: dt,
                ),
                (
                    r"^(\d{2,4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$",
                    "%Y-%m-%d %H:%M:%S",
                    lambda dt: dt,
                ),
                (r"^(\d{2,4}-\d{2}-\d{2})$", "%Y-%m-%d", lambda dt: dt.date()),
                (
                    r"^(\d{2}:\d{2}:\d{2}(\.\d+))$",
                    "%H:%M:%S.%f",
                    lambda dt: dt.time(),
                ),
                (r"^(\d{2}:\d{2}:\d{2})$", "%H:%M:%S", lambda dt: dt.time()),
            ]

            for reg, pattern, formatter in datetime_patterns:
                if re.match(reg, value):
                    try:
                        dt = datetime.datetime.strptime(value, pattern)
                        dct[key] = formatter(dt)
                        break  # Exit loop after successful conversion
                    except ValueError:
                        continue  # Try next pattern

    return dct


def dumps(*args, **kwargs):
    kwargs.setdefault("cls", JSONSerializer)
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs.setdefault("cls", JSONSerializer)
    return json.dump(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs.setdefault("object_hook", json_deserializer)
    return json.loads(*args, **kwargs)


def load(*args, **kwargs):
    kwargs.setdefault("object_hook", json_deserializer)
    return json.load(*args, **kwargs)
