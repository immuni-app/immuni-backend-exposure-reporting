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
from immuni_common.models.mongoengine.batch_file import BatchFile
from immuni_exposure_reporting.core import config
from tests.fixtures.batch_file import create_random_batches


async def test_index_no_batches(client: TestClient) -> None:
    response = await client.get("/v1/keys/index")
    assert response.status == 404


@mock_config(config, "MANIFEST_CACHE_TIME_IN_MINUTES", timedelta(minutes=30).total_seconds())
@pytest.mark.parametrize("num_batches, oldest, newest", ((1, 0, 0), (10, 0, 9), (20, 6, 19)))
async def test_index(client: TestClient, num_batches: int, oldest: int, newest: int) -> None:
    create_random_batches(num_batches)

    response = await client.get("/v1/keys/index")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "public, max-age=1800"

    actual = await response.json()
    assert actual == {"oldest": oldest, "newest": newest}


async def test_batch(client: TestClient, batch_file: BatchFile) -> None:
    response = await client.get("/v1/keys/1")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "public, max-age=1296000"

    assert response.content_type == "application/zip"


async def test_batch_not_found(client: TestClient) -> None:
    response = await client.get("/v1/keys/1")
    assert response.status == 404
    assert "Cache-Control" not in response.headers


async def test_batch_not_found_v0(client: TestClient) -> None:
    response = await client.get("/v0/keys/1")
    assert response.status == 404
    assert "Cache-Control" not in response.headers


@pytest.mark.parametrize("index", ("asd", "none", "12d", "-23", 0, -1, 23456789876543234567898765))
async def test_batch_weird_characters(client: TestClient, index: str) -> None:
    response = await client.get(f"/v1/keys/{index}")
    assert response.status == 400

    content = await response.json()
    assert content["message"] == "Request not compliant with the defined schema."
