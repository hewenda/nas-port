import asyncio

async def try_connect(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool]:
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout
        )
        writer.close()
        await writer.wait_closed()
        return port, True
    except Exception:
        return port, False

async def scan(host: str, ports: list[int] = list(range(11001, 11100)), concurrency: int = 500) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)
    async def sem_task(p: int) -> tuple[int, bool]:
        async with sem:
            return await try_connect(host, p, timeout=1.0)
    tasks = [asyncio.create_task(sem_task(p)) for p in ports]
    results = await asyncio.gather(*tasks)
    return [p for p, ok in results if ok]