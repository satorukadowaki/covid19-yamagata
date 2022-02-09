#!/bin/sh
python -m table_ocr.extract_tables yamagata_table.jpg  | grep table > ./extracted-tables.txt
cat ./extracted-tables.txt | xargs -I{} python -m table_ocr.extract_cells {} | grep cells > ./extracted-cells.txt
cat ./extracted-cells.txt | xargs -I{} python -m table_ocr.ocr_image {}

for image in $(cat ./extracted-tables.txt); do
    dir=$(dirname $image)
    python -m table_ocr.ocr_to_csv $(find $dir/cells -name "*.txt")
done
