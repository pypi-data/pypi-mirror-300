#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil

import pytest

from poppy.core.test import CommandTestCase
from poppy.core.logger import logger

from roc.idb.models.idb import IdbRelease
from .idb_test_util import reset_db, load_idb


class TestSetTrangeCommand(CommandTestCase):
    """
    Test the set_trange command of roc.idb plugin.

    """

    # @pytest.mark.skip
    @pytest.mark.parametrize(
        "idb_source,idb_version,validity_min,validity_max",
        [
            ("MIB", "20200113", "2020-01-13T00:00:00", "2050-12-31T23:59:59"),
        ],
    )
    def test_set_trange(self, idb_source, idb_version, validity_min, validity_max):
        # Initializing database
        logger.debug("Reset database ...")
        reset_db(self)

        # Installing IDB
        logger.debug(f"Installing IDB [{idb_source}-{idb_version}] ...")
        self.install_dir = load_idb(self, idb_source, idb_version)

        # Command to test
        command_to_test = [
            "pop",
            "idb",
            "set_trange",
            idb_version,
            "-s",
            idb_source,
            "--validity-min",
            validity_min,
            "--validity-max",
            validity_max,
            "-ll",
            "INFO",
        ]

        # Run command to test
        self.run_command(command_to_test)

        # Verify expected behaviour
        expected_values = (
            self.session.query(IdbRelease.validity_min, IdbRelease.validity_max)
            .filter(
                IdbRelease.idb_version == idb_version,
                IdbRelease.idb_source == idb_source,
            )
            .one()
        )

        time_strformat = "%Y-%m-%dT%H:%M:%S"
        assert (expected_values[0].strftime(time_strformat) == validity_min) and (
            expected_values[1].strftime(time_strformat) == validity_max
        )

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # Remove IDB folder
        shutil.rmtree(self.install_dir)
