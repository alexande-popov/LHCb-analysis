import ROOT
from   Ostap.PyRoUts   import *

from AnalysisPython.Logger import getLogger
if '__main__' == __name__ : logger = getLogger ( 'data'   )
else                      : logger = getLogger ( __name__ ) 
logger.info ( "List of files" )
logger.info ( "Signal        channel: Bs -> Jpsi phi eta" )
logger.info ( "Normalization channel: Bs -> Jpsi phi    " )

fpath = '/afs/cern.ch/work/a/alexandp/gangadir/workspace/alexandp/LocalXML/'

files = {}
files_sel8  = {}
files_sel9  = {}
files_sel10 = {}
files_sel11 = {}

files_sig_rd = {
    ## signal_rd Selection 11
    'Sig-RD-2011-U'          : [fpath + '402/*/output/DVNtuples.root'],
    'Sig-RD-2011-D'          : [fpath + '403/*/output/DVNtuples.root'],
    'Sig-RD-2012-U'          : [fpath + '404/*/output/DVNtuples.root'],
    'Sig-RD-2012-D'          : [fpath + '405/*/output/DVNtuples.root'],
    }

files_sig_mc = {
    #signal_mc
    'Sig-MC-Pythia6-2011-U'  : [fpath + '388/*/output/DVNtuples.root'], 
    'Sig-MC-Pythia6-2011-D'  : [fpath + '389/*/output/DVNtuples.root'], 
    'Sig-MC-Pythia6-2012-U'  : [fpath + '386/*/output/DVNtuples.root'],
    'Sig-MC-Pythia6-2012-D'  : [fpath + '387/*/output/DVNtuples.root'],

    'Sig-MC-Pythia8-2011-U'  : [fpath + '391/*/output/DVNtuples.root'], 
    'Sig-MC-Pythia8-2011-D'  : [fpath + '392/*/output/DVNtuples.root'], 
    'Sig-MC-Pythia8-2012-U'  : [fpath + '393/*/output/DVNtuples.root'],
    'Sig-MC-Pythia8-2012-D'  : [fpath + '394/*/output/DVNtuples.root'],
    }

files_norm_rd = {
    #norm_rd
    'Norm-RD-2011-U'         : [fpath + '400/*/output/DVNtuples.root'],
    'Norm-RD-2011-D'         : [fpath + '401/*/output/DVNtuples.root'],
    'Norm-RD-2012-U'         : [fpath + '398/*/output/DVNtuples.root'],
    'Norm-RD-2012-D'         : [fpath + '399/*/output/DVNtuples.root'],
    }

files_norm_mc = {
    #norm_mc
    'Norm-MC-Pythia6-2011-U' : [fpath + '374/*/output/DVNtuples.root'],
    'Norm-MC-Pythia6-2011-D' : [fpath + '375/*/output/DVNtuples.root'],
    'Norm-MC-Pythia6-2012-U' : [fpath + '376/*/output/DVNtuples.root'],
    'Norm-MC-Pythia6-2012-D' : [fpath + '377/*/output/DVNtuples.root'],

    'Norm-MC-Pythia8-2011-U' : [fpath + '380/*/output/DVNtuples.root'],
    'Norm-MC-Pythia8-2011-D' : [fpath + '381/*/output/DVNtuples.root'],
    'Norm-MC-Pythia8-2012-U' : [fpath + '378/*/output/DVNtuples.root'],
    'Norm-MC-Pythia8-2012-D' : [fpath + '379/*/output/DVNtuples.root'],
}

files_psieta_rd = {
    #PsiEta_rd
    'Sig-RD-2011-U'         : [fpath + '406/*/output/DVNtuples.root'],
    'Sig-RD-2011-D'         : [fpath + '407/*/output/DVNtuples.root'],
    'Sig-RD-2012-U'         : [fpath + '408/*/output/DVNtuples.root'],
    'Sig-RD-2012-D'         : [fpath + '409/*/output/DVNtuples.root'],
    }

files_psieta_mc = {
    #PsiEta_mc
    'Sig-MC-Pythia6-2012-U'  : [fpath + '410/*/output/DVNtuples.root'],
    'Sig-MC-Pythia6-2012-D'  : [fpath + '411/*/output/DVNtuples.root'],

    'Sig-MC-Pythia8-2012-U'  : [fpath + '412/*/output/DVNtuples.root'],
    'Sig-MC-Pythia8-2012-D'  : [fpath + '413/*/output/DVNtuples.root'],
    }



