#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from poppy.core.test import CommandTestCase

from roc.idb.constants import IDB_CACHE_DIR


def reset_db(command_test_case: CommandTestCase, log_level: str = "INFO"):
    # Clear database
    clear_db_cmd = ["pop", "db", "downgrade", "base", "-ll", log_level]
    command_test_case.run_command(clear_db_cmd)

    # Run database migrations
    create_db_cmd = ["pop", "db", "upgrade", "heads", "-ll", log_level]
    command_test_case.run_command(create_db_cmd)


def load_idb(
    command_test_case: CommandTestCase,
    idb_source: str,
    idb_version: str,
    install_dir: str = None,
    log_level="INFO",
) -> str:
    if install_dir is None:
        install_dir = os.path.join(IDB_CACHE_DIR, f"idb-{idb_source}-{idb_version}")
        os.makedirs(install_dir, exist_ok=True)

    # IDB loading
    load_idb_cmd = [
        "pop",
        "idb",
        "install",
        "--force",
        "--install-dir",
        install_dir,
        "-s",
        idb_source,
        "-v",
        idb_version,
        "--load",
        "-ll",
        log_level,
    ]
    command_test_case.run_command(load_idb_cmd)

    return install_dir
