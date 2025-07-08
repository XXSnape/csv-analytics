import argparse
from typing import TYPE_CHECKING

from commands import aggregate_command, where_command
from exceptions.incorrect_data import IncorrectDataException
from handler import FileHandler

if TYPE_CHECKING:
    from commands.base import BaseCommand


def create_parser(
    commands: list["BaseCommand"],
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Аналитика csv файлов"
    )
    parser.add_argument(
        "--file",
        help="Абсолютный путь к csv файлу",
        required=True,
    )
    for command in commands:
        parser.add_argument(
            f"--{command.command}",
            help=command.help_text,
            required=command.required,
        )
    return parser


def create_handler(
    commands: list["BaseCommand"],
    args: argparse.Namespace,
) -> FileHandler:
    handler = FileHandler(
        file_path=args.file,
        values={
            command.command: getattr(args, command.command)
            for command in commands
        },
    )
    for command in commands:
        handler.register_handler(command)
    return handler


def main() -> None:
    commands = [where_command, aggregate_command]
    parser = create_parser(commands=commands)
    args = parser.parse_args()

    try:
        handler = create_handler(commands=commands, args=args)
        handler.handle()
    except IncorrectDataException as e:
        print(e)
    except Exception:
        print("Что-то пошло не так. Попробуйте ещё раз")


if __name__ == "__main__":
    main()
