"""
The timing decorator (~timing).

This decorator allows the timing of agent messages to be communicated
and constrained.
"""

from datetime import datetime
from typing import Union

from marshmallow import EXCLUDE, fields

from ..models.base import BaseModel, BaseModelSchema
from ..util import datetime_to_str
from ..valid import IndyISO8601DateTime


class TimingDecorator(BaseModel):
    """Class representing the timing decorator."""

    class Meta:
        """TimingDecorator metadata."""

        schema_class = "TimingDecoratorSchema"

    def __init__(
        self,
        *,
        in_time: Union[str, datetime] = None,
        out_time: Union[str, datetime] = None,
        stale_time: Union[str, datetime] = None,
        expires_time: Union[str, datetime] = None,
        delay_milli: int = None,
        wait_until_time: Union[str, datetime] = None,
    ):
        """
        Initialize a TimingDecorator instance.

        Args:
            in_time: The time the message was received
            out_time: The time the message was dispatched
            stale_time: When the message should be considered stale
            expires_time: When the message should be considered expired
            delay_milli: The number of milliseconds to delay processing
            wait_until_time: The earliest time at which to perform processing
        """
        super().__init__()
        self.in_time = datetime_to_str(in_time)
        self.out_time = datetime_to_str(out_time)
        self.stale_time = datetime_to_str(stale_time)
        self.expires_time = datetime_to_str(expires_time)
        self.delay_milli = delay_milli
        self.wait_until_time = datetime_to_str(wait_until_time)


class TimingDecoratorSchema(BaseModelSchema):
    """Timing decorator schema used in serialization/deserialization."""

    class Meta:
        """TimingDecoratorSchema metadata."""

        model_class = TimingDecorator
        unknown = EXCLUDE

    in_time = fields.Str(
        required=False,
        description="Time of message receipt",
        validate=IndyISO8601DateTime(),
        example=IndyISO8601DateTime.EXAMPLE,
    )
    out_time = fields.Str(
        required=False,
        description="Time of message dispatch",
        validate=IndyISO8601DateTime(),
        example=IndyISO8601DateTime.EXAMPLE,
    )
    stale_time = fields.Str(
        required=False,
        description="Time when message should be considered stale",
        validate=IndyISO8601DateTime(),
        example=IndyISO8601DateTime.EXAMPLE,
    )
    expires_time = fields.Str(
        required=False,
        description="Time when message should be considered expired",
        validate=IndyISO8601DateTime(),
        example=IndyISO8601DateTime.EXAMPLE,
    )
    delay_milli = fields.Int(
        required=False,
        description="Number of milliseconds to delay processing",
        example=1000,
        strict=True,
    )
    wait_until_time = fields.Str(
        required=False,
        description="Earliest time at which to perform processing",
        validate=IndyISO8601DateTime(),
        example=IndyISO8601DateTime.EXAMPLE,
    )
