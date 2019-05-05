from xblock.core import XBlock
from xblock.fields import String, Scope


class ToyXblockWithFieldsOnly(XBlock):
    user_relative = String(default="for some user", scope=Scope.user_state, help="State of the user")
    settings_relative = String(default="this is setting", scope=Scope.content, help="This is content")
    all_user_relative = String(default="all user info", scope=Scope.user_state_summary, help="State of all users")
