# vLLM Benchmark Results



## 1. Goal



This experiment benchmarks a local LLM serving pipeline with a cloud GPU vLLM backend.



The tested pipeline is:



```text

Windows FastAPI Server

   ↓

SSH Tunnel

   ↓

Cloud vLLM Server

   ↓

RTX 4090D

   ↓

Qwen2.5 Instruct Model

```



The goal is to compare inference latency and throughput across different model sizes.



---



## 2. Environment



### Local Side



* OS: Windows

* Application Server: FastAPI

* Client: Python requests

* API format: OpenAI-compatible API

* Endpoint: `/chat`



### Cloud Side



* GPU: NVIDIA GeForce RTX 4090D

* GPU Memory: 24GB

* Backend: vLLM

* Connection: SSH tunnel

* API server: vLLM OpenAI-compatible server



---



## 3. Models Tested



| Model                      | Backend | GPU       | Max Model Length |

| --------------------------: | -------: | ---------: | ---------------: |

| Qwen/Qwen2.5-1.5B-Instruct | vLLM    | RTX 4090D |             8192 |

| Qwen/Qwen2.5-7B-Instruct   | vLLM    | RTX 4090D |             4096 |



---



## 4. Qwen2.5-1.5B Benchmark Result



| Concurrency | Requests | Success | Failed | Avg Latency (s) | P50 (s) | P95 (s) |    QPS |

| ----------: | -------: | ------: | -----: | --------------: | ------: | ------: | -----: |

|           1 |        3 |       3 |      0 |          0.4207 |  0.3963 |  0.4681 | 2.3732 |

|           2 |        4 |       4 |      0 |          0.5219 |  0.5512 |  0.6217 | 3.6233 |

|           4 |        4 |       4 |      0 |          0.4632 |  0.4702 |  0.4839 | 8.2149 |



---



## 5. Qwen2.5-7B Benchmark Result



| Concurrency | Requests | Success | Failed | Avg Latency (s) | P50 (s) | P95 (s) |    QPS |

| ----------: | -------: | ------: | -----: | --------------: | ------: | ------: | -----: |

|           1 |        3 |       3 |      0 |          1.2211 |  1.2506 |  1.2535 | 0.8185 |

|           2 |        4 |       4 |      0 |          1.2931 |  1.2853 |  1.3293 | 1.5273 |

|           4 |        4 |       4 |      0 |          1.2284 |  1.2146 |  1.3208 | 2.9921 |



---



## 6. GPU Memory Usage



For Qwen2.5-7B-Instruct, the GPU memory usage recorded by `nvidia-smi` was:



```text

GPU Memory Usage: 21629 MiB / 24564 MiB

Process: VLLM::EngineCore

Process Memory Usage: 21620 MiB

```



This memory usage includes model weights, KV cache allocation, CUDA runtime memory, and vLLM execution-related memory.



---



## 7. Analysis



The 1.5B model has lower latency and higher QPS because it has fewer parameters and requires less computation during inference.



The 7B model has higher latency and lower QPS, but it provides a more realistic deployment scenario for LLM inference. Even with a 7B model, vLLM on RTX 4090D can still serve concurrent requests with stable success rate and low-second-level latency.



The results show that model size has a clear impact on inference performance:



```text

Larger model size

   ↓

More computation per token

   ↓

Higher latency

   ↓

Lower QPS

```



At the same time, vLLM can still improve serving efficiency through GPU acceleration, batching, KV cache management, and optimized attention backends.



---



## 8. Conclusion



This experiment verifies that the project can switch from local Ollama inference to cloud GPU vLLM inference through configuration.



The project successfully benchmarks different Qwen2.5 model sizes on a cloud RTX 4090D GPU and records latency, P50/P95 latency, QPS, success rate, and GPU memory usage.



This provides a foundation for further experiments such as AWQ quantization, streaming benchmark, TTFT measurement, and tokens-per-second analysis.



