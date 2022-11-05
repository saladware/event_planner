"""
    User auth application. Should not have any dependencies on other applications!!!
"""


from .routes import user_router
from .auth import get_current_user
from .models import User
