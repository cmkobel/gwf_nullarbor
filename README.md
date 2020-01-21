# gwf wrapper for nullarbor


## Usage

Create a tab-delimited file in inputs with the following specs:
 - First line starts with '#' and denotes the reference genome used and the mlst-scheme wanted (optional)
 - Each line thereafter has sample_name, read_forward, read_reverse
 
Example:
```
#	kpneumoniae/GCF_240185.gbff	kpneumoniae
CPO20180025_AMA2216	../CPO20180025_AMA2216_S70_L555_R1_001.fastq.gz	../CPO20180025_AMA2216_S70_L555_R2_001.fastq.gz
CPO20180077_S88	../CPO20180077_R1_001.fastq.gz	../CPO20180077_R2_001.fastq.gz
CPO20180080_S80	../CPO20180080_R1_001.fastq.gz	../CPO20180080_R2_001.fastq.gz
CPO20180087_S43	../CPO20180087_R1_001.fastq.gz	../CPO20180087_R2_001.fastq.gz
CPO20180152_S1	../CPO20180152_R1_001.fastq.gz	../CPO20180152_R2_001.fastq.gz
```

Make sure to have all dependencies installed. Besides all nullarbor dependencies, only gwf-org is necessary.

** 1) Initialize batch **
```gwf status```
This will check that all dependencies are installed, and place the central makefile in an appropriate folder in output/.

** 2) Execute batch **
```gwf run```
This will apply the job list to the cluster.


If the *1) Initialize* is skipped, *2) Execute batch ** will automatically do it. 



