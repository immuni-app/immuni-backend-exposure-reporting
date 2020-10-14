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

from datetime import timedelta

import pytest
from pytest_sanic.utils import TestClient

from immuni_common.helpers.tests import mock_config
from immuni_common.models.mongoengine.batch_file_eu import BatchFileEu
from immuni_exposure_reporting.core import config
from tests.fixtures.batch_file_eu import create_random_batches_eu


async def test_index_no_batches_eu(client: TestClient) -> None:
    response = await client.get("/v1/keys/eu/DK/index")
    assert response.status == 404


@mock_config(config, "MANIFEST_CACHE_TIME_IN_MINUTES", timedelta(minutes=30).total_seconds())
@pytest.mark.parametrize("num_batches, oldest, newest", ((1, 0, 0), (10, 0, 9), (20, 6, 19)))
@pytest.mark.parametrize("country", ("DK", "DE", "AT", "ES"))
async def test_index_eu(client: TestClient, num_batches: int, oldest: int, newest: int, country: str) -> None:
    create_random_batches_eu(num_batches)

    response = await client.get(f"/v1/keys/eu/{country}/index")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "public, max-age=1800"

    actual = await response.json()
    assert actual == {"oldest": oldest, "newest": newest}


@pytest.mark.parametrize("country", ("DK", "DE", "AT", "ES"))
async def test_batch_eu(client: TestClient, batch_file_eu: BatchFileEu, country: str) -> None:
    response = await client.get(f"/v1/keys/eu/{country}/1")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "public, max-age=1296000"

    assert response.content_type == "application/zip"


@pytest.mark.parametrize("country", ("DK", "DE", "AT", "ES"))
async def test_batch_eu_not_found(client: TestClient, country: str) -> None:
    response = await client.get(f"/v1/keys/eu/{country}/1")
    assert response.status == 404
    assert "Cache-Control" not in response.headers


@pytest.mark.parametrize("country", ("DK", "DE", "AT", "ES"))
async def test_batch_eu_not_found_v0(client: TestClient, country: str) -> None:
    response = await client.get(f"/v0/keys/eu/{country}/1")
    assert response.status == 404
    assert "Cache-Control" not in response.headers


@pytest.mark.parametrize("index", ("asd", "none", "12d", "-23", 0, -1, 23456789876543234567898765))
@pytest.mark.parametrize("country", ("DK", "DE", "AT", "ES"))
async def test_batch_eu_index_weird_characters(client: TestClient, index: str, country: str) -> None:
    response = await client.get(f"/v1/keys/eu/{country}/{index}")
    assert response.status == 400

    content = await response.json()
    assert content["message"] == "Request not compliant with the defined schema."


@pytest.mark.parametrize("country", ("ITA", "none", "DENMARK", "-23", "it", "It"))
async def test_batch_eu_country_weird_characters(client: TestClient, country: str) -> None:
    response = await client.get(f"/v1/keys/eu/{country}/1")
    assert response.status == 400

    content = await response.json()
    assert content["message"] == "Request not compliant with the defined schema."
