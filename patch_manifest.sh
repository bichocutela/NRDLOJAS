sed -i '/<application/a \
        <provider\
            android:name="com.google.firebase.provider.FirebaseInitProvider"\
            android:authorities="${applicationId}.firebaseinitprovider"\
            tools:node="remove" />' app/src/main/AndroidManifest.xml
sed -i '/<manifest/a \
    xmlns:tools="http://schemas.android.com/tools"' app/src/main/AndroidManifest.xml
