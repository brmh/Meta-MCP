META_ERROR_CODES = {
    1:   "Unknown error. Please retry.",
    2:   "Service temporarily unavailable.",
    4:   "App request limit reached. Backing off.",
    10:  "Permission denied. Verify app permissions.",
    17:  "User request limit reached. Slowing down.",
    32:  "Page-level throttling. Wait before retrying.",
    100: "Invalid parameter. Check input values.",
    102: "Session key invalid. Re-authenticate.",
    190: "Access token expired or invalid. Refresh token.",
    200: "Missing permission for this action.",
    275: "Cannot create ad — account in restricted mode.",
    368: "Account temporarily blocked due to policy.",
    506: "Duplicate post detected.",
    1487: "Creative already in use. Cannot delete.",
    2635: "Ad account not associated with this business.",
}

def get_error_message(error_code: int, default_message: str = "An unknown error occurred with the Meta API.") -> str:
    """Returns a human-readable error message for a given Meta API error code."""
    return META_ERROR_CODES.get(error_code, default_message)

class MetaAPIError(Exception):
    def __init__(self, message: str, error_code: int = None, error_subcode: int = None, fbtrace_id: str = None):
        super().__init__(message)
        self.error_code = error_code
        self.error_subcode = error_subcode
        self.fbtrace_id = fbtrace_id
        
    def __str__(self):
        base_msg = super().__str__()
        extras = []
        if self.error_code:
            extras.append(f"Code: {self.error_code}")
        if self.error_subcode:
            extras.append(f"Subcode: {self.error_subcode}")
        if self.fbtrace_id:
            extras.append(f"Trace ID: {self.fbtrace_id}")
            
        if extras:
            return f"{base_msg} ({', '.join(extras)})"
        return base_msg
