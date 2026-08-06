sed -i '/<uses-permission android:name="android.permission.POST_NOTIFICATIONS" \/>/a \    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />' app/src/main/AndroidManifest.xml
sed -i '/<application/a \
        <provider\
            android:name="androidx.core.content.FileProvider"\
            android:authorities="${applicationId}.fileprovider"\
            android:exported="false"\
            android:grantUriPermissions="true">\
            <meta-data\
                android:name="android.support.FILE_PROVIDER_PATHS"\
                android:resource="@xml/file_paths" />\
        </provider>' app/src/main/AndroidManifest.xml
