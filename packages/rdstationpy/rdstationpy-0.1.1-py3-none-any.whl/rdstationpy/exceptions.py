class RDStationException(Exception):
    def __init__(self, http_code, error):
        self.http_code = http_code
        self.error = error

    def __str__(self):
        return f"HTTP Code: {self.http_code} - Error:{self.error}"
