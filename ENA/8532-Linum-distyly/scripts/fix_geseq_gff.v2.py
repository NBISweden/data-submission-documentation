#!/usr/bin/env python3
"""
fix_geseq_gff.py

Fixes GeSeq GFF3 files for EMBLmyGFF3:
1. Strips region/source lines so locus tag indexing starts at 1 and /organelle is generated.
2. Creates intermediate mRNA features to force multi-segment CDS joining (join(complement(...))).
3. Recalculates CDS phases and coordinate-sorts features.
"""

import sys
import os
import argparse

def parse_attributes(attr_str):
    attrs = {}
    for item in attr_str.split(';'):
        if '=' in item:
            k, v = item.split('=', 1)
            attrs[k] = v
    return attrs

def format_attributes(attr_dict):
    return ';'.join([f"{k}={v}" for k, v in attr_dict.items()])

def fix_gff_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    genes = {}
    cdss = {}
    exons = {}
    other_features = []

    # Pass 1: Parse features
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) < 9:
            continue

        seqid, source, ftype, start, end, score, strand, phase, attrs_str = parts
        attrs = parse_attributes(attrs_str)

        # 1. Strip top-level region/source features completely
        if ftype in ('region', 'source'):
            continue

        start_i, end_i = int(start), int(end)

        if ftype == 'gene':
            gene_id = attrs.get('ID')
            genes[gene_id] = {
                'seqid': seqid, 'source': source, 'ftype': 'gene',
                'start': start_i, 'end': end_i, 'score': score,
                'strand': strand, 'phase': '.', 'attrs': attrs
            }
        elif ftype == 'CDS':
            cds_id = attrs.get('ID')
            if cds_id not in cdss:
                cdss[cds_id] = []
            cdss[cds_id].append({
                'seqid': seqid, 'source': source, 'ftype': 'CDS',
                'start': start_i, 'end': end_i, 'score': score,
                'strand': strand, 'phase': phase, 'attrs': attrs
            })
        elif ftype == 'exon':
            parent = attrs.get('Parent')
            if parent not in exons:
                exons[parent] = []
            exons[parent].append({
                'seqid': seqid, 'source': source, 'ftype': 'exon',
                'start': start_i, 'end': end_i, 'score': score,
                'strand': strand, 'phase': '.', 'attrs': attrs
            })
        else:
            other_features.append({
                'seqid': seqid, 'source': source, 'ftype': ftype,
                'start': start_i, 'end': end_i, 'score': score,
                'strand': strand, 'phase': phase, 'attrs': attrs
            })

    output_records = []

    # Pass 2: Reconstruct hierarchy with intermediate mRNA
    for gene_id, gdata in genes.items():
        output_records.append(gdata)

        # Construct mRNA ID
        mrna_id = gene_id.replace('gene-', 'mrna-', 1) if gene_id.startswith('gene-') else f"mrna-{gene_id}"
        
        mrna_attrs = gdata['attrs'].copy()
        mrna_attrs['ID'] = mrna_id
        mrna_attrs['Parent'] = gene_id

        output_records.append({
            'seqid': gdata['seqid'], 'source': gdata['source'], 'ftype': 'mRNA',
            'start': gdata['start'], 'end': gdata['end'], 'score': gdata['score'],
            'strand': gdata['strand'], 'phase': '.', 'attrs': mrna_attrs
        })

        # Match CDS segments to gene
        target_cds_id = gene_id.replace('gene-', 'cds-', 1) if gene_id.startswith('gene-') else f"cds-{gene_id}"
        matching_cds = cdss.get(target_cds_id, [])

        # Calculate phase for CDS segments
        if gdata['strand'] == '-':
            sorted_cds = sorted(matching_cds, key=lambda x: x['start'], reverse=True)
        else:
            sorted_cds = sorted(matching_cds, key=lambda x: x['start'])

        curr_phase = 0
        for seg in sorted_cds:
            seg['phase'] = str(curr_phase)
            seg_len = seg['end'] - seg['start'] + 1
            curr_phase = (3 - ((seg_len - curr_phase) % 3)) % 3

            seg_attrs = seg['attrs'].copy()
            seg_attrs['Parent'] = mrna_id  # Attach CDS to mRNA
            seg['attrs'] = seg_attrs
            output_records.append(seg)

        # Attach exons to mRNA if present
        if gene_id in exons:
            for ex in exons[gene_id]:
                ex_attrs = ex['attrs'].copy()
                ex_attrs['Parent'] = mrna_id
                ex['attrs'] = ex_attrs
                output_records.append(ex)

    for oth in other_features:
        output_records.append(oth)

    # Sort records
    type_priority = {'gene': 0, 'mRNA': 1, 'exon': 2, 'CDS': 3}
    sorted_records = sorted(
        output_records,
        key=lambda x: (x['seqid'], x['start'], type_priority.get(x['ftype'], 4), x['end'])
    )

    # Write output
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write("##gff-version 3\n")
        for rec in sorted_records:
            attr_str = format_attributes(rec['attrs'])
            line_str = f"{rec['seqid']}\t{rec['source']}\t{rec['ftype']}\t{rec['start']}\t{rec['end']}\t{rec['score']}\t{rec['strand']}\t{rec['phase']}\t{attr_str}\n"
            fout.write(line_str)

    print(f"Fixed & generated: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fix GeSeq GFF for EMBLmyGFF3 multi-exon joining.")
    parser.add_argument("-i", "--input", help="Input GFF3 file")
    parser.add_argument("-o", "--output", help="Output GFF3 file")
    parser.add_argument("files", nargs="*", help="Batch GFF3 files (e.g. *.gff)")

    args = parser.parse_args()

    if args.input and args.output:
        fix_gff_file(args.input, args.output)
    elif args.files:
        for filepath in args.files:
            if os.path.isfile(filepath):
                base_name = os.path.splitext(filepath)[0]
                out_path = f"{base_name}_fixed.gff"
                fix_gff_file(filepath, out_path)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
