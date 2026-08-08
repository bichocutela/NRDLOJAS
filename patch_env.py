import sys

with open(".github/workflows/main.yml", "r") as f:
    content = f.read()

target = """    - name: Build with Gradle
      env:
        KEYSTORE_PATH: ${{ github.workspace }}/release.keystore
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      run: ./gradlew assembleRelease"""

replacement = """    - name: Build with Gradle
      env:
        KEYSTORE_PATH: ${{ github.workspace }}/release.keystore
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
        SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
      run: ./gradlew assembleRelease"""

if target in content:
    content = content.replace(target, replacement)
    with open(".github/workflows/main.yml", "w") as f:
        f.write(content)
    print("Patched .github/workflows/main.yml successfully.")
else:
    print("Target not found in main.yml.")
