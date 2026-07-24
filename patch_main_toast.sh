cat app/src/main/java/com/example/MainActivity.kt | awk '
/import androidx.compose.ui.Modifier/ {
    print $0
    print "import android.widget.Toast"
    print "import androidx.compose.ui.platform.LocalContext"
    next
}
/setContent \{/ {
    print $0
    if (in_set == 0) {
        in_set = 1
        print "            val context = LocalContext.current"
        print "            LaunchedEffect(Unit) {"
        print "                viewModel.syncMessage.collect { msg ->"
        print "                    Toast.makeText(context, msg, Toast.LENGTH_LONG).show()"
        print "                }"
        print "            }"
    }
    next
}
{ print $0 }
' > MainActivity_new.kt
mv MainActivity_new.kt app/src/main/java/com/example/MainActivity.kt
