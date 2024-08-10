import asyncio
import random

import pytest

from short_url.domain.services.short_url.id_generator import IdGenerator


@pytest.mark.asyncio
async def test_id_generator():
    ig = IdGenerator(
        node_id=random.randrange(0, 1000),  # noqa
    )
    expected_unique_ids = 1000
    actual_results = await asyncio.gather(
        *[
            ig.get_next_id()
            for _ in range(expected_unique_ids)
        ],
    )
    unique_ids = set(actual_results)
    assert len(unique_ids) == expected_unique_ids
