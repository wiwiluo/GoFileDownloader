"""Centralized configuration module for managing constants used across the project.

These configurations aim to improve modularity and readability by consolidating settings
into a single location.
"""

# ============================
# Paths and Files
# ============================
DOWNLOAD_FOLDER = "Downloads"    # The folder where downloaded files will be stored.
URLS_FILE = "URLs.txt"           # The file containing the list of URLs to process.
SESSION_LOG = "session_log.txt"  # The file used to log session errors.

# ============================
# API Endpoints
# ============================
GOFILE_API = "https://api.gofile.io"            # The base URL for the GoFile API.
GOFILE_API_ACCOUNTS = f"{GOFILE_API}/accounts"  # The endpoint for GoFile account
                                                # related operations.

# ============================
# Command Usage Instructions
# ============================
DEFAULT_USAGE = "python3 downloader.py <album_url>"
PASSWORD_USAGE = "python3 downloader.py <album_url> <password>"  # noqa: S105

# ============================
# Download Settings
# ============================
MAX_WORKERS = 3  # The maximum number of threads for concurrent downloads.

# Constants for file sizes, expressed in bytes.
KB = 1024
MB = 1024 * KB

# Thresholds for file sizes and corresponding chunk sizes used during download.
THRESHOLDS = [
    (1 * MB, 8 * KB),      # Less than 1 MB
    (10 * MB, 16 * KB),    # 1 MB to 10 MB
    (50 * MB, 64 * KB),    # 10 MB to 50 MB
    (100 * MB, 128 * KB),  # 50 MB to 100 MB
    (250 * MB, 256 * KB),  # 100 MB to 250 MB
]

# Default chunk size for files larger than the largest threshold.
LARGE_FILE_CHUNK_SIZE = 512 * KB

# ============================
# HTTP / Network
# ============================
# HTTP status codes
HTTP_STATUS_OK = 200

# Base headers common for all requests
BASE_HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}
