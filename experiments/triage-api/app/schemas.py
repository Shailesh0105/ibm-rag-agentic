"""Data shapes for the API: what comes in and what goes out."""
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["billing", "technical", "account", "other"]
Urgency = Literal["low", "medium", "high"]


class TicketIn(BaseModel):
    """What the caller sends to POST /triage."""
    message: str = Field(min_length=1, max_length=2000)


class TriageResult(BaseModel):
    """What the model must return, and what the API sends back."""
    category: Category = Field(description="The one category that best fits the ticket")
    urgency: Urgency = Field(description="How urgent the ticket is")
    summary: str = Field(description="One sentence summarising the customer's problem")
    reply_draft: str = Field(description="A short, friendly first reply to the customer")
