#!/bin/bash

# Create the output directory
mkdir -p outputs

# Loop over all *_inputs directories
for INPUT_DIR in *_inputs; do
    # Skip if not a directory
    [ -d "$INPUT_DIR" ] || continue

    # Set number of processes based on method
    if [[ "$INPUT_DIR" == fci* || "$INPUT_DIR" == cc* ]]; then
        NP=1
    else
        NP=6
    fi

    # Loop over each .inp file in the directory
    for inp_file in "$INPUT_DIR"/*.inp; do
        base_name=$(basename "$inp_file" .inp)
        log_name="${INPUT_DIR}_${base_name}.log"
        log_path="outputs/${log_name}"

        echo "Running $base_name from $INPUT_DIR with $NP process(es)..."
        ./rungms-dev "$inp_file" 00 $NP >& "$log_path"
    done
done

