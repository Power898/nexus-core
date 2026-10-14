from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Абстрактний базовий клас для транспортних адаптерів (Messenger Agnostic)."""

    @abstractmethod
    async def start(self) -> None:
        """Запуск транспортного адаптера (прослуховування/ініціалізація)."""

    @abstractmethod
    async def stop(self) -> None:
        """Коректна зупинка адаптера."""

    @abstractmethod
    async def send_message(
        self, recipient_id: int | str, text: str, **kwargs: Any
    ) -> None:
        """Надсилання повідомлення отримувачу."""
