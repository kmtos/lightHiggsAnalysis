// -*- C++ -*-
//
// Package:    temp/MuonsID
// Class:      MuonsID
// 
/**\class MuonsID MuonsID.cc temp/MuonsID/plugins/MuonsID.cc

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

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "Tools/Common/interface/Common.h"
//
//
// class declaration
//

class MuonsID : public edm::EDFilter {
   public:
      explicit MuonsID(const edm::ParameterSet&);
      ~MuonsID();

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
edm::EDGetTokenT<reco::MuonRefVector> muonTag_; 
edm::EDGetTokenT<reco::VertexCollection> vtxTag_;
std::string muonID_;
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
MuonsID::MuonsID(const edm::ParameterSet& iConfig):
  muonTag_(consumes<reco::MuonRefVector>(iConfig.getParameter<edm::InputTag>("muonTag"))),
  vtxTag_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vtxTag"))),
  muonID_(iConfig.getParameter<std::string>("muonID"))
{
   //now do what ever initialization is needed
   produces<reco::MuonRefVector>();
}


MuonsID::~MuonsID()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
MuonsID::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   int CountMuon=0;

   edm::Handle<reco::MuonRefVector> pMuons;
   iEvent.getByToken(muonTag_, pMuons);
   edm::Handle<reco::VertexCollection> pVertices;
   iEvent.getByToken(vtxTag_, pVertices);
   reco::Vertex* pPV = Common::getPrimaryVertex(pVertices); 
   math::XYZPoint pVertex(0., 0., 0.);
   if(pPV != NULL){
     pVertex=math::XYZPoint(pPV->position().x(), pPV->position().y(), pPV->position().z());
   }
   std::auto_ptr<reco::MuonRefVector> muonColl(new reco::MuonRefVector);
   if((pMuons->size())<1)
     return 0;
   if(muonID_=="medium")
   {
     for(reco::MuonRefVector::const_iterator iMuon=pMuons->begin();
         iMuon!=pMuons->end();++iMuon)
     {
       if (!((*iMuon)->muonBestTrack().isAvailable()) ){
             continue;
       }
       double dxy=(*iMuon)->muonBestTrack()->dxy(pVertex);
       double dz=(*iMuon)->muonBestTrack()->dz(pVertex);
       if (dxy > 0.5 || dz > 1.0){
         continue;
       }
       if(muon::isLooseMuon(**iMuon)){
         CountMuon+=1;
         muonColl->push_back(*iMuon);
       }
     }
   }
   else throw cms::Exception("CustomMuonSelector") << "Error: unsupported muon1 ID.\n";

   if(CountMuon>=2){
     iEvent.put(muonColl);
     return true;
   }
   return false;
}

// ------------ method called once each job just before starting event loop  ------------
void 
MuonsID::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MuonsID::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
MuonsID::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
MuonsID::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
MuonsID::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
MuonsID::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MuonsID::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MuonsID);
