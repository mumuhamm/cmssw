import FWCore.ParameterSet.Config as cms

omtfParamsSource = cms.ESSource(
    "EmptyESSource",
    recordName = cms.string('L1TMuonOverlapParamsRcd'),
    iovIsRunNotTime = cms.bool(True),
    firstValid = cms.vuint32(1)
)

###OMTF ESProducer. Fills CondFormats from XML files.
omtfParams = cms.ESProducer(
    "L1TMuonOverlapPhase1ParamsESProducer",
    patternsXMLFiles = cms.VPSet(
        #patterns used in the CMS from 19 March 2024
        cms.PSet(patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_ExtraplMB1andMB2RFixedP_ValueP1Scale_DT_2_2_2_t35__classProb17_recalib2.xml")),
    ),
    #corresponds to the algorithm version used in the CMS from 19 March 2024
    configXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0209.xml"),
)



