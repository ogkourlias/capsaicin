
snakemake --cluster sbatch --default-resources -j 6 --use-conda --latency-wait 300 -q --rerun-incomplete