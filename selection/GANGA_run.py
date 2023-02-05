my_area   = '/afs/cern.ch/user/a/alexandp/cmtuser'
code_area = '/afs/cern.ch/user/a/alexandp/Analis/v6/GangaRun/'

j = Job (
    #
    name           = ''  ,
    #
    application    = Bender (
    events         = -1      ,
    version        = 'v29r5' ,
    module         = code_area + 'Bs_jpsi_kk_eta_v6.py'
    ) ,
    #
    #inputfiles     = [ '/afs/cern.ch/user/a/alexandp/Analis/v3/' + 'StrippingPsiXForBandQ.py' ],
    outputfiles    = [ LocalFile("*.root" ),   
                       LocalFile("*.xml"  ),
                       LocalFile("*.txt"  )],
    ##
    #outputsandbox  = [ 'DVHistos.root'  ]  , 
    #outputdata     = [ 'DVNtuples.root' ]  , 
    ##
    backend        = Dirac () ,
    #
    splitter=SplitByFiles( filesPerJob=5, maxFiles=-1, bulksubmit = False )
    #
    )

#from cond_run import conditions
conditions = {
    "Sig-RD-2011": [
        ('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21r1/WGBandQSelection11/90000000/PSIX0.MDST'),
        ('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21r1/WGBandQSelection11/90000000/PSIX0.MDST'),
    ],
    "Sig-RD-2012": [
        ('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21/WGBandQSelection11/Merge/90000000/PSIX0.MDST'),
        ('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/WGBandQSelection11/Merge/90000000/PSIX0.MDST'),
    ],
    "Sig-RD-2015": [
        ('/LHCb/Collision15/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco15a/Stripping24/WGBandQSelection11/90000000/PSIX0.MDST'),
        ('/LHCb/Collision15/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco15a/Stripping24/WGBandQSelection11/90000000/PSIX0.MDST'),
    ],
    "Sig-RD-2016": [
        ('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagUp/Real Data/Reco16/Stripping26/WGBandQSelection11/90000000/PSIX0.MDST'),
        ('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Reco16/Stripping26/WGBandQSelection11/90000000/PSIX0.MDST'),
    ],
}

for job_prefix, job_configs in conditions.items():

    year = "2011"
    if "2012" in job_prefix:
        year = "2012"

    for path in job_configs:

        mag = "-U"
        if "Down" in path:
            mag = "-D"

        if j.status != 'new':
            j = j.copy()

        j.name = job_prefix + mag
        j.splitter.ignoremissing = False
        j.application.params = {
            #'Mode': mode,
            'Year': year,
            #'DDDB': dddb,
            #'SIMCOND': cond,
        }

        j.inputdata = BKQuery(path).getDataset()
        #j.comment = str((path, dddb, cond))

        j.submit()


##    JpsiKKEta2gg Selection 8
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20r1/WGBandQSelection8/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20r1/WGBandQSelection8/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20/WGBandQSelection8/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20/WGBandQSelection8/90000000/PSIX0.MDST')

##    JpsiKKEta2gg Selection 9
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20r1/WGBandQSelection9/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20r1/WGBandQSelection9/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20/WGBandQSelection9/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20/WGBandQSelection9/90000000/PSIX0.MDST')

##    JpsiKKEta2gg Selection 10
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21r1/WGBandQSelection10/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21r1/WGBandQSelection10/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21/WGBandQSelection10/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/WGBandQSelection10/90000000/PSIX0.MDST')

##    JpsiKKEta2gg Selection 11
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21r1/WGBandQSelection11/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21r1/WGBandQSelection11/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping21/WGBandQSelection11/Merge/90000000/PSIX0.MDST')
#query = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/WGBandQSelection11/Merge/90000000/PSIX0.MDST')

##    JpsiPhi Selection 8
#query    = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20r1/WGBandQSelection8/90000000/PSIX.MDST')
#query    = BKQuery('/LHCb/Collision11/Beam3500GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20r1/WGBandQSelection8/90000000/PSIX.MDST')
#query    = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagUp/Real Data/Reco14/Stripping20/WGBandQSelection8/90000000/PSIX.MDST')
#query    = BKQuery('/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping20/WGBandQSelection8/90000000/PSIX.MDST')

#=============================#
#               M C           #
#=============================#

## MC JpsiKKEta2gg  13444401 
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia6/Sim08d/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia6/Sim08d/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08d/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08d/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13444401/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13444401/ALLSTREAMS.DST')

## MC JpsiKKEta2gg  13144441 OLD
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08b/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144441/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08b/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144441/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08b/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144441/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08b/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144441/ALLSTREAMS.DST')

## MC JpsiPhi 
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia6/Sim08a/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia6/Sim08a/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08a/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08a/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144001/ALLSTREAMS.DST')
#query = BKQuery('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/13144001/ALLSTREAMS.DST')


