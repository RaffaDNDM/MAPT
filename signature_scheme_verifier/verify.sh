for file in *.apk; do
    [ -f "$file" ] || continue
    echo "\n$file\n"
    apksigner verify -verbose $file
done
