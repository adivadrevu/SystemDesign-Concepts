# Chapter 1: Load Balancer

A simple round-robin load balancer implementation that distributes incoming requests across multiple backend servers.

## 🎯 What is a Load Balancer?

A load balancer is a device or software that distributes network traffic across multiple servers to ensure no single server bears too much load. This improves:

- **Availability**: If one server fails, others continue serving
- **Performance**: Distributes load evenly across servers
- **Scalability**: Easy to add/remove servers

## 🏗️ Implementation Details

### Round-Robin Algorithm
- Distributes requests sequentially across backend servers
- Simple and effective for equal-capacity servers
- No server state tracking required

### Architecture
```
Client Request → Load Balancer (Port 9000)
                      ↓
        ┌─────────────────────────┐
        ↓                         ↓
   Backend 1 (Port 8001)    Backend 2 (Port 8002)
   "Red Server"             "Blue Server"
```

## 🚀 Running the Load Balancer

### Prerequisites
- Python 3.6+
- No external dependencies required

### Quick Start
```bash
cd Chapter-01-Load-Balancer
python load_balancer.py
```

### What Happens
1. **Backend servers start** on ports 8001 and 8002
2. **Load balancer starts** on port 9000
3. **Requests are distributed** in round-robin fashion

### Testing
```bash
# Test multiple requests to see round-robin in action
curl http://localhost:9000
curl http://localhost:9000
curl http://localhost:9000
curl http://localhost:9000
```

You should see alternating responses:
- `<h1 style='color:red;'>Red Server - Server 1</h1>`
- `<h1 style='color:blue;'>Blue Server - Server 2</h1>`

## 🔧 Code Structure

### Key Components

1. **Backend Servers**
   - Simple HTTP servers with different colored responses
   - Run in separate threads
   - Simulate real backend services

2. **Load Balancer**
   - `LoadBalancerHandler` class handles incoming requests
   - Uses `itertools.cycle()` for round-robin distribution
   - Forwards requests to backend servers

3. **Request Flow**
   ```
   Client → LoadBalancer → Backend Server → Response
   ```

## 🧪 Testing Scenarios

### Basic Functionality
- ✅ Round-robin distribution
- ✅ Multiple backend support
- ✅ Error handling for failed backends

### Advanced Testing
```bash
# Test with multiple concurrent requests
for i in {1..10}; do
  curl -s http://localhost:9000 | grep -o "Server [0-9]" &
done
wait
```

## 🔍 Monitoring

The load balancer provides console output showing:
- Backend server startup
- Request routing decisions
- Error messages for failed backends

## 🚀 Production Considerations

For production use, consider:
- **Health checks** for backend servers
- **Session persistence** (sticky sessions)
- **SSL/TLS termination**
- **Metrics and monitoring**
- **Auto-scaling integration**

## 📚 Related Concepts

- **Health Checks**: Verify backend server availability
- **Session Affinity**: Route same user to same server
- **Weighted Round-Robin**: Assign different weights to servers
- **Least Connections**: Route to server with fewest active connections

---

**Next Chapter**: [Chapter 2 - Cache](../Chapter-02-Cache/README.md)
