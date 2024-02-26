# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
process = cms.Process("L1TMuonEmulation")
from pathlib import Path
import os
import random
import sys
import re
from os import listdir
from os.path import isfile, join
import glob

process.load("FWCore.MessageLogger.MessageLogger_cfi")
dumpHitsFileName = 'OMTFHits_pats0x00013_MuonMatcherNewAlgos_New' 
#version = 'interleaved_iPt2_SampleFeb15'
#version = 'GT131X_Extrapolation_GhostBusterTest_FlatPt0To1000Dxy3m_NonDegraded_Stub_v6'
version = 'small_statHTo2LLPTo4Mu'
#version = 'GT131X_Extrapolation_GhostBusterTest_MinBiasPU200'
verbose = True
runDebug = "INFO" # or "INFO" DEBUG
useExtraploationAlgo = True
#useExtraploationAlgo = False

if verbose: 
    process.MessageLogger = cms.Service("MessageLogger",
       #suppressInfo       = cms.untracked.vstring('AfterSource', 'PostModule'),
       destinations   = cms.untracked.vstring(
                                               #'detailedInfo',
                                               #'critical',
                                               #'cout',
                                               'cerr',
                                               'omtfEventPrint'
                    ),
       categories        = cms.untracked.vstring('l1tOmtfEventPrint', 'OMTFReconstruction'),
       omtfEventPrint = cms.untracked.PSet(    
                         filename  = cms.untracked.string('log_' + dumpHitsFileName),
                         extension = cms.untracked.string('.txt'),                
                         threshold = cms.untracked.string('DEBUG'),
                         default = cms.untracked.PSet( limit = cms.untracked.int32(10000) ), 
                         #INFO   =  cms.untracked.int32(0),
                         #DEBUG   = cms.untracked.int32(0),
                         l1tOmtfEventPrint = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) ),
                         OMTFReconstruction = cms.untracked.PSet( limit = cms.untracked.int32(1000000000) )
                       ),
       debugModules = cms.untracked.vstring('simOmtfDigis') 
    )
  
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
if not verbose:
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(50000)
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False), 
                                         #SkipEvent = cms.untracked.vstring('ProductNotFound') 
                                     )
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D88_cff')
process.load('Configuration.Geometry.GeometryExtended2026D99_cff')#Extended2026D99
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '131X_mcRun3_2023_realistic_v10', '') 
#process.GlobalTag = GlobalTag(process.GlobalTag, '131X_mcRun4_realistic_v7', '') 
#process.GlobalTag = GlobalTag(process.GlobalTag, 'run3_mc_FULL', '')


# input files (up to 255 files accepted)
process.source = cms.Source('PoolSource',
fileNames = cms.untracked.vstring( 
#'root:///eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt0_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084310/0000'
'root:///eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/XTo2LLPTo4Mu_cTau5m_50Files_SmallStatistics.root'    
#'file:/eos/user/a/almuhamm/ZMu_Test/Displaced13_1_0_04_11_2023/DisplacedMu_ch0_iPt1_Run2023_13_1_0_04_11_2023/13_1_0_04_11_2023/231104_150000/0000/DisplacedSingleMu_iPt_1_m_359.root'
#'file:/scratch_cmsse/akalinow/CMS/Data/SingleMu/12_5_2_p1_15_02_2023/SingleMu_ch2_iPt0_12_5_2_p1_15_02_2023/12_5_2_p1_15_02_2023/230216_100239/0000/SingleMu_iPt_0_p_47.root',

),
skipEvents =  cms.untracked.uint32(0),       
)

#samplefor Ch0 - pTbin(GeV) 0-10 10-100 100-1000
#prefixPath = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt0_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_121719/0000'
#prefixPath = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt1_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_122340/0000'
#prefixPath ='/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch0_iPt2_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_122935/0000'
#prefixPath = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt0_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_122122/0000'
#prefixPath = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt1_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_122700/0000'
#prefixPath = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy3m_pT0To1000_condPhase2_realistic/DisplacedMu_ch2_iPt2_Run2029_13_1_0_01_12_2023/13_1_0_01_12_2023/231201_123253/0000'

#prefixPath = '/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt0_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084310/0000'
#prefixPath = '/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt1_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084317/0000'
#prefixPath ='/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch0_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084329/0000'
#prefixPath ='/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt0_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084253/0000'
#prefixPath ='/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt1_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084324/0000'
#prefixPath ='/eos/user/a/akalinow/Data/SingleMu/12_5_2_p1_04_04_2023/SingleMu_ch2_iPt2_12_5_2_p1_04_04_2023/12_5_2_p1_04_04_2023/230404_084334/0000'
#prefixPath ='/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/NeutrinoGun_PU200_ForRateEstimation'
#fileList_plus = glob.glob(prefixPath + '/*.root')
#fileList_mix = ['file:' + aFile for aFile in fileList_plus]
#process.source.fileNames = fileList_mix




"""
prefix_path_1 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt0_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_093027/0000'
prefix_path_2 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt1_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_093405/0000'
prefix_path_3 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch0_iPt2_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_093827/0000'
prefix_path_4 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt0_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_093216/0000'
prefix_path_5 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt1_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_093548/0000'
prefix_path_6 = '/eos/user/a/almuhamm/ZMu_Test/simPrivateProduction/Displaced_Dxy5m_pT0To1000_condRun3_131X_mcRun3_2023_realistic_v10/DisplacedMu_ch2_iPt2_Run2023_13_1_0_23_11_2023/13_1_0_23_11_2023/231123_094009/0000'

add_allprefix_path = prefix_path_1 + prefix_path_2 + prefix_path_3 + prefix_path_4 + prefix_path_5 + prefix_path_6
fileList = glob.glob(add_allprefix_path + '/*.root')
random.shuffle(fileList)
fileList_mix = ['file:' + aFile for aFile in fileList]
process.source.fileNames = fileList_mix
"""

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000))

####Event Setup Producer
process.load('L1Trigger.L1TMuonOverlapPhase1.fakeOmtfParams_cff')
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
   toGet = cms.VPSet(
      cms.PSet(record = cms.string('L1TMuonOverlapParamsRcd'),
               data = cms.vstring('L1TMuonOverlapParams'))
                   ),
   verbose = cms.untracked.bool(False)
)


process.TFileService = cms.Service("TFileService", 
                                    fileName = cms.string('SingleMu_' + version + '.root'), 
                                    closeFileFast = cms.untracked.bool(True) )
      
                               
####OMTF Emulator
if useExtraploationAlgo :
    process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_extrapolSimple_cfi')
else :
    process.load('L1Trigger.L1TMuonOverlapPhase1.simOmtfDigis_cfi')


process.simOmtfDigis.dumpHitsToROOT = cms.bool(True)
process.simOmtfDigis.candidateSimMuonMatcher = cms.bool(True)
#process.simOmtfDigis.simTracksTag = cms.InputTag('g4SimHits')
#process.simOmtfDigis.simVertexesTag = cms.InputTag('g4SimHits')
process.simOmtfDigis.muonMatcherFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/muonMatcherHists_100files_smoothStdDev_withOvf.root")

process.simOmtfDigis.sorterType = cms.string("byLLH")
process.simOmtfDigis.ghostBusterType = cms.string("GhostBusterPreferRefDt") # byLLH byRefLayer GhostBusterPreferRefDt

if useExtraploationAlgo:
    process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0009.xml")
    process.simOmtfDigis.dtRefHitMinQuality =  cms.int32(4)
    process.simOmtfDigis.usePhiBExtrapolationFromMB1 = cms.bool(True)
    process.simOmtfDigis.usePhiBExtrapolationFromMB2 = cms.bool(True)
else :
    process.simOmtfDigis.patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0009.xml")

process.simOmtfDigis.rpcMaxClusterSize = cms.int32(3)
process.simOmtfDigis.rpcMaxClusterCnt = cms.int32(2)
process.simOmtfDigis.rpcDropAllClustersIfMoreThanMax = cms.bool(True)

process.simOmtfDigis.goldenPatternResultFinalizeFunction = cms.int32(10)

process.simOmtfDigis.noHitValueInPdf = cms.bool(True)

process.simOmtfDigis.minDtPhiQuality = cms.int32(2)
process.simOmtfDigis.minDtPhiBQuality = cms.int32(2)

process.simOmtfDigis.lctCentralBx = cms.int32(8)
####################################################
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")

process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.L1TMuonSeq = cms.Sequence( process.esProd          
                                   + process.simOmtfDigis 
                                   #+ process.dumpED
                                   #+ process.dumpES
)

process.L1TMuonPath = cms.Path(process.L1TMuonSeq)
