/*
 * DataDumper.cc
 *
 *  Created on: Nov 5, 2021
 *      Author: kbunkow
 */

//The includes in the PreTrackMatchedMuons and other places have no the proper includes of the below files,
//so they must be before  DataDumper.h
#include "DataFormats/L1TMuon/interface/RegionalMuonCand.h"
#include "DataFormats/L1TMuonPhase2/interface/MuonStub.h"
#include "DataFormats/L1TrackTrigger/interface/TTTrack.h"
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "L1Trigger/Phase2L1GMT/interface/DataDumper.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <iostream>

namespace Phase2L1GMT {

DataDumper::DataDumper(const edm::EDGetTokenT< TTTrackAssociationMap< Ref_Phase2TrackerDigi_ > >& ttTrackMCTruthToken,
    const edm::EDGetTokenT< std::vector< TrackingParticle > >& trackingParticleToken, bool dumpToRoot) :
    ttTrackMCTruthToken(ttTrackMCTruthToken), trackingParticleToken(trackingParticleToken)
{
  if (dumpToRoot) initializeTTree();
}



void DataDumper::initializeTTree() {

  edm::Service<TFileService> fs;
  
  rootTree = fs->make<TTree>("GmtMuonTree", "");
  rootTree->Branch("tpPt", &record.tpPt);
  rootTree->Branch("tpEta", &record.tpEta);
  rootTree->Branch("tpPhi", &record.tpPhi);
  rootTree->Branch("tpCharge", &record.tpCharge); 
  rootTree->Branch("type", &record.type);

  rootTree->Branch("matching", &record.matching);

  rootTree->Branch("tttCharge", &record.tttCharge);
  rootTree->Branch("tttPt", &record.tttPt);
  rootTree->Branch("tttEta", &record.tttEta);

  rootTree->Branch("tttPhi", &record.tttPhi);
  rootTree->Branch("tttZ0", &record.tttZ0);
  rootTree->Branch("tttD0", &record.tttD0);

  rootTree->Branch("beta", &record.beta);

  rootTree->Branch("isGlobal", &record.isGlobal);

  rootTree->Branch("quality", &record.quality);

  rootTree->Branch("deltaCoords1", &record.deltaCoords1);
  rootTree->Branch("deltaCoords2", &record.deltaCoords2);
  rootTree->Branch("deltaEta1", &record.deltaEta1);
  rootTree->Branch("deltaEta2", &record.deltaEta2);
  rootTree->Branch("eventNum", &record.eventNum);

}

void DataDumper::getHandles(const edm::Event& event) {
  
  // MC truth association maps
  event.getByToken(ttTrackMCTruthToken, mcTruthTTTrackHandle);

  // tracking particles
  event.getByToken(trackingParticleToken, trackingParticleHandle);

  muonTrackingParticlesFilled = false;
  muonTrackingParticles.clear();

  eventNum=0;
  eventNum=event.id().event();
  
}

void DataDumper::process(PreTrackMatchedMuon& preTrackMatchedMuon) {

  if(!rootTree) {  
    return;}
  record.reset();
  record.eventNum = eventNum;

  auto& ttTrackPtr = preTrackMatchedMuon.trkPtr();

  if(ttTrackPtr.isNull()){
  //  rootTree->Fill();
  return;
  }
  //from ttTrack
  record.tttCharge = preTrackMatchedMuon.charge();
  record.tttPt = ttTrackPtr->momentum().perp();
  record.tttEta = preTrackMatchedMuon.eta();
  record.tttPhi = preTrackMatchedMuon.phi();
  record.tttZ0 = preTrackMatchedMuon.z0();
  record.tttD0 = preTrackMatchedMuon.d0();

  LogTrace("gmtDataDumper")<<"DataDumper::process(): preTrackMatchedMuon pt: "<<record.tttPt<<" eta "<<record.tttEta<<" phi "<<record.tttPhi;
  std::cout<<"!!!!!!!!!!!!!!!!!!!!!!!Begin of MUON!!!!!!!!!!!!!!!!!!!!!!!!!!"<<std::endl;
  std::cout<<"DataDumper::process(): preTrackMatchedMuon pt: "<<record.tttPt<<" eta: "<<record.tttEta<<" phi: "<<record.tttPhi<<std::endl;
  record.beta = preTrackMatchedMuon.beta();
  record.isGlobal =  preTrackMatchedMuon.isGlobalMuon();
  record.quality = preTrackMatchedMuon.quality();

  edm::Ptr< TrackingParticle > tpMatchedToL1MuCand = mcTruthTTTrackHandle->findTrackingParticlePtr(ttTrackPtr);

  if(tpMatchedToL1MuCand.isNonnull() ) {
    LogTrace("gmtDataDumper")<<" findTrackingParticlePtr() - found matching TrackingParticle";

    //something not good here, crashing
    if(mcTruthTTTrackHandle->isGenuine(ttTrackPtr))
      record.matching = 3;
    else if(mcTruthTTTrackHandle->isLooselyGenuine(ttTrackPtr))
      record.matching = 2;

    //record.matching = 2;
  }
  else {
    LogTrace("gmtDataDumper")<<" findTrackingParticlePtr() - nothing found";
    if(!muonTrackingParticlesFilled) {
      for (unsigned int iTP = 0; iTP < trackingParticleHandle->size(); ++iTP) {
        edm::Ptr< TrackingParticle > tpPtr(trackingParticleHandle, iTP);
        if(abs(tpPtr->pdgId()) == 13 || abs(tpPtr->pdgId()) == 1000015) {
          muonTrackingParticles.push_back(tpPtr);
        }
      }
      LogTrace("gmtDataDumper")<<"filling muonTrackingParticles: muonTrackingParticles.size() = "<<muonTrackingParticles.size();
      muonTrackingParticlesFilled = true;
    }

    bool isVeryLoose = false;
    for(auto& muonTrackingPart : muonTrackingParticles) {
      //here we have ttTracks tagged as muon by correlator that have no matching genuine/loose genuine tracking particle
      //so we go over all muonTrackingParticles and check if muonTrackingParticle has given ttTrack matched,
      //here, "match" means ttTracks that can be associated to a TrackingParticle with at least one hit of at least one of its clusters - so it is very loose match
      std::vector< edm::Ptr< TTTrack< Ref_Phase2TrackerDigi_ > > > matchedTracks = mcTruthTTTrackHandle->findTTTrackPtrs(muonTrackingPart);
      for(auto& matchedTTTrack : matchedTracks) {
        bool match = matchedTTTrack->getHitPatternWord() == ttTrackPtr->getHitPatternWord();//workaround for MVA bits missing in matches stored in EDM file
        //match = matchedTTTrack==ttTrackPtr;
        if(match) {
          isVeryLoose = true;
          tpMatchedToL1MuCand = muonTrackingPart;
          LogTrace("l1tMuBayesEventPrint") <<" veryLoose matching muonTrackingPart found";
          break;
        }
      }
      if(isVeryLoose) {
        record.matching = 1;
        break;
      }
    }
  }

  if(tpMatchedToL1MuCand.isNonnull() ) {
    if(abs(tpMatchedToL1MuCand->pdgId()) == 13 || abs(tpMatchedToL1MuCand->pdgId()) == 1000015) {
      record.type = tpMatchedToL1MuCand->pdgId();
      record.tpPt = tpMatchedToL1MuCand->pt();
      record.tpEta = tpMatchedToL1MuCand->momentum().eta();
      record.tpPhi = tpMatchedToL1MuCand->momentum().phi();

      LogTrace("gmtDataDumper")<<"ttTrack matched to the TrackingParticle";
      LogTrace("gmtDataDumper")<<" TrackingParticle type "<<(int)record.type<<" tpPt "<<record.tpPt<<" tpEta "<<record.tpEta<<" tpPhi "<<record.tpPhi ;
      std::cout<<"ttTrack matched to the TrackingParticle"<<std::endl;
      std::cout<<" TrackingParticle type "<<(int)record.type<<" tpPt "<<record.tpPt<<" tpEta "<<record.tpEta<<" tpPhi "<<record.tpPhi <<std::endl;

      
      std::cout<<"!!!!!!!!!!!!!!!!!!!!!END OF MUON!!!!!!!!!!!!!!!!!!!!!!!!"<<std::endl;
    }
  }

  record.propagatedStates = preTrackMatchedMuon.propagatedStates();



  int numStubs = 0;
  for (const auto& stub : preTrackMatchedMuon.stubs()) {
    numStubs++;
    auto prop = preTrackMatchedMuon.propagatedState(stub->tfLayer());

    // record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
    // record.deltaCoords2.at(stub->tfLayer()) = std::abs(prop.coord2 - stub->coord2());
    // record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
    // record.deltaEta2.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta2());


    // Below is the selection of the delta variables stored in the root file.
    // The selection is based on the type of the stub and the etaQuality of the stub. type==1 is barrel, type==0 is endcap.

    if(stub->type()==1){
      if(stub->etaQuality()==0 || stub->etaQuality()==1){
        record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
        record.deltaEta2.at(stub->tfLayer()) = 172;
        record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
        record.deltaCoords2.at(stub->tfLayer()) = std::abs(prop.coord2 - stub->coord2());
        //etaQuality 0 means that the stub is in the barrel and the eta2 is not defined. Eta is based on a coarse eta calculation.
        //etaQuality 1 means that the stub is in the barrel and the eta2 is not defined. Eta is based on a more precise calculation.
      }
      else if(stub->etaQuality()==3){
        record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
        record.deltaEta2.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta2());
        record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
        record.deltaCoords2.at(stub->tfLayer()) = std::abs(prop.coord2 - stub->coord2());
        //etaQuality 3 means that the stub is in the barrel and the eta2 is defined. Eta2 here is probably eta of another stub close to the first one.
      }
    }
    else if(stub->type()==0){
      if(stub->etaQuality()==1){
        record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
        record.deltaEta2.at(stub->tfLayer()) = 172;
        record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
        record.deltaCoords2.at(stub->tfLayer()) = 172;
        //etaQuality 1 means that the stub is in the endcap and is from CSC. Eta2 and coords2 are not defined.
      }
      else if(stub->etaQuality()==2){
        record.deltaEta1.at(stub->tfLayer()) = 172;
        record.deltaEta2.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta2());
        record.deltaCoords1.at(stub->tfLayer()) = 172;
        record.deltaCoords2.at(stub->tfLayer()) = std::abs(prop.coord2 - stub->coord2());
        //etaQuality 2 means that the stub is in the endcap and is from RPC. Eta1 and coords1 are not defined.
      }
      else if(stub->etaQuality()==3){
        if(stub->quality()==1){
          record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
          record.deltaEta2.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta2());
          record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
          record.deltaCoords2.at(stub->tfLayer()) = 172;
          //etaQuality 3 means that the stub is in the endcap and it is
        }
        else{
          record.deltaEta1.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta1());
          record.deltaEta2.at(stub->tfLayer()) = std::abs(prop.eta - stub->eta2());
          record.deltaCoords1.at(stub->tfLayer()) = std::abs(prop.coord1 - stub->coord1());
          record.deltaCoords2.at(stub->tfLayer()) = std::abs(prop.coord2 - stub->coord2());
          //Another option is that etaQuality 3 means that the stub is in the endcap and it is a combined RPC and CSC stub. 
        }

      }
    }
   
    
    // if(record.deltaEta2.at(0)<10){
      std::cout<<"!!!!!!!!!!!!!!!! Deltas !!!!!!!!!!!!!!!!!!!!!!!!1"<<std::endl;
      std::cout<<"Layer and variables for stub: Layer:"<<stub->tfLayer()<<" eta1:"<<stub->eta1()<<" eta2:"<<stub->eta2()<<" coord1:"<<stub->coord1()<<" coord2:"<<stub->coord2()<<" BX:"<<stub->bxNum() <<std::endl;
      std::cout<<"Variables for prop: eta:"<<prop.eta<<" coord1:"<<prop.coord1<<" coord2:"<<prop.coord2<<std::endl;
      std::cout<<"DeltaEta1 "<<(int)record.deltaEta1.at(stub->tfLayer())<<std::endl;
      std::cout<<"DeltaEta2 "<<(int)record.deltaEta2.at(stub->tfLayer())<<std::endl;
      std::cout<<"Coords1 "<<(int)record.deltaCoords1.at(stub->tfLayer())<<std::endl;
      std::cout<<"Coords2 "<<(int)record.deltaCoords2.at(stub->tfLayer())<<std::endl;
      std::cout<<"!!!!!!!!!!!!!! End of deltas !!!!!!!!!!!!!!!!!"<<std::endl;


    // }
    // else{
    //   std::cout<<"!!!!!!!!!!!!!!!! Normal deltaEta2 !!!!!!!!!!!!!!!!!!!!!!!!1"<<std::endl;
    //   std::cout<<"Layer and variables for stub: Layer:"<<stub->tfLayer()<<" eta1:"<<stub->eta1()<<" eta2:"<<stub->eta2()<<" coord1:"<<stub->coord1()<<" coord2:"<<stub->coord2()<<std::endl;
    //   std::cout<<"Variables for prop: eta:"<<prop.eta<<" coord1:"<<prop.coord1<<" coord2:"<<prop.coord2<<std::endl;
    //   std::cout<<"DeltaEta1 "<<(int)record.deltaEta1.at(stub->tfLayer())<<std::endl;
    //   std::cout<<"DeltaEta2 "<<(int)record.deltaEta2.at(stub->tfLayer())<<std::endl;
    //   std::cout<<"Coords1 "<<(int)record.deltaCoords1.at(stub->tfLayer())<<std::endl;
    //   std::cout<<"Coords2 "<<(int)record.deltaCoords2.at(stub->tfLayer())<<std::endl;
    //   std::cout<<"!!!!!!!!!!!!!! End of normal deltaEta2 !!!!!!!!!!!!!!!!!"<<std::endl;

    // }
      if(stub->bxNum()==1){
        std::cout<<"!!!!!!!!!!!!!!!!!!!!!!!Begin of stub!!!!!!!!!!!!!!!!!!!!!!!!!!"<<std::endl;
        std::cout<<"Layer and variables for stub: Layer:"<<stub->tfLayer()<<" eta1:"<<stub->eta1()<<" eta2:"<<stub->eta2()<<" coord1:"<<stub->coord1()<<" coord2:"<<stub->coord2()<<" BX:"<<stub->bxNum() <<std::endl;
        std::cout<<"Variables for prop: eta:"<<prop.eta<<" coord1:"<<prop.coord1<<" coord2:"<<prop.coord2<<std::endl;
        std::cout<<"deltaEta1: "<<(int)record.deltaEta1.at(stub->tfLayer())<<std::endl;
        std::cout<<"deltaEta2: "<<(int)record.deltaEta2.at(stub->tfLayer())<<std::endl;
        std::cout<<"deltaCoords1: "<<(int)record.deltaCoords1.at(stub->tfLayer())<<std::endl;
        std::cout<<"deltaCoords2: "<<(int)record.deltaCoords2.at(stub->tfLayer())<<std::endl;
        std::cout<<"!!!!!!!!!!!!!!!!!!!!!END OF stub!!!!!!!!!!!!!!!!!!!!!!!!"<<std::endl;
      }

    LogTrace("gmtDataDumper")<<"gmtDataDumper record: tfLayer "<<stub->tfLayer()
        <<" deltaCoords1 "<<(int)record.deltaCoords1.at(stub->tfLayer())
        <<" deltaCoords2 "<<(int)record.deltaCoords2.at(stub->tfLayer())
        <<" deltaEta1 "<<(int)record.deltaEta1.at(stub->tfLayer())
        <<" deltaEta2 "<<(int)record.deltaEta2.at(stub->tfLayer());

  }
  std::cout<<"NUMBER OF STUBS for a muon: "<<numStubs<<std::endl;
  

  // Coords1 is phi for: endcap CSC, barrel DT
  // Coords2 is phi for: endcap RPC, bending angle from barrel DT
  // Eta1 is eta for: endcap CSC, barrel DT
  // Eta2 is eta for: endcap RPC, combined eta from barrel DT and RPC
  //TF layer explanation:
  // 0- 1st station barrel/ ME1/3 CSC
  // 1- 2nd station barrel/ ME3/2 CSC or RPC
  // 2- 3rd station barrel/ ME2/2 CSC or RPC
  // 3- 4th station barrel/ ME4/2 CSC or RPC
  // 4- ME1/3 CSC or RPC
  rootTree->Fill();
  evntCnt++;
}

} /* namespace Phase2L1GMT */
