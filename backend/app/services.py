from collections import defaultdict
from collections.abc import Iterable
from datetime import date
from decimal import Decimal


def month_bounds(year: int, month: int) -> tuple[date, date]:
    """Return [first day of month, first day of next month)."""
    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return start, end


def totals_by_category(rows: Iterable[tuple[str, Decimal]]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for name, amount in rows:
        totals[name] += amount
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
