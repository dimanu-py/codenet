"""
This  module is needed for alembic to detect correctly all models of the project.

When we import Base.metadata in the env.py file it will include all the models that inherit from it only if these models
have already been imported. To keep the env.py file clean, we import the Base.metadata in this file and then import all the
needed models.
"""

from src.shared.infra.persistence.sqlalchemy.base import Base
from src.social.user.infra.persistence.user_model import UserModel

base = Base

_ = UserModel
