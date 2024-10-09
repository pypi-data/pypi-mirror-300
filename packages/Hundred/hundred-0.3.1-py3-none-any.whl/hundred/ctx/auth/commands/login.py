from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.domain import Session, User
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher
from hundred.services.token import TokenService
from hundred.services.uuid import UUIDGenerator


class LoginCommand(Command):
    application_id: UUID
    identifier: str
    password: SecretStr

    @property
    def raw_password(self) -> str:
        return self.password.get_secret_value()


@command_handler(LoginCommand)
class LoginHandler:
    __slots__ = (
        "datetime_service",
        "hasher",
        "session_repository",
        "shared_logic",
        "token_service",
        "user_repository",
        "uuid_gen",
    )

    def __init__(
        self,
        datetime_service: DateTimeService,
        hasher: Hasher,
        session_repository: SessionRepository,
        shared_logic: AuthSharedLogic,
        token_service: TokenService,
        user_repository: UserRepository,
        uuid_gen: UUIDGenerator,
    ) -> None:
        self.datetime_service = datetime_service
        self.hasher = hasher
        self.session_repository = session_repository
        self.shared_logic = shared_logic
        self.token_service = token_service
        self.user_repository = user_repository
        self.uuid_gen = uuid_gen

    async def handle(self, command: LoginCommand) -> Authenticated:
        user = await self.user_repository.get_by_identifier(command.identifier)
        password = command.raw_password
        hashed_password = None

        if (
            user is None
            or not user.is_active
            or (hashed_password := user.raw_password) is None
            or not self.hasher.verify(password, hashed_password)
        ):
            raise Unauthorized(_("bad_credentials"))

        if self.hasher.needs_rehash(hashed_password):
            user.password = SecretStr(self.hasher.hash(password))
            user.bump_version()
            await self.user_repository.save(user)

        await self.shared_logic.logout(command.application_id)

        session_token = self.token_service.generate(256)
        session = self.new_session(command.application_id, session_token, user)
        await self.session_repository.save(session)

        access_token = self.shared_logic.new_access_token(session=session)
        return Authenticated(
            access_token=SecretStr(access_token),
            session_token=SecretStr(session_token),
            session_status=session.status,
        )

    def new_session(self, application_id: UUID, token: str, user: User) -> Session:
        now = self.datetime_service.utcnow()
        return Session(
            id=next(self.uuid_gen),
            application_id=application_id,
            created_at=now,
            last_seen=now,
            token=SecretStr(self.hasher.hash(token)),
            user=user,
        )
