import logging

import requests
from flask import current_app

logger = logging.getLogger(__name__)


def build_issue_sms(visitor):
    return (
        "🙏 Shantikunj Haridwar\n\n"
        f"Issue ID: {visitor.issue_id}\n\n"
        f"Gadda: {visitor.gadda_qty}\n"
        f"Rajai: {visitor.rajai_qty}\n\n"
        f"Security Deposit: ₹{visitor.deposit_amount}\n\n"
        "Please show this message while returning bedding."
    )


def send_issue_sms(visitor):
    """Send issue confirmation SMS. Returns (success, message)."""
    if not current_app.config["SMS_ENABLED"]:
        logger.info("SMS disabled. Would send to %s: %s", visitor.mobile, build_issue_sms(visitor))
        return True, "SMS disabled in local config"

    api_key = current_app.config["FAST2SMS_API_KEY"]
    if not api_key:
        return False, "FAST2SMS_API_KEY is missing"

    payload = {
        "authorization": api_key,
        "route": "q",
        "message": build_issue_sms(visitor),
        "language": "unicode",
        "numbers": visitor.mobile,
    }

    try:
        response = requests.post("https://www.fast2sms.com/dev/bulkV2", data=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("SMS sending failed")
        return False, str(exc)

    return True, "SMS sent"
