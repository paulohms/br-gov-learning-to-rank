#! /bin/bash

workdir=$PATH

cd $workdir/datasets

for folder in *; do

  echo "Directory -> $folder"

  cd $workdir/datasets/$folder

  for file in *; do

    # This file contains all information about dataset and doesn't need be parsed
    if [ "dataset.json" == "$file" ]; then
        continue
    fi

    echo "=====> File -> $file"

    # Apply apache tika parser
    java -jar $workdir/tika-app-1.24.jar --text $file >> metadata-temp.txt

  done

  # Clean text
  sed -e "s/[0-9*]//g" -e "s/\t//g" -e "s/[[:punct:]]\+/ /g" -e "s/data\|valor//g" -e "s/./\L&/g" -e "/^[[:space:]]*$/d" metadata-temp.txt > metadata.txt

done