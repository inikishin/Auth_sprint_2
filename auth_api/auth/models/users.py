import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from auth.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    last_login_at = Column(DateTime, nullable=True)
    current_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String, nullable=True)
    current_login_ip = Column(String, nullable=True)
    login_count = Column(Integer, nullable=True)

    login_history = relationship('UserLoginHistory', back_populates='user')
    refresh_token = relationship('RefreshToken', back_populates='user')
    roles = relationship('UserRole', back_populates='user')

    def __init__(self, password=None, **kwargs):
        super(User, self).__init__(**kwargs)

        if password is not None:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email} (id: {self.id})>'


class UserLoginHistory(Base):
    __tablename__ = 'user_login_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='login_history')
    user_agent = Column(String, nullable=True)
    login_ip = Column(String, nullable=True)
    login_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<UserLoginHistory: {self.id}>'


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), unique=True,
                     nullable=False)
    user = relationship('User', back_populates='refresh_token')
    token = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<RefreshToken: {self.token}>'


class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    users = relationship('UserRole', back_populates='role')

    def __repr__(self):
        return f'<Role {self.name} (id: {self.id})>'


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)
    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')
