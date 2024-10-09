"""Hello module for uv-demo."""

from loguru import logger as log


def say_hello() -> None:
    """Entrypoint for uv-demo."""
    log.info("Hello from uv-demo!")


def say_goodbye() -> None:
    """Another entrypoint for uv-demo."""
    log.info("Goodbye from uv-demo!")
