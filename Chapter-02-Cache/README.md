# Chapter 2: Cache

Implementation of a simple in-memory cache system with TTL (Time To Live) support.

## What is Caching?

Caching is a technique that stores frequently accessed data in fast-access storage to improve performance. Benefits include:

- **Speed**: Faster data retrieval
- **Reduced Load**: Less pressure on primary data sources
- **Scalability**: Better system performance under load

## Implementation Details

### Simple In-Memory Cache
- **Key-Value Storage**: Simple dictionary-based storage
- **TTL Support**: Automatic expiration of cached items
- **Thread-Safe**: Basic thread safety for concurrent access

### Architecture
```
Client Request → Cache Check → Cache Hit/Miss
                      ↓
              Primary Data Source (if miss)
```

## Running the Cache

### Prerequisites
- Python 3.6+
- No external dependencies required (for simple_cache.py)

### Quick Start

#### Simple Cache (No Dependencies)
```bash
cd Chapter-02-Cache
python simple_cache.py
```

#### FastAPI Cache (Requires Dependencies)
```bash
# Install dependencies
pip install fastapi uvicorn requests pydantic

# Run the server
uvicorn cache:app --reload --port 8000
```

## Code Structure

### SimpleCache Class
```python
class SimpleCache:
    def get(self, key: str) -> Optional[str]    # Retrieve value
    def put(self, key: str, value: str) -> None # Store value
    def size(self) -> int                       # Get cache size
    def clear(self) -> None                     # Clear all entries
```

### FastAPI Implementation
- **GET /get/**: Retrieve cached article by URL
- **PUT /put/**: Store article in cache
- **Automatic Fetching**: Fetches from server if not cached

## Testing

### Simple Cache Tests
```bash
python simple_cache.py
```

Tests include:
- ✅ Basic put and get operations
- ✅ Cache size tracking
- ✅ TTL expiration
- ✅ Cache clearing

### FastAPI Cache Tests
```bash
# Test GET endpoint
curl "http://localhost:8000/get/?url=https://example.com"

# Test PUT endpoint
curl -X PUT "http://localhost:8000/put/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "content": "Cached content"}'
```

## Cache Performance

### Cache Hit/Miss Scenarios
```
Cache HIT: Data found in cache (fast)
Cache MISS: Data not in cache (slower, fetches from source)
Cache EXPIRED: Data expired, needs refresh
```

### Performance Benefits
- **Cache Hit**: ~1ms response time
- **Cache Miss**: ~100-500ms (network + processing)
- **Memory Usage**: Proportional to cached data size

## Monitoring

The cache provides console output showing:
- Cache hits and misses
- TTL expiration events
- Cache size changes

## Production Considerations

For production use, consider:
- **Redis/Memcached**: Distributed caching
- **Cache Invalidation**: Smart cache refresh strategies
- **Memory Management**: LRU eviction policies
- **Monitoring**: Cache hit rates and performance metrics
- **Persistence**: Cache persistence across restarts

## Related Concepts

- **Cache Hit Rate**: Percentage of requests served from cache
- **Cache Invalidation**: Removing stale data from cache
- **Write-Through Cache**: Immediate write to both cache and storage
- **Write-Behind Cache**: Delayed write to storage
- **Cache Warming**: Pre-loading frequently accessed data

## API Endpoints (FastAPI)

### GET /get/
Retrieve cached article by URL
```bash
curl "http://localhost:8000/get/?url=https://example.com"
```

### PUT /put/
Store article in cache
```bash
curl -X PUT "http://localhost:8000/put/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "content": "Article content"}'
```

---

**Previous Chapter**: [Chapter 1 - Load Balancer](../Chapter-01-Load-Balancer/README.md)  
**Next Chapter**: [Chapter 4 - Rate Limiting](../Chapter-04-Rate-Limiting/Token-Bucket/README.md)
