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

from cuts import mB
mPhi     = ROOT.RooRealVar ( "mPhi"     , "mass(Phi)"       , 0.995   , 1.050  )

# reduce ds
cut  = " mPsi>3.02 && mPsi<3.135"
cut += " && %s<mPhi && mPhi<%s "     % (mPhi.getMin() , mPhi.getMax())
cut += " && c2dtf < 5 "
cut += " && ptk > 0.6 "
cut += " && minann_K > 0.2 "
cut += " && (psi_l0tos&2)==2 && (psi_l1tos&2)==2 && (psi_l2tos&2)==2"
with timing("Reduce dataset") :
    ds = ds.reduce(cut)
logger.info ( "Reduce Dataset with cuts: %s" % cut)

from cuts import mB
from fits import model_2D


# fit training
with timing("First fit") :
    r,f = model_2D.fitTo(ds, silent = False)
#r,f = model_2D.fitTo(ds, silent = True)
#r,f = model_2D.fitTo(ds)
print r

# draw 2d hist
cb  = ROOT.TCanvas("cb", "cb", 1000, 800)
cb.SetLogz()
hd = ds          .createHistogram( mB,mPhi, 30,30)
hm = model_2D.pdf.createHistogram("mB,mPhi", 30,30)
hd.Draw("lego2")
hm.Draw("surf same")
cb.SaveAs("Pics/2d.png")
cb.Clear()
cb.SetLogz(0)

# draw m(B)
model_2D.draw(mB ,ds,50)
model_2D.draw(mB ,ds,50).SetXTitle("m_{ B}, GeV")
cb >> "Pics/mb_2d"
cb.Clear()
cb.SetLogy(1)
model_2D.draw(mB ,ds,50)
model_2D.draw(mB ,ds,50).SetXTitle("m_{ B}, GeV")
cb >> "Pics/mb_2d_log"
cb.Clear()
cb.SetLogy(0)

# draw m(phi)
model_2D.draw(mPhi,ds,50)
model_2D.draw(mPhi,ds,50).SetXTitle("m_{#phi}, GeV")
cb >> "Pics/mphi_2d"
cb.Clear()
cb.SetLogy(1)
model_2D.draw(mPhi,ds,50)
model_2D.draw(mPhi,ds,50).SetXTitle("m_{#phi}, GeV")
cb >> "Pics/mphi_2d_log"

# write fit params into file
params = model_2D.pdf.getVariables()
params .writeToFile("Pics/results_2D.txt")

# sPlot
splot = model_2D.sPlot ( ds )
WriteDB = False
if WriteDB:
    db = DBASE.open("Pics/ds.db","w")
    db["dsRD:2D"] = ds
    db.close()


