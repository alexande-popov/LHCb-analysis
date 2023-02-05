#!/usr/bin/env python
# ==========================================================================================
## @file RealConv.py
#
#  reconstraction for gamma -> e+ e- decay
# ===========================================================================================
import ROOT                           ## needed to produce/visualize the histograms
from   Bender.MainMC       import *   ## import all bender goodies
##
from   GaudiKernel.SystemOfUnits     import GeV, MeV, mm
from   GaudiKernel.PhysicalConstants import c_light
##
import math
from   LoKiCore.basic import cpp
##
import BenderTools.TisTosMC
import BenderTools.Fill 
##
from LoKiAlgoMC.fArrayMCP import _fArrayMCP_, _Tuple
_Tuple.fArrayMCP = _fArrayMCP_
##
from AnalysisPython.Logger import getLogger
logger = getLogger (  __name__ )
## 
class JpsiPhi(AlgoMC) :
    """
    Simple algorithm to study XXX -> Jpsi Jpsi
    """
    def initialize ( self ) :
        """
        Initialization
        """
        sc = AlgoMC.initialize ( self )
        if sc.isFailure() : return sc

        self._rfit = self.vertexFitter() # new
        
        ## sc = self.  fill_initialize ()
        ## if sc.isFailure() : return sc

        triggers = {}
        triggers [ 'psi'  ] = {}
        
        lines           = {}
        lines ['psi'  ] = {}
        lines ['psi1' ] = {}
        lines ['psi2' ] = {}
        lines ['psi3' ] = {}
        
        #
        ## J/psi
        #
        lines [ "psi" ][   'L0TOS' ] = 'L0(DiMuon|Muon)Decision'
        lines [ "psi" ][   'L0TIS' ] = 'L0(Hadron|DiMuon|Muon|Electron|Photon)Decision'
        lines [ "psi" ][ 'Hlt1TOS' ] = 'Hlt1(DiMuon|SingleMuon|TrackMuon).*Decision'
        lines [ "psi" ][ 'Hlt1TIS' ] = 'Hlt1(DiMuon|SingleMuon|Track).*Decision'
        lines [ "psi" ][ 'Hlt2TOS' ] = 'Hlt2(DiMuon|ExpressJPsi|SingleMuon).*Decision'
        lines [ "psi" ][ 'Hlt2TIS' ] = 'Hlt2(Charm|Topo|DiMuon|Single).*Decision'
        #
        ## J/psi ("clean-1")
        #
        lines [ "psi1" ][   'L0TOS' ] = 'L0(DiMuon|Muon)Decision'
        lines [ "psi1" ][   'L0TIS' ] = 'L0(Hadron|DiMuon|Muon|Electron|Photon)Decision'
        lines [ "psi1" ][ 'Hlt1TOS' ] = 'Hlt1(DiMuon|TrackMuon).*Decision'
        lines [ "psi1" ][ 'Hlt1TIS' ] = 'Hlt1(DiMuon|SingleMuon|Track).*Decision'
        lines [ "psi1" ][ 'Hlt2TOS' ] = 'Hlt2DiMuon.*Decision'
        lines [ "psi1" ][ 'Hlt2TIS' ] = 'Hlt2(Charm|Topo|DiMuon|Single).*Decision'
        #
        ## J/psi ("clean-2")
        #
        lines [ "psi2" ][   'L0TOS' ] = 'L0(DiMuon|Muon)Decision'
        lines [ "psi2" ][   'L0TIS' ] = 'L0(Hadron|DiMuon|Muon|Electron|Photon)Decision'
        lines [ "psi2" ][ 'Hlt1TOS' ] = 'Hlt1DiMuonHighMass.*Decision'
        lines [ "psi2" ][ 'Hlt1TIS' ] = 'Hlt1(DiMuon|SingleMuon|Track).*Decision'
        lines [ "psi2" ][ 'Hlt2TOS' ] = 'Hlt2DiMuonDetached(Heavy|JPsi)Decision'
        lines [ "psi2" ][ 'Hlt2TIS' ] = 'Hlt2(Charm|Topo|DiMuon|Single).*Decision'
        #
        ## J/psi ("unbiased")
        #
        lines [ "psi3" ][   'L0TOS' ] = 'L0(DiMuon|Muon)Decision'
        lines [ "psi3" ][   'L0TIS' ] = 'L0(Hadron|DiMuon|Muon|Electron|Photon)Decision'
        lines [ "psi3" ][ 'Hlt1TOS' ] = 'Hlt1DiMuonHighMass.*Decision'
        lines [ "psi3" ][ 'Hlt1TIS' ] = 'Hlt1(DiMuon|SingleMuon|Track).*Decision'
        lines [ "psi3" ][ 'Hlt2TOS' ] = 'Hlt2DiMuonJPsiHighPT.*Decision'
        lines [ "psi3" ][ 'Hlt2TIS' ] = 'Hlt2(Charm|Topo|DiMuon|Single).*Decision'
        
        sc = self.tisTos_initialize ( triggers , lines )
        if sc.isFailure() : return sc
        
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

        del self._rfit # new        
        
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
        
        ## self.tisTos_finalize ()
        ## self.  fill_finalize ()
        
        return AlgoMC.finalize ( self )
    
    ## the only one esential method: 
    def analyse  (self ) :
        """
        The only one essential method
        """
        
        mcbs    = self.mcselect ( 'mcbs' , ' ( B_s0 | B_s~0 ) ==> ( J/psi(1S) => mu+ mu- ) ( phi(1020) => K+ K- ) (eta => gamma gamma) ' )
        
        t0 = self.nTuple('MC0')
        t0.fArrayMCP ( 'pt'   , MCPT / GeV , 
                       'pz'   , MCPZ / GeV ,
                       'y'    , MCY        ,
                       'ctau' , MCCTAU     ,
                       mcbs   , 
                       'nBs'  ,           ## the name of 'length' column
                       10     )           ## maximal length
        t0.column_int( 'year' , self.year   )
        t0.write()
        cnt  = self.counter('#MC')
        cnt += len(mcbs)

        if mcbs  .empty() :
            self.Warning('No true MC-Bs are found!', SUCCESS)
            mcbs1   = self.mcselect ( 'mcbs' , ' ( B_s0 | B_s~0 ) ==> ( J/psi(1S) => mu+ mu- ) K+ K-  eta ' )
            if mcbs1.empty() :
                mcbs0 = self.mcselect ( 'mcbs_all' , 'B_s0' == MCABSID  )
                print mcbs0
            return SUCCESS

        mcmu    = self.mcselect ( 'mcmu'   , ' ( B_s0 | B_s~0 ) =>  ( J/psi(1S) => ^mu+ ^mu- )  ( phi(1020) =>  K+  K- ) (eta => gamma gamma) ' )
        if mcmu  .empty() : return self.Warning('No true MC-mu  are found!', SUCCESS)

        mck     = self.mcselect ( 'mck'    , ' ( B_s0 | B_s~0 ) =>  ( J/psi(1S) =>  mu+  mu- )  ( phi(1020) => ^K+ ^K- ) (eta => gamma gamma) ' )
        if mck   .empty() : return self.Warning('No true MC-K    are found!', SUCCESS)
        
        mcg     = self.mcselect ( 'mcg'    , ' ( B_s0 | B_s~0 ) =>  ( J/psi(1S) =>  mu+  mu- )  ( phi(1020) => K+ K- ) (eta => ^gamma ^gamma) ' )
        if mcg   .empty() : return self.Warning('No true MC-gamma    are found!', SUCCESS)
        
        mcpsi   = self.mcselect ( 'mcpsi'  , ' ( B_s0 | B_s~0 ) => ^( J/psi(1S) =>  mu+  mu- )  ( phi(1020) =>  K+  K- ) (eta => gamma gamma) ' )
        if mcpsi .empty() : return self.Warning('No true MC-psi  are found!', SUCCESS)
        
        mcphi   = self.mcselect ( 'mcphi'  , ' ( B_s0 | B_s~0 ) =>  ( J/psi(1S) =>  mu+  mu- ) ^( phi(1020) =>  K+  K- ) (eta => gamma gamma) ' )
        if mcphi .empty() : return self.Warning('No true MC-phi  are found!', SUCCESS)

        mceta   = self.mcselect ( 'mceta'  , ' ( B_s0 | B_s~0 ) =>  ( J/psi(1S) =>  mu+  mu- ) ( phi(1020) =>  K+  K- ) ^(eta => gamma gamma) ' )
        if mceta .empty() : return self.Warning('No true MC-eta  are found!', SUCCESS)
        
        mcBs  = MCTRUTH ( self.mcTruth() , mcbs  )
        mcPsi = MCTRUTH ( self.mcTruth() , mcpsi )
        mcPhi = MCTRUTH ( self.mcTruth() , mcphi )
        mcEta = MCTRUTH ( self.mcTruth() , mceta )
        mcK   = MCTRUTH ( self.mcTruth() , mck   )
        mcMu  = MCTRUTH ( self.mcTruth() , mcmu  )
        mcG   = MCTRUTH ( self.mcTruth() , mcg   )
        
        tup      = self.nTuple ( 'Bp'   )
        tupmc    = self.nTuple ( 'mcBp' )

        if 1 != len( mcbs ) :
            print mcbs
            return self.Warning('illegal number of MC-decays', SUCCESS )
        
        for b in mcbs:
            #print b.decay()
            tupmc.column( "Nbs", mcbs.size() )
            tupmc.write()

        primaries = self.vselect( 'PVs' , ISPRIMARY )
        if primaries.empty() :
            return self.Warning('No primary vertices are found', SUCCESS )
        
        minPTk   = MINTREE( 'K+' == ABSID , PT            )

        minProbNNkaon = MINTREE ( 'K+' == ABSID  , PROBNNk)       
        minProbNNmuon = MINTREE ( 'mu+' == ABSID  , PROBNNmu)  

        ## pi0 veto
        vetoFun = PINFO(25015, -1000)
        
        bplus    = self.select   ( 'Bs'  , 'Beauty -> J/psi(1S) K- K+ ( eta -> gamma gamma )' )
        if bplus.empty()   : return SUCCESS

        for B in bplus:


            sc = self._rfit.reFit ( B )   # new
            if sc.isFailure() : continue  # new


            mass = M ( B ) 
            if not 5.1 * GeV < mass < 5.7 * GeV : continue
            
            psi  = B  .child ( 1 )
            k1   = B  .child ( 2 )
            k2   = B  .child ( 3 )
            mu1  = psi.child ( 1 )
            mu2  = psi.child ( 2 )
            eta  = B  .child ( 4 )
            g1   = eta.child ( 1 )
            g2   = eta.child ( 2 )
            
            #
            ## check for psi'
            #
            m_psi = M ( psi ) / GeV 
            if    m_psi  < 2.7 : continue 
            elif  m_psi  > 4.0 : continue
            elif  m_psi  > 3.3 :
                psi.setParticleID ( LHCb.ParticleID ( 100443 ) )

            if not 0.95 * GeV < M23(B) < 1.1  * GeV : continue
         
            c2dtf_0   = self._c2dtf_0 ( B )
            if not -1 < c2dtf_0 < 10 : continue
            
            ctau_0    = self._ctau_0  ( B )
            mass_0    = self._mass_0  ( B ) / GeV
            
            c2dtf_1   = self._c2dtf_1 ( B )
            ctau_1    = self._ctau_1  ( B )
            mass_1    = self._mass_1  ( B ) / GeV 
            
            c2dtf_2   = self._c2dtf_2 ( B )
            ctau_2    = self._ctau_2  ( B )
            mass_2    = self._mass_2  ( B ) / GeV 
            
            c2dtf_3   = self._c2dtf_3 ( B )
            ctau_3    = self._ctau_3  ( B )
            mass_3    = self._mass_3  ( B ) / GeV 
            

            #if not mcBs(B) == 1 : continue
            
            tup.column_float ( 'ptk' , minPTk( B ) / GeV   )
            tup.column_float ( "nnk" , minProbNNkaon ( B ) )
            tup.column_float ( "nnm" , minProbNNmuon ( B ) )
            tup.column_float ( 'cl1' , CL(g1) )
            tup.column_float ( 'cl2' , CL(g2) )

            #pi0 vetos for photons
            tup.column("pi0veto", vetoFun(eta) )   
            
            tup.column_float ( 'mass_0'  , mass_0  )
            tup.column_float ( 'mass_1'  , mass_1  )
            tup.column_float ( 'mass_2'  , mass_2  )
            tup.column_float ( 'mass_3'  , mass_3  )
            tup.column_float ( 'c2dtf_0' , c2dtf_0 )
            tup.column_float ( 'c2dtf_1' , c2dtf_1 )
            tup.column_float ( 'c2dtf_2' , c2dtf_2 )
            tup.column_float ( 'c2dtf_3' , c2dtf_3 )
            tup.column_float ( 'ctau_0'  , ctau_0  )
            tup.column_float ( 'ctau_1'  , ctau_1  )
            tup.column_float ( 'ctau_2'  , ctau_2  )
            tup.column_float ( 'ctau_3'  , ctau_3  )
            #
            tup.column_bool  ( 'hasRich_k1'  , HASRICH( k1 )  )
            tup.column_bool  ( 'hasRich_k2'  , HASRICH( k2 )  )
            #
            #
            ## fill all nmass sub-combinations 
            #
            self.fillMasses ( tup , B , ''   )
            self.fillMasses ( tup , B , 'c0' , True )
            self.fillMasses ( tup , B , 'c1' , True , strings ( [ 'J/psi(1S)' , 'psi(2S)'  ] ) )
            self.fillMasses ( tup , B , 'c2' , True , strings ( [ 'eta' ] ) )
            self.fillMasses ( tup , B , 'c3' , True , strings ( [ 'J/psi(1S)' , 'psi(2S)' , 'eta' ] ) )
            
            self.treatKine   ( tup , B    , '_b'   )
            self.treatKine   ( tup , psi  , '_psi' )
            self.treatKine   ( tup , eta  , '_eta' )
            self.treatKine   ( tup , k1   , '_k1'  )
            self.treatKine   ( tup , k2   , '_k2'  )
            self.treatKine   ( tup , g1   , '_g1'  )
            self.treatKine   ( tup , g2   , '_g2'  )
            
            self.treatPhotons ( tup , B ) 
            self.treatKaons   ( tup , B )
            self.treatMuons   ( tup , B )
            self.treatTracks  ( tup , B )

            self.tisTos ( psi , tup  , 'psi_'  , self.lines['psi'  ] )
            self.tisTos ( psi , tup  , 'psi1_' , self.lines['psi1' ] )
            self.tisTos ( psi , tup  , 'psi2_' , self.lines['psi2' ] )
            self.tisTos ( psi , tup  , 'psi3_' , self.lines['psi3' ] )

            tup.column_int  ( 'year'   , self.year   )

            #
            ## mc-truth flags
            #
            tup.column_bool ( 'mcBs'   , mcBs  ( B   ) )
            tup.column_bool ( 'mcPsi'  , mcPsi ( psi ) )
            tup.column_bool ( 'mcEta'  , mcEta ( eta ) )
            tup.column_bool ( 'mcK1'   , mcK   ( k1  ) )
            tup.column_bool ( 'mcK2'   , mcK   ( k2  ) )
            tup.column_bool ( 'mcG1'   , mcG   ( g1  ) )
            tup.column_bool ( 'mcG2'   , mcG   ( g2  ) )
            tup.column_bool ( 'mcmu1'  , mcMu  ( mu1 ) )
            tup.column_bool ( 'mcmu2'  , mcMu  ( mu2 ) )
            tup.column_bool ( 'mcPhi'  , mcPhi ( k1  ) and mcPhi( k2 ) )
            
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
    from Configurables           import EventSelector ## needed for job configuration

    from Configurables import LHCbApp
    LHCbApp().XMLSummary = 'summary.xml'



    from Configurables import PhysConf
    PhysConf().CaloReProcessing=True    

    # =========================================================================
    ## 0) Otherwise use existing stripping ilne 
    # =========================================================================
    
    from PhysSelPython.Wrappers import AutomaticData
    jpsi_location = 'FullDSTDiMuonJpsi2MuMuDetachedLine'
    jpsi = AutomaticData ( Location = '/Event/AllStreams/Phys/%s/Particles' % jpsi_location )
    
    # =============================================================================
    from StrippingArchive.Stripping21r0p1.StrippingBandQ.StrippingPsiX0        import PsiX0Conf    as PsiX0 
    from StrippingArchive.Stripping21r0p1.StrippingBandQ.StrippingPsiXForBandQ import PsiX_BQ_Conf as PsiX

    
    conf = {
        'NOPIDHADRONS'   : True ,  ## USE FOR SUIMULATION 
        ## use for B&Q wg production
        'DIMUONLINES'    : ['/Event/AllStreams/Phys/%s/Particles' % jpsi_location ] ## USE FOR B&Q WG-selection
        }
    
    psix   = PsiX   ( 'PsiX'  , conf )
    psix0  = PsiX0  ( 'PsiX0' , conf )
    
    from PhysSelPython.Wrappers import      SelectionSequence    
    selseq_kketa    = SelectionSequence ( 'B2KKeta'   , psix0 . b2KKeta    () )
    #selseq_2k       = SelectionSequence ( 'B2phi'     , psix  . psi_2K     () )
    
    #
    ## define "our" sequence
    #
    selseq          = selseq_kketa  
    #selseq          = selseq_keta_2g 
    my_alg_name     = 'Bs2JpsiPhiEta2gg'

    #
    ##
    # 
    the_year = "2012"
    
    
    davinci = DaVinci (
        DataType      = params['Year']    ,
        DDDBtag       = params['DDDB']    ,
        CondDBtag     = params['SIMCOND'] ,
        Simulation    = True     ,
        PrintFreq     = 1000     ,
        EvtMax        = -1               , 
        HistogramFile = 'DVHistos.root'  ,
        TupleFile     = 'DVNtuples.root' ,
        ##
        ## 2012 MD
        #DDDBtag       = 'dddb-20130929-1',
        #CondDBtag     = 'sim-20130522-1-vc-md100'
        ## 2012 MU
        #DDDBtag       = 'dddb-20130929-1',
        #CondDBtag     = 'sim-20130522-1-vc-mu100'
        ## 2011 MD
        #DDDBtag       = 'dddb-20130929',
        #CondDBtag     = 'sim-20130522-vc-md100'
        ## 2011 MU
        #DDDBtag       = 'dddb-20130929',
        #CondDBtag     = 'sim-20130522-vc-mu100'
        #
        )
    
    davinci.UserAlgorithms = [ selseq.sequence() , my_alg_name ] 

    #
    ## define input data
    #
    setData ( datafiles , catalogs , castor )

    #
    ## start GaudiPython/Bender
    #
    gaudi = appMgr()
    
    alg = JpsiPhi (
        my_alg_name           ,   ## Algorithm name
        Inputs = [ selseq.outputLocation() ]      ,
        #PP2MCs = [ 'Relations/Rec/ProtoP/Charged' ]  ## ONLY FOR CHARGED MODES!! , keep empty for model with neutrals!!
        ReFitPVs = True
        )

    alg.year = int( the_year )
        
    return SUCCESS 

# =============================================================================
# The actual job steering
if '__main__' == __name__ :

    ## DB:  '/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13444401/ALLSTREAMS.DST'
    inputs = [
        #'/lhcb/MC/2012/ALLSTREAMS.DST/00033514/0000/00033514_00000005_1.allstreams.dst',
        '/lhcb/MC/2012/ALLSTREAMS.DST/00033514/0000/00033514_00000006_1.allstreams.dst',
        '/lhcb/MC/2012/ALLSTREAMS.DST/00033514/0000/00033514_00000007_1.allstreams.dst',
        '/lhcb/MC/2012/ALLSTREAMS.DST/00033514/0000/00033514_00000008_1.allstreams.dst',
    ]
    #params_test = {'Year': '2012', 'DDDB': 'dddb-20130929-1', 'SIMCOND': 'sim-20130522-1-vc-md100'}
    params_test = {'Year': '2012', 'DDDB': 'dddb-20150928', 'SIMCOND': 'sim-20150522-2-vc-md100'}
    # == new calo reco (str >= 21)
    # -- sim08 familly :
    #sim['2010,reco14++']='sim-20150522'
    #sim['2011,reco14++']='sim-20150522-1'
    #sim['2012,reco14++']='sim-20150522-2'
    #sim['2013,reco14++']='sim-20150522-2'
    #sim['2015,reco14++']='sim-20150812'
    #dddb['2010']='dddb-20160318'
    #dddb['2011']='dddb-20160318-1'
    #dddb['2012']='dddb-20150928'
    #dddb['2013']='dddb-20150928'
    #dddb['2015']='dddb-20150724'
    #dddb['2016']='dddb-20150724' # as for 08/31/2016   

    configure ( inputs, params = params_test, castor = True )

    run ( 1000 )
    
    gaudi = appMgr()
    
# =============================================================================
# The END 
# =============================================================================
