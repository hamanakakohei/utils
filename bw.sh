#!/usr/bin/env bash

merge_bws(){
  BW_LIST=$1
  REF=$2
  GENOME_SIZES=$3
  PREFIX=$4
  APPTAINER=/usr/local/biotools/j/jvarkit:2024.08.25--hdfd78af_2

  singularity exec $APPTAINER bash -c "
    export JAVA_HOME=/usr/local
    bigwigmerge \
      $BW_LIST \
      -R $REF \
      -m average \
      -o ${PREFIX}.bg
  "

  bedGraphToBigWig ${PREFIX}.bg $GENOME_SIZES ${PREFIX}.bw
}
