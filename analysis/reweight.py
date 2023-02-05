#!/usr/bin/env python
# =============================================================================
import ROOT
from Ostap.PyRoUts import *
import Ostap.ZipShelve as DBASE
# =============================================================================
from AnalysisPython.Logger import getLogger
if '__main__' == __name__ : logger = getLogger ('reweight')
else : logger = getLogger ( __name__ )
# =============================================================================

db_ref = 'RD_histos.db' # have histos of variables for reweighting

### Prepare Real Data
prepare = True
if prepare :
    logger.info('PREPARE reference data histograms') 

    hPT = h1_axis ( [0, 2, 3, 4, 5, 6.5, 8, 10, 12, 15, 50 ] )
    hY  = h1_axis ( [ 1.8, 2.5, 3.0, 3.5, 4.0, 4.7 ] )

    rd_path = "/afs/cern.ch/user/a/alexandp/Analis/v6/B2JpsiKK/RD/Pics/ds.db"
    dbRD = DBASE.open(rd_path)
    dsRD = dbRD["dsRD:2D"]
    dbRD.close()

    dsRD.project(hPT, "ptb", "S1S2_sw")
    dsRD.project(hY , "yb" , "S1S2_sw")

    with DBASE.open ( db_ref ) as db :

        logger.info ( 'Store DATA variables historgams in DB' )
        db['DATA:pt(B)' ] = hPT
        db['DATA:y(B)'  ] = hY
        db.ls()

with DBASE.open ( db_ref , 'r' ) as db :

    logger.info ( 'Get DATA histograms from DB for reweighting' )
    db.ls()
    hPT = db['DATA:pt(B)' ]
    hY  = db['DATA:y(B)'  ]

### Prepare MC
from cuts_reduced import c         as mccuts   
from data import chainb    as mctree
from dataset import variables as mcvars

# some important OSTAP stuff (thanks Vanya!!)
from Ostap.Reweighting import Weight, makeWeights
from Ostap.Selectors import SelectorWithVars

## prepare templates for MC-histograms
mc_PT = hPT . Clone () ; mc_PT *= 0
mc_Y  = hY  . Clone () ; mc_Y *= 0

# create database for saving weights or 'open', if it's already exists..
dbname = 'Reweighting.db'
import os
if not os.path.exists( dbname ) :
   db = DBASE.open ( dbname , 'c' )
   db.close() 

# here wright variables on witch you will re-weight
weighting = [
    ( lambda s : s.pt_b, 'pt(B)-weighting' ) ,
    ( lambda s : s.y_b  , 'y(B)-weighting' )
    ]

# number of re-weighting iterations
rwIter = 1

mcds = 1 ## fake....
for iIter in range(0,rwIter) :

    del mcds

    weighter = Weight( dbname , weighting )
    ## variables to be used in MC-dataset
    variables = mcvars + [
    ( 'mcweight' , 'mcweight' , -1e+5 , 1.e+5 , lambda s : weighter ( s ) )
    ]

    #
    ## create new "weighted" mcdataset
    #
    selector = SelectorWithVars(variables , mccuts)
    mctree.process ( selector) ##
    mcds = selector.data ## new reweighted dataset

    #
    ## update weights
    #
    plots = [
        ( 'ptb' , 'mcweight' , 'pt(B)-weighting' , hPT , mc_PT ) ,
        ( 'yb'  , 'mcweight' , 'y(B)-weighting'  , hY  , mc_Y  )
        ]

   # Special function in Bender that calculates weights
    more = makeWeights ( mcds , plots , dbname , delta = 0.001 / len ( plots ) )
    
    ## make MC-histogram
    mcds.project ( mc_PT , 'ptb' , 'mcweight' )
    mcds.project ( mc_Y  , 'yb'  , 'mcweight' )
    
    cmps = [
        ( hPT , mc_PT , 'PT(B)' ) ,
        ( hY  , mc_Y  , 'Y(B)'  ) ,
        ]

    hPT.Draw()
    mc_PT.Draw("same")
    
    ## checking how good calculated weights are
    logger.info ( 'Compare DATA and MC for iteration #%d' % iIter )
    for p in cmps :

        hdata = p[0]
        hmc = p[1]
        logger.info ( 'Check variable %s' % p[2] )

        #
        ## compare the basic properties: mean, rms, skewness and kurtosis
        #
        hdata.cmp_prnt ( hmc , 'DATA' , 'MC' , 'DATA vs MC' )
        #
        ## calculate the "distances"
        #
        dist = hdata.cmp_dist ( hmc , rescale = True )
        logger.info ('DATA-MC "distance" %s' % dist )
        #
        ## calculate the "orthogonality"
        #
        cost = hdata.cmp_cos ( hmc , rescale = True )
        logger.info ('DATA-MC "orthogonality" %s' % cost )
        #
        ## try to fit it DATA with MC and vice versa
        #
        fit1 = hdata.cmp_fit ( hmc , rescale = True )
        if fit1 and 0 == fit1.Status() :
            logger.info ( 'Fit DATA with MC Prob=%.3g[%%] ' % ( fit1.Prob() * 100 ) )
        fit2 = hmc .cmp_fit ( hdata , rescale = True )
        if fit2 and 0 == fit2.Status() :
            logger.info ( 'Fit MC with DATA Prob=%.3g[%%] ' % ( fit2.Prob() * 100 ) )
        #
        ## make chi2-comparison between data and MC
        #
        c2ndf,prob = hdata.cmp_chi2 ( hmc , rescale = True )
        logger.info ( 'DATA/MC: chi2/ndf (%.4g) and Prob %.5g%% ' % ( c2ndf , prob*100 ) )
        c2ndf,prob = hmc .cmp_chi2 ( hdata , rescale = True )
        logger.info ( 'MC/DATA: chi2/ndf (%.4g) and Prob %.5g%% ' % ( c2ndf , prob*100 ) )

SaveDB = True
if SaveDB:
    db = DBASE.open ( "Pics/ds.db" , "w")
    db["dsMC:weights"] = mcds
    db.close()














