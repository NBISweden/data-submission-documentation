#!/usr/bin/env python3
"""
fix_geseq_gff.py
Generalized script to fix GeSeq/Chloe GFF3 files for EMBLmyGFF3 conversion.

Fixes applied:
1. Prioritizes 'gene' features over child features (exon/CDS) at identical start
   coordinates so EMBLmyGFF3 can merge multi-exon CDS features into join(...) records.
2. Fixes Chloe Parent ID mismatches (_1_2 vs _1_1) across all spliced genes (pafI, rpoC1, ndhB, etc.).
3. Generates exactly 2 rps12 gene entries (1 per locus) to preserve locus_tag indexing.
4. Replaces Column 3 with the value of 'gbkey'.
5. Removes 'region' and 'source' lines so locus_tag indexing starts at 1.
6. Sets Column 8 (phase) to '.' for non-CDS features.
7. Coordinate-sorts all features by genomic position and strict hierarchy.
"""

import sys
import os
import glob

def parse_attributes(attr_str):
    attrs = {}
    for item in attr_str.split(';'):
        if '=' in item:
            k, v = item.split('=', 1)
            attrs[k] = v
    return attrs

def format_attributes(attrs):
    return ";".join(f"{k}={v}" for k, v in attrs.items())

def extract_and_build_rps12(rps12_raw_features, seqid):
    """
    Dynamically extracts rps12 coordinates and generates EXACTLY 2 gene
    features (one for rps12_1 and one for rps12_2) to prevent locus tag inflation.
    """
    exon_cds_parts = []
    intron_parts = []

    for f in rps12_raw_features:
        ftype = f['ftype']
        start = f['start']
        end = f['end']
        strand = f['strand']
        length = end - start + 1

        if ftype in ['exon', 'CDS']:
            if not any(p['start'] == start and p['end'] == end for p in exon_cds_parts):
                exon_cds_parts.append({'start': start, 'end': end, 'strand': strand, 'length': length})
        elif ftype == 'intron':
            if not any(i['start'] == start and i['end'] == end for i in intron_parts):
                intron_parts.append({'start': start, 'end': end, 'strand': strand, 'length': length})

    exon1_candidates = [p for p in exon_cds_parts if 100 <= p['length'] <= 130]
    exon2_candidates = [p for p in exon_cds_parts if 200 <= p['length'] <= 250]
    exon3_candidates = [p for p in exon_cds_parts if 15 <= p['length'] <= 40]

    if not exon1_candidates or len(exon2_candidates) < 2 or len(exon3_candidates) < 2:
        return rps12_raw_features

    ex1 = exon1_candidates[0]
    exon2_candidates.sort(key=lambda x: x['start'])
    exon3_candidates.sort(key=lambda x: x['start'])

    clusters = []
    for e2 in exon2_candidates:
        e3_match = min(exon3_candidates, key=lambda e3: abs(e3['start'] - e2['start']))
        c_strand = e2['strand']
        intron_match = [i for i in intron_parts if min(e2['start'], e3_match['start']) <= i['start'] <= max(e2['end'], e3_match['end'])]
        if intron_match:
            c_strand = intron_match[0]['strand']
        elif e3_match['strand'] in ['+', '-']:
            c_strand = e3_match['strand']

        clusters.append({
            'e2': e2,
            'e3': e3_match,
            'intron': intron_match[0] if intron_match else None,
            'strand': c_strand
        })

    len1 = ex1['length']
    rem1 = len1 % 3
    phase2 = (3 - rem1) % 3

    generated = []
    for idx, c in enumerate(clusters, 1):
        gene_id = f"gene-chloe_rps12_{idx}"
        cds_id = f"cds-chloe_rps12_{idx}"

        len2 = c['e2']['length']
        rem2 = (rem1 + len2) % 3
        phase3 = (3 - rem2) % 3

        gene_attrs = {
            'ID': gene_id,
            'gbkey': 'gene',
            'gene': 'rps12',
            'gene_biotype': 'protein_coding',
            'exception': 'trans-splicing'
        }

        # Single gene feature per rps12 copy (spanning the IR cluster locus)
        ir_start = min(c['e2']['start'], c['e3']['start'])
        ir_end = max(c['e2']['end'], c['e3']['end'])
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'gene',
            'start': ir_start, 'end': ir_end, 'score': '.',
            'strand': c['strand'], 'phase': '.', 'attrs': gene_attrs
        })

        cds_attrs = {
            'ID': cds_id,
            'Parent': gene_id,
            'gbkey': 'CDS',
            'gene': 'rps12',
            'exception': 'trans-splicing'
        }

        # CDS 1 (Exon 1 in LSC)
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'CDS',
            'start': ex1['start'], 'end': ex1['end'], 'score': '.',
            'strand': ex1['strand'], 'phase': '0', 'attrs': cds_attrs
        })

        # CDS 2 (Exon 2 in IR)
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'CDS',
            'start': c['e2']['start'], 'end': c['e2']['end'], 'score': '.',
            'strand': c['strand'], 'phase': str(phase2), 'attrs': cds_attrs
        })

        # CDS 3 (Exon 3 in IR)
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'CDS',
            'start': c['e3']['start'], 'end': c['e3']['end'], 'score': '.',
            'strand': c['strand'], 'phase': str(phase3), 'attrs': cds_attrs
        })

        # Exon features
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'exon',
            'start': ex1['start'], 'end': ex1['end'], 'score': '.',
            'strand': ex1['strand'], 'phase': '.',
            'attrs': {'ID': f"exon-chloe_rps12_{idx}_1", 'Parent': gene_id, 'gbkey': 'exon', 'gene': 'rps12'}
        })
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'exon',
            'start': c['e2']['start'], 'end': c['e2']['end'], 'score': '.',
            'strand': c['strand'], 'phase': '.',
            'attrs': {'ID': f"exon-chloe_rps12_{idx}_2", 'Parent': gene_id, 'gbkey': 'exon', 'gene': 'rps12'}
        })
        generated.append({
            'seqid': seqid, 'source': 'Chloe', 'ftype': 'exon',
            'start': c['e3']['start'], 'end': c['e3']['end'], 'score': '.',
            'strand': c['strand'], 'phase': '.',
            'attrs': {'ID': f"exon-chloe_rps12_{idx}_3", 'Parent': gene_id, 'gbkey': 'exon', 'gene': 'rps12'}
        })

        # Intron
        if c['intron']:
            generated.append({
                'seqid': seqid, 'source': 'Chloe', 'ftype': 'intron',
                'start': c['intron']['start'], 'end': c['intron']['end'], 'score': '.',
                'strand': c['strand'], 'phase': '.',
                'attrs': {'ID': f"intron-chloe_rps12_{idx}_1", 'Parent': gene_id, 'gbkey': 'intron', 'gene': 'rps12'}
            })

    return generated

def fix_gff(input_file, output_file):
    lines = []
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

    # Pass 1: Build set of all defined gene IDs
    gene_ids = set()
    for l in lines:
        parts = l.split('\t')
        if len(parts) >= 9 and parts[2] == 'gene':
            attrs = parse_attributes(parts[8])
            if 'ID' in attrs:
                gene_ids.add(attrs['ID'])

    parsed_features = []
    rps12_raw_features = []
    seqid_found = "seq"

    # Pass 2: Parse features and repair Chloe Parent mismatches (_1_2 -> _1_1)
    for line in lines:
        parts = line.split('\t')
        if len(parts) < 9:
            continue

        seqid, source, ftype, start_s, end_s, score, strand, phase, attr_str = parts
        seqid_found = seqid
        attrs = parse_attributes(attr_str)
        gbkey = attrs.get('gbkey', ftype)

        if ftype in ['source', 'region'] or gbkey == 'source':
            continue

        if 'rps12' in attrs.get('gene', '') or 'rps12' in attrs.get('ID', '') or 'rps12' in attrs.get('Parent', ''):
            rps12_raw_features.append({
                'seqid': seqid, 'source': source, 'ftype': gbkey,
                'start': int(start_s), 'end': int(end_s), 'score': score,
                'strand': strand, 'phase': phase, 'attrs': attrs
            })
            continue

        # Repair Chloe Parent mismatch for multi-exon features (e.g. pafI, rpoC1, ndhB)
        if 'Parent' in attrs:
            parent = attrs['Parent']
            if parent not in gene_ids:
                if parent.rsplit('_', 1)[0] + '_1' in gene_ids:
                    attrs['Parent'] = parent.rsplit('_', 1)[0] + '_1'
                elif parent + '_1' in gene_ids:
                    attrs['Parent'] = parent + '_1'

        new_ftype = gbkey
        new_phase = phase if new_ftype == 'CDS' else '.'

        parsed_features.append({
            'seqid': seqid,
            'source': source,
            'ftype': new_ftype,
            'start': int(start_s),
            'end': int(end_s),
            'score': score,
            'strand': strand,
            'phase': new_phase,
            'attrs': attrs
        })

    # Process rps12 features dynamically
    if rps12_raw_features:
        clean_rps12_features = extract_and_build_rps12(rps12_raw_features, seqid_found)
        parsed_features.extend(clean_rps12_features)

    # STRICT HIERARCHY SORTING ORDER:
    # 'gene' MUST have the lowest order index so it sorts BEFORE exons/CDSs starting at the same position.
    feature_order = {
        'gene': 0,
        'tRNA': 1,
        'rRNA': 1,
        'mRNA': 2,
        'exon': 3,
        'CDS': 4,
        'intron': 5,
        'repeat_region': 6,
        'misc_feature': 7
    }

    # CRITICAL FIX: Sort by (seqid, start, feature_order, end)
    # Placing feature_order BEFORE end guarantees 'gene' is written before its child features!
    parsed_features.sort(key=lambda x: (
        x['seqid'],
        x['start'],
        feature_order.get(x['ftype'], 9),
        x['end']
    ))

    with open(output_file, 'w') as out:
        out.write("##gff-version 3\n")
        for f in parsed_features:
            attr_text = format_attributes(f['attrs'])
            out.write(f"{f['seqid']}\t{f['source']}\t{f['ftype']}\t{f['start']}\t{f['end']}\t{f['score']}\t{f['strand']}\t{f['phase']}\t{attr_text}\n")

    print(f"Fixed and sorted: {input_file} -> {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 fix_geseq_gff.py input.gff or python3 fix_geseq_gff.py *.gff")
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        files.extend(glob.glob(arg))

    for gff_file in files:
        if gff_file.endswith('_fixed.gff'):
            continue
        out_file = os.path.splitext(gff_file)[0] + '_fixed.gff'
        fix_gff(gff_file, out_file)
