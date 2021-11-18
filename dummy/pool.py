import os
import glob
import json
import asyncio
import janus


class Connection:
    def __init__(self, fixtures_dir='fixtures'):
        self._responses = {}
        for fixture_file in glob.glob(os.path.join(fixtures_dir, '*.json')):
            with open(fixture_file) as fh:
                filename = os.path.split(fixture_file)[-1]
                self._responses[filename] = json.loads(fh.read())

    async def get(self, fixture, latency_ms: int = 1):
        await asyncio.sleep(latency_ms / 1000)
        return self._responses[fixture].get('response', {}).get('payload', '')


class Pool:
    def __init__(self,
                 data_getter: Connection,
                 pool_size: int = 100):
        self.pool_size = pool_size
        self._data_getter = data_getter
        self._async_q = None

    @property
    def queue(self):
        # Lazy load from async context to be sure that event-loop is running
        if self._async_q is None:
            self._async_q = janus.Queue().async_q
            for i in range(self.pool_size):
                self._async_q.put_nowait(None)
        return self._async_q

    async def __aenter__(self):
        await self.queue.get()
        return self._data_getter

    async def __aexit__(self, exc_type, exc, tb):
        await self.queue.put(None)


async def main(pool: Pool):
    async with pool as connection:
        print(await connection.get("userinfo.json"))

if __name__ == '__main__':
    pool = Pool(data_getter=Connection(fixtures_dir='../fixtures'))
    asyncio.run(main(pool))
