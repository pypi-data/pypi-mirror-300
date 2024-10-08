#!/usr/bin/env python3

import asyncio

import logging
from argparse import ArgumentParser, Namespace

from contextlib import suppress
from pathlib import Path

from typing import Optional

from pydantic import BaseModel

from textual import on, work
from textual.app import ComposeResult

from textual.widgets import Button, Header, Input, Label, RichLog, Switch, Tree
from trickkiste.base_tui_app import TuiBaseApp
from trickkiste.logging_helper import apply_common_logging_cli_args

from rmc import rmc_common
from rmc.rmc_common import Config

def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.rmc")


class RmCommanderTui(TuiBaseApp):
    """mpide Textual app tailoring all features"""

    CSS_PATH = Path(__file__).parent / "tui.css"

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self.doc_tree = Tree[None]("Documents")
        self.doc_tree.root.expand()

    def compose(self) -> ComposeResult:
        """Set up the UI"""
        yield Header(show_clock=True, id="header")
        yield self.doc_tree
        yield from super().compose()

    async def initialize(self) -> None:
        log().info("initialize")
        self.ssh_connection = await rmc_common.ssh_connection(self.config)
        self.update_status_info()
        await asyncio.sleep(0)
        self.update_tree()

    @work(exit_on_error=True)
    async def update_status_info(self) -> None:
        batt_now = int(
            (
                await self.ssh_connection.run(
                    "cat /sys/class/power_supply/max1726x_battery/charge_now"
                )
            ).stdout.strip()
        )
        batt_full = int(
            (
                await self.ssh_connection.run(
                    "cat /sys/class/power_supply/max1726x_battery/charge_full"
                )
            ).stdout.strip()
        )
        df = (await self.ssh_connection.run("df /home")).stdout.strip().split()[-2]
        version = (
            (await self.ssh_connection.run("strings /etc/os-release | grep IMG_VERSION"))
            .stdout.strip()
            .split("=")[-1]
        )

        while True:
            self.update_status_bar(
                f"{self.ssh_connection._host} ({self.ssh_connection._local_addr})"
                f" | version: {version} | disk: {df} | bat: {100 * batt_now // batt_full}%"
            )
            await asyncio.sleep(10)

    @work(exit_on_error=True)
    async def update_tree(self) -> None:

        rm_ftp = await rmc_common.sftp_connection(self.ssh_connection)
        content = {k: v async for k, v in rmc_common.list_docs(rm_ftp)}

        for uid, metadata in sorted(content.items(), key=lambda e: e[1]["visibleName"]):
            if metadata["type"] == "DocumentType":
                parent_str = (
                    parent["visibleName"]
                    if (parent := content.get(metadata["parent"]))
                    else metadata["parent"]
                )
                self.doc_tree.root.add_leaf(
                    f"{uid.split('-', 1)[0]}: {metadata['visibleName']} ({parent_str})"
                )
