# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User  # noqa
from app.models.media import Media  # noqa
from app.models.guardian_vault import GuardianVault  # noqa
from app.models.user_settings import UserSettings  # noqa
