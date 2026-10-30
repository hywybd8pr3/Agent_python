import logging

from agent_app.cli import main


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    for name in ("httpx", "httpx2"):
        logging.getLogger(name).setLevel(logging.WARNING)

    main()