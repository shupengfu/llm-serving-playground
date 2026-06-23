# Benchmark Result

## 1. Goal

This benchmark tests the latency and throughput of a local LLM serving pipeline.

The tested pipeline is:

```text
benchmark_chat.py
    ↓
FastAPI /chat endpoint
    ↓
llm_client.py
    ↓
OpenAI SDK
    ↓
Ollama
    ↓
qwen2.5:0.5b
```

The goal of this stage is to understand how concurrency affects latency and throughput in a local LLM inference service.

---

## 2. Test Environment

* Backend: Ollama
* Model: qwen2.5:0.5b
* API server: FastAPI
* Endpoint: POST /chat
* Hardware: Local CPU environment
* OS: Windows
* Client: Python requests
* Benchmark method: concurrent requests with ThreadPoolExecutor

---

## 3. Metrics

The benchmark records the following metrics:

| Metric                | Meaning                                      |
| --------------------- | -------------------------------------------- |
| Success count         | Number of successful requests                |
| Failed count          | Number of failed requests                    |
| Total time            | Total benchmark execution time               |
| QPS                   | Successful requests per second               |
| Average latency       | Average response time of successful requests |
| P50 latency           | Approximate 50th percentile latency          |
| P95 latency           | Approximate 95th percentile latency          |
| Average answer length | Average length of generated answers          |

---

## 4. Results

| Concurrency | Requests | Success | Failed | Total Time (s) | Avg Latency (s) | P50 (s) | P95 (s) |    QPS | Avg Answer Length |
| ----------: | -------: | ------: | -----: | -------------: | --------------: | ------: | ------: | -----: | ----------------: |
|           1 |        3 |       3 |      0 |         6.7767 |          2.2582 |  2.3587 |  3.4257 | 0.4427 |           98.6667 |
|           2 |        4 |       4 |      0 |         6.0423 |          2.6765 |  3.6844 |  3.7442 | 0.6620 |          120.2500 |
|           4 |        4 |       4 |      0 |         6.0072 |          4.1719 |  5.1170 |  6.0061 | 0.6659 |          120.7500 |

---

## 5. Analysis

All benchmark requests succeeded, which means the FastAPI service and the Ollama backend were able to handle the tested workload without request failures.

When concurrency increased from 1 to 2, QPS improved from 0.4427 to 0.6620. This shows that the service can benefit from a small amount of concurrency.

However, when concurrency increased from 2 to 4, QPS almost stopped increasing. It only changed from 0.6620 to 0.6659. At the same time, the average latency increased from 2.6765 seconds to 4.1719 seconds, and P95 latency increased to about 6.0061 seconds.

This indicates that the local model backend became the bottleneck. Additional concurrent requests did not significantly improve throughput. Instead, they increased waiting time and response latency.

The result is reasonable because the benchmark was executed on a local CPU environment. LLM inference is compute-intensive, and the backend can only generate a limited number of tokens per second.

Another factor is answer length. Longer generated responses usually require more decoding steps, so they tend to have higher latency.

---

## 6. Conclusion

This benchmark shows that the local LLM serving pipeline works correctly and can handle concurrent requests.

The main observation is:

```text
Increasing concurrency improves throughput at first,
but after the backend reaches its capacity,
QPS saturates and latency increases.
```

This is a common behavior in LLM serving systems.

The same benchmark script can be reused later to compare Ollama and vLLM. In the next stage, the backend can be replaced with vLLM on a cloud GPU, and the same metrics can be collected again for comparison.
