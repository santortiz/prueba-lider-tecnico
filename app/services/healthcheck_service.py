def check_api() -> bool:
    try:
        return "Service is running"
    except Exception:
        return "Service is down"