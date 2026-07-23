import re

with open("app/src/main/java/com/example/ui/BarcodeScannerScreen.kt", "r") as f:
    content = f.read()

content = content.replace("val previewView = PreviewView(ctx).apply {", "val previewView = PreviewView(ctx).apply {\n                        implementationMode = PreviewView.ImplementationMode.COMPATIBLE")

with open("app/src/main/java/com/example/ui/BarcodeScannerScreen.kt", "w") as f:
    f.write(content)
