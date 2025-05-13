#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "L1Trigger/Phase2L1GMT/interface/PreTrackMatchedMuon.h"
#include "L1Trigger/Phase2L1GMT/interface/L1TPhase2GMTEndcapStubProcessor.h"
#include "L1Trigger/Phase2L1GMT/interface/L1TPhase2GMTBarrelStubProcessor.h"
#include "L1Trigger/Phase2L1GMT/interface/DataDumper.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/ESProducts.h"
#include "FWCore/Utilities/interface/ESGetToken.h"
//
// class declaration
//

class Phase2L1TGMTStubProducer : public edm::stream::EDProducer<> {
public:
  explicit Phase2L1TGMTStubProducer(const edm::ParameterSet&);
  ~Phase2L1TGMTStubProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;
  l1t::MuonStub convertToHybrid(const l1t::MuonStub& stub);
  edm::EDGetTokenT<MuonDigiCollection<CSCDetId, CSCCorrelatedLCTDigi>> srcCSC_;
  edm::EDGetTokenT<L1Phase2MuDTPhContainer> srcDT_;
  edm::EDGetTokenT<L1MuDTChambThContainer> srcDTTheta_;
  edm::EDGetTokenT<RPCDigiCollection> srcRPC_;

  L1TPhase2GMTEndcapStubProcessor* procEndcap_;
  L1TPhase2GMTBarrelStubProcessor* procBarrel_;
  L1TMuon::GeometryTranslator* translator_;
  edm::EDGetTokenT< TTTrackAssociationMap< Ref_Phase2TrackerDigi_ > > ttTrackMCTruthToken_;
  edm::EDGetTokenT< std::vector< TrackingParticle > > trackingParticleToken_;
  Phase2L1GMT::DataDumper dataDumper;
  int verbose_;
};

Phase2L1TGMTStubProducer::Phase2L1TGMTStubProducer(const edm::ParameterSet& iConfig)
    : srcCSC_(consumes<MuonDigiCollection<CSCDetId, CSCCorrelatedLCTDigi>>(iConfig.getParameter<edm::InputTag>("srcCSC"))),
      srcDT_(consumes<L1Phase2MuDTPhContainer>(iConfig.getParameter<edm::InputTag>("srcDT"))),
      srcDTTheta_(consumes<L1MuDTChambThContainer>(iConfig.getParameter<edm::InputTag>("srcDTTheta"))),
      srcRPC_(consumes<RPCDigiCollection>(iConfig.getParameter<edm::InputTag>("srcRPC"))),
      procEndcap_(new L1TPhase2GMTEndcapStubProcessor(iConfig.getParameter<edm::ParameterSet>("Endcap"))),
      procBarrel_(new L1TPhase2GMTBarrelStubProcessor(iConfig.getParameter<edm::ParameterSet>("Barrel"))),
      ttTrackMCTruthToken_(consumes< TTTrackAssociationMap< Ref_Phase2TrackerDigi_ > >(iConfig.getParameter<edm::InputTag>("mcTruthTrackInputTag"))),
      trackingParticleToken_(consumes< std::vector< TrackingParticle > >(iConfig.getParameter<edm::InputTag>("trackingParticleInputTag"))),
      dataDumper(ttTrackMCTruthToken_, trackingParticleToken_, iConfig.getParameter<bool>("dumpToRoot")), 
      verbose_(iConfig.getParameter<int>("verbose")) {
  produces<l1t::MuonStubCollection>("kmtf");
  produces<l1t::MuonStubCollection>("tps");
  edm::ConsumesCollector consumesColl(consumesCollector());
  translator_ = new L1TMuon::GeometryTranslator(consumesColl);
}

Phase2L1TGMTStubProducer::~Phase2L1TGMTStubProducer() {
  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
  if (procEndcap_ != nullptr)
    delete procEndcap_;
  if (procBarrel_ != nullptr)
    delete procBarrel_;
  if (translator_ != nullptr)
    delete translator_;
}

//
// member functions
//

l1t::MuonStub Phase2L1TGMTStubProducer::convertToHybrid(const l1t::MuonStub& stub) {
  l1t::MuonStub hybrid(stub.etaRegion(),
                       stub.phiRegion(),
                       stub.depthRegion(),
                       stub.tfLayer(),
                       stub.coord1() / 256,  //for track matching was 1024
                       stub.coord2() / 256,  //for track matching was 1024
                       stub.id(),
                       stub.bxNum(),
                       0x3,  //for track matching
                       stub.eta1(),
                       stub.eta2(),
                       stub.etaQuality(),
                       stub.type());
  hybrid.setOfflineQuantities(stub.offline_coord1(), stub.offline_coord2(), stub.offline_eta1(), stub.offline_eta2());
  return hybrid;
}

// ------------ method called to produce the data  ------------
void Phase2L1TGMTStubProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  translator_->checkAndUpdateGeometry(iSetup);

  Handle<MuonDigiCollection<CSCDetId, CSCCorrelatedLCTDigi>> cscDigis;
  iEvent.getByToken(srcCSC_, cscDigis);

  Handle<RPCDigiCollection> rpcDigis;
  iEvent.getByToken(srcRPC_, rpcDigis);

  Handle<L1Phase2MuDTPhContainer> dtDigis;
  iEvent.getByToken(srcDT_, dtDigis);

  Handle<L1MuDTChambThContainer> dtThetaDigis;
  iEvent.getByToken(srcDTTheta_, dtThetaDigis);


    //edm::Handle<std::vector<TTTrack<Ref_Phase2TrackerDigi_>>> mcTruthTTTrackHandle
    edm::Handle<TTTrackAssociationMap<Ref_Phase2TrackerDigi_>> mcTruthTTTrackHandle;
    iEvent.getByToken(ttTrackMCTruthToken_, mcTruthTTTrackHandle);


  //Generate a unique stub ID
  l1t::MuonStubCollection stubs;
  l1t::MuonStubCollection stubsKMTF;

  l1t::MuonStubCollection stubsEndcap = procEndcap_->makeStubs(*cscDigis, *rpcDigis, translator_, iSetup);
  for (auto& stub : stubsEndcap) {
    stubs.push_back(stub);
  }
  l1t::MuonStubCollection stubsBarrel = procBarrel_->makeStubs(dtDigis.product(), dtThetaDigis.product());
  for (auto& stub : stubsBarrel) {
    //convert to Hybrid
    stubs.push_back(convertToHybrid(stub));
    stubsKMTF.push_back(stub);
  }

   // Put the stubs into the event
    auto stubsHandle = iEvent.put(std::make_unique<l1t::MuonStubCollection>(stubs), "tps");
    iEvent.put(std::make_unique<l1t::MuonStubCollection>(stubsKMTF), "kmtf");

    // Create PreTrackMatchedMuon objects
    std::vector<Phase2L1GMT::PreTrackMatchedMuon> preTrackMatchedMuons;
   
 for (size_t index = 0; index < stubs.size(); ++index) {
    // Create a reference to the stub
    edm::Ref<l1t::MuonStubCollection> stubRef(stubsHandle, index);

    // Create a PreTrackMatchedMuon object
    Phase2L1GMT::PreTrackMatchedMuon preTrackMatchedMuon(
        0,  // Default charge value
        stubRef->coord1(), stubRef->coord2(), stubRef->tfLayer(), stubRef->bxNum(), 0);

    // Add the stub reference to the PreTrackMatchedMuon object
    preTrackMatchedMuon.addStub(stubRef, 0x1);

    edm::Ptr<TTTrack<Ref_Phase2TrackerDigi_>> matchedTTTrackPtr;

    // Loop over all TTTracks in the association map
    const auto& trackToTPMap = mcTruthTTTrackHandle->getTTTrackToTrackingParticleMap();
    for (const auto& [ttTrackPtr, trackingParticlePtr] : trackToTPMap) {
      std::cout << "TTTrack ID: " << ttTrackPtr.id() << ", TrackingParticle ID: " << trackingParticlePtr.id() << std::endl;
        // Check if the TTTrack is associated with the current stub
        // Since there is no direct link, you may need to implement custom logic here
        // For example, you could check if the TTTrack's eta/phi matches the MuonStub's eta/phi
        if (std::abs(stubRef->eta1() - ttTrackPtr->momentum().eta()) < 0.1 &&
    std::abs(stubRef->coord1() - ttTrackPtr->momentum().phi()) < 0.1) {
    matchedTTTrackPtr = ttTrackPtr;
    break;
}
    }

    if (matchedTTTrackPtr.isNonnull()) {
        // Retrieve the associated TrackingParticle
        edm::Ptr<TrackingParticle> trackingParticlePtr = mcTruthTTTrackHandle->findTrackingParticlePtr(matchedTTTrackPtr);

        if (trackingParticlePtr.isNonnull()) {
            // Retrieve the associated TTTrack pointers using the TrackingParticle
            std::vector<edm::Ptr<TTTrack<Ref_Phase2TrackerDigi_>>> ttTrackPtrs =
                mcTruthTTTrackHandle->findTTTrackPtrs(trackingParticlePtr);

            // Check if there are any associated tracks
            if (!ttTrackPtrs.empty()) {
                edm::Ptr<TTTrack<Ref_Phase2TrackerDigi_>> associatedTTTrackPtr = ttTrackPtrs[0];  // Use the first associated track
                preTrackMatchedMuon.setTrkPtr(associatedTTTrackPtr);
            } else {
                std::cout << "Phase2L1TGMTStubProducer: No TTTrack pointer found for TrackingParticle!" << std::endl;
            }
        } else {
            std::cout << "Phase2L1TGMTStubProducer: No TrackingParticle found for TTTrack!" << std::endl;
        }
    } else {
        std::cout << "Phase2L1TGMTStubProducer: No TTTrack found for stub!" << std::endl;
    }

    // Add the PreTrackMatchedMuon to the collection
    preTrackMatchedMuons.push_back(preTrackMatchedMuon);
}
    // Call DataDumper to process the PreTrackMatchedMuon objects
    dataDumper.getHandles(iEvent);

    for (auto& preTrackMatchedMuon : preTrackMatchedMuons) {
        dataDumper.process(preTrackMatchedMuon);
    }

}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void Phase2L1TGMTStubProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void Phase2L1TGMTStubProducer::endStream() {}

void Phase2L1TGMTStubProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // gmtStubs
  edm::ParameterSetDescription desc;
  desc.add<int>("verbose", 0);
  desc.add<edm::InputTag>("srcCSC", edm::InputTag("simCscTriggerPrimitiveDigis"));
  desc.add<edm::InputTag>("srcDT", edm::InputTag("dtTriggerPhase2PrimitiveDigis"));
  desc.add<edm::InputTag>("srcDTTheta", edm::InputTag("simDtTriggerPrimitiveDigis"));
  desc.add<edm::InputTag>("srcRPC", edm::InputTag("simMuonRPCDigis"));
  {
    edm::ParameterSetDescription psd0;
    psd0.add<unsigned int>("verbose", 0);
    psd0.add<int>("minBX", 0);
    psd0.add<int>("maxBX", 0);
    psd0.add<double>("coord1LSB", 0.02453124992);
    psd0.add<double>("eta1LSB", 0.024586688);
    psd0.add<double>("coord2LSB", 0.02453124992);
    psd0.add<double>("eta2LSB", 0.024586688);
    psd0.add<double>("phiMatch", 0.05);
    psd0.add<double>("etaMatch", 0.1);
    desc.add<edm::ParameterSetDescription>("Endcap", psd0);
  }
  {
    edm::ParameterSetDescription psd0;
    psd0.add<int>("verbose", 0);
    psd0.add<int>("minPhiQuality", 0);
    psd0.add<int>("minThetaQuality", 0);
    psd0.add<int>("minBX", 0);
    psd0.add<int>("maxBX", 0);
    psd0.add<double>("phiLSB", 0.02453124992);
    psd0.add<int>("phiBDivider", 16);
    psd0.add<double>("etaLSB", 0.024586688);
    psd0.add<std::vector<int>>(
        "eta_1",
        {
            -46, -45, -43, -41, -39, -37, -35, -30, -28, -26, -23, -20, -18, -15, -9, -6, -3, -1,
            1,   3,   6,   9,   15,  18,  20,  23,  26,  28,  30,  35,  37,  39,  41, 43, 45, 1503,
        });
    psd0.add<std::vector<int>>(
        "eta_2",
        {
            -41, -39, -38, -36, -34, -32, -30, -26, -24, -22, -20, -18, -15, -13, -8, -5, -3, -1,
            1,   3,   5,   8,   13,  15,  18,  20,  22,  24,  26,  30,  32,  34,  36, 38, 39, 1334,
        });
    psd0.add<std::vector<int>>(
        "eta_3",
        {
            -35, -34, -32, -31, -29, -27, -26, -22, -20, -19, -17, -15, -13, -11, -6, -4, -2, -1,
            1,   2,   4,   6,   11,  13,  15,  17,  19,  20,  22,  26,  27,  29,  31, 32, 34, 1148,
        });
    psd0.add<std::vector<int>>("coarseEta_1",
                               {
                                   0,
                                   23,
                                   41,
                               });
    psd0.add<std::vector<int>>("coarseEta_2",
                               {
                                   0,
                                   20,
                                   36,
                               });
    psd0.add<std::vector<int>>("coarseEta_3",
                               {
                                   0,
                                   17,
                                   31,
                               });
    psd0.add<std::vector<int>>("coarseEta_4",
                               {
                                   0,
                                   14,
                                   27,
                               });
    psd0.add<std::vector<int>>("phiOffset",
                               {
                                   1,
                                   0,
                                   0,
                                   0,
                               });
    desc.add<edm::ParameterSetDescription>("Barrel", psd0);
    desc.add<edm::InputTag>("mcTruthTrackInputTag", edm::InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"));
    desc.add<edm::InputTag>("trackingParticleInputTag", edm::InputTag("mix", "MergedTrackTruth"));
    desc.add<bool>("dumpToRoot", true); 

  }
  descriptions.add("gmtStubs", desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Phase2L1TGMTStubProducer);
