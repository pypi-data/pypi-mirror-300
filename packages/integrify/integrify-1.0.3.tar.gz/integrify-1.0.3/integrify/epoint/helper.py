import base64
import json

from hashlib import sha1
from integrify.epoint import env
from integrify.epoint.schemas.types import CallbackDataSchema, DecodedCallbackDataSchema

__all__ = ['generate_signature', 'decode_callback_data']


def generate_signature(data: str) -> str:
    sgn_string = env.EPOINT_PRIVATE_KEY + data + env.EPOINT_PRIVATE_KEY
    return base64.b64encode(sha1(sgn_string.encode(), usedforsecurity=False).digest()).decode()


def decode_callback_data(data: CallbackDataSchema) -> DecodedCallbackDataSchema:
    if data.signature != generate_signature(data.data):
        return None  # type: ignore[return-value]

    return DecodedCallbackDataSchema.model_validate(json.loads(base64.b64decode(data.data)))
