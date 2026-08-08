import sys

with open(".github/workflows/main.yml", "r") as f:
    content = f.read()

target = """    - name: Decode Release Keystore
      run: |
        echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > release.keystore
    - name: Build with Gradle
      env:
        KEYSTORE_PATH: ${{ github.workspace }}/release.keystore
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      run: ./gradlew assembleRelease
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: app-release
        path: app/build/outputs/apk/release/app-release.apk
    - name: Get app version
      id: app_version
      run: |
        VERSION=$(grep 'versionName = ' app/build.gradle.kts | head -1 | sed 's/.*versionName = "\([^"]*\)".*/\\1/')
        echo "version=$VERSION" >> "$GITHUB_OUTPUT"
    - name: Create GitHub Release
      if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')
      uses: softprops/action-gh-release@v2
      with:
        tag_name: v${{ steps.app_version.outputs.version }}
        name: Release v${{ steps.app_version.outputs.version }}
        files: app/build/outputs/apk/release/app-release.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""

replacement = """    - name: Decode Release Keystore
      run: |
        echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > release.keystore

    - name: Calculate Next Version
      id: calc_version
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        LATEST_TAG=$(gh api repos/${{ github.repository }}/releases/latest --jq .tag_name 2>/dev/null || echo "v1.0.59")
        
        if [[ "$LATEST_TAG" =~ ^v1\.0\.([0-9]+)$ ]]; then
          PATCH="${BASH_REMATCH[1]}"
        else
          PATCH=59
        fi
        
        NEXT_PATCH=$((PATCH + 1))
        
        echo "APP_VERSION_CODE=$NEXT_PATCH" >> "$GITHUB_ENV"
        echo "APP_VERSION_NAME=1.0.$NEXT_PATCH" >> "$GITHUB_ENV"
        echo "NEXT_TAG=v1.0.$NEXT_PATCH" >> "$GITHUB_ENV"

    - name: Build with Gradle
      env:
        KEYSTORE_PATH: ${{ github.workspace }}/release.keystore
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      run: ./gradlew assembleRelease

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: app-release
        path: app/build/outputs/apk/release/app-release.apk

    - name: Create GitHub Release
      if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')
      uses: softprops/action-gh-release@v2
      with:
        tag_name: ${{ env.NEXT_TAG }}
        name: Release ${{ env.NEXT_TAG }}
        files: app/build/outputs/apk/release/app-release.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""

if target in content:
    content = content.replace(target, replacement)
    with open(".github/workflows/main.yml", "w") as f:
        f.write(content)
    print("Patched .github/workflows/main.yml successfully.")
else:
    print("Target not found in main.yml. Let me try matching with regex or split.")
