from typing import Generic, TypeVar, Dict, Any, Optional, Callable
from pydantic import BaseModel
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import hashlib
import json


class State(BaseModel):
    """Base state class for flows"""

    started_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    status: str = "initialized"
    metadata: Dict[str, Any] = {}


StateType = TypeVar("StateType", bound=State)


class Flow(Generic[StateType]):
    """
    Base flow class for building AI automations.

    Example:
        ```python
        class MyFlow(Flow[MyState]):
            async def run(self):
                await self.step_one()
                await self.step_two()
        ```
    """

    def __init__(
        self,
        state_class: Optional[type[StateType]] = None,
        cache_dir: str = ".cache",
        log_dir: str = "logs",
        **kwargs,
    ):
        # Setup state
        self.state_class = state_class or State
        self.state = self.state_class(**kwargs)

        # Setup directories
        self.cache_dir = Path(cache_dir)
        self.log_dir = Path(log_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

        # Setup logging
        self.logger = self._setup_logger()

        # Track execution
        self._start_time = datetime.now()
        self._steps: Dict[str, float] = {}

    def _setup_logger(self) -> logging.Logger:
        """Setup logging with file and console handlers"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(self.log_dir / f"{self.__class__.__name__}.log")
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    async def run(self) -> Dict[str, Any]:
        """Override this method to implement your flow"""
        raise NotImplementedError

    async def step(self, name: str):
        """Context manager for tracking flow steps"""
        start_time = datetime.now()
        self.logger.info(f"Starting step: {name}")

        try:
            yield
            duration = (datetime.now() - start_time).total_seconds()
            self._steps[name] = duration
            self.logger.info(f"Completed step: {name} in {duration:.2f}s")

        except Exception as e:
            self.logger.error(f"Error in step {name}: {str(e)}")
            raise

    async def call_api(
        self,
        key: str,
        func: Callable,
        *args,
        use_cache: bool = True,
        cache_ttl: int = 3600,
        **kwargs,
    ) -> Any:
        """
        Call API with caching and rate limiting.

        Args:
            key: Base cache key
            func: Async function to call
            use_cache: Whether to use cache
            cache_ttl: Cache TTL in seconds
            *args, **kwargs: Passed to func
        """
        # Generate cache key
        cache_key = self._generate_cache_key(key, args, kwargs)
        cache_file = self.cache_dir / f"{cache_key}.json"

        # Check cache
        if use_cache and cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                if data["expires"] > datetime.now().timestamp():
                    self.logger.info(f"Cache hit: {key}")
                    return data["value"]
            except Exception as e:
                self.logger.warning(f"Cache error: {str(e)}")

        # Call API
        try:
            self.logger.info(f"Calling API: {key}")
            result = await func(*args, **kwargs)

            # Cache result
            if use_cache:
                cache_data = {
                    "value": result,
                    "expires": datetime.now().timestamp() + cache_ttl,
                }
                cache_file.write_text(json.dumps(cache_data))

            return result

        except Exception as e:
            self.logger.error(f"API error: {str(e)}")
            raise

    def _generate_cache_key(self, key: str, args: tuple, kwargs: dict) -> str:
        """Generate unique cache key"""
        # Combine all inputs
        cache_input = {"key": key, "args": args, "kwargs": kwargs}

        # Create hash
        return hashlib.md5(json.dumps(cache_input, sort_keys=True).encode()).hexdigest()

    def get_duration(self) -> float:
        """Get total flow duration in seconds"""
        return (datetime.now() - self._start_time).total_seconds()

    def get_step_durations(self) -> Dict[str, float]:
        """Get duration of all steps"""
        return self._steps.copy()

    async def __aenter__(self):
        """Enable async context manager"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on exit"""
        self.state.completed_at = datetime.now()
        self.state.status = "error" if exc_type else "completed"
