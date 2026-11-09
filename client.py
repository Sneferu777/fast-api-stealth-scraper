import asyncio
import logging
from typing import Dict, Optional, Any 
from curl_cffi.requests import AsyncSession, Response
from config import config 

logging.basicConfig(level=logging.INFO, format=("%(asctime)s [%(levelname)s] %(message)s"))

class StealthClient:
    def __init__(self, impersonate : str = "chrome120", max_concurrency = config.DEFAULT_CONCURRENCY):
        self.impersonate = impersonate
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session : Optional[AsyncSession] = None 

    async def __aenter__(self):
        
        self.session = AsyncSession(impersonate=self.impersonate)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb)::

        if self.session : 
            await self.session.close()

    async def fetch(
        self,
        url : str,
        headers : Optional[Dict[str, str]] = None,
        params : Optional[Dict[str, Any]] = None,
        max_retries : int = 3,
    ) -> Optional[Response] :

        async with self.semaphore :

            for attempt in range(1, max_retries + 1):
                try : 
                    response = await self.session.get(url, headers=headers, params=params , timeout=config.REQUEST_TIMEOUT)


                    if response.status_code == 200 : 
                        return response
                    
                    logging.info(f"Attempt {attempt}/{max_retries} Status {response.status_code} for {url}")

                except Exception as e : 
                    logging.error(f"Attemp {attempt}/{max_retries} Request failed for {url}")
                    
                
                await asyncio.sleep(1 * attempt)

            return None

async def stealth_worker(
    worker_id : int ,
    tasks_queue : asyncio.Queue,
    results_queue : asyncio.Queue,
    client : StealthClient
):

    while True : 
        
        task = await tasks_queue.get()

        if not task:
            tasks_queue.task_done()
            break
    
        url = task.get("url")
        
        logging.info(f"Worker {worker_id} fetching : {url}")

        response = await client.fetch(url, headers=task.get("headers"))

        if response :
            payload = (
                response.json()
                if "application/json" in response.headers.get("Content-Type", "")
                else response.content 
            )
            await results_queue.put(payload)
        
        else:
            logging.error(f"Worker {worker_id} failed to fetch {url}")

        tasks_queue.task_done()



