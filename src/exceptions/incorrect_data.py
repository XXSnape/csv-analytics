class IncorrectDataException(Exception):
    """Исключение для обработки некорректных данных."""

    def __init__(self, message: str) -> None:
        """Инициализирует исключение с сообщением."""
        super().__init__(message)
        self.message = message

    def __repr__(self) -> str:
        """Возвращает строковое представление исключения."""
        return self.message
