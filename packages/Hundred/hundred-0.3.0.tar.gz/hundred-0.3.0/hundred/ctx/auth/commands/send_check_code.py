from datetime import timedelta
from uuid import UUID

from pydantic import SecretStr

from hundred import Command, command_handler
from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.domain import CheckCode
from hundred.ctx.auth.ports import SessionRepository, TwoFactorAuthenticator
from hundred.exceptions import NotModified, Unauthorized
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher
from hundred.services.uuid import UUIDGenerator


class SendCheckCodeCommand(Command):
    application_id: UUID
    claimant_id: UUID


@command_handler(SendCheckCodeCommand)
class SendCheckCodeHandler:
    __slots__ = (
        "datetime_service",
        "hasher",
        "provider",
        "session_repository",
        "shared_logic",
        "uuid_gen",
    )

    def __init__(
        self,
        datetime_service: DateTimeService,
        hasher: Hasher,
        provider: TwoFactorAuthenticator,
        session_repository: SessionRepository,
        shared_logic: AuthSharedLogic,
        uuid_gen: UUIDGenerator,
    ) -> None:
        self.datetime_service = datetime_service
        self.hasher = hasher
        self.provider = provider
        self.session_repository = session_repository
        self.shared_logic = shared_logic
        self.uuid_gen = uuid_gen

    async def handle(self, command: SendCheckCodeCommand) -> None:
        session = await self.shared_logic.check_session(
            command.application_id,
            command.claimant_id,
        )

        if not session.user.is_active:
            raise Unauthorized()

        if session.is_verified:
            raise NotModified(session.readable)

        code = await self.provider.send_code(session.user.id)

        if not code:
            return

        session.check_code = self.new_check_code(code)
        session.bump_version()
        await self.session_repository.save(session)

    def new_check_code(
        self,
        code: str,
        lifespan: timedelta = timedelta(minutes=5),
    ) -> CheckCode:
        expiration = self.datetime_service.utcnow() + lifespan
        return CheckCode(
            id=next(self.uuid_gen),
            value=SecretStr(self.hasher.hash(code)),
            expiration=expiration,
        )
