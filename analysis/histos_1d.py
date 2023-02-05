import ROOT
from   Ostap.PyRoUts    import * 
from   AnalysisPython.Logger import getLogger
from   Ostap.Utils      import timing
import Ostap.ZipShelve as DBASE

from   AnalysisPython.Logger import getLogger
if     '__main__' == __name__ : logger = getLogger ( 'histos'   )
else                          : logger = getLogger ( __name__ ) 
logger.info ( "Make histograms" )

ReadDB = True
if ReadDB:
    db = DBASE.open("/afs/cern.ch/user/a/alexandp/Analis/v6/B2JpsiKK/RD/reduce_ds/"+"Pics/ds.db", "r")
    ds = db["ds"]
    db.close()
else: from dataset import ds

# reduce ds
cut  = " mPsi>3.02 && mPsi<3.135"
cut += " && mPhi<1.032 && mPhi>1.008"
cut += " && c2dtf < 5 "
cut += " && ptk > 0.6 "
cut += " && minann_K > 0.2 "
cut += " && (psi_l0tos&2)==2 && (psi_l1tos&2)==2 && (psi_l2tos&2)==2"
with timing("Reduce dataset") :
    ds = ds.reduce(cut)
logger.info ( "Reduce Dataset with cuts: %s" % cut)

from fits import model_Bn

cb  = ROOT.TCanvas("cb", "cb", 1000, 800)

model_Bn.signal.sigma.setVal(0.006)
model_Bn.signal.aL.setVal(1.2)
model_Bn.signal.aR.setVal(1.2)
model_Bn.signal.nR.setVal(10.)
model_Bn.signal.nL.setVal(10.)

model_Bn.signal.mean .release()
model_Bn.signal.sigma.release()
model_Bn.signal.aL.release()
model_Bn.signal.aR.release()
model_Bn.signal.nL.release()
model_Bn.signal.nR.release()
model_Bn.background.phi_list[0].release()
model_Bn.background.tau.release()

with timing("First fit") :
    r,f = model_Bn.fitTo(ds, silent = True)
r,f = model_Bn.fitTo(ds, draw = True)

f.SetTitle("B mass")
f.SetXTitle("m_{ B}, GeV")
cb >> "Pics/mb_1d"
cb.Clear()

# in log scale
cb.SetLogy()
r,f = model_Bn.fitTo(ds, draw = True)
f.SetTitle("B mass")
f.SetXTitle("m_{ B}, GeV")
cb >> "Pics/mb_1d_log"

# write fit params into file
params  = model_Bn.signal.pdf.getVariables()
params .add(model_Bn.S)
params .add(model_Bn.B)
params .writeToFile("Pics/results_mb_1d.txt")

# sPlot
splot = model_Bn.sPlot ( ds )
WriteDB = False
if WriteDB:
    db = DBASE.open("Pics/ds.db","c")
    db["dsRD:1D"] = ds
    db.close()














