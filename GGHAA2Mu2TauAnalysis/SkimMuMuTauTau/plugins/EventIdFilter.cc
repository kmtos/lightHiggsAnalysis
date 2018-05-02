// -*- C++ -*-
//
// Package:    temp/EventIdFilter
// Class:      EventIdFilter
// 
/**\class EventIdFilter EventIdFilter.cc temp/EventIdFilter/plugins/EventIdFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Mengyao Shi
//         Created:  Wed, 25 Nov 2015 16:25:51 GMT
//
//


// system include files
#include <sstream>
#include <memory>
#include <iostream>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
//
//
// class declaration
//

class EventIdFilter : public edm::EDFilter {
   public:
      explicit EventIdFilter(const edm::ParameterSet&);
      ~EventIdFilter();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::FileInPath filename_;
      std::vector<std::string> events_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
EventIdFilter::EventIdFilter(const edm::ParameterSet& iConfig):
  filename_(iConfig.getParameter<edm::FileInPath>("filename"))
{

    std::cout<<"Reading file: "<<filename_.fullPath()<<std::endl;
    std::ifstream f(filename_.fullPath().c_str());


    std::string line;
    while (std::getline(f, line)) 
        events_.push_back(line);

    std::cout<<"Found "<<events_.size()<<" events to check"<<std::endl;

}


EventIdFilter::~EventIdFilter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
EventIdFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  long eventBranch_ = iEvent.id().event();
  int runBranch_   = iEvent.run();
  int lumiBranch_  = iEvent.luminosityBlock();
  std::stringstream EventIDss;
  EventIDss << runBranch_ << ':' << lumiBranch_ << ':' << eventBranch_;
  std::string EventID = EventIDss.str();

  bool printEvent = std::find(events_.begin(), events_.end(), EventID) != events_.end();
  if (printEvent)
    std::cout << EventID << std::endl;

  return printEvent; 
}
   

// ------------ method called once each job just before starting event loop  ------------
void 
EventIdFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EventIdFilter::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
EventIdFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
EventIdFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
EventIdFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
EventIdFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EventIdFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(EventIdFilter);

