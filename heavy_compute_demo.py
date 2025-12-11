import ray
import time
import socket
from collections import Counter

# Connect to existing Ray cluster (head node must already be running)
ray.init(address="auto")

@ray.remote
def heavy_compute(x):
    total = 0
    for i in range(800_000):
        total += (x * i) % 97
    hostname = socket.gethostname()
    return {"input": x, "hostname": hostname}

def main():
    start = time.time()

    numbers = list(range(24))  # 24 parallel tasks
    futures = [heavy_compute.remote(n) for n in numbers]
    results = ray.get(futures)

    elapsed = time.time() - start

    counts = Counter(r["hostname"] for r in results)

    print("\nTask distribution across nodes:")
    for host, count in counts.items():
        print(f"{host}: {count} tasks")

    print("\nPer-task details:")
    for r in results:
        print(f"Input {r['input']:2d} ran on {r['hostname']}")

    print(f"\nTotal runtime: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
