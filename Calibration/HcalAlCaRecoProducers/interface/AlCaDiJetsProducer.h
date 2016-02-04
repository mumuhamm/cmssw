#ifndef AlCaDiJetsProducer_h
#define AlCaDiJetsProducer_h


// -*- C++ -*-


// system include files
#include <memory>
#include <string>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"
#include "DataFormats/DetId/interface/DetId.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"

//
// class declaration
//
namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace cms
{

class AlCaDiJetsProducer : public edm::EDProducer {
   public:
     explicit AlCaDiJetsProducer(const edm::ParameterSet&);
     ~AlCaDiJetsProducer();

     virtual void beginJob() ;

     virtual void produce(edm::Event &, const edm::EventSetup&);
   private:
      // ----------member data ---------------------------
     edm::InputTag jetsInput_;
     std::vector<edm::InputTag> ecalLabels_;
     edm::InputTag hbheInput_;
     edm::InputTag hoInput_;
     edm::InputTag hfInput_;

     bool allowMissingInputs_;

};
}// end namespace cms
#endif
