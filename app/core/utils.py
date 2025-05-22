from fastapi import HTTPException


def validate_year(year: int, start_year: int, end_year: int):
    if year < start_year or year > end_year:
        raise HTTPException(
            status_code=400,
            detail=(
                (
                    f"Year out of range. Available range: {start_year} to "
                    f"{end_year}"
                )
            )
        )
