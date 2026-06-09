from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import Inventory
from app.services.storage import active_issued_counts, load_inventory, save_inventory

bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@bp.route("/", methods=["GET", "POST"])
def settings():
    inventory = load_inventory()
    issued_gadda, issued_rajai = active_issued_counts()
    if request.method == "POST":
        try:
            total_gadda = int(request.form.get("total_gadda", 0))
            total_rajai = int(request.form.get("total_rajai", 0))
            deposit_per_item = int(request.form.get("deposit_per_item", 0))
            if total_gadda < issued_gadda:
                raise ValueError(f"Total Gadda cannot be less than currently issued ({issued_gadda}).")
            if total_rajai < issued_rajai:
                raise ValueError(f"Total Rajai cannot be less than currently issued ({issued_rajai}).")
            if deposit_per_item < 0:
                raise ValueError("Deposit per item cannot be negative.")

            inventory.total_gadda = total_gadda
            inventory.available_gadda = total_gadda - issued_gadda
            inventory.total_rajai = total_rajai
            inventory.available_rajai = total_rajai - issued_rajai
            inventory.deposit_per_item = deposit_per_item
            save_inventory(inventory)
            flash("Inventory settings saved.", "success")
            return redirect(url_for("inventory.settings"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template("inventory/settings.html", inventory=inventory, issued_gadda=issued_gadda, issued_rajai=issued_rajai)
