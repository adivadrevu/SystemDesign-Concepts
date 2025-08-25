#!/usr/bin/env python3
"""
Simple example of TokenBucket usage
"""

from token_bucket import TokenBucket
import time

# Create a token bucket with 10 tokens capacity, refilling 2 tokens per second
bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)

print(f"Created bucket: {bucket}")

# Simulate some API requests
for i in range(15):
    if bucket.consume(1):
        print(f"Request {i+1}: ✅ ALLOWED (tokens: {bucket.get_available_tokens():.1f})")
    else:
        print(f"Request {i+1}: ❌ RATE LIMITED (tokens: {bucket.get_available_tokens():.1f})")
    
    time.sleep(0.2)  # Small delay between requests

print(f"\nFinal state: {bucket}")
