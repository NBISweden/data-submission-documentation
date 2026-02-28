#!/bin/bash

# Usage: ./reformat_md5_tsv.sh input.md5 > paired_output.tsv

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_md5_file>" >&2
    exit 1
fi

INPUT_FILE=$1

# Print the TSV header (using -e to interpret the \t tab character)
echo -e "Sample_Key\tMD5_R1\tFile_R1\tMD5_R2\tFile_R2"

# Declare associative arrays
declare -A r1_md5 r1_path r2_md5 r2_path
declare -a samples

# Process the file, stripping carriage returns first
while read -r md5 filepath; do
    # Skip empty lines or lines without an MD5
    [[ -z "$md5" ]] && continue
    
    # Remove any trailing carriage returns from the filepath
    filepath=$(echo "$filepath" | tr -d '\r')
    
    # Match the sample naming pattern (captures everything before _R1_ or _R2_)
    if [[ "$filepath" =~ (.*)_R1_.*\.fastq\.gz ]]; then
        key="${BASH_REMATCH[1]}"
        r1_md5["$key"]="$md5"
        r1_path["$key"]="$filepath"
        # Add to unique sample list if not already present
        [[ ! " ${samples[*]} " =~ " ${key} " ]] && samples+=("$key")
        
    elif [[ "$filepath" =~ (.*)_R2_.*\.fastq\.gz ]]; then
        key="${BASH_REMATCH[1]}"
        r2_md5["$key"]="$md5"
        r2_path["$key"]="$filepath"
        [[ ! " ${samples[*]} " =~ " ${key} " ]] && samples+=("$key")
    fi
done < "$INPUT_FILE"

# Output the results in TSV format
for key in "${samples[@]}"; do
    # Extract just the filename for the Sample_Key column
    clean_name=$(basename "$key")
    echo -e "${clean_name}\t${r1_md5[$key]}\t${r1_path[$key]}\t${r2_md5[$key]}\t${r2_path[$key]}"
done
