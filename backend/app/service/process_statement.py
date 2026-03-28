import pandas as pd

def process_file(file, person, months_option, data_option):
    df = pd.read_excel(file, header=[0, 1])
    df = df.fillna("")

    cleaned_cols = []
    base_cols = []
    month_cols = []

    base_names = ["Sr. No", "Name", "Location", "MonthlyBF Amt"]

    for col in df.columns:
        top, sub = col

        if "Unnamed" in str(top) and sub in base_names:
            cleaned_cols.append((sub, ""))
            base_cols.append((sub, ""))
        elif top in base_names:
            cleaned_cols.append((top, ""))
            base_cols.append((top, ""))
        else:
            cleaned_cols.append((top, sub))
            month_cols.append((top, sub))

    df.columns = pd.MultiIndex.from_tuples(cleaned_cols)

    months = []
    for col in month_cols:
        if col[0] not in months:
            months.append(col[0])

    name_col = [col for col in base_cols if col[0] == "Name"][0]
    person_df = df[df[name_col] == person]

    options_map = {
        "Current Month": 1,
        "Last 2 Months": 2,
        "Last 3 Months": 3,
        "Last 4 Months": 4,
        "Last 5 Months": 5,
        "All Months": len(months)
    }

    selected_months = months[:options_map.get(months_option, len(months))]

    data = []

    for m in selected_months:
        amt = ""
        receipt = ""

        for col in month_cols:
            if col[0] == m:
                if col[1] == "Amt":
                    if not person_df.empty and col in person_df.columns:
                        values = person_df[col].values
                        amt = values[0] if len(values) > 0 else ""
                elif col[1] == "Receipt No":
                    if not person_df.empty and col in person_df.columns:
                        values = person_df[col].values
                        receipt = values[0] if len(values) > 0 else ""

        if data_option == "Amt Only":
            data.append({"Month": str(m), "Amt": str(amt)})
        else:
            data.append({
                "Month": str(m),
                "Amt": str(amt),
                "Receipt No": str(receipt)
            })

    return data