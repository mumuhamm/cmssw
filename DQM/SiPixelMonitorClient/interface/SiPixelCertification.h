#ifndef DQM_SiPixelMonitorClient_SiPixelCertification_H
#define DQM_SiPixelMonitorClient_SiPixelCertification_H

// system include files
#include <memory>
#include <iostream>
#include <fstream>

// FWCore
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//DQM
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/MonitorElement.h"


class SiPixelCertification : public edm::EDAnalyzer {
public:
  explicit SiPixelCertification(const edm::ParameterSet&);
  ~SiPixelCertification();
  

private:
  virtual void beginJob() ;
  virtual void beginLuminosityBlock(const edm::LuminosityBlock& , const  edm::EventSetup&);
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endLuminosityBlock(const edm::LuminosityBlock& , const  edm::EventSetup&);
  virtual void endRun(const edm::Run&, const  edm::EventSetup&) ;
  virtual void endJob() ;
  
  DQMStore *dbe_;  
  
  MonitorElement * CertificationPixel;
  MonitorElement * CertificationBarrel;
  MonitorElement * CertificationEndcap;

};

#endif
