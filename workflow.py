"""
This file has two purposes
	1: Initializes new makefiles from the list of jobs in inputs/
	2: submits new makefiles to slurm
"""
print("""             _ _            _
 _ __  _   _| | | __ _ _ __| |__   ___  _ __
| '_ \| | | | | |/ _` | '__| '_ \ / _ \| '__|
| | | | |_| | | | (_| | |  | |_) | (_) | |
|_| |_|\__,_|_|_|\__,_|_|  |_.__/ \___/|_|
""")


from gwf import *
import os, subprocess, workflow_templates, sys
from os.path import isfile, isdir, join
gwf = Workflow()

ROOT = os.getcwd() + '/'
INPUT_DIR = "input"
OUTPUT_DIR = "output"

inputs = list()
inputs_dicts = list()
outputs = list()

# Read files in input dir
inputs = [f for f in os.listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))]

# Read tab files from inputs
print('reading tab files')
for file in inputs:
    print(file)
    n_lines = 0
    with open(INPUT_DIR + "/" + file, 'r') as raw:
        firstline = True
        for line in raw:
            if firstline:
                if line[0] != "#":
                    raise Exception("Error: lack of comment line in " + file + ".\nComment line should contain reference and mlst. Example:\n# reference.gbk kpneumoniae" )
                hash, reference, mlst = [i.strip() for i in line.split('\t')]
                firstline = False
            #print(hash, reference, mlst)
            n_lines += 1
    print('number of lines:', n_lines)	
    inputs_dicts.append({'name': file, 'reference': reference, 'mlst': mlst, 'n_lines': n_lines, 'stem': '.'.join(file.split('.')[:-1])})


print()


outputs = [d for d in os.listdir(OUTPUT_DIR) if isdir(join(OUTPUT_DIR, d))]

print(f'list of files in {INPUT_DIR}/ :')
for i in inputs_dicts:
    print(i['name'], i['reference'], i['mlst'], sep = '\t')
print()
print(f'list of directories in {OUTPUT_DIR}/ :')
print(outputs)
print()





for i_, input in enumerate(inputs_dicts):
    #stem = '.'.join(input['name'].split(".")[:-1])
    if input["stem"] in outputs:
        print('Already exists in output dir:', input["stem"], )
    else:
        print(f'Does not exist in output dir: {input["stem"]}. Job will be initialized...')

        #subprocess.run(f'source activate nullarbor', shell = True)
        
        

        #subprocess.run('export NULLARBOR_CONF="/project/ClinicalMicrobio/faststorage/nullarbor/nullarbor.conf"')

        #subprocess.run(f'nullarbor.pl --check', shell = True, check = True)
        if input['mlst'] == '':
            mlst_string = ''
        else:
            mlst_string = ' --mlst ' + input['mlst']
        print('mlst string given:', mlst_string)

        try:
            subprocess.run(f'nullarbor.pl --name {input["stem"]}{mlst_string} --taxoner kraken --ref reference_genomes/{input["reference"]} --input input/{input["name"]} --trim --outdir output/{input["stem"]}', shell = True, check = True)
        except subprocess.CalledProcessError as e:
            print(f'\nAn error occured while initializing {input["stem"]}:\n', e)
            sys.exit()

    title = 'nb_' + input['stem']
    gwf.target_from_template(title.replace('-', '_'), workflow_templates.nullarbor(path = OUTPUT_DIR + "/" + input['stem'], stem = input['stem'], inputsize = input['n_lines']))
	




