import base64

jpeg_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
jpeg_bytes = base64.b64decode(jpeg_b64)

themes = ["red", "gold", "green", "blue", "orange"]
for t in themes:
    with open(f"app/src/main/assets/themes/theme_{t}.jpg", "wb") as f:
        f.write(jpeg_bytes)
    print(f"theme_{t}.jpg restored as placeholder")

