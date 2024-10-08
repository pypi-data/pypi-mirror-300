#!/usr/bin/env python3

"""rMC CLI
"""

import asyncio
import json
import logging
from argparse import ArgumentParser, ArgumentTypeError
from argparse import Namespace as Args

# from collections.abc import Iterable, Mapping
from pathlib import Path

from trickkiste.logging_helper import apply_common_logging_cli_args, setup_logging

from rmc import rmc_common
from rmc.rmc_common import ConfigManager

CFG_FILE = Path("~/.config/rmc.cfg")


def log() -> logging.Logger:
    """Our logger"""
    return logging.getLogger("trickkiste.rmc")


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = apply_common_logging_cli_args(ArgumentParser())

    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--hostname", type=str)
    parser.add_argument("--username", "-u", type=str)
    parser.add_argument("--password", "-p", type=str)

    parser.add_argument("--timeout", "-t", type=int)
    parser.add_argument("--config-file", "-c", type=Path, default=CFG_FILE)

    subparsers = parser.add_subparsers(help="types of A")
    parser.set_defaults(func=fn_tui)

    parser_show = subparsers.add_parser("info")
    parser_show.set_defaults(func=fn_info)

    parser_show = subparsers.add_parser("reboot")
    parser_show.set_defaults(func=fn_reboot)

    parser_show = subparsers.add_parser("config-auth")
    parser_show.set_defaults(func=fn_config)
    parser_show.add_argument("auth_kwargs", type=split_kw, nargs="+")

    parser_show = subparsers.add_parser("list", aliases=["ls"])
    parser_show.set_defaults(func=fn_list)
    parser_show.add_argument("path", type=str, nargs="*")

    parser_build = subparsers.add_parser("upload", aliases=["push"])
    parser_build.set_defaults(func=fn_upload)
    parser_build.add_argument("path", type=Path, nargs="+")

    return parser.parse_args()


def split_kw(string: str) -> tuple[str, str]:
    """Config element splitter"""
    try:
        key, value = string.split("=", 1)
    except ValueError as exc:
        raise ArgumentTypeError("Syntax: '<KEY>=<VALUE> ...'") from exc
    return key, value


def fn_config(args: Args) -> None:
    """Entry point for configuration"""
    with ConfigManager(args) as config:
        auth_kwargs = dict(args.auth_kwargs)
        if "hostname" in auth_kwargs:
            config.config.hostname = auth_kwargs["hostname"]
        if "username" in auth_kwargs:
            config.config.username = auth_kwargs["username"]
        if "password" in auth_kwargs:
            config.config.password = auth_kwargs["password"]
        config.persist()


def fn_info(args: Args) -> None:
    """Entry point for info"""
    with ConfigManager(args) as config:
        print(f"Config file located at '{args.config_file}'")
        for key, value in config.config.__dict__.items():
            print(key, value)


async def fn_reboot(args: Args) -> None:
    """Entry point for info"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = await rmc_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return
    await rmc_common.reboot(rm_ssh)


async def fn_upload(args: Args) -> None:
    """Entry point for file upload via CLI"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = await rmc_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

    rm_ftp = await rmc_common.sftp_connection(rm_ssh)

    for path in args.path:
        await rmc_common.upload_file(rm_ftp, path)


async def fn_list(args: Args) -> None:
    """Entry point for content listing via CLI"""
    with ConfigManager(args) as config:
        try:
            rm_ssh = await rmc_common.ssh_connection(config.config)
        except RuntimeError as exc:
            print(f"Connection failed: {exc}")
            return

    rm_ftp = await rmc_common.sftp_connection(rm_ssh)
    content = {k: v async for k, v in rmc_common.list_docs(rm_ftp)}

    for uid, metadata in sorted(content.items(), key=lambda e: e[1]["visibleName"]):
        if metadata["type"] == "DocumentType":
            parent_str = (
                parent["visibleName"]
                if (parent := content.get(metadata["parent"]))
                else metadata["parent"]
            )
            print(f"{uid.split('-', 1)[0]}: {metadata['visibleName']} ({parent_str})")


async def fn_ui(args: Args) -> None:
    """Entry point for UI"""

    # pylint: disable=import-outside-toplevel # (late import to allow headless operation)
    from rmc.ui import main as ui_main

    with ConfigManager(args) as config:
        ui_main(config.config)
        config.persist()


def fn_tui(args: Args) -> None:
    """Entry point for UI"""

    # pylint: disable=import-outside-toplevel # (late import to allow headless operation)
    from rmc.tui import RmCommanderTui

    with ConfigManager(args) as config:
        asyncio.run(RmCommanderTui(config.config).execute())
        config.persist()


def main() -> None:
    """Entry point for everything else"""
    args = parse_args()
    setup_logging(log(), args.log_level)
    if asyncio.iscoroutinefunction(args.func):
        return asyncio.run(args.func(args))
    return args.func(args)


if __name__ == "__main__":
    main()
