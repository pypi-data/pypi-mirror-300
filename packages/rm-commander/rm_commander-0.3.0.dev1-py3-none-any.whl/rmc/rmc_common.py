#!/usr/bin/env python3

"""This module contains stuff shared between UI and CLI"""

# pylint: disable=unspecified-encoding


import json
import logging
import time
import zipfile
from collections.abc import AsyncIterable, Iterable, Mapping
from contextlib import suppress
from pathlib import Path
from uuid import uuid4

# from paramiko import SFTPClient, SSHClient, ssh_exception
from asyncssh import (
    ConnectionLost,
    HostKeyNotVerifiable,
    PermissionDenied,
    SFTPClient,
    SSHClientConnection,
)
from asyncssh import connect as ssh_connect
from asyncssh import set_debug_level as ssh_set_debug_level
from lxml import etree
from pydantic import BaseModel

XOCHITL_DIR = Path(".local/share/remarkable/xochitl")


def log() -> logging.Logger:
    """Our logger"""
    return logging.getLogger("trickkiste.rmc.common")


def first_not_none(*values: int | str | None) -> int | str | None:
    """First element of @values which is not None"""
    for value in values:
        if value is not None:
            return value
    return None


def load_json(path: Path):
    """Convenience wrapper for reading a JSON file"""
    with suppress(FileNotFoundError, json.JSONDecodeError):
        with path.expanduser().open(encoding="utf-8") as file:
            return json.load(file)
    return {}


class Config(BaseModel):
    """Application config model"""

    hostname: str
    username: str
    password: str
    timeout: int
    window_geometry: tuple[int, int, int, int] | None = None


class ConfigManager:
    """Context manager for configuration"""

    def __init__(self, args):
        self.config_file_path = args.config_file
        persisted = load_json(self.config_file_path)
        self.config = Config(
            hostname=first_not_none(args.hostname, persisted.get("hostname"), "reMarkable"),
            username=first_not_none(args.username, persisted.get("username"), "root"),
            password=first_not_none(args.password, persisted.get("password"), ""),
            timeout=first_not_none(args.timeout, persisted.get("timeout"), 6),
            window_geometry=persisted.get("window_geometry"),
        )

    def __enter__(self) -> "ConfigManager":
        return self

    def __exit__(self, *args: object) -> None:
        ...

    def persist(self) -> None:
        """Write out the current configuration"""
        log().debug("write config file to %s", self.config_file_path)
        with self.config_file_path.expanduser().open("w", encoding="utf-8") as file:
            json.dump(self.config, file, default=lambda o: o.__dict__, indent=4, sort_keys=True)


async def ssh_connection(config) -> SSHClientConnection:
    """Establishes and returns a paramiko SSH client session"""
    try:
        log().info("try to connect to %s@%s...", config.username, config.hostname)
        ssh_set_debug_level(2)
        return await ssh_connect(
            config.hostname,
            **{
                key: value
                for key, value in (
                    # ("port", self.host_info.ssh_port),
                    ("username", config.username or None),
                    # ("client_keys", self.host_info.ssh_key_file),
                )
                if value is not None
            },
            keepalive_interval=5,
            keepalive_count_max=2,
            # known_hosts=None,  # setting to None results in ConnectionLost being thrown
            connect_timeout=config.timeout,
        )
    except ConnectionLost as exc:
        raise RuntimeError(f"{exc}") from exc
    except PermissionDenied as exc:
        raise RuntimeError(f"{exc}") from exc
    except HostKeyNotVerifiable as exc:
        raise RuntimeError(f"{exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"{exc}") from exc


async def sftp_connection(client: SSHClientConnection) -> SFTPClient:
    """Returns a ready to use SFTP connection"""
    return await client.start_sftp_client()


async def list_dir(
    sftp: SFTPClient,
    directory: str | Path = XOCHITL_DIR,
) -> Iterable[Path]:
    """Lists remote directory content"""
    return (Path(path) for path in await sftp.listdir(Path(directory)))


async def list_docs(sftp: SFTPClient) -> AsyncIterable[tuple[str, Mapping[str, str]]]:
    """Yields UID and metadata mapping for each document on device"""
    files = set(p.name for p in await list_dir(sftp))
    for doc in set(p.split(".")[0] for p in files):
        if f"{doc}.metadata" not in files:
            log().warning("file %s has no metadata file", doc)
            continue

        async with sftp.open(filepath := XOCHITL_DIR / f"{doc}.metadata") as file:
            try:
                yield doc, json.loads(await file.read())
            except json.JSONDecodeError as exc:
                print(f"Could not read {filepath}: {exc}")


def epub_info(fname: str) -> str:
    def xpath(element, path):
        return (
            results[0]
            if (
                results := element.xpath(
                    path,
                    namespaces={
                        "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                        "pkg": "http://www.idpf.org/2007/opf",
                        "dc": "http://purl.org/dc/elements/1.1/",
                    },
                )
            )
            else None
        )

    with zipfile.ZipFile(fname) as zip_content:
        cfname = xpath(
            etree.fromstring(zip_content.read("META-INF/container.xml")),
            "n:rootfiles/n:rootfile/@full-path",
        )
        metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

    return {
        s: value
        for s in ("title", "language", "creator", "date", "identifier")
        if (value := xpath(metadata, f"dc:{s}/text()"))
    }


async def upload_file(rm_sftp: SFTPClient, path: Path) -> None:
    if path.suffix.lower() == ".pdf":
        log().info("upload PDF %s", path)
        uuid = uuid4()

        def ph(path_local, path_remote, size_transferred, size_total):
            log().debug(
                "%s -> %s (%.1f/%d)",
                path_local.decode(),
                path_remote.decode(),
                100 / size_total * size_transferred,
                size_total,
            )

        log().debug("PUT pdf content..")
        t1 = time.time()
        await rm_sftp.put(path, XOCHITL_DIR / f"{uuid}.pdf", progress_handler=ph)
        t2 = time.time()
        log().debug("%.2fs", t2 - t1)
        # with path.open("rb") as inputfile:
        #    async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.pdf"), "wb") as payloadfile:
        #        log().debug("write pdf content..")
        #        await payloadfile.write(inputfile.read(), progress_handler=ph)
        #        log().debug(".")

        async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.content"), "w") as contentfile:
            log().debug("write content file..")
            await contentfile.write(json.dumps({"coverPageNumber": 0, "fileType": "pdf"}))
            log().debug(".")

        async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.metadata"), "w") as metadatafile:
            log().debug("write metadata file..")
            await metadatafile.write(
                json.dumps(
                    {
                        # "deleted": False,
                        # "lastModified": "1649503474223",
                        # "lastOpened": "1658044625089",
                        # "lastOpenedPage": 0,
                        # "metadatamodified": False,
                        # "modified": True,
                        "parent": "",
                        # "pinned": False,
                        # "synced": False,
                        "type": "DocumentType",
                        "version": 0,
                        "visibleName": path.stem,
                    }
                )
            )
            log().debug(".")

    if path.suffix.lower() == ".epub":

        t = time.time()
        info = epub_info(path)
        print(info)

        uuid = uuid4()

        print(f"{time.time() - t:.2f}s")

        print(f"{uuid}")

        print(f"{time.time() - t:.2f}s")
        with path.open("rb") as inputfile:
            async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.epub"), "wb") as payloadfile:
                await payloadfile.write(inputfile.read())
                print(f"{time.time() - t}")

        async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.content"), "w") as contentfile:
            await contentfile.write(json.dumps({"coverPageNumber": 0, "fileType": "epub"}))

        print(f"{time.time() - t:.2f}s")

        async with rm_sftp.open(str(XOCHITL_DIR / f"{uuid}.metadata"), "w") as metadatafile:
            await metadatafile.write(
                json.dumps(
                    {
                        # "deleted": False,
                        # "lastModified": "1649503474223",
                        # "lastOpened": "1658044625089",
                        # "lastOpenedPage": 0,
                        # "metadatamodified": False,
                        # "modified": True,
                        "parent": "",
                        # "pinned": False,
                        # "synced": False,
                        "type": "DocumentType",
                        "version": 0,
                        "visibleName": info["title"],
                    }
                )
            )


async def reboot(client: SSHClientConnection) -> None:
    """Shortcut for rebooting the device"""
    await client.run("/sbin/reboot")
