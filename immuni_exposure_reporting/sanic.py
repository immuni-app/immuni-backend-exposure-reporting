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

from immuni_common.sanic import create_app, run_app
from immuni_exposure_reporting.apis import keys
from immuni_exposure_reporting.core.managers import managers

sanic_app = create_app(
    api_title="Exposure Reporting Service",
    api_description="The Exposure Reporting Service makes the TEK Chunks created by the Exposure "
    "Ingestion Service available to the Mobile Client. Only TEK Chunks for the last 14 days are "
    "made available."
    "<br><br>"
    "To avoid downloading the same TEKs multiple times, the Mobile Clients fetch the indexes of "
    "the TEK Chunks available to download first. "
    "Then, they only actually download TEK Chunks with indexes for which TEK Chunks have not been "
    "downloaded before.",
    blueprints=(keys.bp,),
    managers=managers,
)

if __name__ == "__main__":  # pragma: no cover
    run_app(sanic_app)
