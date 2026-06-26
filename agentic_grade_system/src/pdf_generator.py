from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from pathlib import Path

import qrcode
import uuid
import os
from datetime import datetime


def create_grade_card(student, output_file):

    doc = SimpleDocTemplate(
        output_file,
        topMargin=20,
        bottomMargin=20,
        leftMargin=30,
        rightMargin=30
    )

    styles = getSampleStyleSheet()

    styles["Title"].alignment = TA_CENTER
    styles["Heading2"].alignment = TA_CENTER

    content = []

    # ==================================
    # PROJECT ROOT
    # ==================================

    BASE_DIR = Path(__file__).resolve().parent.parent

    logo_path = BASE_DIR / "assets" / "logo.png"
    sign_path = BASE_DIR / "assets" / "sign.png"
    stamp_path = BASE_DIR / "assets" / "stamp.png"

    print("\n===== ASSET CHECK =====")
    print("Logo Exists :", logo_path.exists())
    print("Sign Exists :", sign_path.exists())
    print("Stamp Exists:", stamp_path.exists())
    print("=======================\n")

    # ==================================
    # LOGO
    # ==================================

    try:
        if logo_path.exists():

            logo = Image(
                str(logo_path),
                width=60,
                height=60
            )

            logo.hAlign = "CENTER"

            content.append(logo)

    except Exception as e:
        print("Logo Error:", e)

    content.append(
        Paragraph(
            "LLOYD INSTITUTE OF ENGINEERING & TECHNOLOGY",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Training Performance Grade Card",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 8)
    )

    # ==================================
    # VERIFICATION
    # ==================================

    verification_id = str(uuid.uuid4())[:12]

    content.append(
        Paragraph(
            f"<b>Verification ID:</b> {verification_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Issue Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 5)
    )

    # ==================================
    # STUDENT DETAILS
    # ==================================

    fields = [
        "Name",
        "Email",
        "Total",
        "Percentage",
        "Percentile",
        "Rank",
        "Grade",
        "Performance_Category"
    ]

    for field in fields:

        if field in student:

            content.append(
                Paragraph(
                    f"<b>{field}</b>: {student[field]}",
                    styles["Normal"]
                )
            )

            content.append(
                Spacer(1, 4)
            )

    content.append(
        Spacer(1, 5)
    )

    # ==================================
    # QR CODE
    # ==================================

    qr_text = (
        f"Student Name: {student.get('Name', '')}\n"
        f"Email: {student.get('Email', '')}\n"
        f"Verification ID: {verification_id}\n"
        f"Grade: {student.get('Grade', '')}\n"
        f"Rank: {student.get('Rank', '')}"
    )

    qr = qrcode.make(qr_text)

    qr_file = "temp_qr.png"

    qr.save(qr_file)

    content.append(
        Paragraph(
            "Student Verification QR Code",
            styles["Heading3"]
        )
    )

    qr_img = Image(
        qr_file,
        width=80,
        height=80
    )

    qr_img.hAlign = "CENTER"

    content.append(qr_img)

    content.append(
        Spacer(1, 8)
    )

    # ==================================
    # SIGNATURE
    # ==================================

    try:
        if sign_path.exists():

            sign = Image(
                str(sign_path),
                width=90,
                height=35
            )

            sign.hAlign = "LEFT"

            content.append(sign)

            content.append(
                Paragraph(
                    "<b>Authorized Signatory</b>",
                    styles["Normal"]
                )
            )

    except Exception as e:
        print("Signature Error:", e)

    content.append(
        Spacer(1, 3)
    )

    # ==================================
    # STAMP
    # ==================================

    try:
        if stamp_path.exists():

            stamp = Image(
                str(stamp_path),
                width=70,
                height=70
            )

            stamp.hAlign = "RIGHT"

            content.append(stamp)

    except Exception as e:
        print("Stamp Error:", e)

    content.append(
        Spacer(1, 8)
    )

    content.append(
        Paragraph(
            "This is a system generated grade card and can be verified using the QR Code and Verification ID.",
            styles["Normal"]
        )
    )

    # ==================================
    # BUILD PDF
    # ==================================

    doc.build(content)

    if os.path.exists(qr_file):
        os.remove(qr_file)

    print(
        f"Grade card generated successfully: {output_file}"
    )