# Username of the destination group
# Supported formats:
# username
# @username
# t.me/username
# https://telegram.dog/username
GROUP_DESTINATION = "bullybuy_it"

# Target groups: specify the groups from which to retrieve members
GROUP_TARGETS = [
    "eFOOTBALL_Italia",
    "TavernaLoLGroup",
]

# Telegram API credentials (optional if sessions are already active)
API_ID = "611335"
API_HASH = "d524b414d21f4d37f08684c1df41ac9c"

# Operation modes
#
# By default, at every execution, members from the destination group will be extracted to avoid re-adding them.
# Additionally, members added in previous executions are saved to prevent re-adding them, and members extracted from target groups are stored
# to reduce the number of operations in future executions.
#
# If True, members to be added will be retrieved on-demand from the target groups.
FRESH_MODE = True
#
# If True, filter the members to be added
FILTER_MODE = True
#
# Specify the maximum inactivity time for a member in seconds 
MEMBER_MAXIMUM_INACTIVITY_SECONDS = 2592000  # 30 * 24 * 60 * 60 (30 days)

# Limits to avoid a Flood Wait error (Recommended)
#
# Number of invites sent by a single account during execution
INVITATIONS_PER_ACCOUNT = 35
#
# Time in seconds after which a worker can be reused
ACCOUNT_REUSE_DELAY_SECONDS = 172800  # 48 hours
#
# Maximum daily invitations that can be sent to a specific group
MAX_DAILY_INVITATIONS_PER_DESTINATION_GROUP = 70
#
# Pause interval between executions in seconds
MIN_EXECUTION_PAUSE_SECONDS = 1600
MAX_EXECUTION_PAUSE_SECONDS = 1800
#
# Pause interval between invites in seconds
MIN_INVITATION_PAUSE_SECONDS = 180
MAX_INVITATION_PAUSE_SECONDS = 240
# 
# Number of days of pause after receiving a peer flood error
PEER_FLOOD_ERROR_PAUSE_DAYS = 7

# Datetime format
# Set the format for displaying date and time
# Examples:
# '%Y-%m-%d %H:%M:%S' -> '2023-09-20 15:30:45'
# '%d/%m/%Y %I:%M %p' -> '20/09/2023 03:30 PM'
DATETIME_FORMAT = '%d-%m-%Y_%H-%M-%S'
#
# Date format
DATE_FORMAT = '%d-%m-%Y'
#
# Timezone settings
# List of valid timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONE_NAME = 'Europe/Rome'
import pytz
TZ_INFO = pytz.timezone(TIMEZONE_NAME)

# Folder and file name
ACCOUNTS_FOLDER_NAME = "accounts"
ACCOUNT_FILE_NAME = "{}.json"
SESSIONS_FOLDER_NAME = "sessions"
SESSION_FILE_NAME = "{}"
GROUPS_FOLDER_NAME = "groups"
GROUP_FILE_NAME = "{}.json"
LOGS_FOLDER_NAME = "logs"
LOG_FILE_NAME = "{}.log"

import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FOLDER_PATH = os.path.join(DIR_PATH, ACCOUNTS_FOLDER_NAME)
ACCOUNT_FILE_PATH = os.path.join(ACCOUNTS_FOLDER_PATH, ACCOUNT_FILE_NAME)
SESSIONS_FOLDER_PATH = os.path.join(DIR_PATH, SESSIONS_FOLDER_NAME)
SESSION_FILE_PATH = os.path.join(SESSIONS_FOLDER_PATH, SESSION_FILE_NAME)
GROUPS_FOLDER_PATH = os.path.join(DIR_PATH, GROUPS_FOLDER_NAME)
GROUP_FILE_PATH = os.path.join(GROUPS_FOLDER_PATH, GROUP_FILE_NAME)
LOGS_FOLDER_PATH = os.path.join(DIR_PATH, LOGS_FOLDER_NAME)
LOG_FILE_PATH = os.path.join(LOGS_FOLDER_PATH, LOG_FILE_NAME)
