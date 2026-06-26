import pandas as pd
from pathlib import Path


def load_quiz_files(folder):

    files = sorted(Path(folder).glob("*.csv"))

    print("\n=== FILES FOUND ===")
    for f in files:
        print(f)
    print("===================\n")

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in folder: {folder}"
        )

    master = None

    for i, file in enumerate(files, start=1):

        print(f"\nProcessing: {file.name}")

        df = pd.read_csv(file)

        print("\nFILE",file.name)
        print("COLUMNS:")
        for c in df.columns:
            print(repr(c))

        # Clean column names
        df.columns = df.columns.str.strip()

        print("Columns found:")
        print(df.columns.tolist())

        email_col = next(
            (c for c in df.columns if "email" in c.lower()),
            None
        )

        name_col = next(
            (c for c in df.columns if "name" in c.lower()),
            None
        )

        if email_col is None:
            raise ValueError(
                f"Email column not found in {file.name}"
            )

        if name_col is None:
            raise ValueError(
                f"Name column not found in {file.name}"
            )

        score_columns = [
            c for c in df.columns
            if "score" in c.lower()
        ]

        if not score_columns:
            raise ValueError(
                f"No score column found in {file.name}"
            )

        # Prefer exact "Total score"
        score_col = next(
            (
                c for c in df.columns
                if c.strip().lower() == "total score"
            ),
            score_columns[0]
        )

        print(f"Score column selected: {score_col}")
        print(df[[score_col]].head())

        temp = df[
            [email_col, name_col, score_col]
        ].copy()

        temp.columns = [
            "Email",
            "Name",
            f"Quiz_{i}"
        ]

        temp[f"Quiz_{i}"] = (
            temp[f"Quiz_{i}"]
            .astype(str)
            .str.split("/")
            .str[0]
            .str.strip()
        )

        temp[f"Quiz_{i}"] = pd.to_numeric(
            temp[f"Quiz_{i}"],
            errors="coerce"
        ).fillna(0)
        

        print("\nTEMP DATA:")
        print(temp.head())
        print(temp[f"Quiz_{i}"].sum())

        if master is None:

            master = temp

        else:

            master = master.merge(
                temp,
                on="Email",
                how="outer",
                suffixes=("", "_new")
            )

            if "Name_new" in master.columns:
                master["Name"] = master["Name"].fillna(
                    master["Name_new"]
                )

                master.drop(
                    columns=["Name_new"],
                    inplace=True
                )

    quiz_cols = [
        c for c in master.columns
        if c.startswith("Quiz_")
    ]

    master[quiz_cols] = master[
        quiz_cols
    ].fillna(0)

    master.drop_duplicates(
        subset=["Email"],
        inplace=True
    )

    master.reset_index(
        drop=True,
        inplace=True
    )

    print(
        f"\nSuccessfully merged {len(files)} quiz files."
    )

    print("\n===== MASTER DATA =====")
    print(master.head(10))

    print("\n===== QUIZ COLUMN TOTALS =====")
    print(master[quiz_cols].sum())

    print("\n===== QUIZ COLUMN STATS =====")
    print(master[quiz_cols].describe())

    return master