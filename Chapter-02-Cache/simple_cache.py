#!/usr/bin/env python3
"""
Simple Cache Implementation for testing
"""

import time
from typing import Dict, Optional


class SimpleCache:
    """A simple in-memory cache with TTL support"""
    
    def __init__(self):
        self.cache: Dict[str, tuple] = {}  # key -> (value, timestamp)
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            # Simple TTL check (5 seconds)
            if time.time() - timestamp < 5:
                print(f"Cache HIT for key: {key}")
                return value
            else:
                print(f"Cache EXPIRED for key: {key}")
                del self.cache[key]
        
        print(f"Cache MISS for key: {key}")
        return None
    
    def put(self, key: str, value: str) -> None:
        """Put value in cache"""
        self.cache[key] = (value, time.time())
        print(f"Cached key: {key}")
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        print("Cache cleared")


def test_cache():
    """Test the cache implementation"""
    print("🧪 Testing Simple Cache Implementation\n")
    
    cache = SimpleCache()
    
    # Test 1: Basic put and get
    print("Test 1: Basic put and get")
    cache.put("user:1", "John Doe")
    cache.put("user:2", "Jane Smith")
    
    assert cache.get("user:1") == "John Doe"
    assert cache.get("user:2") == "Jane Smith"
    assert cache.get("user:3") is None
    print("✅ Basic operations work\n")
    
    # Test 2: Cache size
    print("Test 2: Cache size")
    assert cache.size() == 2
    print("✅ Cache size correct\n")
    
    # Test 3: TTL expiration (simulate)
    print("Test 3: TTL expiration")
    cache.put("temp:1", "Temporary data")
    # Manually expire by modifying timestamp
    cache.cache["temp:1"] = (cache.cache["temp:1"][0], time.time() - 10)
    assert cache.get("temp:1") is None
    print("✅ TTL expiration works\n")
    
    # Test 4: Clear cache
    print("Test 4: Clear cache")
    cache.clear()
    assert cache.size() == 0
    assert cache.get("user:1") is None
    print("✅ Cache clear works\n")
    
    print("🎉 All cache tests passed!")


if __name__ == "__main__":
    test_cache()
