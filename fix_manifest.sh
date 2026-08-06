sed -i 's/<application/<application/g' app/src/main/AndroidManifest.xml
sed -i '/<meta-data/d' app/src/main/AndroidManifest.xml
sed -i '/android:value="barcode" \/>/d' app/src/main/AndroidManifest.xml
sed -i '/android:name="com.google.mlkit.vision.DEPENDENCIES"/d' app/src/main/AndroidManifest.xml

sed -i '/<application/a \
        <meta-data\
            android:name="com.google.mlkit.vision.DEPENDENCIES"\
            android:value="barcode" />' app/src/main/AndroidManifest.xml
