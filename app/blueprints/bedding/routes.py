import re
from datetime import datetime, timezone

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.models import Visitor
from app.services.issue_ids import generate_issue_id
from app.services.sms import send_issue_sms
from app.services.storage import (
    append_visitor,
    find_visitor_by_issue_or_mobile,
    get_next_issue_number,
    load_inventory,
    save_inventory,
    update_visitor,
)

bp = Blueprint("bedding", __name__, url_prefix="/bedding")

MOBILE_RE = re.compile(r"^[6-9]\d{9}$")


def get_inventory():
    return load_inventory()


def parse_positive_int(value, field_name, minimum=0, maximum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number.")
    if parsed < minimum:
        raise ValueError(f"{field_name} cannot be less than {minimum}.")
    if maximum is not None and parsed > maximum:
        raise ValueError(f"{field_name} cannot be more than {maximum}.")
    return parsed


@bp.route("/issue", methods=["GET", "POST"])
def issue():
    inventory = get_inventory()
    if request.method == "POST":
        form = request.form
        try:
            full_name = form.get("full_name", "").strip()
            mobile = form.get("mobile", "").strip()
            stay_days = parse_positive_int(form.get("stay_days"), "Expected stay days", minimum=1, maximum=365)
            gadda_qty = parse_positive_int(form.get("gadda_qty"), "Gadda quantity", minimum=0)
            rajai_qty = parse_positive_int(form.get("rajai_qty"), "Rajai quantity", minimum=0)
            deposit_amount = parse_positive_int(form.get("deposit_amount"), "Security deposit", minimum=0)

            if not full_name:
                raise ValueError("Full name is required.")
            if not MOBILE_RE.match(mobile):
                raise ValueError("Enter a valid 10-digit Indian mobile number.")
            if gadda_qty == 0 and rajai_qty == 0:
                raise ValueError("Select at least one bedding item.")
            if gadda_qty > inventory.available_gadda:
                raise ValueError("Not enough Gadda available.")
            if rajai_qty > inventory.available_rajai:
                raise ValueError("Not enough Rajai available.")

            next_number = get_next_issue_number()
            visitor = Visitor(
                issue_id=generate_issue_id(next_number),
                full_name=full_name,
                mobile=mobile,
                stay_days=stay_days,
                gadda_qty=gadda_qty,
                rajai_qty=rajai_qty,
                deposit_amount=deposit_amount,
                issue_datetime=datetime.now(timezone.utc),
                return_datetime=None,
                status="active",
            )
            append_visitor(visitor)
            inventory.available_gadda -= gadda_qty
            inventory.available_rajai -= rajai_qty
            save_inventory(inventory)

            sms_ok, sms_message = send_issue_sms(visitor)
            if sms_ok:
                flash(f"Bedding issued successfully. Issue ID: {visitor.issue_id}", "success")
            else:
                flash(f"Bedding issued, but SMS failed: {sms_message}", "warning")
            return redirect(url_for("bedding.issue_success", issue_id=visitor.issue_id))
        except ValueError as exc:
            flash(str(exc), "danger")
        except Exception:
            flash("Something went wrong while issuing bedding. Please try again.", "danger")

    suggested_deposit = inventory.deposit_per_item * 2
    return render_template("bedding/issue.html", inventory=inventory, suggested_deposit=suggested_deposit)


@bp.route("/issue/<issue_id>")
def issue_success(issue_id):
    visitor = find_visitor_by_issue_or_mobile(issue_id)
    if not visitor:
        abort(404)
    return render_template("bedding/issue_success.html", visitor=visitor)


@bp.route("/return", methods=["GET", "POST"])
def return_search():
    query = request.values.get("q", "").strip()
    visitor = None
    if query:
        visitor = find_visitor_by_issue_or_mobile(query, active_only=True)
        if not visitor:
            flash("No active issue found for that Issue ID or mobile number.", "warning")
    return render_template("bedding/return.html", query=query, visitor=visitor)


@bp.post("/return/<issue_id>")
def return_bedding(issue_id):
    visitor = find_visitor_by_issue_or_mobile(issue_id, active_only=True)
    if not visitor:
        abort(404)

    inventory = get_inventory()
    try:
        update_visitor(issue_id, status="returned", return_datetime=datetime.now(timezone.utc))
        inventory.available_gadda += visitor.gadda_qty
        inventory.available_rajai += visitor.rajai_qty
        save_inventory(inventory)
        flash(f"Return completed. Refund amount: ₹{visitor.deposit_amount}", "success")
    except Exception:
        flash("Could not complete return. Please try again.", "danger")
    return redirect(url_for("bedding.return_search", q=visitor.issue_id))
