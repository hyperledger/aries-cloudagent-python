"""Inner structure of keylist message. Represents a single item in keylist.keys."""

from marshmallow import EXCLUDE, fields

from ......messaging.models.base import BaseModel, BaseModelSchema
from ......messaging.valid import IndyRawPublicKey


class KeylistKey(BaseModel):
    """Inner structure of Keylist keys attribute."""

    class Meta:
        """KeylistKey metadata."""

        schema_class = "KeylistKeySchema"

    def __init__(
        self,
        *,
        recipient_key: str = None,
        action: str = None,
        result: str = None,
        **kwargs
    ):
        """
        Initialize a KeylistKey instance.

        Args:
            recipient_key: The recipient verkey of the route
            action: The requested action to perform
            result: The result of the requested action

        """
        super().__init__(**kwargs)
        self.recipient_key = recipient_key


class KeylistKeySchema(BaseModelSchema):
    """KeylistKey schema."""

    class Meta:
        """KeylistKeySchema metadata."""

        model_class = KeylistKey
        unknown = EXCLUDE

    recipient_key = fields.Str(
        required=True, validate=IndyRawPublicKey(), example=IndyRawPublicKey.EXAMPLE
    )
