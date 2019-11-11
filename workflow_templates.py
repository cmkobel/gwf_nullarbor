
def nullarbor(path):

    inputs = [path + "/Makefile"]
    outputs = [path + "/report/index.html"]
    options = {'nodes': 1, 'cores': 8, 'memory': '8g', 'walltime': '06:09:00', 'account': 'clinicalmicrobio'}
    spec = '''
echo JOBID $SLURM_JOBID


source activate nullarbor
nice make -j 4 -l 12 -C {path}"

jobinfo $SLURM_JOBID

'''.format(path = path)
    return inputs, outputs, options, spec
