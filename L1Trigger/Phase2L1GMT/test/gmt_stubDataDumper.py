import FWCore.ParameterSet.Config as cms
process = cms.Process("L1Phase2GMTEmulation")
from pathlib import Path
import os
import random
import sys
import re
from os import listdir
from os.path import isfile, join
import glob
import copy
import datetime
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

dumpHitsFileName = 'OMTFHits_patsminDP0_v3_MuonMatcher_smoothStdDev_hwToL0X0209' 
version = 'CMSSW_15_1_0_pre2_PhaseIIGMT_ExistingV1' + timestamp 

import numpy as np


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
#process.load("Configuration.StandardSequences.GeometryDB_cff")
#process.load("Configuration.StandardSequences.GeometryIdeal_cff")
# Geometry configuration
process.load('Geometry.CMSCommonData.cmsExtendedGeometryRun4D116XML_cfi')
process.load('Configuration.Geometry.GeometryDD4hep_cff')
process.load('Configuration.Geometry.GeometryDD4hepExtendedRun4D116Reco_cff')
process.load('Geometry.MuonNumbering.muonGeometryConstants_cff')
process.load('Geometry.MuonNumbering.muonOffsetESProducer_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun4_realistic_v4', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '131X_mcRun4_realistic_v5', '') 
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T25', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '150X_mcRun4_realistic_v1', '')
#from Configuration.AlCa.autoCond import autoCond
#print("Available keys in autoCond:")
#for k in autoCond: print(k)

process.load("TrackingTools.RecoGeometry.RecoGeometries_cff")
process.load("TrackingTools.TrackRefitter.TracksToTrajectories_cff")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')





process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source

prefixPath="/scratch_cmsse/alibordi/data/simPrivateProduction/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_realistic/XTo2LLPTo4Mu_CTau5m_Phase2Exotic/231203_175643/0000" #1st Alibordi's sample
#prefixPath="/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/PrivateProductionForOMTFStudy/Displaced_cTau5m_XTo2LLTo4Mu_condPhase2_GP2024/13_1_0_23_03_2024_XTo2LLPTo4Mu/240323_145610/0000"
prefixPath1="/eos/user/a/akalinow/Data/SingleMu/14_2_1_21_03_2025/SingleMu_ch0_OneOverPt_Run2029_14_2_1_21_03_2025/*/*/*"
prefixPath2="/eos/user/a/akalinow/Data/SingleMu/14_2_1_21_03_2025/SingleMu_ch2_OneOverPt_Run2029_14_2_1_21_03_2025/*/*/*"

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:'+prefixPath+'SingleMu_OneOverPt_1_100_m_1000.root'),
                            secondaryFileNames = cms.untracked.vstring(),
                            dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
          inputCommands=cms.untracked.vstring('keep *',
                                              'drop *_l1tKMTFMuonsGmt_*_*')  
)


fileList1 = glob.glob(prefixPath1 + '/*.root')
fileList2 = glob.glob(prefixPath2 + '/*.root')
fileList = fileList1 + fileList2
random.shuffle(fileList)
fileList_mix = ['file:' + aFile for aFile in fileList]
process.source.fileNames = fileList_mix




"""
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.files.muCorrelatorEventPrint = dict()
process.MessageLogger.cerr.threshold = "DEBUG"
process.MessageLogger.cerr.DEBUG = dict(limit = -1)
process.MessageLogger.cerr.gmtDataDumper = dict(limit = -1)
process.MessageLogger.cerr.l1tGMTMuons = dict(limit = -1)
process.MessageLogger.cerr.trackMatching = dict(limit = -1)
process.MessageLogger.cerr.TrackerMuon = dict(limit = -1)
process.MessageLogger.cerr.ConvertedTTTrack = dict(limit = -1)
process.MessageLogger.debugModules = ['gmtDataDumper','EndcapStub','BarrelStub','MuonStub']
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
"""
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = "DEBUG"
process.MessageLogger.cerr.DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.debugModules = ['*']
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))







"""
#Calibrate Digi
process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi")
process.CalibratedDigis.dtDigiTag = "simMuonDTDigis"
process.CalibratedDigis.scenario = 0

#DTTriggerPhase2
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")
process.dtTriggerPhase2PrimitiveDigis.digiTag = cms.InputTag("CalibratedDigis")
process.dtTriggerPhase2PrimitiveDigis.debug = False
process.dtTriggerPhase2PrimitiveDigis.dump = False
process.dtTriggerPhase2PrimitiveDigis.scenario = 0
"""



process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
############################################
#Phase2 GMT
import L1Trigger.Phase2L1GMT.gmtStubs_cfi
process.gmtStubs = L1Trigger.Phase2L1GMT.gmtStubs_cfi.gmtStubs.clone()
process.gmtStubs.srcCSC = cms.InputTag("simCscTriggerPrimitiveDigis")
process.gmtStubs.srcDT = cms.InputTag("dtTriggerPhase2PrimitiveDigis")
process.gmtStubs.srcDTTheta = cms.InputTag("simDtTriggerPrimitiveDigis")
process.gmtStubs.srcRPC = cms.InputTag("simMuonRPCDigis")
process.gmtStubs.trackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth")
process.gmtStubs.mcTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks")
process.gmtStubs.dumpToRoot = True
process.gmtStubs.Endcap.verbose=1
process.gmtStubs.Barrel.verbose=0
process.gmtStubs.Endcap.minBX=0
process.gmtStubs.Endcap.maxBX=1
process.gmtStubs.Barrel.minBX=0
process.gmtStubs.Barrel.maxBX=1
process.gmtStubs.Barrel.minPhiQuality=0
process.gmtStubs.Barrel.minThetaQuality=0


# Load the Tracklet Emulation module
process.load("L1Trigger.TrackFindingTracklet.l1tTTTracksFromTrackletEmulation_cfi")

# Load the gmtTkMuons module
import L1Trigger.Phase2L1GMT.gmtTkMuons_cfi
process.gmtTkMuons = L1Trigger.Phase2L1GMT.gmtTkMuons_cfi.gmtTkMuons.clone()
process.gmtTkMuons.srcTracks = cms.InputTag("l1tTTTracksFromTrackletEmulation:Level1TTTracks")
process.gmtTkMuons.srcStubs = cms.InputTag("gmtStubs:tps")
process.gmtTkMuons.minTrackStubs = cms.int32(4)
process.gmtTkMuons.muonBXMin = cms.int32(0)
process.gmtTkMuons.muonBXMax = cms.int32(0)
process.gmtTkMuons.verbose = cms.int32(0)

# Configure nested PSets if needed
process.gmtTkMuons.trackConverter.verbose = cms.int32(0)
process.gmtTkMuons.trackMatching.verbose = cms.int32(0)
process.gmtTkMuons.isolation.AbsIsoThresholdL = cms.int32(160)
process.gmtTkMuons.isolation.AbsIsoThresholdM = cms.int32(120)
process.gmtTkMuons.isolation.AbsIsoThresholdT = cms.int32(80)
process.gmtTkMuons.isolation.RelIsoThresholdL = cms.double(0.1)
process.gmtTkMuons.isolation.RelIsoThresholdM = cms.double(0.05)
process.gmtTkMuons.isolation.RelIsoThresholdT = cms.double(0.01)
process.gmtTkMuons.isolation.verbose = cms.int32(0)
process.gmtTkMuons.isolation.IsodumpForHLS = cms.int32(0)


import L1Trigger.Phase2L1GMT.gmtFwdMuons_cfi
process.gmtFwdMuons = L1Trigger.Phase2L1GMT.gmtFwdMuons_cfi.gmtFwdMuons.clone()
process.gmtFwdMuons.stubs = cms.InputTag("gmtStubs", "tps")
process.gmtFwdMuons.omtfTracks = cms.InputTag("simOmtfPhase2Digis", "OMTF")
process.gmtFwdMuons.emtfTracks = cms.InputTag("simEmtfDigisPhase2")



process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")
#process.debugPath = cms.Path(process.dumpED + process.dumpES)


process.GMTPhase2Seq = cms.Sequence(process.gmtStubs + process.gmtTkMuons + process.gmtFwdMuons)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.L1TPhase2GMTPath = cms.Path(process.GMTPhase2Seq)
#process.L1TPhase2GMTPath = cms.Path(process.CalibratedDigis * process.dtTriggerPhase2PrimitiveDigis * process.GMTPhase2Seq)
process.schedule = cms.Schedule(process.L1TPhase2GMTPath, process.endjob_step)
#process.schedule.append(process.debugPath)


# Output ROOT file service
process.TFileService = cms.Service("TFileService", 
                                    fileName = cms.string(version + '.root'), 
                                    closeFileFast = cms.untracked.bool(True) )

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.numberOfConcurrentLuminosityBlocks = 1
process.options.eventSetup.numberOfConcurrentIOVs = 1


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
