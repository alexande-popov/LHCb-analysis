import ROOT
from   Ostap.PyRoUts   import *
from   Ostap.Data      import DataAndLumi 

from   Ostap.GetLumi   import getLumi

## make Ttree-structure of dataset
RAD = ROOT.RooAbsData
if RAD.Tree != RAD.getDefaultStorageType() :
     print 'DEFINE default storage type to be TTree! '
     RAD.setDefaultStorageType ( RAD.Tree )

#fpath = '/afs/cern.ch/user/a/alexandp/gangadir/workspace/alexandp/LocalXML/'
fpath = '/data/Alexander/lhcb/work/Bs2JpsiPhiX0/Analis/files/'
    
data = DataAndLumi (  'Bplus/Bp' , files = [
     fpath + '150/*/output/DVNtuples.root' ,  # 2012 up
     fpath + '151/*/output/DVNtuples.root' ,  # 2012 down
     fpath + '152/*/output/DVNtuples.root' ,  # 2011 up
     fpath + '153/*/output/DVNtuples.root' ,  # 2011 down
     ]
                      )
                      
chainb  = data.chain 
tLumi   = data.lumi


print  data 

