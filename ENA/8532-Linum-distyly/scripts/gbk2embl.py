#!/usr/bin/env python3
"""
Convert GeSeq GenBank (.gb / .gbk) files directly into ENA-compliant EMBL (.embl) format 
for submission via Webin-CLI.
"""

import sys
import os
import re
import argparse

# Fixed taxonomy structure for Linum
CUSTOM_OC_LINES = [
    "OC   cellular organisms; Eukaryota; Viridiplantae; Streptophyta; Streptophytina;",
    "OC   Embryophyta; Tracheophyta; Euphyllophyta; Spermatophyta; Magnoliopsida;",
    "OC   Mesangiospermae; eudicotyledons; Gunneridae; Pentapetalae; rosids; fabids;",
    "OC   Malpighiales; Linaceae; Linum."
]


def extract_organelle_from_gbk(lines):
    """Extracts /organelle qualifier from GenBank source feature."""
    in_features = False
    in_source = False
    for line in lines:
        if line.startswith("FEATURES"):
            in_features = True
            continue
        if in_features:
            if line.startswith("     source"):
                in_source = True
                continue
            elif line.startswith("     ") and not line.startswith("                     "):
                in_source = False
            if in_source and "/organelle=" in line:
                m = re.search(r'/organelle="([^"]+)"', line)
                if m:
                    return m.group(1)
    return "plastid:chloroplast"


def parse_genbank_features(feature_lines):
    """
    Parses raw GenBank feature table lines into structured feature records,
    handling multi-line locations and multi-line qualifiers.
    """
    features = []
    current_ft = None

    for line in feature_lines:
        line_str = line.rstrip("\r\n")
        if not line_str.strip():
            continue

        # Check for new feature header (starts at column 5 in GenBank, e.g. '     gene            ')
        if len(line_str) > 5 and not line_str.startswith("                     "):
            ft_key = line_str[5:21].strip()
            loc_str = line_str[21:].strip()

            current_ft = {
                "key": ft_key,
                "location_lines": [loc_str],
                "qualifiers": []
            }
            features.append(current_ft)
        elif current_ft is not None:
            sub_str = line_str[21:].strip() if len(line_str) >= 21 else line_str.strip()
            if not sub_str:
                continue

            if sub_str.startswith("/"):
                current_ft["qualifiers"].append(sub_str)
            else:
                # If no qualifiers exist yet, it's a multi-line location continuation
                if not current_ft["qualifiers"]:
                    current_ft["location_lines"].append(sub_str)
                else:
                    # Append to previous qualifier value
                    current_ft["qualifiers"][-1] += " " + sub_str

    return features


def wrap_embl_qualifier(qual_str, max_len=79):
    """Wraps qualifier string so each line with 'FT                   ' prefix fits max_len."""
    indent = "FT                   "
    avail_width = max_len - len(indent)

    if len(qual_str) <= avail_width:
        return [f"{indent}{qual_str}"]

    words = qual_str.split(" ")
    lines = []
    curr_line = words[0]

    for word in words[1:]:
        if len(curr_line) + 1 + len(word) <= avail_width:
            curr_line += " " + word
        else:
            lines.append(f"{indent}{curr_line}")
            curr_line = word

    if curr_line:
        lines.append(f"{indent}{curr_line}")

    return lines


def convert_gbk_to_embl(gbk_path, embl_path, project_id, locus_tag_prefix, species_name, entry_name=None, topology="circular", molecule="genomic DNA", data_class="STD"):
    with open(gbk_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    organelle = extract_organelle_from_gbk(lines)
    clean_entry_name = (entry_name if entry_name else locus_tag_prefix).lstrip("_")

    in_comment = False
    in_features = False
    in_origin = False

    comments_raw = []
    features_raw = []
    raw_seq = []

    for line in lines:
        if line.startswith("COMMENT"):
            in_comment = True
            val = line[12:].strip() if len(line) > 12 else ""
            if val:
                comments_raw.append(val)
        elif in_comment and line.startswith("            "):
            comments_raw.append(line.strip())
        elif line.startswith("FEATURES"):
            in_comment = False
            in_features = True
        elif line.startswith("ORIGIN"):
            in_features = False
            in_origin = True
        elif line.startswith("//"):
            break
        elif in_features:
            features_raw.append(line)
        elif in_origin:
            raw_seq.append(re.sub(r"[\d\s]", "", line))

    seq_str = "".join(raw_seq).lower()
    seq_len = len(seq_str)

    a_cnt = seq_str.count("a")
    c_cnt = seq_str.count("c")
    g_cnt = seq_str.count("g")
    t_cnt = seq_str.count("t")
    other_cnt = seq_len - (a_cnt + c_cnt + g_cnt + t_cnt)

    embl_lines = []

    # 1. ID Line
    embl_lines.append(f"ID   XXX; XXX; {topology}; {molecule}; {data_class}; PLN; {seq_len} BP.")
    embl_lines.append("XX")

    # 2. Accession Lines
    embl_lines.append("AC   XXX;")
    embl_lines.append("XX")
    embl_lines.append(f"AC * _{clean_entry_name}")
    embl_lines.append("XX")

    # 3. PR Line (ENA Project ID)
    proj_formatted = project_id if project_id.startswith("PRJ") else f"PRJEB{project_id}"
    embl_lines.append(f"PR   Project:{proj_formatted};")
    embl_lines.append("XX")

    # 4. DE & KW Lines
    embl_lines.append(f"DE   {species_name} chloroplast genome.")
    embl_lines.append("XX")
    embl_lines.append("KW   .")
    embl_lines.append("XX")

    # 5. OS, OC, OG Lines
    embl_lines.append(f"OS   {species_name}")
    embl_lines.extend(CUSTOM_OC_LINES)
    embl_lines.append(f"OG   {organelle}")
    embl_lines.append("XX")

    # 6. CC Lines (GeSeq Comments)
    if comments_raw:
        for c in comments_raw:
            embl_lines.append(f"CC   {c}")
        embl_lines.append("XX")

    # 7. Features Header
    embl_lines.append("FH   Key             Location/Qualifiers")
    embl_lines.append("FH")

    parsed_features = parse_genbank_features(features_raw)

    tag_counter = 0
    current_locus_tag = None

    for ft in parsed_features:
        ft_key = ft["key"]
        loc_lines = ft["location_lines"]
        quals = ft["qualifiers"]

        # Manage locus_tag increments across gene -> subfeature hierarchies
        if ft_key == "gene":
            tag_counter += 1
            current_locus_tag = f"{locus_tag_prefix}_LOCUS{tag_counter}"
        elif ft_key in ["CDS", "tRNA", "rRNA", "mRNA", "ncRNA", "exon"]:
            if not current_locus_tag:
                tag_counter += 1
                current_locus_tag = f"{locus_tag_prefix}_LOCUS{tag_counter}"
        elif ft_key == "source":
            current_locus_tag = None

        # Print Feature Key + ALL location lines first
        first_loc = loc_lines[0] if loc_lines else ""
        embl_lines.append(f"FT   {ft_key:<15} {first_loc}")
        for extra_loc in loc_lines[1:]:
            embl_lines.append(f"FT                   {extra_loc}")

        # Insert /locus_tag right after all location lines
        if ft_key in ["gene", "CDS", "tRNA", "rRNA", "mRNA", "ncRNA"]:
            embl_lines.append(f'FT                   /locus_tag="{current_locus_tag}"')

        cds_has_transl_table = False
        cds_has_codon_start = False

        # Process qualifiers
        for q in quals:
            if q.startswith("/locus_tag="):
                continue

            # Convert unrecognised GeSeq qualifiers to /note
            if q.startswith("/annotator="):
                val = re.sub(r'^/annotator="?', '', q).rstrip('"')
                q = f'/note="annotator: {val}"'
            elif q.startswith("/info="):
                val = re.sub(r'^/info="?', '', q).rstrip('"')
                q = f'/note="info: {val}"'
            elif q.startswith("/organism="):
                q = f'/organism="{species_name}"'
            elif q.startswith("/mol_type="):
                q = f'/mol_type="{molecule}"'

            if q.startswith("/transl_table="):
                cds_has_transl_table = True
            if q.startswith("/codon_start="):
                cds_has_codon_start = True

            # Wrap qualifier lines to 80 chars max
            embl_lines.extend(wrap_embl_qualifier(q))

        # Ensure mandatory CDS qualifiers
        if ft_key == "CDS":
            if not cds_has_transl_table:
                embl_lines.append('FT                   /transl_table=11')
            if not cds_has_codon_start:
                embl_lines.append('FT                   /codon_start=1')

    embl_lines.append("XX")

    # 8. SQ Line
    embl_lines.append(f"SQ   Sequence {seq_len} BP; {a_cnt} A; {c_cnt} C; {g_cnt} G; {t_cnt} T; {other_cnt} other;")

    # 9. Formatted Sequence
    for pos in range(0, seq_len, 60):
        chunk = seq_str[pos:pos + 60]
        blocks = [chunk[i:i + 10] for i in range(0, len(chunk), 10)]
        line_seq = " ".join(blocks)
        curr_len = pos + len(chunk)
        embl_lines.append(f"     {line_seq:<59} {curr_len:>9}")

    embl_lines.append("//")

    with open(embl_path, "w", encoding="utf-8") as out:
        out.write("\n".join(embl_lines) + "\n")

    print(f"[SUCCESS] Converted '{gbk_path}' -> '{embl_path}'")


def main():
    parser = argparse.ArgumentParser(description="Convert GeSeq GenBank to ENA EMBL format.")
    parser.add_argument("gbk", nargs="?", help="Input GenBank file path")
    parser.add_argument("-i", "--gbk_file", dest="gbk_opt", help="Input GenBank file path")
    parser.add_argument("-p", "--project_id", required=True, help="ENA Study / Project ID (e.g. PRJEB108312)")
    parser.add_argument("-l", "--locus_tag", required=True, help="Locus tag prefix (e.g. LAUSTCHL)")
    parser.add_argument("-s", "--species", required=True, help="Binomial scientific name (e.g. 'Linum austriacum')")
    parser.add_argument("-e", "--entry_name", required=False, help="Assembly entry name for AC * line (e.g. Laustriacum)")
    parser.add_argument("-t", "--topology", default="circular", choices=["circular", "linear"], help="Genome topology")
    parser.add_argument("-m", "--molecule", default="genomic DNA", help="Molecule type")
    parser.add_argument("-o", "--output", required=True, help="Output EMBL file path")

    args = parser.parse_args()
    input_file = args.gbk or args.gbk_opt

    if not input_file or not os.path.exists(input_file):
        sys.exit("Error: Valid input GenBank file required.")

    convert_gbk_to_embl(
        gbk_path=input_file,
        embl_path=args.output,
        project_id=args.project_id,
        locus_tag_prefix=args.locus_tag,
        species_name=args.species,
        entry_name=args.entry_name,
        topology=args.topology,
        molecule=args.molecule
    )


if __name__ == "__main__":
    main()