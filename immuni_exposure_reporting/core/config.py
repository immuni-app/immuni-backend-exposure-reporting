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

from decouple import config

EXPOSURE_MONGO_URL = config(
    "EXPOSURE_MONGO_URL", default="mongodb://localhost:27017/immuni-exposure-reporting-dev"
)

MANIFEST_LENGTH_IN_DAYS = config("MANIFEST_LENGTH_IN_DAYS", cast=int, default=14)
MANIFEST_CACHE_TIME_IN_MINUTES = config("MANIFEST_CACHE_TIME_IN_MINUTES", cast=int, default=30)
SINGLE_BATCH_CACHE_TIME_IN_DAYS = config("SINGLE_BATCH_CACHE_TIME_IN_DAYS", cast=int, default=15)

APP_BUNDLE_ID = config("APP_BUNDLE_ID", default="it.ministerodellasalute.immuni")
ANDROID_PACKAGE = config("ANDROID_PACKAGE", default="org.immuni.android")

EXPORT_BIN_HEADER = config("EXPORT_BIN_HEADER", default="EK Export v1")
