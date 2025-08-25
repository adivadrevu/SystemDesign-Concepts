#!/usr/bin/env python3
"""
Simple test script to verify TokenBucket implementation
"""

import time
import threading
from token_bucket import TokenBucket


def test_basic_functionality():
    """Test basic token bucket functionality"""
    print("Testing basic functionality...")
    
    # Create a token bucket with 10 tokens, refilling 2 per second
    bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
    
    # Test initial state
    assert bucket.tokens == 10, f"Expected 10 tokens, got {bucket.tokens}"
    print("✓ Initial state correct")
    
    # Test successful consumption
    assert bucket.consume(3) is True, "Should be able to consume 3 tokens"
    assert bucket.tokens == 7, f"Expected 7 tokens, got {bucket.tokens}"
    print("✓ Successful consumption works")
    
    # Test failed consumption
    assert bucket.consume(10) is False, "Should not be able to consume 10 tokens"
    assert bucket.tokens == 7, "Tokens should remain unchanged"
    print("✓ Failed consumption works")
    
    # Test zero consumption
    assert bucket.consume(0) is True, "Should be able to consume 0 tokens"
    assert bucket.tokens == 7, "Tokens should remain unchanged"
    print("✓ Zero consumption works")


def test_token_refill():
    """Test token refill functionality"""
    print("\nTesting token refill...")
    
    bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
    
    # Consume all tokens
    bucket.consume(10)
    assert bucket.tokens == 0, "Should have 0 tokens"
    print("✓ All tokens consumed")
    
    # Wait for refill
    print("Waiting 1.1 seconds for refill...")
    time.sleep(1.1)
    
    # Should have refilled 2 tokens
    available = bucket.get_available_tokens()
    assert available >= 2, f"Expected at least 2 tokens, got {available}"
    print(f"✓ Tokens refilled: {available}")


def test_capacity_limit():
    """Test that tokens don't exceed capacity"""
    print("\nTesting capacity limit...")
    
    bucket = TokenBucket(capacity=5, refill_rate=10, refill_interval=1)
    
    # Consume all tokens
    bucket.consume(5)
    assert bucket.tokens == 0, "Should have 0 tokens"
    
    # Wait for refill (should only refill up to capacity)
    time.sleep(1.1)
    
    available = bucket.get_available_tokens()
    assert available == 5, f"Expected 5 tokens, got {available}"
    print("✓ Capacity limit respected")


def test_thread_safety():
    """Test thread safety"""
    print("\nTesting thread safety...")
    
    bucket = TokenBucket(capacity=100, refill_rate=10, refill_interval=1)
    results = []
    
    def consume_tokens():
        for _ in range(10):
            result = bucket.consume(1)
            results.append(result)
    
    # Create multiple threads
    threads = []
    for _ in range(10):  # Changed from 5 to 10 threads
        thread = threading.Thread(target=consume_tokens)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Should have exactly 100 successful consumptions
    successful = sum(results)
    assert successful == 100, f"Expected 100 successful consumptions, got {successful}"
    assert bucket.tokens == 0, "Should have 0 tokens remaining"
    print("✓ Thread safety verified")


def test_edge_cases():
    """Test edge cases"""
    print("\nTesting edge cases...")
    
    # Test invalid parameters
    try:
        TokenBucket(capacity=0, refill_rate=2, refill_interval=1)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Invalid capacity caught")
    
    try:
        TokenBucket(capacity=10, refill_rate=0, refill_interval=1)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Invalid refill rate caught")
    
    try:
        TokenBucket(capacity=10, refill_rate=2, refill_interval=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Invalid refill interval caught")
    
    # Test negative token consumption
    bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
    try:
        bucket.consume(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Negative token consumption caught")


def main():
    """Run all tests"""
    print("🚀 Starting TokenBucket Tests\n")
    
    try:
        test_basic_functionality()
        test_token_refill()
        test_capacity_limit()
        test_thread_safety()
        test_edge_cases()
        
        print("\n🎉 All tests passed! TokenBucket implementation is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
