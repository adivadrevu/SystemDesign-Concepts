import pytest
import time
import threading
from token_bucket import TokenBucket


class TestTokenBucket:
    """Test cases for TokenBucket implementation"""

    def test_initialization(self):
        """Test TokenBucket initialization with valid parameters"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        assert bucket.capacity == 10
        assert bucket.refill_rate == 2
        assert bucket.refill_interval == 1
        assert bucket.tokens == 10  # Should start with full capacity

    def test_initialization_with_invalid_parameters(self):
        """Test TokenBucket initialization with invalid parameters"""
        with pytest.raises(ValueError):
            TokenBucket(capacity=0, refill_rate=2, refill_interval=1)
        
        with pytest.raises(ValueError):
            TokenBucket(capacity=10, refill_rate=0, refill_interval=1)
        
        with pytest.raises(ValueError):
            TokenBucket(capacity=10, refill_rate=2, refill_interval=0)

    def test_consume_successful(self):
        """Test successful token consumption"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        # Should be able to consume tokens when available
        assert bucket.consume(3) is True
        assert bucket.tokens == 7
        
        assert bucket.consume(5) is True
        assert bucket.tokens == 2

    def test_consume_failure(self):
        """Test failed token consumption when not enough tokens"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        # Should not be able to consume more tokens than available
        assert bucket.consume(15) is False
        assert bucket.tokens == 10  # Tokens should remain unchanged
        
        # Consume some tokens first
        bucket.consume(8)
        assert bucket.tokens == 2
        
        # Try to consume more than available
        assert bucket.consume(5) is False
        assert bucket.tokens == 2  # Should remain unchanged

    def test_consume_zero_tokens(self):
        """Test consuming zero tokens"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        initial_tokens = bucket.tokens
        
        assert bucket.consume(0) is True
        assert bucket.tokens == initial_tokens

    def test_consume_negative_tokens(self):
        """Test consuming negative tokens should raise error"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        with pytest.raises(ValueError):
            bucket.consume(-1)

    def test_token_refill_over_time(self):
        """Test that tokens refill over time"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        # Consume all tokens
        bucket.consume(10)
        assert bucket.tokens == 0
        
        # Wait for 1 second to allow refill
        time.sleep(1.1)
        
        # Try to consume tokens - should refill first
        assert bucket.consume(2) is True
        assert bucket.tokens == 0  # 2 tokens consumed, 2 refilled = 0 remaining

    def test_token_refill_multiple_intervals(self):
        """Test token refill over multiple time intervals"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        # Consume all tokens
        bucket.consume(10)
        assert bucket.tokens == 0
        
        # Wait for 3 seconds to allow refill
        time.sleep(3.1)
        
        # Should have refilled 6 tokens (3 seconds * 2 tokens/second)
        assert bucket.consume(6) is True
        assert bucket.tokens == 0

    def test_token_refill_capacity_limit(self):
        """Test that tokens don't exceed capacity when refilling"""
        bucket = TokenBucket(capacity=5, refill_rate=10, refill_interval=1)
        
        # Consume all tokens
        bucket.consume(5)
        assert bucket.tokens == 0
        
        # Wait for 1 second to allow refill
        time.sleep(1.1)
        
        assert bucket.get_available_tokens() == 5  # Should be at capacity, not 10

    def test_get_available_tokens(self):
        """Test getting available tokens"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        assert bucket.get_available_tokens() == 10
        
        bucket.consume(3)
        assert bucket.get_available_tokens() == 7

    def test_reset_bucket(self):
        """Test resetting the bucket to full capacity"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        bucket.consume(5)
        assert bucket.tokens == 5
        
        bucket.reset()
        assert bucket.tokens == 10

    def test_thread_safety(self):
        """Test that TokenBucket is thread-safe"""
        bucket = TokenBucket(capacity=100, refill_rate=10, refill_interval=1)
        results = []
        
        def consume_tokens():
            for _ in range(10):
                result = bucket.consume(1)
                results.append(result)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=consume_tokens)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have exactly 100 successful consumptions
        assert sum(results) == 100
        assert bucket.tokens == 0

    def test_edge_case_exact_consumption(self):
        """Test consuming exactly the available tokens"""
        bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
        
        assert bucket.consume(10) is True
        assert bucket.tokens == 0
        
        # Should not be able to consume more
        assert bucket.consume(1) is False

    def test_edge_case_fractional_refill(self):
        """Test handling of fractional token refills"""
        bucket = TokenBucket(capacity=10, refill_rate=1, refill_interval=2)
        
        bucket.consume(10)
        assert bucket.tokens == 0
        
        # Wait for 1 second (half interval) - should not refill yet
        time.sleep(1)
        
        # Should not refill yet (only half interval passed)
        assert bucket.consume(1) is False
        assert bucket.tokens == 0

    def test_edge_case_large_consumption(self):
        """Test consuming a very large number of tokens"""
        bucket = TokenBucket(capacity=1000, refill_rate=100, refill_interval=1)
        
        # Should be able to consume up to capacity
        assert bucket.consume(1000) is True
        assert bucket.tokens == 0
        
        # Should not be able to consume more than capacity
        assert bucket.consume(1001) is False

    def test_edge_case_very_small_refill_rate(self):
        """Test with very small refill rate"""
        bucket = TokenBucket(capacity=10, refill_rate=0.1, refill_interval=1)
        
        bucket.consume(10)
        assert bucket.tokens == 0
        
        # Wait for 10 seconds to allow refill
        time.sleep(10.1)
        
        # Should have refilled 1 token (10 * 0.1)
        assert bucket.consume(1) is True
        assert bucket.tokens == 0

    def test_edge_case_very_large_refill_interval(self):
        """Test with very large refill interval"""
        bucket = TokenBucket(capacity=10, refill_rate=10, refill_interval=100)
        
        bucket.consume(10)
        assert bucket.tokens == 0
        
        # Wait for 50 seconds (half interval) - should not refill yet
        time.sleep(50)
        
        # Should not refill yet
        assert bucket.consume(1) is False
        assert bucket.tokens == 0
