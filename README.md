# System Design Concepts

A comprehensive collection of system design concepts, algorithms, and implementations with hands-on projects.

## 📚 Chapters

### Chapter 1: Load Balancer
- **Round-Robin Load Balancer** - A simple HTTP load balancer that distributes requests across multiple backend servers using round-robin algorithm

### Chapter 2: Cache
- **In-Memory Cache** - A simple cache implementation with TTL support and FastAPI integration for article caching

### Chapter 4: Rate Limiting
- **Token Bucket Algorithm** - A thread-safe implementation of the Token Bucket rate limiting algorithm using Test-Driven Development (TDD)

## 🚀 Getting Started

### Quick Setup
```bash
# Run the setup script (recommended)
./setup.sh

# Or manually setup with uv
uv sync --dev
source .venv/bin/activate
```

### Running Chapters

Each chapter contains its own projects with specific setup instructions:

```bash
# For Chapter 1 - Load Balancer
cd Chapter-01-Load-Balancer
python load_balancer.py

# For Chapter 2 - Cache
cd Chapter-02-Cache
python simple_cache.py
# Or run FastAPI version:
uvicorn cache:app --reload

# For Chapter 4 - Rate Limiting
cd Chapter-04-Rate-Limiting/Token-Bucket
python test_simple.py
python demo.py
```

## 📁 Repository Structure

```
SystemDesign-Concepts/
├── Chapter-01-Load-Balancer/
│   ├── README.md                  # Chapter documentation
│   └── load_balancer.py           # Round-robin load balancer
├── Chapter-02-Cache/
│   ├── README.md                  # Chapter documentation
│   ├── cache.py                   # FastAPI cache implementation
│   └── simple_cache.py            # Simple cache with TTL
├── Chapter-04-Rate-Limiting/
│   └── Token-Bucket/
│       ├── token_bucket/          # Main implementation
│       ├── tests/                 # Test suite
│       ├── README.md              # Chapter documentation
│       ├── demo.py                # Interactive demo
│       ├── example.py             # Basic usage example
│       ├── test_simple.py         # Simple test runner
│       ├── pyproject.toml         # Project configuration
│       └── uv.lock                # Dependency lock file
├── .gitignore
└── README.md                      # Main documentation
```

## 🛠️ Technologies Used

- **Python 3.8+** - Primary programming language
- **uv** - Fast Python package manager
- **pytest** - Testing framework
- **Threading** - For concurrent operations

## 📖 Learning Path

1. **Start with Chapter 1** - Load Balancer concepts and round-robin distribution
2. **Continue with Chapter 2** - Caching strategies and TTL implementation
3. **Advanced to Chapter 4** - Rate Limiting concepts and Token Bucket algorithm
4. **Follow TDD approach** - Learn Test-Driven Development principles
5. **Run demos** - See algorithms in action
6. **Experiment** - Modify parameters and observe behavior

## 🤝 Contributing

Feel free to contribute by:
- Adding new chapters
- Improving existing implementations
- Adding more test cases
- Enhancing documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy Learning! 🎉**
