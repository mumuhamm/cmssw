# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --conditions 123X_mcRun4_realistic_v3 -n 2 --era Phase2C9 --eventcontent FEVTDEBUGHLT --runUnscheduled file:/eos/cms/store/relval/CMSSW_11_0_0/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200-v2/10000/01054EE2-1B51-C449-91A2-5202A60D16A3.root -s RAW2DIGI,L1TrackTrigger,L1 --datatier FEVTDEBUGHLT --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,L1Trigger/Configuration/customisePhase2TTNoMC.customisePhase2TTNoMC,Configuration/DataProcessing/Utils.addMonitoring,L1Trigger/Configuration/customisePhase2FEVTDEBUGHLT.customisePhase2FEVTDEBUGHLT --geometry Extended2026D49 --fileout file:/tmp/step1_Reprocess_TrackTrigger_L1.root --no_exec --nThreads 8 --python step1_L1_ProdLike.py --processName=L1REPR
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('L1REPROCESS',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D114Reco_cff')
process.load("TrackingTools.RecoGeometry.RecoGeometries_cff")
process.load("TrackingTools.TrackRefitter.TracksToTrajectories_cff")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("TrackingTools.RecoGeometry.RecoGeometries_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(2000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
# prefixPath="/scratch_cmsse/akalinow/CMS/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_OneOverPt_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084346/0000/" #second sample
#prefixPath = "/scratch_cmsse/akalinow/CMS/Data/SingleMu/13_1_0_03_01_2024/SingleMu_ch2_OneOverPt_Run2029_13_1_0_03_01_2024/13_1_0_03_01_2024/240103_094121/0000/" #first sample
#prefixPath = "/scratch_cmsse/akalinow/CMS/Data/SingleMu/13_1_0_04_01_2024/"
#prefixPath = "/scratch_cmsse/akalinow/CMS/Data/SingleMu/13_1_0_13_02_2024/"
#prefixPath = '/scratch_cmsse/akalinow/CMS/Data/DisplacedMu/14_1_0pre3_11_06_2024_Dxy5m_PhaseII/'
#prefixPath = '/scratch/rkomuda/Magisterium/Analysis/'
prefixPath="/scratch_cmsse/alibordi/data/simPrivateProduction/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_realistic/XTo2LLPTo4Mu_CTau5m_Phase2Exotic/231203_175643/0000" #1st Alibordi's sample
# prefixPath="/scratch_cmsse/alibordi/data/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt0_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_121719/0000" #2nd Alibordi's sample


process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:'+prefixPath+'SingleMu_OneOverPt_1_100_m_1000.root'),
                            secondaryFileNames = cms.untracked.vstring(),
                                      dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
          inputCommands=cms.untracked.vstring('keep *',
                                              'drop *_l1tKMTFMuonsGmt_*_*')  
)

import glob
import numpy as np
fileList = glob.glob(prefixPath+'/*.root')
if not len(fileList):
    fileList = glob.glob(prefixPath+'/*/*/*/*/*.root')
fileList = np.random.default_rng().permutation(fileList)
fileList = ['file:'+aFile for aFile in fileList]

# for i in range(fileList.size):
#     fileList[i] = 'file:'+fileList[i]+'.root'
# print(fileList)

process.source.fileNames = fileList


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.files.muCorrelatorEventPrint = dict()
process.MessageLogger.cerr.threshold = "DEBUG"
process.MessageLogger.cerr.DEBUG = dict(limit = -1)
process.MessageLogger.cerr.OMTFReconstruction = dict(limit = -1)
process.MessageLogger.cerr.gmtDataDumper = dict(limit = -1)
process.MessageLogger.cerr.l1tGMTMuons = dict(limit = -1)
process.MessageLogger.cerr.trackMatching = dict(limit = -1)
process.MessageLogger.cerr.TrackerMuon = dict(limit = -1)
process.MessageLogger.cerr.ConvertedTTTrack = dict(limit = -1)
process.MessageLogger.debugModules = ['gmtDataDumper','EndcapStub','BarrelStub','MuonStub']
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Geometry
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun4_realistic_v4', '')

####Event Setup Producer (Run4 GlobalTag has outdated OMTF parameters)
process.load('L1Trigger.L1TMuonOverlapPhase1.fakeOmtfParams_cff')
process.omtfParams.configXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0209.xml")
process.omtfParams.patternsXMLFiles = cms.VPSet(
        cms.PSet(patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1nadMB2DTQualAndRFixedP_DT_2_2_t30__classProb17_recalib2.xml")),
)
#reading config and patterns from the DB
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
   toGet = cms.VPSet(
      cms.PSet(record = cms.string('L1TMuonOverlapParamsRcd'),
               data = cms.vstring('L1TMuonOverlapParams'))
                   ),
   verbose = cms.untracked.bool(False)
)
############################################
# Output ROOT file service
process.TFileService = cms.Service("TFileService", 
                                    fileName = cms.string('test.root'), 
                                    closeFileFast = cms.untracked.bool(True) )
############################################
##
#Calibrate Digi
process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi")
process.CalibratedDigis.dtDigiTag = "simMuonDTDigis" 
process.CalibratedDigis.scenario = 0

#DTTriggerPhase2
# process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi") #tak było przed zmianą od Karola
# process.dtTriggerPhase2PrimitiveDigis.debug = True
# process.dtTriggerPhase2PrimitiveDigis.dump = False
# process.dtTriggerPhase2PrimitiveDigis.scenario = 0

# process.DTPhase2DigisPath = cms.Path(process.CalibratedDigis*process.dtTriggerPhase2PrimitiveDigis)

#DTTriggerPhase2
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")
process.dtTriggerPhase2PrimitiveDigis.debug = False
process.dtTriggerPhase2PrimitiveDigis.dump = False
process.dtTriggerPhase2PrimitiveDigis.scenario = 0

process.L1TMuonPath = cms.Path(process.CalibratedDigis * process.dtTriggerPhase2PrimitiveDigis )
############################################
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
############################################
#Phase2 GMT
process.load("L1Trigger.Phase2L1GMT.gmt_cff")
process.l1tGMTMuons.isolation.IsodumpForHLS = 0
process.l1tGMTMuons.trackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth")
process.l1tGMTMuons.mcTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks")
process.l1tGMTMuons.dumpToRoot = cms.bool(True)
process.l1tGMTStubs.Endcap.verbose=0
process.l1tGMTStubs.Barrel.verbose=0
process.l1tGMTStubs.Endcap.minBX=0
process.l1tGMTStubs.Endcap.maxBX=1
process.l1tGMTStubs.Barrel.minBX=0
process.l1tGMTStubs.Barrel.maxBX=1
process.l1tGMTMuons.muonBXMin=0
process.l1tGMTMuons.muonBXMax=1
# process.l1tGMTMuons.minTrackStubs=2

process.GMTPhase2Path = cms.Path(process.L1TrackTrigger*process.l1tGMTStubs*process.l1tGMTMuons)
############################################
####OMTF Emulator
import L1Trigger.L1TMuonOverlapPhase2.simOmtfPhase2Digis_DT_2_2_2_cff
process.simOmtfPhase2Digis=L1Trigger.L1TMuonOverlapPhase2.simOmtfPhase2Digis_DT_2_2_2_cff.simOmtfPhase2Digis.clone() 
process.simOmtfPhase2Digis.dumpHitsToROOT = cms.bool(True)
process.simOmtfPhase2Digis.dumpResultToXML = cms.bool(False)
process.simOmtfPhase2Digis.candidateSimMuonMatcher = cms.bool(True)
process.simOmtfPhase2Digis.candidateSimMuonMatcherType = cms.string("propagation")   
process.simOmtfPhase2Digis.simTracksTag = cms.InputTag('g4SimHits')
process.simOmtfPhase2Digis.simVertexesTag = cms.InputTag('g4SimHits')
process.simOmtfPhase2Digis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")
process.simOmtfPhase2Digis.bxMin = cms.int32(0)
process.simOmtfPhase2Digis.bxMax = cms.int32(1)
process.omtfPath = cms.Path(process.esProd*process.simOmtfPhase2Digis)
############################################
# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.L1TMuonPath,process.omtfPath,process.GMTPhase2Path,process.endjob_step)

#Setup FWK for multithreaded
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.numberOfConcurrentLuminosityBlocks = 1
process.options.eventSetup.numberOfConcurrentIOVs = 1

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000 

#call to customisation function customise_aging_1000 imported from SLHCUpgradeSimulations.Configuration.aging
process = customise_aging_1000(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2TTNoMC
from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC 

#call to customisation function customisePhase2TTNoMC imported from L1Trigger.Configuration.customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)
# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
