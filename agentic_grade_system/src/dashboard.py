import streamlit as st
import pandas as pd
from pathlib import Path

from email_service import send_email

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Training Performance Dashboard",
    layout="wide"
)

st.title("🎓 Agentic AI Training Performance Dashboard")

# ==================================================
# LOAD DATA
# ==================================================

performance_file = "outputs/Master_Performance.xlsx"
student_file = "student_data/Master_Student_List.xlsx"

try:

    df = pd.read_excel(performance_file)

except Exception as e:

    st.error(f"Cannot load {performance_file}")
    st.stop()

try:

    student_df = pd.read_excel(student_file)

except Exception as e:

    st.error(f"Cannot load {student_file}")
    st.stop()

# ==================================================
# METRICS
# ==================================================

st.subheader("📊 Overall Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    len(df)
)

col2.metric(
    "Average Percentage",
    round(df["Percentage"].mean(), 2)
)

col3.metric(
    "Highest Percentage",
    round(df["Percentage"].max(), 2)
)

col4.metric(
    "Average Percentile",
    round(df["Percentile"].mean(), 2)
)

st.divider()

# ==================================================
# SEARCH STUDENT
# ==================================================

st.subheader("🔍 Search Student")

search_text = st.text_input(
    "Search by Student Name or Email"
)

filtered_students = student_df.copy()

if search_text:

    filtered_students = student_df[
        student_df.astype(str)
        .apply(
            lambda row: row.str.contains(
                search_text,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]

if len(filtered_students) == 0:

    st.warning(
        "No student found."
    )

else:

    st.dataframe(
        filtered_students,
        use_container_width=True
    )

    selected_student = st.selectbox(
        "Select Student",
        filtered_students["Name"].tolist()
    )

    student_info = filtered_students[
        filtered_students["Name"]
        == selected_student
    ].iloc[0]

    st.markdown("### Student Details")

    col1, col2 = st.columns(2)

    col1.write(
        f"**Name:** {student_info['Name']}"
    )

    col2.write(
        f"**Email:** {student_info['Email']}"
    )

    # ======================================
    # SEND INDIVIDUAL REPORT CARD
    # ======================================

    if st.button(
        "📨 Send Report Card",
        key="send_single"
    ):

        try:

            pdf_path = (
                Path("outputs")
                / "Grade_Cards"
                / f"{selected_student}.pdf"
            )

            if not pdf_path.exists():

                st.error(
                    f"PDF not found:\n{pdf_path}"
                )

            else:

                send_email(
                    student_info["Email"],
                    str(pdf_path)
                )

                st.success(
                    f"Report card sent to {student_info['Email']}"
                )

        except Exception as e:

            st.error(str(e))

st.divider()

# ==================================================
# SEND ALL REPORT CARDS
# ==================================================

st.subheader("📧 Bulk Email Report Cards")

if st.button("🚀 Send Report Cards To All Students"):

    total = len(student_df)

    progress = st.progress(0)

    success_count = 0
    fail_count = 0

    status_box = st.empty()

    for index, row in student_df.iterrows():

        try:

            name = row["Name"]
            email = row["Email"]

            pdf_path = (
                Path("outputs")
                / "grade_cards"
                / f"{name}.pdf"
            )

            if pdf_path.exists():

                send_email(
                    email,
                    str(pdf_path)
                )

                success_count += 1

            else:

                fail_count += 1

            progress.progress(
                (index + 1) / total
            )

            status_box.info(
                f"Sending {index+1}/{total}"
            )

        except Exception:

            fail_count += 1

    st.success(
        f"""
Completed

Success : {success_count}
Failed  : {fail_count}
"""
    )

st.divider()

# ==================================================
# TOP PERFORMERS
# ==================================================

st.subheader("🏆 Top 10 Performers")

st.dataframe(
    df.sort_values("Rank")
    .head(10),
    use_container_width=True
)

# ==================================================
# GRADE DISTRIBUTION
# ==================================================

st.subheader("📊 Grade Distribution")

st.bar_chart(
    df["Grade"]
    .value_counts()
)

# ==================================================
# PERFORMANCE CATEGORY
# ==================================================

if "Performance_Category" in df.columns:

    st.subheader(
        "📈 Performance Category Distribution"
    )

    st.bar_chart(
        df["Performance_Category"]
        .value_counts()
    )

# ==================================================
# PERCENTAGE DISTRIBUTION
# ==================================================

st.subheader(
    "📉 Percentage Distribution"
)

st.bar_chart(
    df["Percentage"]
)

# ==================================================
# RANK DISTRIBUTION
# ==================================================

st.subheader(
    "🏅 Rank Distribution"
)

rank_df = df.sort_values(
    "Rank"
)

st.line_chart(
    rank_df["Percentage"]
)

# ==================================================
# COMPLETE DATA
# ==================================================

st.subheader(
    "📋 Complete Student Performance Data"
)

st.dataframe(
    df,
    use_container_width=True
)

st.success(
    "Dashboard Loaded Successfully"
)