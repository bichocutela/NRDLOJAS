awk '
{
    if ($0 ~ /var updateInfo by remember/) {
        skip = 1
    }
    if ($0 ~ /AlertDialog\(/ && skip == 1) {
        # continue skipping
    }
    
    if (skip == 1) {
        if ($0 ~ /}\)/ && prev_line ~ /Mais tarde/) {
            skip = 0
            getline
            getline
            continue
        }
        prev_line = $0
        continue
    }
    print
}' app/src/main/java/com/example/MainActivity.kt > app/src/main/java/com/example/MainActivity.kt.new
mv app/src/main/java/com/example/MainActivity.kt.new app/src/main/java/com/example/MainActivity.kt
