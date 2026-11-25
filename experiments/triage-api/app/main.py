"""The web layer: turns HTTP requests into calls to the triage chain."""
import logging
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException

from app.schemas import TicketIn, TriageResult
from app.triage import build_chain

load_dotenv()
logger = logging.getLogger("triage")

app = FastAPI(title="Ticket Triage API")


@lru_cache
def get_chain():
    """Build the chain once and reuse it. Tests replace this with a fake."""
    return build_chain()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResult)
def triage_ticket(ticket: TicketIn, chain=Depends(get_chain)):
    try:
        return chain.invoke({"message": ticket.message})
    except Exception:
        logger.exception("Triage failed")  # full detail stays in the server log
        raise HTTPException(status_code=502, detail="Triage service unavailable, try again")
