
from pathlib import Path
from crewai import Crew

from agents import (
    file_agent,
    data_agent,
    analysis_agent,
    feedback_agent,
    email_agent
)

from tasks import (
    detect_task,
    process_task,
    analysis_task,
    feedback_task,
    email_task
)

from data_processor import load_quiz_files
from grade_engine import calculate_performance
from pdf_generator import create_grade_card
from config import QUIZ_FOLDER, OUTPUT_FOLDER


def run_agents():
    """
    Runs CrewAI agents for workflow orchestration.
    """

    crew = Crew(
        agents=[
            file_agent,
            data_agent,
            analysis_agent,
            feedback_agent,
            email_agent
        ],
        tasks=[
            detect_task,
            process_task,
            analysis_task,
            feedback_task,
            email_task
        ],
        verbose=True
    )

    crew.kickoff()


def process_data():
    """
    Main processing pipeline.
    """

    print("Loading quiz files...")

    df = load_quiz_files(QUIZ_FOLDER)

    print("Calculating performance metrics...")

    df = calculate_performance(df)

    # Create output folders
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

    gradecard_folder = Path(OUTPUT_FOLDER) / "Grade_Cards"
    gradecard_folder.mkdir(exist_ok=True)

    # ==========================================
    # MASTER REPORT
    # ==========================================

    master_file = Path(OUTPUT_FOLDER) / "Master_Performance.xlsx"

    df.to_excel(
        master_file,
        index=False
    )

    print(
        f"Master report saved: {master_file}"
    )

    # ==========================================
    # RANKING REPORT
    # ==========================================

    ranking_file = Path(OUTPUT_FOLDER) / "Final_Rankings.xlsx"

    df.sort_values(
        by="Rank"
    ).to_excel(
        ranking_file,
        index=False
    )

    print(
        f"Ranking report saved: {ranking_file}"
    )

    # ==========================================
    # GRADE CARDS
    # ==========================================

    print(
        "\nGenerating grade cards..."
    )

    for _, student in df.iterrows():

        # Student Name

        student_name = str(
            student["Name"]
        ).strip()

        # Remove invalid filename characters

        invalid_chars = '<>:"/\\|?*'

        for ch in invalid_chars:
            student_name = student_name.replace(
                ch,
                "_"
            )

        # Avoid empty names

        if not student_name:
            student_name = "Unknown_Student"

        pdf_path = (
            gradecard_folder /
            f"{student_name}.pdf"
        )

        create_grade_card(
            student,
            str(pdf_path)
        )

        print(
            f"Generated: {student_name}.pdf"
        )

    print(
        "\nAll grade cards generated successfully."
    )

    return df


def main():

    #print("========== AGENTIC AI GRADE SYSTEM ==========")

    # Agent workflow
    #run_agents()

    # Actual processing
    process_data()

    #print("========== PROCESS COMPLETED ==========")


if __name__ == "__main__":
    main()

