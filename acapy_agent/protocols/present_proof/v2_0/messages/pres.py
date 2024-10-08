"""A (proof) presentation content message."""

from typing import Optional, Sequence

from marshmallow import EXCLUDE, ValidationError, fields, validates_schema

from .....messaging.agent_message import AgentMessage, AgentMessageSchema
from .....messaging.decorators.attach_decorator import (
    AttachDecorator,
    AttachDecoratorSchema,
)
from ..message_types import PRES_20, PROTOCOL_PACKAGE
from .pres_format import V20PresFormat, V20PresFormatSchema

HANDLER_CLASS = f"{PROTOCOL_PACKAGE}.handlers.pres_handler.V20PresHandler"


class V20Pres(AgentMessage):
    """Class representing a presentation."""

    class Meta:
        """Presentation metadata."""

        handler_class = HANDLER_CLASS
        schema_class = "V20PresSchema"
        message_type = PRES_20

    def __init__(
        self,
        _id: Optional[str] = None,
        *,
        comment: Optional[str] = None,
        formats: Sequence[V20PresFormat] = None,
        presentations_attach: Sequence[AttachDecorator] = None,
        **kwargs,
    ):
        """Initialize presentation object.

        Args:
            _id (str, optional): The ID of the presentation object.
            comment (str, optional): An optional comment.
            formats (Sequence[V20PresFormat], optional): A sequence of presentation
                formats.
            presentations_attach (Sequence[AttachDecorator], optional): A sequence of
                attachments.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(_id=_id, **kwargs)
        self.comment = comment
        self.formats = formats if formats else []
        self.presentations_attach = (
            list(presentations_attach) if presentations_attach else []
        )

    def attachment(self, fmt: V20PresFormat.Format = None) -> dict:
        """Return attached presentation item.

        Args:
            fmt: format of attachment in list to decode and return

        """
        target_format = (
            fmt
            if fmt
            else next(
                filter(
                    lambda ff: ff,
                    [V20PresFormat.Format.get(f.format) for f in self.formats],
                ),
                None,
            )
        )
        return (
            target_format.get_attachment_data(self.formats, self.presentations_attach)
            if target_format
            else None
        )


class V20PresSchema(AgentMessageSchema):
    """Presentation schema."""

    class Meta:
        """Presentation schema metadata."""

        model_class = V20Pres
        unknown = EXCLUDE

    comment = fields.Str(
        required=False,
        allow_none=True,
        metadata={"description": "Human-readable comment"},
    )
    formats = fields.Nested(
        V20PresFormatSchema,
        many=True,
        required=True,
        metadata={"description": "Acceptable attachment formats"},
    )
    presentations_attach = fields.Nested(
        AttachDecoratorSchema, required=True, many=True, data_key="presentations~attach"
    )

    @validates_schema
    def validate_fields(self, data, **kwargs):
        """Validate presentation attachment per format."""

        def get_attach_by_id(attach_id):
            """Return attachment with input attachment identifier."""
            for atch in attachments:
                if atch.ident == attach_id:
                    return atch
            raise ValidationError(f"No attachment for attach_id {attach_id} in formats")

        formats = data.get("formats") or []
        attachments = data.get("presentations_attach") or []
        if len(formats) != len(attachments):
            raise ValidationError("Formats/attachments length mismatch")

        for fmt in formats:
            atch = get_attach_by_id(fmt.attach_id)
            pres_format = V20PresFormat.Format.get(fmt.format)
            if pres_format:
                if isinstance(atch.content, Sequence):
                    for el in atch.content:
                        pres_format.validate_fields(PRES_20, el)
                else:
                    pres_format.validate_fields(PRES_20, atch.content)
