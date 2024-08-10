import asyncio
import datetime as dt
import math
import operator
import time
from functools import reduce
from random import random

import bloomfilter


class IdGenerator:
    def __init__(
        self,
        node_id: int,
        custom_epoch: int | None = None,
        ids_per_second: int = 10000,
    ) -> None:
        self.custom_epoch = custom_epoch or math.ceil(
            dt.datetime(2024, 1, 1, tzinfo=dt.UTC).timestamp(),
        )
        self.ids_per_second = ids_per_second
        self.node_id = node_id
        self.lock = asyncio.Lock()

        self.base62_dict: list[str] = []
        self.prepare_base62_dictionary()

        self.bloom_filter_per_time: dict[int, bloomfilter.BloomFilter] = {}

        self.node_id_bits = 10
        self.node_id_max = (1 << self.node_id_bits) - 1

        assert self.node_id <= self.node_id_max, (
            f"Invalid node_id: {self.node_id}, expected to in range [0, {self.node_id_max}"
        )

    def prepare_base62_dictionary(self) -> None:
        assert len(self.base62_dict) == 0, "base62_dict is already initialized"
        for i in range(10):
            self.base62_dict.append(str(i))

        for i in range(26):
            self.base62_dict.append(chr(ord("a") + i))

        for i in range(26):
            self.base62_dict.append(chr(ord("A") + i))

    def get_current_bloom_filter(self) -> bloomfilter.BloomFilter:
        current_time = self.get_current_time()
        if current_time not in self.bloom_filter_per_time:
            bf = bloomfilter.BloomFilter[int](self.ids_per_second, 0.1)
            self.bloom_filter_per_time = {current_time: bf}
        return self.bloom_filter_per_time[current_time]

    def get_current_time(self) -> int:
        return math.ceil(time.time() - self.custom_epoch)

    def get_random_value(self) -> int:
        return math.ceil(random() * 10**10)  # noqa

    async def gen_next_integer_id(self) -> int:

        async with self.lock:
            while True:
                current_time = self.get_current_time()
                rand_val = self.get_random_value()
                bf = self.get_current_bloom_filter()

                id_candidate = reduce(
                    operator.or_,
                    [
                        (current_time + rand_val) << self.node_id_bits,
                        self.node_id,
                    ],
                    0,
                )
                if bf.contains(id_candidate):
                    continue
                else:
                    bf.add(id_candidate)
                    return id_candidate

    def cast_to_base62(self, val: int) -> str:
        res = []
        while val:
            val, remain = divmod(val, 62)
            res.append(self.base62_dict[remain])

        return "".join(res[::-1])

    async def get_next_id(self) -> str:
        int_id = await self.gen_next_integer_id()
        return self.cast_to_base62(int_id)
