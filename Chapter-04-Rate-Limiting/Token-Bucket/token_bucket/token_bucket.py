import time
import threading
from typing import Optional


class TokenBucket:
    """
    A thread-safe implementation of the Token Bucket rate limiting algorithm.
    
    The Token Bucket algorithm maintains a bucket with a maximum capacity of tokens.
    Tokens are refilled at a constant rate over time, and requests consume tokens.
    If the bucket is empty, requests are rejected.
    
    Attributes:
        capacity (int): Maximum number of tokens the bucket can hold
        refill_rate (float): Number of tokens added per time unit
        refill_interval (float): Time interval between refills in seconds
        tokens (float): Current number of tokens in the bucket
        last_refill_time (float): Timestamp of the last refill
        lock (threading.Lock): Thread lock for thread safety
    """
    
    def __init__(self, capacity: int, refill_rate: float, refill_interval: float = 1.0):
        """
        Initialize a TokenBucket with the specified parameters.
        
        Args:
            capacity (int): Maximum number of tokens the bucket can hold
            refill_rate (float): Number of tokens added per time unit
            refill_interval (float): Time interval between refills in seconds
            
        Raises:
            ValueError: If any parameter is invalid (<= 0)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be greater than 0")
        if refill_interval <= 0:
            raise ValueError("Refill interval must be greater than 0")
        
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.refill_interval = refill_interval
        self.tokens = float(capacity)  # Start with full capacity
        self.last_refill_time = time.time()
        self.lock = threading.Lock()
    
    def _refill_tokens(self) -> None:
        """
        Refill tokens based on elapsed time since last refill.
        This method is called internally and is thread-safe.
        """
        current_time = time.time()
        time_passed = current_time - self.last_refill_time
        
        # Calculate how many complete intervals have passed
        intervals_passed = time_passed / self.refill_interval
        
        if intervals_passed >= 1.0:
            # Calculate tokens to add
            tokens_to_add = intervals_passed * self.refill_rate
            
            # Update tokens (don't exceed capacity)
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            
            # Update last refill time
            self.last_refill_time = current_time
    
    def consume(self, tokens_requested: int) -> bool:
        """
        Attempt to consume the specified number of tokens.
        
        Args:
            tokens_requested (int): Number of tokens to consume
            
        Returns:
            bool: True if tokens were successfully consumed, False otherwise
            
        Raises:
            ValueError: If tokens_requested is negative
        """
        if tokens_requested < 0:
            raise ValueError("Tokens requested cannot be negative")
        
        if tokens_requested == 0:
            return True
        
        with self.lock:
            # Refill tokens first
            self._refill_tokens()
            
            # Check if we have enough tokens
            if self.tokens >= tokens_requested:
                self.tokens -= tokens_requested
                return True
            else:
                return False
    
    def get_available_tokens(self) -> float:
        """
        Get the current number of available tokens (after refilling).
        
        Returns:
            float: Number of available tokens
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens
    
    def reset(self) -> None:
        """
        Reset the bucket to full capacity.
        """
        with self.lock:
            self.tokens = float(self.capacity)
            self.last_refill_time = time.time()
    
    def __repr__(self) -> str:
        """String representation of the TokenBucket."""
        return (f"TokenBucket(capacity={self.capacity}, "
                f"refill_rate={self.refill_rate}, "
                f"refill_interval={self.refill_interval}, "
                f"tokens={self.tokens:.2f})")
