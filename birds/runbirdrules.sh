#!/bin/bash

# usage: bash ./runbirdrules.sh transactions_file_prefix
# e.g., bash ./runbirdrules.sh birds_v1

trans_file="$1"
k_values=(100 150 170 200)
M_values=(-2 -5 -10)
q_value=300

# transform our transaction data into the format required by kingfisher
../namescodes/namescodes -n"$trans_file".txt -t"$trans_file"_table.txt -L

# run kingfisher with different parameter settings
for k in "${k_values[@]}"; do
  for M in "${M_values[@]}"; do
    out_file="${trans_file}_k${k}_M${M}_rules.txt"
    echo "Running Kingfisher with -k${k} -M${M} → $out_file"
    
    ../kingfisher/kingfisher \
      -i "${trans_file}.txt.codes" \
      -k"$k" \
      -M"$M" \
      -q"$q_value" \
      -o "$out_file"
    # transform the output back to names
    ../namescodes/namescodes -c"$out_file" -t"$trans_file"_table.txt

  done
done
