## Messing around with the parameters

#### The parameters in the program

All adjustable parameters of the running of _inmembrane_ have been collected in a parameters file, which is typically stored in the `inmembrane.config`. 

On the first use of the program, when no such `inmembrane.config` is found, a default `inmembrane.config` will be generated. Existing `inmembrane.config` will be read and interpreted.

### General parameters

These are the general parameters to the program, representing the top-down organization of the work-flow. 

A fasta program is the input, following one of currently two different protocols - one for Gram+ bacteria, and one for Gram- bacteria. The results are saved to a csv file as an output.

- 'fasta': the pathname of the fasta file holding the sequences
- 'protocol': switches between different protocols for analysising the proteomes
- 'csv': the name of the output file in CSV (Excel-compatible) format. Defaults to a file using the same filename as 'fasta'

For potential debugging, it's important that all intermediate files are saved, and they are saved in: 

- 'out_dir': the directory where all intermediate output files are located

### Optional binaries

One of the problems that _inmembrane_ tackles is the complexity of using and installing multiple binaries. In older programs, the only option was to install local binaires of the external programs. This raises problems involved with getting the binary for the right platform, compilation with the right tools, and installation in the correct file system. In contrast, many of these tools now provide a web-interface. In _inmembrane_, we have added facilities to use the web service, whether through a RESTful interface, or through a SOAP interface, when provided.

Consequently, the parameters for the binaries are needed, where _inmembrane_ will attempt to run the program in the default directory, or if a full-path name is given, _inmembrane_ can run the binary in the correct location. 

In order to turn off the local binary option, if in a *_bin parameter is given the empty string, the local binary step will be skipped and the web version will be used instead.

- 'signalp4_bin', 'lipop1_bin', 'tmhmm_bin', 'memsat3_bin': the full pathname of the binaries used for the analysis. If empty, it is not run, and the web version is used instead

#### transmembrane helix predictors

A key part of surface exposure prediction requires the prediction of transmembrane helix. Once the helices are predicted, then the intervening loops can be used to predict actual surface exposure. There is no dominant transmembrane helix predictor, and thus _inmembrane_ has been written to allow pluggable options for transmembrane helix prediction.

- 'helix_programs': a choice of which transmembrane-helix predictors are used. Currently, the program loops over all designated helix predictors and chooses the longest predicted loops.

#### key parameters to determine surface-exposure

- 'terminal_exposed_loop_min': this is the length in terms of amino acids given to define an external loop of a protein to be long enough to stick out of the bacterial cell-wall to be considered surface-epxosed
- 'internal_exposed_loop_min': similarly to above, except is double the length as internal loops need to go up, and down again, for continuity with the rest of the protein.

#### HMMER parameters for signal proteins for cell-wall attachment

- 'hmmsearch3_bin': the binary for HMMER
- 'hmm_profiles_dir': the directory that holds the HMMER profiles for cell-wall signals
- 'hmm_evalue_max': the maximum expectation value cutoff for acceptable prediction in HMMER
- 'hmm_score_min': the minimum score cutoff for acceptatble prediction in HMMER

#### &beta;-barrel predictors

- 'barrel_programs': list of programs to do &beta-barel ['bomp', 'tmbetadisc-rbf'],
- 'bomp_clearly_cutoff': 3, # >= to this, always classify as an OM(barrel)
- 'bomp_maybe_cutoff': 1, # must also have a signal peptide to be OM(barrel)
- 'tmbhunt_clearly_cutoff': 0.95,
- 'tmbhunt_maybe_cutoff': 0.5,
- 'tmbetadisc_rbf_method': 'aadp', # aa, dp, aadp or pssm

----

## Programming philosophy
