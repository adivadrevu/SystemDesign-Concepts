#!/usr/bin/env python3
"""
Demo script showcasing the TokenBucket rate limiting algorithm
"""

import time
import threading
import random
from token_bucket import TokenBucket


def simulate_api_requests(bucket, request_id, num_requests):
    """Simulate API requests using the token bucket"""
    print(f"Thread {request_id}: Starting {num_requests} requests...")
    
    for i in range(num_requests):
        # Simulate some processing time
        time.sleep(random.uniform(0.1, 0.3))
        
        # Try to consume 1 token (1 request)
        if bucket.consume(1):
            print(f"Thread {request_id}: Request {i+1} ✅ ALLOWED (tokens: {bucket.get_available_tokens():.1f})")
        else:
            print(f"Thread {request_id}: Request {i+1} ❌ RATE LIMITED (tokens: {bucket.get_available_tokens():.1f})")
    
    print(f"Thread {request_id}: Completed")


def demo_basic_usage():
    """Demonstrate basic token bucket usage"""
    print("=" * 60)
    print("🚀 TOKEN BUCKET ALGORITHM DEMO")
    print("=" * 60)
    
    # Create a token bucket: 10 tokens capacity, 2 tokens per second refill
    bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
    
    print(f"Created TokenBucket: {bucket}")
    print(f"Initial tokens: {bucket.get_available_tokens()}")
    print()
    
    # Simulate some requests
    print("📡 Simulating API requests...")
    for i in range(15):
        if bucket.consume(1):
            print(f"Request {i+1:2d}: ✅ ALLOWED  (tokens: {bucket.get_available_tokens():.1f})")
        else:
            print(f"Request {i+1:2d}: ❌ RATE LIMITED  (tokens: {bucket.get_available_tokens():.1f})")
        
        time.sleep(0.2)  # Small delay between requests
    
    print()


def demo_concurrent_requests():
    """Demonstrate concurrent requests with rate limiting"""
    print("🔄 CONCURRENT REQUESTS DEMO")
    print("-" * 40)
    
    # Create a token bucket for concurrent testing
    bucket = TokenBucket(capacity=20, refill_rate=5, refill_interval=1)
    
    print(f"Created TokenBucket: {bucket}")
    print("Starting 3 concurrent threads with 8 requests each...")
    print()
    
    # Create multiple threads
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=simulate_api_requests,
            args=(bucket, i+1, 8)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"\nFinal token count: {bucket.get_available_tokens():.1f}")
    print()


def demo_different_scenarios():
    """Demonstrate different rate limiting scenarios"""
    print("🎯 DIFFERENT SCENARIOS DEMO")
    print("-" * 40)
    
    scenarios = [
        ("High Rate", TokenBucket(capacity=50, refill_rate=10, refill_interval=1)),
        ("Low Rate", TokenBucket(capacity=5, refill_rate=1, refill_interval=2)),
        ("Burst Protection", TokenBucket(capacity=3, refill_rate=1, refill_interval=1)),
    ]
    
    for name, bucket in scenarios:
        print(f"\n{name} Scenario:")
        print(f"  Bucket: {bucket}")
        
        # Simulate burst of requests
        allowed = 0
        denied = 0
        
        for i in range(10):
            if bucket.consume(1):
                allowed += 1
            else:
                denied += 1
        
        print(f"  Results: {allowed} allowed, {denied} denied")
        print(f"  Final tokens: {bucket.get_available_tokens():.1f}")


def demo_reset_functionality():
    """Demonstrate reset functionality"""
    print("\n🔄 RESET FUNCTIONALITY DEMO")
    print("-" * 40)
    
    bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)
    
    print(f"Initial: {bucket}")
    
    # Consume some tokens
    bucket.consume(7)
    print(f"After consuming 7: {bucket}")
    
    # Reset the bucket
    bucket.reset()
    print(f"After reset: {bucket}")


def main():
    """Run all demos"""
    try:
        demo_basic_usage()
        demo_concurrent_requests()
        demo_different_scenarios()
        demo_reset_functionality()
        
        print("=" * 60)
        print("✅ All demos completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
