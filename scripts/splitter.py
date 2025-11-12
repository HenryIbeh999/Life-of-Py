from PIL import Image
from collections import deque
import os

def extract_objects(image_path, output_dir):
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    visited = [[False] * height for _ in range(width)]
    objects = []

    for y in range(height):
        for x in range(width):
            if not visited[x][y] and pixels[x, y][3] > 0:  # non-transparent
                # BFS flood-fill to find connected region
                queue = deque([(x, y)])
                visited[x][y] = True
                min_x, max_x, min_y, max_y = x, x, y, y

                while queue:
                    cx, cy = queue.popleft()
                    # Update bounds
                    min_x, max_x = min(min_x, cx), max(max_x, cx)
                    min_y, max_y = min(min_y, cy), max(max_y, cy)

                    # Neighbors
                    for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                        if 0 <= nx < width and 0 <= ny < height:
                            if not visited[nx][ny] and pixels[nx, ny][3] > 0:
                                visited[nx][ny] = True
                                queue.append((nx, ny))

                # Store bounding box
                objects.append((min_x, min_y, max_x+1, max_y+1))

    # Save cropped objects
    os.makedirs(output_dir, exist_ok=True)
    for i, box in enumerate(objects):
        cropped = img.crop(box)
        cropped.save(os.path.join(output_dir, f"{i}.png"))

    print(f"Extracted {len(objects)} objects into {output_dir}")

# Example usage
extract_objects("frame.png", "object")
