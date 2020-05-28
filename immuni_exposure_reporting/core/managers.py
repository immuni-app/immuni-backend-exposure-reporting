#    Copyright (C) 2020 Presidenza del Consiglio dei Ministri.
#    Please refer to the AUTHORS file for more information.
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

from typing import Optional

from mongoengine import connect
from pymongo import MongoClient

from immuni_common.core.exceptions import ImmuniException
from immuni_common.core.managers import BaseManagers
from immuni_exposure_reporting.core import config


class Managers(BaseManagers):
    """
    Singleton objects containing API clients used somewhere in the application.
    """

    _exposure_mongo: Optional[MongoClient] = None

    @property
    def exposure_mongo(self) -> MongoClient:
        """
        Return the MongoDB manager to handle TEKs.
        :return: the MongoDB manager to handle TEKs.
        :raise: ImmuniException if the manager is not initialized.
        """
        if self._exposure_mongo is None:
            raise ImmuniException("Cannot use the MongoDB manager before initializing it.")
        return self._exposure_mongo

    async def initialize(self) -> None:
        """
        Initialize managers on demand.
        """
        await super().initialize()
        self._exposure_mongo = connect(host=config.EXPOSURE_MONGO_URL)

    async def teardown(self) -> None:
        """
        Perform teardown actions (e.g., close open connections.)
        """
        await super().teardown()
        if self._exposure_mongo is not None:
            self._exposure_mongo.close()


managers = Managers()
