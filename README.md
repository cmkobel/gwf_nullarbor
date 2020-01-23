# gwf wrapper for nullarbor


## Usage

Create a tab-delimited file in inputs with the following specs:
 - First line starts with '#' and denotes the reference genome used and the mlst-scheme wanted (optional)
 - Each line thereafter has sample_name, read_forward, read_reverse
 
Example:
```
#	kpneumoniae/GCF_000240175.1_ASM24017v2_genomic.gbff	kpneumoniae
CPO20170025_AMA2316	../CPO20170025_R1_001.fastq.gz	../CPO20170025_R2_001.fastq.gz
CPO20170077_S76	../CPO20170077_R1_001.fastq.gz	../CPO20170077_R2_001.fastq.gz
CPO20170070_S78	../CPO20170070_R1_001.fastq.gz	../CPO20170070_R2_001.fastq.gz
CPO20170077_S33	../CPO20170077_R1_001.fastq.gz	../CPO20170077_R2_001.fastq.gz
CPO20170152_S2	../CPO20170152_R1_001.fastq.gz	../CPO20170152_R2_001.fastq.gz
```

Make sure to have all dependencies installed. Besides all nullarbor dependencies, only gwf-org is necessary.

**1) Initialize batch**

`gwf status`

This will check that all dependencies are installed, and place the central makefile in an appropriate folder in output/.


**2) Execute batch**

`gwf run`

This will apply the job list to the cluster.


If the *1) Initialize* is skipped, *2) Execute batch* will automatically do it. 


## Side note about hardlinking
If you're not able to create hard-links, like nullarbor does when linking contigs, it might be necessary to change the linking command in file `nullarbor.pl` from `ln` instead of `cp`:

```
%.gff : %/contigs.gff
  cp $< $@
  #ln -f $< $@
```

This workaround is not necessary related to this wrapper, but any system lacking hardlinking capabilities.


