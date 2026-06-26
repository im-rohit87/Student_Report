from crewai import Task

from agents import (
    file_agent,
    data_agent,
    analysis_agent,
    feedback_agent,
    email_agent
)

detect_task = Task(
    description="""
    Detect newly uploaded quiz files in the quizzes folder.
    Verify that files are valid CSV files.
    """,
    expected_output="List of valid quiz files detected.",
    agent=file_agent
)

process_task = Task(
    description="""
    Merge all quiz files using student email IDs.
    Remove duplicates and missing records.
    """,
    expected_output="Merged student performance dataset.",
    agent=data_agent
)

analysis_task = Task(
    description="""
    Calculate:
    - Percentage
    - Percentile
    - Rank
    - Grade
    """,
    expected_output="""
    Student-wise performance metrics including
    percentage, percentile, rank and grade.
    """,
    agent=analysis_agent
)

feedback_task = Task(
    description="""
    Generate personalized feedback
    for each student
    """,
    expected_output="""
    Personalized improvement suggestions
    for every student.
    """,
    agent=feedback_agent
)

email_task = Task(
    description="""
    Email grade cards
    to all students
    """,
     expected_output="""
    Email delivery confirmation report.
    """,
    agent=email_agent
)