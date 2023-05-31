#!/bin/bash

TF_MODEL_FILE_EXT=".pb"
TF_MODEL_CKPT_EXT=".ckpt"

function is_tensorflow_dir {
  contents=($(ls "$1"))
  assets="assets"
  variables="variables"
  if [[ " ${contents[*]} " =~ " ${assets} " ]] ; then
    if [[ " ${contents[*]} " =~ " ${variables} " ]] ; then   # (($contents[(Ie)$variables])) ; then
      for i in $contents; do
        if [[ "$i"=="model.pb" ]] ; then
          return 0
        fi
      done
      return 1
    else
      return 1
    fi 
  else
    return 1
  fi
}

SEARCH_DIR=$1
STAGING_DIR=$2

matches=()

# Find Tensorflow directories (based on signature)
for f in $SEARCH_DIR/**/* ; do
  if [[ -d "$f" ]] ; then
    if is_tensorflow_dir $f; then
      for g in $(realpath $f)/* ; do
        matches+=$(realpath $g)
      done
    fi
  fi
done

# Find Tensorflow checkpoint (.ckpt) files
ckpt_files=$(find $SEARCH_DIR -name "*$TF_MODEL_CKPT_EXT*" -type f -not -path '*/\.*' 2>/dev/null)
matches+=$ckpt_files

# Stage files
if [ ${#matches[@]} -ne 0 ] ; then
  mkdir -p $STAGING_DIR
  for m in $matches; do
    cp -r $m $STAGING_DIR 2>/dev/null;
  done
fi

echo $STAGING_DIR
