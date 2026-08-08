import sys

with open(".github/workflows/main.yml", "r") as f:
    content = f.read()

target = """    - name: Create GitHub Release
      if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')
      uses: softprops/action-gh-release@v2
      with:
        tag_name: v1.0.${{ github.run_number }}
        name: Release v1.0.${{ github.run_number }}
        files: app/build/outputs/apk/release/app-release.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""

replacement = """    - name: Extract Version
      id: extract_version
      run: |
        VERSION=$(grep 'versionName' app/build.gradle.kts | awk -F '"' '{print $2}')
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Create GitHub Release
      if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master')
      uses: softprops/action-gh-release@v2
      with:
        tag_name: v${{ steps.extract_version.outputs.version }}
        name: Release v${{ steps.extract_version.outputs.version }}
        files: app/build/outputs/apk/release/app-release.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""

if target in content:
    content = content.replace(target, replacement)
    with open(".github/workflows/main.yml", "w") as f:
        f.write(content)
    print("Patched main.yml successfully.")
else:
    print("Target not found in main.yml.")
