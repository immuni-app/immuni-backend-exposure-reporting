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
from http import HTTPStatus

from mongoengine import DoesNotExist
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, raw
from sanic_openapi import doc

from immuni_common.core.exceptions import (
    BatchNotFoundException,
    NoBatchesException,
    SchemaValidationException,
)
from immuni_common.helpers.cache import cache
from immuni_common.helpers.sanic import json_response
from immuni_common.helpers.swagger import doc_exception
from immuni_common.models.mongoengine.batch_file import BatchFile
from immuni_exposure_reporting.core import config
from immuni_exposure_reporting.helpers.validation import validate_batch_index
from immuni_exposure_reporting.models.swagger import Index

bp = Blueprint("keys", url_prefix="keys")


@bp.route("/index", version=1, methods=["GET"])
@doc.summary("Fetch TEK Chunk indexes (caller: Mobile Client).")
@doc.description(
    "Return the index of the oldest relevant TEK Chunk (no older than 14 days) and the index of "
    "the newest available TEK Chunk. "
    "It is up to the Mobile Client not to download the same TEK Chunk more than once."
)
@doc_exception(NoBatchesException)
@doc.response(
    HTTPStatus.OK.value,
    Index,
    description="The index of the oldest relevant TEK Chunk (no older than 14 days) and the index "
    "of the newest available TEK Chunk.",
)
@cache(max_age=timedelta(minutes=config.MANIFEST_CACHE_TIME_IN_MINUTES))
async def index(request: Request) -> HTTPResponse:
    """
    Return the index of the oldest relevant TEK Chunk (no older than 14 days) and the index of the
    newest available TEK Chunk.
    :param request: the HTTP request object.
    :return: the indexes of the oldest relevant and newest available TEK Chunks.
    """
    indexes = BatchFile.get_oldest_and_newest_indexes(days=config.MANIFEST_LENGTH_IN_DAYS)
    return json_response(indexes)


@bp.route("/<batch_index>", version=1, methods=["GET"])
@doc.summary("Download TEKs (caller: Mobile Client).")
@doc.description(
    "Given a specific TEK Chunk index, the Mobile Client downloads the associated TEK Chunk from "
    "the Exposure Reporting Service."
)
@doc_exception(SchemaValidationException)
@doc_exception(BatchNotFoundException)
@doc.produces(None, content_type="application/zip")
@doc.response(
    HTTPStatus.OK.value,
    None,
    description="The TEK Chunk's zip file associated with the provided index.",
)
@cache(max_age=timedelta(days=config.SINGLE_BATCH_CACHE_TIME_IN_DAYS))
async def get_batch(request: Request, batch_index: str) -> HTTPResponse:
    """
    Fetch a specific TEK Chunk, serialized as zip file as required by the Mobile Client.
    :param request: the HTTP request object.
    :param batch_index: the index of the TEK Chunk to fetch.
    :return: the TEK Chunk's zip file associated with the provided index.
    :raises: BatchNotFoundException if the index is not associated with any TEK Chunk.
    """
    try:
        batch = BatchFile.from_index(validate_batch_index(batch_index))
    except DoesNotExist:
        raise BatchNotFoundException()
    return raw(batch.client_content, content_type="application/zip")
