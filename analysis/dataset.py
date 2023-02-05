import ROOT
from   Ostap.PyRoUts    import * 
from   Ostap.Selectors  import SelectorWithVars 
from   AnalysisPython.Logger import getLogger
if     '__main__' == __name__ : logger = getLogger ( 'dataset'   )
else                          : logger = getLogger ( __name__ ) 
logger.info ( "Make datasets" )

import data, cuts 
from EvtID import funEvtID 
from random import randint as rnd

variables = [
    ( cuts.mB     ,                                    lambda s : s.mass_3  ) , 
    ( cuts.mPhi   ,                                    lambda s : s.m23     ) ,
    ( cuts.mEta   ,                                    lambda s : s.m4      ) ,
    ( 'c2dtf'     , 'c2dtf'      , 0.    , 1000. ,     lambda s: s.c2dtf_3  ) ,
    ##( 'mKK22'   ,  'mass(K+K-)' , 1.0   , 1.040 ,      lambda s : s.m23c1  ) ,
    ]
variables += [ ( 'run'       , 'Run'        , 0.    , 1.0e+12,     lambda s: s.run      ) ]
variables += [ ( 'evt'       , 'Event'      , 0.    , 1.0e+12,     lambda s: s.evt      ) ]
variables += [ ( 'hSPD'      , 'hSPD'       , 0.    , 1.0e+04,     lambda s: s.hSPD     ) ]
variables += [ ( 'nLong'     , 'nLong'      , 0.    , 1.0e+03,     lambda s: s.nLong    ) ]
variables += [ ( 'nVelo'     , 'nVelo'      , 0.    , 2.0e+04,     lambda s: s.nVelo    ) ]
variables += [ ( 'EvtID'     , 'EvtID'      , 0.    , 2.0e+05,     funEvtID             ) ]
variables += [ ( 'rand'      , 'rand'       , 0.    , 2.0e+12,     lambda s:rnd(0,1000000))]
variables += [ ( 'pteta'     , 'pT(eta)'    , 0.    , 1.0e+07,     lambda s: s.pt_eta   ) ]
variables += [ ( 'ptg1'      , 'pT(gamma1)' , 0.    , 1.0e+07,     lambda s: s.pt_g1    ) ]
variables += [ ( 'ptg2'      , 'pT(gamma2)' , 0.    , 1.0e+07,     lambda s: s.pt_g2    ) ]
variables += [ ( 'cl1'       , 'CL(gamma1)' , 0.    , 1.     ,     lambda s: s.cl1      ) ]
variables += [ ( 'cl2'       , 'CL(gamma2)' , 0.    , 1.     ,     lambda s: s.cl2      ) ]
#variables += [ ( 'effG1'    ,  'eff(G1)'    , -1    , 2      ,     funG1                ) ] 
#variables += [ ( 'effG2'    ,  'eff(G2)'    , -1    , 2      ,     funG2                ) ] 
#variables += [ ( 'effGG'    ,  'eff(GG)'    , -1    , 2      ,     funGG                ) ] 


variables += [ ( cuts.ptb   ,                                lambda s : s.pt_b   )  ]
variables += [ ( cuts.yb    ,                                lambda s : s.y_b    )  ]
variables += [ ( cuts.mPsi  ,                                lambda s : s.m1     )  ]
variables += [ ( cuts.ptpsi ,                                lambda s : s.pt_psi )  ]
##variables += [ ( cuts.ptmu  ,                                lambda s : s.pt_mu  ) ]
#variables += [ ( 'effK1'    ,  'eff(K1)'    , -1    , 2    , funK1               )  ] 
#variables += [ ( 'effK2'    ,  'eff(K2)'    , -1    , 2    , funK2               )  ] 
variables += [ ( 'ctau9_b'  , 'ctau9(B)'    , 0.0   , 1000., lambda s: s.ctau9_b )  ]
variables += [ ( 'pt_b'     , 'pt_b'        , 0.    , 1000., lambda s: s.pt_b    )  ]
variables += [ ( 'ptk'      , 'pT(K)'       , 0.    , 1000., lambda s: s.ptk     )  ]
variables += [ ( 'minann_K' , 'ProbNN(K)'   , 0.    , 1000., lambda s: s.minann_K)  ]
variables += [ ( 'psi_l0tos', 'psi_l0tos'   , 0.    , 100. , lambda s: s.psi_l0tos) ]
variables += [ ( 'psi_l1tos', 'psi_l1tos'   , 0.    , 100. , lambda s: s.psi_l1tos) ]
variables += [ ( 'psi_l2tos', 'psi_l2tos'   , 0.    , 100. , lambda s: s.psi_l2tos) ]
variables += [ ( 'year'     , 'year'        , 2000. , 2020., lambda s: s.year     ) ]
variables += [ ( 'pi0veto'  , 'pi0veto'    ,-1.0e+04, 10.  , lambda s: s.pi0veto  ) ]

selector_rd_sig  = SelectorWithVars ( variables, cuts.cuts_sig_RD  )
data.chainb.process ( selector_rd_sig)
ds  = selector_rd_sig .data

cb  = ROOT.TCanvas("cb", "cb", 1000, 800)
from fits import model_B     as model
r,f = model.fitTo(ds, draw=True, nbins = 40)
logger.info ( "Make sPlot dataset" )
splot = model.sPlot ( ds )







