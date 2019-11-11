"""
This file has two functions
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
import os, subprocess, workflow_templates
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

# Read reference genome and mlst scheme data from each file.
for file in inputs:
    print(file)

    with open(INPUT_DIR + "/" + file, 'r') as raw:
        for line in raw:
            #firstline = line
            if line[0] != "#":
                raise Exception("Error: lack of comment line in " + file + ".\nComment line should contain reference and mlst. Example:\n# reference.gbk kpneumoniae" )
            hash, reference, mlst = [i.strip() for i in line.split(' ')]
            break

    inputs_dicts.append({'name': file, 'reference': reference, 'mlst': mlst, "stem": '.'.join(file.split(".")[:-1])})


print()


outputs = [d for d in os.listdir(OUTPUT_DIR) if isdir(join(OUTPUT_DIR, d))]

print(f'list of files in {INPUT_DIR}/ :')
for i in inputs_dicts:
    print(i['name'], i['reference'], i['mlst'])
print()
print(f'list of directories in {OUTPUT_DIR}/ :')
print(outputs)
print()




for input in inputs_dicts:
    #stem = '.'.join(input['name'].split(".")[:-1])
    if input["stem"] in outputs:
        print(input['name'], 'already exists in output dir')
    else:
        print(input['name'], 'does not exist in output dir: job will be initilized:')

        subprocess.run(f'source activate nullarbor; nullarbor.pl --check && nullarbor.pl --name {input["name"]} --mlst {input["mlst"]} --taxoner kraken2 --ref reference_genomes/{input["reference"]} --input input/{input["name"]} --trim --outdir output/{input["stem"]}', shell = True, check = True)

    gwf.target_from_template("nullarbor_" + input['stem'], workflow_templates.nullarbor(path = OUTPUT_DIR + "/" + input['stem']))
	





