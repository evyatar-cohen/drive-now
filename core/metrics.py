from prometheus_client import Gauge, Histogram

# define the 3 metrics required
active_cars = Gauge("drivenow_active_cars_total", "Number of available cars")
ongoing_rentals = Gauge("drivenow_ongoing_rentals_total", "Number of ongoing rentals")
request_duration = Histogram(
    "drivenow_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)