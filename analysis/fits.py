import ROOT
from   Ostap.PyRoUts    import * 
import Ostap.FitModels  as     Models
from   AnalysisPython.Logger     import getLogger

if     '__main__' == __name__ : logger = getLogger ( 'fits'   )
else                          : logger = getLogger ( __name__ ) 
logger.info ( "Make fits" )

# resonanse name
#import name
#res_name = name.name
res_name = "eta"

from cuts import mB
from cuts import mPsic2, mPhic3, mEtac1, mEta

# Bs
signal_B = Models.CB2_pdf (
    'Bs'                   ,
    mB.getMin()            ,
    mB.getMax()            ,
    #fixMass   = 5.3668e+00 ,
    #fixSigma  = 6.2746e-03 ,
    #fixAlphaL = 1.4260e+00 ,
    #fixAlphaR = 1.4201e+00 ,
    mass      = mB        )
model_B = Models.Fit1D(
    signal     = signal_B ,
    background = Models.Bkg_pdf ( 'B' , mass = mB , power = 1 ) 
    )

# Psi
signal_Psi = Models.Gauss_pdf (
    'psi'             ,
    mPsic2.getMin()     ,
    mPsic2.getMax()     ,
    mass      = mPsic2  
    )
signal_Psi_CB2 = Models.CB2_pdf (
    'psi'             ,
    mPsic2.getMin()     ,
    mPsic2.getMax()     ,
    mass      = mPsic2  
    )
model_Psi = Models.Fit1D(
    signal     = signal_Psi ,
    background = Models.Bkg_pdf ( 'Psi' , mass = mPsic2 , power = 0 ) 
    )

# Phi
mK   = 0.4947 
bw   = cpp.Gaudi.Math.Phi0( 1.0195 , 0.0043 , mK  ) 
signal_Phi  = Models.BreitWigner_pdf ( 'Phi'         ,
                                bw                   ,
                                mPhic3.getMin()        ,
                                mPhic3.getMax()        ,
                                #fixMass     = 1.0195 , 
                                #fixGamma    = 0.0043 , 
                                mass        = mPhic3   ,
                                ##convolution = 7.0351e-04 ,
                                useFFT      = True   ) 
mPhic3.setBins ( 1000000 , 'cache' )
ps = cpp.Gaudi.Math.PhaseSpaceNL ( 2*mK , 5.36677 - 3.0969 - 0.547853 , 2 , 4 ) 
model_Phi = Models.Fit1D (
    signal     = signal_Phi ,
    background = Models.PSPol_pdf('PS', mPhic3, ps, power = 0 )
    )

# Eta
signal_Eta = Models.Gauss_pdf (
    'eta'             ,
    mEtac1.getMin()     ,
    mEtac1.getMax()     ,
    mass      = mEtac1  
    )
#signal_Eta = Models.CB2_pdf (
#    'eta'             ,
#    mEtac1.getMin()     ,
#    mEtac1.getMax()     ,
#    mass      = mEtac1  
#    )
model_Eta = Models.Fit1D(
    signal     = signal_Eta ,
    background = Models.Bkg_pdf ( 'B' , mass = mEtac1 , power = 0 ) 
    )



