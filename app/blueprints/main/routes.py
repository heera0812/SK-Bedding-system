from flask import Blueprint, render_template

from app.services.storage import all_visitors_sorted, load_inventory

bp = Blueprint("main", __name__)


@bp.route("/")
def dashboard():
    inventory = load_inventory()
    visitors = all_visitors_sorted()
    active_visitors = sum(1 for visitor in visitors if visitor.status == "active")
    gadda_issued = sum(visitor.gadda_qty for visitor in visitors if visitor.status == "active")
    rajai_issued = sum(visitor.rajai_qty for visitor in visitors if visitor.status == "active")
    deposits_held = sum(visitor.deposit_amount for visitor in visitors if visitor.status == "active")
    recent_visitors = visitors[:8]

    metrics = {
        "active_visitors": active_visitors,
        "gadda_issued": gadda_issued,
        "rajai_issued": rajai_issued,
        "deposits_held": deposits_held,
        "available_gadda": inventory.available_gadda,
        "available_rajai": inventory.available_rajai,
    }
    return render_template("dashboard.html", metrics=metrics, inventory=inventory, recent_visitors=recent_visitors)
