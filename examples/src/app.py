#!/usr/bin/python3

"""
Run via the run.sh or run.ps1 script
"""

from plombery import get_app  # noqa: F401

from src import vietmap # noqa: F401


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("plombery:get_app", reload=True, factory=True, reload_dirs="..")
