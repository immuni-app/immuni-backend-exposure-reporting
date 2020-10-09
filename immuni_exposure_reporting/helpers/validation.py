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

import re
import sys

from immuni_common.core.exceptions import SchemaValidationException


def validate_batch_index(batch_index: str) -> int:
    """
    Validate the given batch index.
    :param batch_index: the batch index to validate.
    :return: the batch index, if valid.
    :raises: SchemaValidationException if the given batch index is invalid.
    """
    try:
        index = int(batch_index)
        if index < 1 or index > sys.maxsize:
            raise ValueError()
    except ValueError:
        raise SchemaValidationException()
    return index


def validate_batch_country(batch_country: str) -> str:
    """
    Validate the given batch country.
    :param batch_country: the batch country to validate.
    :return: the batch country, if valid.
    :raises: SchemaValidationException if the given batch country is invalid.
    """
    try:
        regex = re.compile(r"^[A-Z]{2}$", re.IGNORECASE)
        match = regex.match(batch_country)
        if not match:
            raise ValueError()
    except ValueError:
        raise SchemaValidationException()
    return batch_country
