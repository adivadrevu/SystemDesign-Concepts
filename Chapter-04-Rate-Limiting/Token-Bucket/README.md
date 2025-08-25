# Token Bucket Algorithm Implementation

This project implements a Token Bucket rate limiting algorithm using Test-Driven Development (TDD) approach.

## What is Token Bucket?

The Token Bucket algorithm is a rate limiting technique that:

1. **Maintains a bucket** with a maximum capacity of tokens
2. **Refills tokens** at a constant rate over time
3. **Consumes tokens** when requests are made
4. **Blocks requests** when the bucket is empty

## Key Components

- **Bucket Capacity**: Maximum number of tokens the bucket can hold
- **Refill Rate**: Number of tokens added per time unit
- **Refill Interval**: Time interval between refills
- **Current Tokens**: Current number of tokens in the bucket
- **Last Refill Time**: Timestamp of the last refill

## Algorithm Flow

1. When a request comes in, check if there are enough tokens
2. If tokens are available, consume them and allow the request
3. If no tokens are available, reject the request
4. Periodically refill the bucket based on elapsed time

## Project Structure

```
├── token_bucket/
│   ├── __init__.py
│   └── token_bucket.py
├── tests/
│   ├── __init__.py
│   └── test_token_bucket.py
├── requirements.txt
└── README.md
```

## Usage

```python
from token_bucket import TokenBucket
import time

# Create a token bucket with 10 tokens capacity, refilling 2 tokens per second
bucket = TokenBucket(capacity=10, refill_rate=2, refill_interval=1)

# Try to consume tokens
if bucket.consume(3):
    print("Request allowed")
else:
    print("Request denied")
```

## Running Tests

```bash
# Install dependencies
uv sync --dev

# Run simple tests (recommended)
python test_simple.py

# Run pytest tests (if pytest works in your environment)
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=token_bucket --cov-report=html
```

## Running Demo

```bash
# Run the interactive demo
python demo.py
```

The demo showcases:
- Basic token bucket usage
- Concurrent request handling
- Different rate limiting scenarios
- Reset functionality

## TDD Approach

This implementation follows TDD principles:

1. **Red**: Write failing tests first
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Improve code while maintaining test coverage

The tests cover:
- Basic token consumption
- Token refill over time
- Bucket capacity limits
- Edge cases and error conditions
- Thread safety considerations
