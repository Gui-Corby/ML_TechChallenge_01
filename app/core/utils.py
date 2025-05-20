import csv
from typing import List, Dict

def load_from_csv(
    csv_path: str,
    year: int,
    columns: List[str],
) -> List[Dict[str, str]]:
    year_str = str(year)
    result = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        fixed_col_indices = {col: i for i, col in enumerate(header) if col in columns}

        year_indices = [i for i, col in enumerate(header) if col == year_str]

        if not year_indices:
            return []

        for row in reader:
            if all(not row[i].strip() for i in year_indices):
                continue

            item = {}

            for col, i in fixed_col_indices.items():
                item[col] = row[i].strip()

            for idx, i in enumerate(year_indices):
                col_name = year_str if len(year_indices) == 1 else f"{year_str}_{idx+1}"
                item[col_name] = row[i].strip()

            result.append(item)

    return result