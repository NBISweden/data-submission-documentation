#!/usr/bin/bash

GFF="/home/yvonnek/Gomphus-clavatus/gomcla.gff3"

echo -e "NBISG00000001526\nNBISG00000001972\nNBISG00000006661" > remove_genes.txt
source activate agat


agat_sp_filter_feature_from_kill_list.pl -f $GFF --kl remove_genes.txt -o gomcla_filtered.gff3
