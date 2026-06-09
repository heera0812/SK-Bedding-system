from datetime import date
from io import BytesIO

from flask import Blueprint, Response, render_template, send_file
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph

from app.services.storage import all_visitors_sorted, visitor_summary

bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.route("/")
def index():
    summary = visitor_summary()
    return render_template(
        "reports/index.html",
        total=summary["total"],
        active=summary["active"],
        returned=summary["returned"],
    )


@bp.route("/excel")
def export_excel():
    visitors = all_visitors_sorted()
    wb = Workbook()
    ws = wb.active
    ws.title = "Bedding Register"
    ws.append(["Issue ID", "Name", "Mobile", "Gadda", "Rajai", "Deposit", "Issue Date", "Return Date", "Status"])
    for visitor in visitors:
        ws.append([
            visitor.issue_id,
            visitor.full_name,
            visitor.mobile,
            visitor.gadda_qty,
            visitor.rajai_qty,
            visitor.deposit_amount,
            visitor.issue_datetime.strftime("%d-%b-%Y %H:%M") if visitor.issue_datetime else "",
            visitor.return_datetime.strftime("%d-%b-%Y %H:%M") if visitor.return_datetime else "",
            visitor.status,
        ])
    for column in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = min(max_length + 2, 28)

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="shantikunj_bedding_register.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@bp.route("/pdf")
def export_pdf():
    summary = visitor_summary()
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Shantikunj Haridwar - Daily Bedding Summary", styles["Title"]),
        Paragraph(date.today().strftime("%d-%b-%Y"), styles["Normal"]),
        Spacer(1, 16),
    ]
    table = Table([
        ["Metric", "Value"],
        ["Total Visitors", summary["total"]],
        ["Total Gadda Issued", summary["total_gadda"]],
        ["Total Rajai Issued", summary["total_rajai"]],
        ["Deposits Collected", f"Rs. {summary['total_deposit']}"],
        ["Active Issues", summary["active"]],
        ["Returned Issues", summary["returned"]],
    ], colWidths=[250, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F28C18")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#EBDAB8")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFDF8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    doc.build(story)
    output.seek(0)
    return Response(output.read(), mimetype="application/pdf", headers={"Content-Disposition": "attachment; filename=shantikunj_daily_summary.pdf"})
