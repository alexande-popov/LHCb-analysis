#!/usr/bin/env python
# ==========================================================================================
## @file RealConv.py
#
#  reconstraction for gamma -> e+ e- decay
# ===========================================================================================
import ROOT                           ## needed to produce/visualize the histograms
from   Bender.Main         import *   ## import all bender goodies
###
import LHCbMath.Types                 ## easy access to various geometry routines 
from   Gaudi.Configuration import *   ## needed for job configuration

from   GaudiKernel.SystemOfUnits     import GeV, MeV, mm
from   GaudiKernel.PhysicalConstants import c_light

import math
from LoKiCore.basic import cpp

import BenderTools.TisTos
import BenderTools.Fill

from AnalysisPython.Logger import getLogger
logger = getLogger (  __name__ )

# ===========================================================================================
#from LoKiHlt.decorators import L0_DATA    
# ============================================================================================
## @class Conv
#  Simple algorithm to study XXX -> Jpsi Jpsi

def track ( part ) :

    if hasattr ( part , 'track'    ) : return         part.track()
    if hasattr ( part , 'proto'    ) : return track ( part.proto()    )
    if hasattr ( part , 'particle' ) : return track ( part.particle() )

    return None

class Jpsi_mu(Algo) :
    """
    Simple algorithm to study XXX -> Jpsi Jpsi
    """
    
    def initialize ( self ) :
        """
        Initialization
        """
        sc = Algo.initialize ( self )
        if sc.isFailure() : return sc
        
        #sc = self.  fill_initialize ()
        #if sc.isFailure() : return sc
        
        self._fun_ctau = BPVLTIME ( 9 ) * c_light 

        triggers = {}
        triggers [ 'J/psi'  ] = {}
        triggers [ 'B'      ] = {}

        lines            = {}
        lines ['J/psi' ] = {}
        lines ['B'     ] = {}

        lines['J/psi'][  'L0TOS'] = 'L0(Muon|DiMuon)Decision'
        lines['J/psi'][  'L0TIS'] = 'L0(Muon|DiMuon|Electron|Hadron|Photon)Decision'

        lines['J/psi']['Hlt1TOS'] = 'Hlt1(DiMuon|SingleMuon|MuTrack).*Decision'
        lines['J/psi']['Hlt1TIS'] = 'Hlt1(DiMuon|SingleMuon|MuTrack|DiHadron|TrackAllL0).*Decision'

        lines['J/psi']['Hlt2TOS'] = 'Hlt2(DiMuon|SingleMuon|MuTrack).*Decision'
        lines['J/psi']['Hlt2TIS'] =  lines['J/psi']['Hlt2TOS']

        lines ['B'] = lines[ 'J/psi' ]

        sc = self.tisTos_initialize ( triggers , lines )
        
        self._c2dtf   = DTF_CHI2NDOF (     False)
        self._mass    = DTF_FUN      ( M , False)
        self._ctau    = DTF_CTAU     ( 0 , False)
        
        self._c2dtf_0 = DTF_CHI2NDOF (     True )
        self._mass_0  = DTF_FUN      ( M , True )
        self._ctau_0  = DTF_CTAU     ( 0 , True )
        
        self._c2dtf_1   = DTF_CHI2NDOF (     True , strings ( [ 'J/psi(1S)' , 'psi(2S)' ] ) )  
        self._mass_1    = DTF_FUN      ( M , True , strings ( [ 'J/psi(1S)' , 'psi(2S)' ] ) ) 
        self._ctau_1    = DTF_CTAU     ( 0 , True , strings ( [ 'J/psi(1S)' , 'psi(2S)' ] ) )
        
        self._c2dtf_2   = DTF_CHI2NDOF (     True , strings ( [ 'eta' ] ) )  
        self._mass_2    = DTF_FUN      ( M , True , strings ( [ 'eta' ] ) ) 
        self._ctau_2    = DTF_CTAU     ( 0 , True , strings ( [ 'eta' ] ) )
        
        self._c2dtf_3   = DTF_CHI2NDOF (     True , strings ( [ 'J/psi(1S)' , 'psi(2S)', 'eta' ] ) )  
        self._mass_3    = DTF_FUN      ( M , True , strings ( [ 'J/psi(1S)' , 'psi(2S)', 'eta' ] ) ) 
        self._ctau_3    = DTF_CTAU     ( 0 , True , strings ( [ 'J/psi(1S)' , 'psi(2S)', 'eta' ] ) )

        return SUCCESS
        
    def finalize ( self ) :
        
        self._c2dtf    = None
        self._mass     = None
        self._ctau     = None
        
        self._c2dtf_0  = None
        self._mass_0   = None
        self._ctau_0   = None
        
        self._c2dtf_1  = None
        self._mass_1   = None
        self._ctau_1   = None
        
        self._c2dtf_2  = None
        self._mass_2   = None
        self._ctau_2   = None
        
        self._c2dtf_3  = None
        self._mass_3   = None
        self._ctau_3   = None
        
        #self.tisTos_finalize ()
        #self.  fill_finalize ()
        
        return Algo.finalize ( self )
    
    ## the only one esential method: 
    def analyse  (self ) :
        """
        The only one essential method
        """
        minPTk   = MINTREE( 'K+' == ABSID , PT            )

        minProbNNkaon = MINTREE ( 'K+' == ABSID  , PROBNNk)       
        minProbNNmuon = MINTREE ( 'mu+' == ABSID  , PROBNNmu)       
 
        minCloneDist = MINTREE ( ISBASIC & HASTRACK , CLONEDIST   )
        maxGhostProb = MAXTREE ( ISBASIC & HASTRACK , TRGHOSTPROB )        
        maxTrChi2    = MAXTREE( ISBASIC  , TRCHI2DOF)

        primaries = self.vselect( 'PVs' , ISPRIMARY )
        if primaries.empty() :
            return self.Warning('No primary vertices are found', SUCCESS )

        mips = MIPCHI2( primaries, self.geo() )
        maxMips  = MINTREE( ISBASIC  , mips )

        ## pi0 veto
        vetoFun = PINFO(25015, -1000)

        ## rec summary
        rc_summary = self.get('/Event/Rec/Summary').summaryData()
        odin       = self.get('/Event/DAQ/ODIN'   )

        tup     = self.nTuple ( 'Bp' )

        bplus   = self.select ( 'Bs' , '[B_s0 -> J/psi(1S) K- K+  ( eta -> gamma gamma) ]CC' )                
        for B in bplus:
            #print B.decay()
            
            mass = M ( B ) 
            if not 5.1 * GeV < mass < 5.7 * GeV : continue
            
            psi  = B.child ( 1 )
            mpsi = M ( psi )/GeV

            if not 0.95 * GeV < M23(B) < 1.1  * GeV : continue

            if minCloneDist ( B ) < 5000 : continue 
            if maxGhostProb ( B ) > 0.3  : continue 
            if maxTrChi2    ( B ) > 4    : continue 
            
            kaon_1  = B.child(2)
            kaon_2  = B.child(3)
            eta     = B.child(4)
            gamma_1 = eta.child(1)
            gamma_2 = eta.child(2)
            
            c2dtf = self._c2dtf ( B )
            ctau  = self._ctau  ( B )
            mass  = self._mass  ( B ) / GeV 
            
            c2dtf_0   = self._c2dtf_0 ( B )
            ctau_0    = self._ctau_0  ( B )
            mass_0    = self._mass_0  ( B ) / GeV
            if not -1 < c2dtf_0 < 10 : continue
            
            c2dtf_1   = self._c2dtf_1 ( B )
            ctau_1    = self._ctau_1  ( B )
            mass_1    = self._mass_1  ( B ) / GeV 
            
            #if not 5.1 < mass_1 < 5.7 : continue
            
            c2dtf_2   = self._c2dtf_2 ( B )
            ctau_2    = self._ctau_2  ( B )
            mass_2    = self._mass_2  ( B ) / GeV 
            
            #if not 5.1 < mass_2 < 5.7 : continue
            c2dtf_3   = self._c2dtf_3 ( B )
            ctau_3    = self._ctau_3  ( B )
            mass_3    = self._mass_3  ( B ) / GeV 
            

            tup.column ( 'ptk'   , minPTk( B ) / GeV )
            tup.column ( "nnk" , minProbNNkaon ( B ) )
            tup.column ( "nnm" , minProbNNmuon ( B ) )
            tup.column ( 'cl1' , CL(gamma_1) )
            tup.column ( 'cl2' , CL(gamma_2) )      

            #pi0 vetos for photons
            tup.column("pi0veto", vetoFun(eta) )      

            #tup.column ( 'pt_eta'  , PT(eta) )
            #tup.column ( 'p4_etaE' , E (eta) )  
            #tup.column ( 'p4_etaX' , PX(eta) )
            #tup.column ( 'p4_etaY' , PY(eta) )
            #tup.column ( 'p4_etaZ' , PZ(eta) )
            
            tup.column_float ( 'mass'    , mass    )
            tup.column_float ( 'mass_0'  , mass_0  )
            tup.column_float ( 'mass_1'  , mass_1  )
            tup.column_float ( 'mass_2'  , mass_2  )
            tup.column_float ( 'mass_3'  , mass_3  )
            tup.column_float ( 'c2dtf'   , c2dtf   )
            tup.column_float ( 'c2dtf_0' , c2dtf_0 )
            tup.column_float ( 'c2dtf_1' , c2dtf_1 )
            tup.column_float ( 'c2dtf_2' , c2dtf_2 )
            tup.column_float ( 'c2dtf_3' , c2dtf_3 )
            tup.column_float ( 'ctau'    , ctau    )
            tup.column_float ( 'ctau_0'  , ctau_0  )
            tup.column_float ( 'ctau_1'  , ctau_1  )
            tup.column_float ( 'ctau_2'  , ctau_2  )
            tup.column_float ( 'ctau_3'  , ctau_3  )
            #
            tup.column_bool  ( 'hasRich_k1'  , HASRICH( kaon_1 )  )
            tup.column_bool  ( 'hasRich_k2'  , HASRICH( kaon_2 )  )
            #
            ## fill all nmass sub-combinations 
            #
            self.fillMasses ( tup , B , ''   )
            self.fillMasses ( tup , B , 'c0' , True )
            self.fillMasses ( tup , B , 'c1' , True , strings ( [ 'J/psi(1S)' , 'psi(2S)'  ] ) )
            self.fillMasses ( tup , B , 'c2' , True , strings ( [ 'eta' ] ) )
            self.fillMasses ( tup , B , 'c3' , True , strings ( [ 'J/psi(1S)' , 'psi(2S)' , 'eta' ] ) )
            
            self.treatKine   ( tup , B       , '_b'   )
            self.treatKine   ( tup , psi     , '_psi' )
            self.treatKine   ( tup , kaon_1  , '_k1'  )
            self.treatKine   ( tup , kaon_2  , '_k2'  )
            self.treatKine   ( tup , eta     , '_eta' )
            self.treatKine   ( tup , gamma_1 , '_g1'  )
            self.treatKine   ( tup , gamma_2 , '_g2'  )

            self.treatPhotons ( tup , B )                        
            self.treatKaons   ( tup , B )
            self.treatMuons   ( tup , B )
            self.treatTracks  ( tup , B )

            self.tisTos ( psi , tup  , 'psi_' , self.lines['B' ] )

            ## add some reco-summary information
            self.addRecSummary ( tup , rc_summary )
            tup.column_aux     ( odin )
            
            tup.write  () 
               
        return SUCCESS

        
# =============================================================================
## configure the job 

## configure the job
def configure ( datafiles        ,
                catalogs = []    ,
                castor   = False ,
                params   = {}    ) :
    """
    Job configuration
    """

    from Configurables           import DaVinci       ## needed for job configuration
    
    from Configurables import LHCbApp
    LHCbApp().XMLSummary = 'summary.xml'

    from BenderTools.Utils import silence
    silence()

    rootInTes = '/Event/PSIX0'
    the_year = params['Year']
    
    davinci = DaVinci (
        DataType      = params['Year']   ,
        RootInTES     = rootInTes  ,
        InputType     = 'MDST'     ,
        Simulation    = False  ,
        PrintFreq     = 1000   ,
        EvtMax        = -1     , 
        HistogramFile = 'DVHistos.root' ,
        TupleFile     = 'DVNtuples.root' ,
        Lumi          = True ,
        )
    
    from Configurables import CondDB
    CondDB ( LatestGlobalTagByDataType = the_year )

    from Configurables import TrackScaleState
    state_scale    = TrackScaleState (
        'StateScale'            ,
        RootInTES  = rootInTes  ,
        )

    davinci.UserAlgorithms = [  state_scale ,
                                'Bplus' ,
                                        ]
    
    setData ( datafiles , catalogs, castor )
    
    gaudi = appMgr()
    
    alg = Jpsi_mu(
        'Bplus'               ,   ## Algorithm name
        RootInTES = rootInTes ,
        Inputs = [
        'Phys/SelB2PsiKKEtaForPsiX0/Particles'
        #'Phys/SelB2PsiKEtaForPsiX0/Particles'
        ]
        )
    
    return SUCCESS 

# =============================================================================
# The actual job steering
if '__main__' == __name__ :

    
    # Selection 11 /LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/WGBandQSelection11/Merge/90000000/PSIX0.MDST
    inputs = [
        '/lhcb/LHCb/Collision12/PSIX0.MDST/00049174/0000/00049174_00000003_1.psix0.mdst',
        '/lhcb/LHCb/Collision12/PSIX0.MDST/00049174/0000/00049174_00000030_1.psix0.mdst',  
    ]
    params_test = {'Year': '2012'}


    configure ( inputs, params = params_test, castor = True )

    run ( 1500 )
    
    gaudi = appMgr()
    
    myalg2 = gaudi.algorithm ( 'Bplus' )

# =============================================================================
# The END 
# =============================================================================
