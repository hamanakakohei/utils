#!/usr/bin/env bash

merge_bws(){
  BW_LIST=$1
  REF=$2
  GENOME_SIZES=$3
  INTERVAL=$4 # chr1:234-567
  PREFIX=$5
  APP1=/usr/local/biotools/j/jvarkit:2024.08.25--hdfd78af_2
  APP2=/usr/local/biotools/u/ucsc-bedgraphtobigwig:482--hdc0a859_0
  
  singularity exec $APP1 bash -c "
    export JAVA_HOME=/usr/local
    bigwigmerge \
      $BW_LIST \
      -R $REF \
      -m average \
      -r $INTERVAL \
      -o ${PREFIX}.bg
  "

  singularity exec $APP2 bash -c "
    bedGraphToBigWig \
      ${PREFIX}.bg \
      $GENOME_SIZES \
      ${PREFIX}.bw  
  "
}

subset_bw(){
  PREFIX=$1
  CHR=$2
  STA=$3
  END=$4
  GENOME_SIZES=$5
  APP1=/usr/local/biotools/u/ucsc-bigwigtobedgraph:482--h0b57e2e_0
  APP2=/usr/local/biotools/u/ucsc-bedgraphtobigwig:482--hdc0a859_0

  singularity exec $APP1 bash -c "
    bigWigToBedGraph \
      ${PREFIX}.bw \
      ${PREFIX}.region.bg \
      -chrom=$CHR \
      -start=$STA \
      -end=$END
  "
  
  singularity exec $APP2 bash -c "
    bedGraphToBigWig \
      ${PREFIX}.region.bg \
      $GENOME_SIZES \
      ${PREFIX}.region.bw  
  "
}
