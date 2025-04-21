import copy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.x509 import Certificate, load_pem_x509_certificate
from jwt.exceptions import DecodeError

from app.config import settings


class JWTManager:
    def __init__(
        self,
        private_key_path: Path | str,
        public_key_path: Path | str,
        expiration_minutes: float,
        algorithm: str = "RS256",
    ):
        self.expiration_minutes = expiration_minutes
        self.private_key = self._load_private_key(self._read_pem_file(private_key_path))
        self.public_cert = self._load_public_certificate(
            self._read_pem_file(public_key_path)
        )
        self.algorithm = algorithm

    def _read_pem_file(
        self,
        file_path: Path | str,
    ) -> bytes:
        return Path(file_path).read_bytes()

    def _load_private_key(
        self, pem_data: bytes, password: bytes | None = None
    ) -> PrivateKeyTypes:
        return serialization.load_pem_private_key(
            pem_data, password=password, backend=default_backend()
        )

    def _load_public_certificate(self, pem_data: bytes) -> Certificate:
        return load_pem_x509_certificate(pem_data, backend=default_backend())

    def create_jwt(self, payload: dict[str, Any]) -> str:
        payload_ = copy.deepcopy(payload)
        payload_.update(
            {
                "iat": datetime.now(tz=timezone.utc).timestamp(),
                "exp": (
                    datetime.now(tz=timezone.utc)
                    + timedelta(minutes=self.expiration_minutes)
                ).timestamp(),
            }
        )
        token = jwt.encode(
            payload_,
            self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ),
            algorithm=self.algorithm,
        )
        return token

    def verify_jwt(self, token: str) -> dict[str, Any] | None:
        public_key = self.public_cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        try:
            decoded = jwt.decode(token, public_key, algorithms=[self.algorithm])  # type: ignore
            return decoded
        except DecodeError:
            return None

    def check_jwt(self, token: str) -> bool:
        payload = self.verify_jwt(token)
        if payload is None:
            return False

        current_time = datetime.now(tz=timezone.utc)
        expiration_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        if current_time > expiration_time:
            return False

        return True


access_jwt_manager = JWTManager(
    private_key_path=settings.jwt.ACCESS_PRIVATE_KEY_PATH,
    public_key_path=settings.jwt.ACCESS_PUBLIC_KEY_PATH,
    expiration_minutes=settings.jwt.ACCESS_LIFE_TIME_MINUTES,
)

refresh_jwt_manager = JWTManager(
    private_key_path=settings.jwt.REFRESH_PRIVATE_KEY_PATH,
    public_key_path=settings.jwt.REFRESH_PUBLIC_KEY_PATH,
    expiration_minutes=settings.jwt.REFRESH_LIFE_TIME_MINUTES,
)
