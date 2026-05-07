from calendar import calendar

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def calculate_remaining_time(target_date):
    today = date.today()
    years_diff = target_date.year - today.year
    months_diff = target_date.month - today.month
    days_diff = target_date.day - today.day

    # Handle negative day difference using actual days in previous month
    if days_diff < 0:
        months_diff -= 1

        previous_month = target_date.month - 1 or 12
        previous_year = target_date.year if target_date.month != 1 else target_date.year - 1

        days_in_previous_month = calendar.monthrange(
            previous_year,
            previous_month
        )[1]

        days_diff += days_in_previous_month

    total_months = (years_diff * 12) + months_diff

    return total_months, days_diff


@app.get("/", response_class=HTMLResponse)
def home(reques: Request):
    target_date = date(2026, 9, 26)
    today = date.today()

    is_today = (today == target_date)

    if is_today:
        months, days = 0, 0
    else:
        months, days = calculate_remaining_time(target_date)

    html_content = templates.get_template("countdown.html").render(
        months=months,
        days=days,
        is_today=is_today
    )
    return html_content