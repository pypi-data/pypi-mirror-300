# Fletcher

While sequence alignments have historically helped infer activity once homology is identified, this is usually limited by the ability of the MSA tool to spot similarities and align them correctly. With the advent of AlphaFold, structural similarities may be found based on sequence similarities that would have flown under the radar if using an MSA exclusively. 'Fletcher' is a tool that will get a list of residues (and alternatives) and look for them in AlphaFold models provided that they lie within a fixed distance. 

Usage: 

```
fletcher.py [-h] -f FILENAME -r RESIDUES -d DISTANCE

The program will try to find a list of residues within a fixed distance from the
centre of mass. Concept: Federico Sabbadin & Jon Agirre, University of York,
UK.

Required arguments:

  -f FILENAME, --filename FILENAME
                        The name of the file to be processed, in PDB or mmCIF
                        format
  -r RESIDUES, --residues RESIDUES
                        A list of residues in one-letter code, comma
                        separated, and including alternatives, e.g. L,A,FWY
  -d DISTANCE, --distance DISTANCE
                        Specifies how far each of the residues can be from the
                        rest, in Angstroems
  -p PLDDT, --plddt PLDDT
                        Flag up candidate residues with average pLDDT below
                        thresold (Jumper et al., 2020).

Optional arguments:

-h, --help            show this help message and exit
```

Fletcher is not an acronym. It is the surname of the greatest musical catalyst I know: Guy Fletcher (https://www.guyfletcher.co.uk). 
