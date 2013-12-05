SilacPeptideCalc

Requirements: 
python 2.6

Python Modules:
optparse
matplotlib
lxml

SilacPeptideCalc is an algorithm to assist in relative quantitation of peptide post-translational modifications using Stable Isotope Labeling by Amino acids in Cell culture (SILAC). This python script  first determines the normalization factor and then calculates SILAC ratios for a list of target peptide masses using precursor ion abundances. 

Usage: python SilacPeptideCalc.py [options]

Options:

  -h, --help            show help message and exit

  -i FILE, --input=FILE

   input FILE must be a centroid mzXML file.  If the file does not load the mzXML namespace may need to changed in the mm_mzxml_lxm.py parser.

  -x FILE, --normfile=FILE

   input normalization FILE.  This option allows for the reuse of a previously generated normalization.  This option will skip the normalization and load the normalization factors

  -m FILE, --mass=FILE  set the monoisotopic M+H mass to search
  Specify the zero charge monoisotopic mass for each target.  Multiple targets can be specified as long as each is preceded by the -m option

  -t TOL, --tol=TOL
  set the absolute mass tolerance for target mass identification

  -y THRESHOLD, --threshold=THRESHOLD
  set absolute signal threshold.  

  -f NORM_RATIO_CUTOFF, --norm_ratio_cutoff=NORM_RATIO_CUTOFF
  set norm_ratio_cutoff.  This option limits the range of ratios used for normalization.  A good option is 2 as this will only used ratios with a +/- 2 fold change for purposes of normalization.  This option can be very useful in reducing noise in the normalization.

  -u START_MASS, --smass=START_MASS
  set lower end of masses used for data parsing

  -v END_MASS, --emass=END_MASS
  set upper end of masses used for data parsing

  -j START_SCAN, --sscan=START_SCAN
  set first scan to begin parsing

  -k END_SCAN, --escan=END_SCAN
  set last scan to end parsing

  -w SCAN_WINDOW, --wind=SCAN_WINDOW
  set width (in seconds) of retention time scan window.  Peptide signals with a time separation greater than the scan window will be reported as separate ratios.

  -n NUM_LABELS, --labeln=NUM_LABELS
  set number of labels for a given peptide.  There must be a separate -n option for each -m.  Multiple labels can be specified for a given peptide by entering the peptide mass more than once.

  -c NUM_LABELS_NORM, --labelnnorm=NUM_LABELS_NORM
  set number of labels for normalization. Program uses a single label mass for normalizaiton.  This option can be changed to any number of labels using this argument. 

  -l LABEL_MASS, --labelm=LABEL_MASS
  set the zero charge accurate mass of of the SILAC label

  -s NORM_RELOAD, --normreload=NORM_RELOAD
  Skip normalization if norm file is present.  This option will automatically skip normalization and load the file is the normfile is detected.

  -p PEPTIDE_SEQ, --peptideseq=PEPTIDE_SEQ
  Input the peptide sequence.  The peptide sequence can be input for each target mass.  This will be used in the generated data and helps with organizing the data.


