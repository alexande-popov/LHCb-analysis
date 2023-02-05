import ROOT
from   Ostap.PyRoUts    import * 
from AnalysisPython.Logger import getLogger
if '__main__' == __name__ : logger = getLogger ( 'cuts'   )
else                      : logger = getLogger ( __name__ ) 
logger.info ( "Define cuts" )

mB       = ROOT.RooRealVar ( "mB"       , "mass(B)"         , 5.2   , 5.6   )
mKK      = ROOT.RooRealVar ( "mKK"      , "mass(KK)"        , 1.0   , 1.040 )

cuts  = "    m1c2     > 3.02 && m1c2     < 3.135 " 
cuts += " && c2dtf_3 > 0     && c2dtf_3 < 5      "
cuts += " && min(cl1,cl2)   > 0.02"
cuts += " && abs(m4c1-0.55) < 0.05"
cuts += " && ctau9_b   > 0.2"
cuts += " && pt_eta   > 1500"
cuts += " && minann_K > 0.2"
cuts += " && ptk      > 0.6"
cuts += " && abs(m23c3-1.020)  < 0.012  "
#cuts += " && %s<m23c1 && m23c1<%s "     % ( mKK.getMin() , mKK.getMax() )
cuts += " && %s<mass_3  && mass_3<%s  " % ( mB .getMin() , mB .getMax() ) 

cuts += " && (psi_l0tos&2)==2 && (psi_l1tos&2)==2 && (psi_l2tos&2)==2 "
