import ray
import time
import socket
from PIL import Image, ImageFilter
from collections import Counter
import os

# Connect to the existing Ray cluster
ray.init(address="auto")

@ray.remote
def process_image(image_path: str) -> dict:
    """Load an image, blur it, save it with a hostname-based name."""
    hostname = socket.gethostname()
    img = Image.open(image_path)

    # Apply a realistic blur filter
    processed = img.filter(ImageFilter.GaussianBlur(radius=5))

    # Save output with hostname in filename
    output_filename = f"processed_{hostname}_{os.path.basename(image_path)}"
    output_path = os.path.join(os.path.dirname(image_path), output_filename)
    processed.save(output_path)

    return {"input": image_path, "output": output_path, "hostname": hostname}

def main() -> None:
    start = time.time()

    # Adjust these paths/filenames as needed
    base_dir = "/home/azureuser/images"
    images = [
        os.path.join(base_dir, "1.jpg"),
        os.path.join(base_dir, "2.jpg"),
        os.path.join(base_dir, "3.jpg"),
        os.path.join(base_dir, "4.jpg"),
        os.path.join(base_dir, "5.jpg"),
        os.path.join(base_dir, "6.jpg"),
    ]

    futures = [process_image.remote(img) for img in images]
    results = ray.get(futures)

    elapsed = time.time() - start

    counts = Counter(r["hostname"] for r in results)

    print("\nImage processing distribution across nodes:")
    for host, count in counts.items():
        print(f"{host}: {count} images processed")

    print("\nPer-image details:")
    for r in results:
        print(f"{r['input']} → {r['hostname']} → saved as {r['output']}")

    print(f"\nTotal runtime for {len(images)} images: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
