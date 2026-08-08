with open(".github/workflows/upload_theme_banners.yml", "r") as f:
    content = f.read()

target1 = """            if not os.path.exists(image_path):
                print(f"Warning: {image_path} not found in repository. Skipping.")
                continue"""

replacement1 = """            if not os.path.exists(image_path):
                print(f"ERROR: {image_path} not found.")
                raise SystemExit(1)"""

target2 = """                try:
                    res_upload.raise_for_status()
                    public_url = res_upload.json().get('url')
                    print(f"Success: {theme.capitalize()} theme uploaded.")
                    print(f"Public URL: {public_url}")
                except Exception as e:
                    print(f"Error uploading {theme} theme: {e}")
                    print(res_upload.text)"""

replacement2 = """                res_upload.raise_for_status()
                public_url = res_upload.json().get('url')
                if not public_url:
                    print(f"ERROR: No public URL returned for {theme} theme.")
                    print(res_upload.text)
                    raise SystemExit(1)
                print(f"Success: {theme.capitalize()} theme uploaded.")
                print(f"Public URL: {public_url}")"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open(".github/workflows/upload_theme_banners.yml", "w") as f:
    f.write(content)
