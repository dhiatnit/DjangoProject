from django.db import connection
from django.shortcuts import render
import json


def _fetch_all_dict(sql: str) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dashboard(request):
    kpi = _fetch_all_dict("SELECT * FROM dwh.v_kpi_summary;")[0]

    station_popularity = _fetch_all_dict("""
        SELECT * FROM dwh.v_station_popularity;
    """)

    monthly_revenue = _fetch_all_dict("""
        SELECT * FROM dwh.v_monthly_revenue_by_membership;
    """)

    user_behavior = _fetch_all_dict("""
        SELECT * FROM dwh.v_user_behavior;
    """)

    low_battery = _fetch_all_dict("""
        SELECT * FROM public.v_maintenance_alert_low_battery;
    """)

    usage_alert = _fetch_all_dict("""
        SELECT * FROM dwh.v_maintenance_alert_usage;
    """)

    payment_status = _fetch_all_dict("""
        SELECT * FROM dwh.v_payment_status_summary;
    """)

    rides_by_membership = _fetch_all_dict("""
        SELECT * FROM dwh.v_rides_by_membership;
    """)

    # Prepare chart data
    revenue_labels = sorted(
        list(
            {
                f"{row['month_name']} {row['year_num']}"
                for row in monthly_revenue
            }
        )
    )
    membership_types = sorted(
        list(
            {
                row["membership_type"]
                for row in monthly_revenue
            }
        )
    )

    revenue_datasets = []
    for membership in membership_types:
        data = []
        for label in revenue_labels:
            month_name, year_num = label.rsplit(" ", 1)
            match = next(
                (
                    row for row in monthly_revenue
                    if row["membership_type"] == membership
                       and row["month_name"] == month_name
                       and str(row["year_num"]) == year_num
                ),
                None
            )
            data.append(float(match["total_revenue"]) if match else 0)
        revenue_datasets.append({
            "label": membership,
            "data": data,
        })

    station_labels = [row["address"] for row in station_popularity]
    station_values = [row["total_starts"] for row in station_popularity]

    payment_status_labels = [row["status_name"] for row in payment_status]
    payment_status_values = [float(row["total_amount"]) for row in payment_status]

    membership_labels = [row["membership_type"] for row in rides_by_membership]
    membership_values = [row["total_rides"] for row in rides_by_membership]

    context = {
        "kpi": kpi,
        "user_behavior": user_behavior,
        "low_battery": low_battery,
        "usage_alert": usage_alert,
        "revenue_labels_json": json.dumps(revenue_labels),
        "revenue_datasets_json": json.dumps(revenue_datasets),
        "station_labels_json": json.dumps(station_labels),
        "station_values_json": json.dumps(station_values),
        "payment_status_labels_json": json.dumps(payment_status_labels),
        "payment_status_values_json": json.dumps(payment_status_values),
        "membership_labels_json": json.dumps(membership_labels),
        "membership_values_json": json.dumps(membership_values),
    }

    return render(request, "dashboard.html", context)


from django.shortcuts import render

# Create your views here.
