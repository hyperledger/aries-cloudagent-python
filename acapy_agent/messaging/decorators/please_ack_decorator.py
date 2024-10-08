"""The please-ack decorator to request acknowledgement."""

from typing import Optional, Sequence

from marshmallow import EXCLUDE, fields

from ..models.base import BaseModel, BaseModelSchema
from ..valid import UUID4_EXAMPLE


class PleaseAckDecorator(BaseModel):
    """Class representing the please-ack decorator."""

    class Meta:
        """PleaseAckDecorator metadata."""

        schema_class = "PleaseAckDecoratorSchema"

    def __init__(
        self,
        message_id: Optional[str] = None,
        on: Sequence[str] = None,
    ):
        """Initialize a PleaseAckDecorator instance.

        Args:
            message_id: identifier of message to acknowledge, if not current message
            on: list of tokens describing circumstances for acknowledgement.

        """
        super().__init__()
        self.message_id = message_id
        self.on = list(on) if on else None


class PleaseAckDecoratorSchema(BaseModelSchema):
    """PleaseAck decorator schema used in serialization/deserialization."""

    class Meta:
        """PleaseAckDecoratorSchema metadata."""

        model_class = PleaseAckDecorator
        unknown = EXCLUDE

    message_id = fields.Str(
        required=False,
        allow_none=False,
        metadata={"description": "Message identifier", "example": UUID4_EXAMPLE},
    )
    on = fields.List(
        fields.Str(metadata={"example": "OUTCOME"}),
        required=False,
        metadata={
            "description": "List of tokens describing circumstances for acknowledgement"
        },
    )
