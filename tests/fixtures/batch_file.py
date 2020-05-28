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

import base64
import random
import string
from datetime import datetime, timedelta
from typing import Optional

import pytest

from immuni_common.models.enums import TransmissionRiskLevel
from immuni_common.models.mongoengine.batch_file import BatchFile
from immuni_common.models.mongoengine.temporary_exposure_key import TemporaryExposureKey


def generate_random_key_data(length: int = 128) -> str:
    letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_batch(
    index: int, num_keys: int, period_start: datetime, period_end: datetime
) -> None:
    rsn = int(datetime.utcnow().timestamp() / 600)

    keys = [
        TemporaryExposureKey(
            key_data=generate_random_key_data(),
            transmission_risk_level=random.choice([tr for tr in TransmissionRiskLevel]),
            rolling_start_number=rsn,
        )
        for _ in range(num_keys)
    ]
    BatchFile(index=index, keys=keys, period_start=period_start, period_end=period_end).save()


def create_random_batches(
    num_batches: int, key_per_batch: int = 10, end_date: Optional[datetime] = None
) -> None:
    if end_date is None:
        end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=num_batches)
    for index in range(num_batches):
        generate_random_batch(
            index=index,
            num_keys=key_per_batch,
            period_start=start_date + timedelta(days=index),
            period_end=start_date + timedelta(days=index + 1),
        )


@pytest.fixture()
def batch_file() -> BatchFile:
    batch = BatchFile(
        index=1,
        keys=[
            TemporaryExposureKey(
                key_data=base64.b64encode("first_key".encode("utf-8")).decode("utf-8"),
                transmission_risk_level=TransmissionRiskLevel.low,
                rolling_start_number=1,
            ),
            TemporaryExposureKey(
                key_data=base64.b64encode("second_key".encode("utf-8")).decode("utf-8"),
                transmission_risk_level=TransmissionRiskLevel.low,
                rolling_start_number=2,
            ),
            TemporaryExposureKey(
                key_data=base64.b64encode("third_key".encode("utf-8")).decode("utf-8"),
                transmission_risk_level=TransmissionRiskLevel.highest,
                rolling_start_number=3,
            ),
        ],
        period_start=datetime.utcnow() - timedelta(days=1),
        period_end=datetime.utcnow(),
        sub_batch_count=2,
        sub_batch_index=1,
        client_content=b"this_is_a_zip_file",
    )
    batch.save()
    return batch
