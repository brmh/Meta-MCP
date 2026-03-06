import asyncio
import time
import random
from structlog import get_logger

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self):
        self._app_lock = asyncio.Lock()
        self._user_lock = asyncio.Lock()
        self._campaign_locks = {}
        
        self.app_resume_time = 0.0
        self.user_resume_time = 0.0
        
        # Concurrent limit (semaphore) to prevent simple overloading
        self._semaphore = asyncio.Semaphore(20)

    async def acquire(self, campaign_id: str = None):
        """Acquires a permit to make an API request, transparently handling backoffs."""
        await self._semaphore.acquire()
        
        now = time.time()
        
        # Global App Level
        if now < self.app_resume_time:
            wait_time = self.app_resume_time - now
            logger.info("RateLimiter: App level throttle hit", wait_time=wait_time)
            await asyncio.sleep(wait_time)
            
        # Global User Level
        if now < self.user_resume_time:
            wait_time = self.user_resume_time - now
            logger.info("RateLimiter: User level throttle hit", wait_time=wait_time)
            await asyncio.sleep(wait_time)

    def release(self):
        """Releases the concurrency permit."""
        self._semaphore.release()

    def handle_rate_limit_headers(self, headers: dict):
        """Analyses the X-App-Usage and X-Business-Use-Case-Usage headers."""
        # This can be expanded to maintain sliding windows for app/user budgets based on the returned percentages
        pass

    def backoff_app(self, pause_seconds: int = 900): # Default 15 mins for app backoff (Error 4)
        """Initiate backoff for App-level rate limits."""
        now = time.time()
        resume = now + pause_seconds + random.uniform(0, 5) # add jitter
        if resume > self.app_resume_time:
            self.app_resume_time = resume
            logger.warning("Initiating app-level backoff", pause_seconds=pause_seconds)

    def backoff_user(self, pause_seconds: int = 64): # Default 64s max for user backoff (Error 17)
        """Initiate backoff for User-level rate limits."""
        now = time.time()
        resume = now + pause_seconds + random.uniform(0, 5) # add jitter
        if resume > self.user_resume_time:
            self.user_resume_time = resume
            logger.warning("Initiating user-level backoff", pause_seconds=pause_seconds)

    async def execute_with_retries(self, api_call, *args, **kwargs):
        """Executes an API call with exponential backoff on retriable errors."""
        max_retries = 3
        base_backoff = 2.0
        
        for attempt in range(max_retries + 1):
            try:
                await self.acquire()
                response = await api_call(*args, **kwargs)
                return response
            except Exception as e: # Catching generic here to type check inside, for MetaAPIError later
                from api.error_handler import MetaAPIError
                if isinstance(e, MetaAPIError):
                    if e.error_code == 4: # App limit
                        self.backoff_app()
                    elif e.error_code == 17: # User limit
                        self.backoff_user(min(64, base_backoff * (2 ** attempt)))
                    elif e.error_code == 80000: # Campaign limit
                        # Handle specific campaign lock backoff if needed, for now just generic sleep
                        pass
                    elif e.error_code not in [1, 2, 4, 17, 32, 80000]: # Not retriable
                        raise e
                    
                    if attempt == max_retries:
                        raise e
                    
                    wait_time = base_backoff * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning("Retrying API call after error", attempt=attempt+1, wait_time=wait_time, error_code=e.error_code)
                    await asyncio.sleep(wait_time)
                else:
                    raise e
            finally:
                self.release()

rate_limiter_instance = RateLimiter()
