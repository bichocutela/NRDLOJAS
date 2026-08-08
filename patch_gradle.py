import re

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

# Remove firebase-storage
content = re.sub(r'\s*implementation\(libs\.firebase\.storage\)', '', content)

# Add buildConfigField for SUPABASE
build_config_str = """        buildConfigField("String", "SUPABASE_URL", "\\"${System.getenv("SUPABASE_URL") ?: ""}\\"")
        buildConfigField("String", "SUPABASE_ANON_KEY", "\\"${System.getenv("SUPABASE_ANON_KEY") ?: ""}\\"")
"""

content = re.sub(r'(defaultConfig \{[\s\S]*?)(\n\s*\})', r'\1\n' + build_config_str + r'\2', content, count=1)

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
print("Patched build.gradle.kts")
