
import pandas as pd


def assign_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def performance_category(percentage):

    if percentage >= 80:
        return "Excellent"
    elif percentage >= 60:
        return "Good"
    elif percentage >= 40:
        return "Average"
    else:
        return "Needs Improvement"


def calculate_performance(df):

    quiz_cols = [
        col for col in df.columns
        if col.startswith("Quiz_")
    ]

    if not quiz_cols:
        raise ValueError(
            "No quiz columns found."
        )

    # Fill missing scores
    df[quiz_cols] = df[quiz_cols].fillna(0)

    # Convert to numeric
    for col in quiz_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    # Total Score
    df["Total"] = df[quiz_cols].sum(axis=1)

    # Assuming each quiz is out of 15 marks
    max_marks = len(quiz_cols) * 15

    df["Percentage"] = round(
        (df["Total"] / max_marks) * 100,
        2
    )

    # Percentile
    df["Percentile"] = round(
        df["Percentage"].rank(
            pct=True
        ) * 100,
        2
    )

    # Rank
    df["Rank"] = (
        df["Percentage"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )

    # Grade
    df["Grade"] = df["Percentage"].apply(
        assign_grade
    )

    # Performance Category
    df["Performance_Category"] = (
        df["Percentage"]
        .apply(performance_category)
    )

    # Sort by Rank
    df = (
        df.sort_values(
            by="Rank"
        )
        .reset_index(drop=True)
    )

    return df

