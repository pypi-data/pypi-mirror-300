DEFAULT_CONFIG = {
    "connection": {
        "use_ssl": True,
        "verify_ssl_certs": True,
        "use_proxy": False,
        "timeout_secs": 5,
        "max_retries": None,
    },
    "max_attempts": None,
    "default_retry_codes": (429, 500),
}


def get_default_config() -> dict:
    return DEFAULT_CONFIG
