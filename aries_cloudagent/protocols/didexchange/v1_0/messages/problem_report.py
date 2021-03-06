"""Represents a connection problem report message."""

from enum import Enum
from marshmallow import EXCLUDE, fields, validate

from .....messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import PROBLEM_REPORT

HANDLER_CLASS = "aries_cloudagent.messaging.problem_report.handler.ProblemReportHandler"


class ProblemReportReason(str, Enum):
    """Supported reason codes."""

    REQUEST_NOT_ACCEPTED = "request_not_accepted"
    REQUEST_PROCESSING_ERROR = "request_processing_error"
    INVITATION_NOT_ACCEPTED = "invitation_not_accepted"
    RESPONSE_NOT_ACCEPTED = "response_not_accepted"
    RESPONSE_PROCESSING_ERROR = "response_processing_error"
    COMPLETE_NOT_ACCEPTED = "complete_not_accepted"


class ProblemReport(AgentMessage):
    """Base class representing a connection problem report message."""

    class Meta:
        """Connection problem report metadata."""

        handler_class = HANDLER_CLASS
        message_type = PROBLEM_REPORT
        schema_class = "ProblemReportSchema"

    def __init__(self, *, problem_code: str = None, explain: str = None, **kwargs):
        """
        Initialize a ProblemReport message instance.

        Args:
            explain: The localized error explanation
            problem_code: The standard error identifier
        """
        super().__init__(**kwargs)
        self.explain = explain
        self.problem_code = problem_code


class ProblemReportSchema(AgentMessageSchema):
    """Schema for ProblemReport base class."""

    class Meta:
        """Metadata for problem report schema."""

        model_class = ProblemReport
        unknown = EXCLUDE

    explain = fields.Str(
        required=False,
        description="Localized error explanation",
        example=ProblemReportReason.REQUEST_NOT_ACCEPTED.value,
    )
    problem_code = fields.Str(
        data_key="problem-code",
        required=False,
        description="Standard error identifier",
        validate=validate.OneOf(
            choices=[prr.value for prr in ProblemReportReason],
            error="Value {input} must be one of {choices}.",
        ),
        example=ProblemReportReason.REQUEST_NOT_ACCEPTED.value,
    )
