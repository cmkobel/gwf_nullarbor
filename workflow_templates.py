
def nullarbor(path, stem, inputsize):

    inputs = [path + "/Makefile", # most important input
              path + "/input.tab",
              path + "/isolates.txt",
              path + "/Makefile",
              path + "/nullarbor.log"]

    outputs = [path + "/report/index.html", # most important output
               path + "/core.aln",
               path + "/core.full.aln",
               path + "/core.newick",
               path + "/core.ref.fa",
               path + "/core.svg",
               path + "/core.tab",
               path + "/core.txt",
               path + "/core.vcf",
               path + "/denovo.tab",
               path + "/distances.tab",
               path + "/mlst.tab",
               path + "/resistome.tab",
               path + "/virulome.tab"]
    if inputsize <= 30:
        ram = 64
        walltime = '14:00:00'
    elif inputsize <= 50:
        ram = 64
        walltime = '1-05:00:00'
    elif inputsize <= 120:
        ram = 128
        walltime = '2-00:00:00'
    else:
        ram = 512
        walltime = '7-00:00:00'
    print('ram, walltime:', ram, walltime)
    options = {'nodes': 1, 'cores': 8, 'memory': str(ram)+'g', 'walltime': walltime, 'account': 'clinicalmicrobio'}
    
    spec = '''

echo JOBID $SLURM_JOBID

# Print date into history
d=`date +%Y-%m-%d_%H:%M:%S`
echo -e "$d\t$SLURM_JOBID\t{path}" >> history.tab


# Call nullarbor
nice make -j 4 -l 12 -C {path}


# Reorganize name of report
cd {path}
jobinfo $SLURM_JOBID >> report/jobinfo.txt
cp -r report report_{stem}
zip -r report_{stem}.zip report_{stem}/
rm -r report_{stem}

echo "this far 1"
# Mail report
mail -s "nullarbor done {stem}" -a report_{stem}.zip kobel@pm.me <<< "$(jobinfo $SLURM_JOBID)"

echo "this far 2"
# Export the environment
conda env export > environment.yml

jobinfo $SLURM_JOBID

echo "this far 3"

'''.format(path = path, stem = stem)
    return inputs, outputs, options, spec
