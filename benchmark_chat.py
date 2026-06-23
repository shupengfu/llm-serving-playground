import time
import csv
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


API_URL = "http://127.0.0.1:8001/chat"


def build_payload(request_id: int):
    return {
        "messages": [
            {
                "role": "system",
                "content": "你是一个中文 AI 学习助手，回答要清楚、简洁。"
            },
            {
                "role": "user",
                "content": f"请用三句话解释什么是大模型推理服务。这是第 {request_id} 个请求。"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 120
    }


def send_request(request_id: int):
    payload = build_payload(request_id)

    start_time = time.perf_counter()

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=180
        )

        end_time = time.perf_counter()
        latency = end_time - start_time

        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")

            return {
                "request_id": request_id,
                "success": True,
                "status_code": response.status_code,
                "latency": latency,
                "answer_length": len(answer),
                "error": ""
            }

        else:
            return {
                "request_id": request_id,
                "success": False,
                "status_code": response.status_code,
                "latency": latency,
                "answer_length": 0,
                "error": response.text
            }

    except Exception as e:
        end_time = time.perf_counter()
        latency = end_time - start_time

        return {
            "request_id": request_id,
            "success": False,
            "status_code": -1,
            "latency": latency,
            "answer_length": 0,
            "error": str(e)
        }


def percentile(values, p):
    if not values:
        return None

    values = sorted(values)

    if len(values) == 1:
        return values[0]

    k = (len(values) - 1) * p / 100
    f = int(k)
    c = min(f + 1, len(values) - 1)

    if f == c:
        return values[int(k)]

    return values[f] + (values[c] - values[f]) * (k - f)


def run_benchmark(concurrency: int, num_requests: int):
    print("=" * 60)
    print(f"Running benchmark: concurrency={concurrency}, num_requests={num_requests}")
    print("=" * 60)

    results = []

    benchmark_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(send_request, i)
            for i in range(num_requests)
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            print(
                f"request_id={result['request_id']}, "
                f"success={result['success']}, "
                f"status={result['status_code']}, "
                f"latency={result['latency']:.2f}s, "
                f"answer_length={result['answer_length']}"
            )

    benchmark_end = time.perf_counter()
    total_time = benchmark_end - benchmark_start

    success_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]

    latencies = [r["latency"] for r in success_results]
    answer_lengths = [r["answer_length"] for r in success_results]

    summary = {
        "concurrency": concurrency,
        "num_requests": num_requests,
        "success_count": len(success_results),
        "failed_count": len(failed_results),
        "total_time": total_time,
        "qps": len(success_results) / total_time if total_time > 0 else 0,
        "avg_latency": statistics.mean(latencies) if latencies else None,
        "p50_latency": percentile(latencies, 50),
        "p95_latency": percentile(latencies, 95),
        "avg_answer_length": statistics.mean(answer_lengths) if answer_lengths else None,
    }

    print("\nSummary:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    print()

    return summary, results


def save_results(all_summaries, all_results):
    with open("benchmark_summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "concurrency",
                "num_requests",
                "success_count",
                "failed_count",
                "total_time",
                "qps",
                "avg_latency",
                "p50_latency",
                "p95_latency",
                "avg_answer_length"
            ]
        )

        writer.writeheader()
        writer.writerows(all_summaries)

    with open("benchmark_details.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "concurrency",
                "request_id",
                "success",
                "status_code",
                "latency",
                "answer_length",
                "error"
            ]
        )

        writer.writeheader()

        for item in all_results:
            writer.writerow(item)

    print("Saved benchmark_summary.csv")
    print("Saved benchmark_details.csv")


if __name__ == "__main__":
    test_cases = [
        {"concurrency": 1, "num_requests": 3},
        {"concurrency": 2, "num_requests": 4},
        {"concurrency": 4, "num_requests": 4},
    ]

    all_summaries = []
    all_results = []

    for case in test_cases:
        summary, results = run_benchmark(
            concurrency=case["concurrency"],
            num_requests=case["num_requests"]
        )

        all_summaries.append(summary)

        for result in results:
            result["concurrency"] = case["concurrency"]
            all_results.append(result)

    save_results(all_summaries, all_results)