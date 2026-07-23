import re
import glob

for filepath in glob.glob("app/src/main/res/mipmap-anydpi-v26/*.xml"):
    with open(filepath, "r") as f:
        content = f.read()
    
    content = re.sub(r'<monochrome[^>]*/>', '', content)
    
    with open(filepath, "w") as f:
        f.write(content)
