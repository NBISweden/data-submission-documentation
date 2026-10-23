#!/usr/bin/env python3
"""
fix_geseq_gff.py

Fixes GeSeq GFF3 files for direct EMBLmyGFF3 conversion:
1. Strips/comments top-level 'region' and 'source' lines preceding the first gene.
2. Directs CDS orphan lines to their parent gene by injecting 'Parent=gene-...'.
3. Sets column 8 (phase) to '.' for all non-CDS features.
4. Calculates valid exon reading frame phases (0, 1, 2) for all CDS features.
5. Sorts features by seqid, start coordinate, end coordinate, and feature hierarchy.
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

    # Pass 1: Parse CDS features grouped by ID/parent to compute correct phases
    cds_groups = {}
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 9 and parts[2] == 'CDS':
            seqid, source, ftype, start, end, score, strand, phase, attrs_str = parts
            attrs = parse_attributes(attrs_str)
            cds_id = attrs.get('ID')
            if cds_id:
                if cds_id not in cds_groups:
                    cds_groups[cds_id] = []
                cds_groups[cds_id].append({
                    'start': int(start),
                    'end': int(end),
                    'strand': strand
                })

    # Calculate frame phase for each CDS exon
    cds_phases = {}
    for cds_id, exons in cds_groups.items():
        strand = exons[0]['strand']
        if strand == '-':
            sorted_exons = sorted(exons, key=lambda x: x['start'], reverse=True)
        else:
            sorted_exons = sorted(exons, key=lambda x: x['start'])

        current_phase = 0
        for exon in sorted_exons:
            key = (cds_id, exon['start'], exon['end'])
            cds_phases[key] = str(current_phase)
            exon_length = exon['end'] - exon['start'] + 1
            current_phase = (3 - ((exon_length - current_phase) % 3)) % 3

    # Pass 2: Clean and format lines
    cleaned_records = []
    seen_first_gene = False

    for line in lines:
        if line.startswith('#') or not line.strip():
            continue

        parts = line.strip().split('\t')
        if len(parts) < 9:
            continue

        seqid, source, ftype, start, end, score, strand, phase, attrs_str = parts
        attrs = parse_attributes(attrs_str)

        # 1. Skip top-level region/source features preceding first gene
        if not seen_first_gene and ftype in ('region', 'source'):
            continue

        if ftype == 'gene':
            seen_first_gene = True

        # 2. Fix Column 8 (Phase)
        if ftype != 'CDS':
            phase = '.'
        else:
            cds_id = attrs.get('ID')
            key = (cds_id, int(start), int(end))
            phase = cds_phases.get(key, '0')

        # 3. Inject Parent attribute into CDS features if missing
        if ftype == 'CDS':
            cds_id = attrs.get('ID', '')
            if 'Parent' not in attrs and cds_id.startswith('cds-'):
                parent_gene_id = 'gene-' + cds_id[4:]
                attrs['Parent'] = parent_gene_id
            attrs_str = format_attributes(attrs)

        cleaned_records.append({
            'seqid': seqid,
            'source': source,
            'ftype': ftype,
            'start': int(start),
            'end': int(end),
            'score': score,
            'strand': strand,
            'phase': phase,
            'attrs_str': attrs_str,
            # Feature tier sorting precedence (genes before CDS/exon children at same coordinate)
            'type_order': 0 if ftype == 'gene' else (1 if ftype == 'exon' else 2)
        })

    # Pass 3: Coordinate & Hierarchy Sorting
    sorted_records = sorted(
        cleaned_records, 
        key=lambda x: (x['seqid'], x['start'], x['type_order'], x['end'])
    )

    # Pass 4: Write formatted output
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write("##gff-version 3\n")
        for rec in sorted_records:
            line_str = f"{rec['seqid']}\t{rec['source']}\t{rec['ftype']}\t{rec['start']}\t{rec['end']}\t{rec['score']}\t{rec['strand']}\t{rec['phase']}\t{rec['attrs_str']}\n"
            fout.write(line_str)

    print(f"Fixed & sorted: {input_path} -> {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fix GeSeq GFF files and coordinate-sort for EMBLmyGFF3.")
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
    