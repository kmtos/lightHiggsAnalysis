// -*- C++ -*-
//
// Package:    temp/VetoMuon
// Class:      VetoMuon
// 
/**\class VetoMuon VetoMuon.cc temp/VetoMuon/plugins/VetoMuon.cc

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
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "Tools/Common/interface/GenTauDecayID.h"
#include "Tools/Common/interface/Common.h"

//
//
// class declaration
//

class VetoMuon : public edm::EDFilter {
   public:
      explicit VetoMuon(const edm::ParameterSet&);
      ~VetoMuon();

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
 edm::EDGetTokenT<edm::View<pat::Muon> > muonTag_;
 edm::EDGetTokenT<edm::View<pat::Muon> > vetoMuonTag_;
 double dRCut_; 
 unsigned int minNumObjsToPassFilter_;
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
VetoMuon::VetoMuon(const edm::ParameterSet& iConfig):
  muonTag_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("muonTag"))),
 vetoMuonTag_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("vetoMuonTag"))),
  dRCut_(iConfig.getParameter<double>("dRCut")),
 minNumObjsToPassFilter_(iConfig.getParameter<unsigned int>("minNumObjsToPassFilter"))
{

   //now do what ever initialization is needed
   produces<std::vector<pat::Muon> >();
}


VetoMuon::~VetoMuon()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
VetoMuon::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  std::auto_ptr<std::vector<pat::Muon> > muonColl(new std::vector<pat::Muon> );

  edm::Handle<edm::View<pat::Muon> > pMuons;
  iEvent.getByToken(muonTag_, pMuons);

  edm::Handle<edm::View<pat::Muon> > pVetoMuons;
  iEvent.getByToken(vetoMuonTag_, pVetoMuons);

  unsigned int nPassingMuons = 0;
  for(edm::View<pat::Muon>::const_iterator iMuon=pMuons->begin(); iMuon!=pMuons->end();++iMuon)
  {
    unsigned int count=0;
    for(edm::View<pat::Muon>::const_iterator iVetoMuons = pVetoMuons->begin(); iVetoMuons != pVetoMuons->end(); ++iVetoMuons)
    {
      if(deltaR(*iMuon, *iVetoMuons) < 0.01 && ( (iMuon->pt()-iVetoMuons->pt()) / iVetoMuons->pt() ) < 0.01)
        continue;
      else if(deltaR(*iMuon, *iVetoMuons) < dRCut_)
        continue;
      else count++;
    }//for iVetoMuons

    if (count == pVetoMuons->size() )
    {
      muonColl->push_back(*iMuon);
      ++nPassingMuons;
    }//if count
  }//for iMuon

  iEvent.put(muonColl);
  return (nPassingMuons >= minNumObjsToPassFilter_);
}
   

// ------------ method called once each job just before starting event loop  ------------
void 
VetoMuon::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
VetoMuon::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
VetoMuon::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
VetoMuon::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
VetoMuon::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
VetoMuon::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
VetoMuon::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(VetoMuon);
