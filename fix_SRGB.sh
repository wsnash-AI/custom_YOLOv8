#!/bin/bash

# Accept the path as an argument
path=$1
base=$(PWD)

# Loop over the directories
for folder in "$path"/{test,train,val}; do
  # Run the command
  echo "Processing $folder..."
  cd $folder/images
  magick mogrify *.png .
  cd $base
done