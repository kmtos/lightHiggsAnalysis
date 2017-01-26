// -*- C++ -*-
//
// Package:    temp/HighestSecondHighestPtSelector
// Class:      HighestSecondHighestPtSelector
// 
/**\class HighestSecondHighestPtSelector HighestSecondHighestPtSelector.cc temp/HighestSecondHighestPtSelector/plugins/HighestSecondHighestPtSelector.cc

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

class HighestSecondHighestPtSelector : public edm::EDFilter {
   public:
      explicit HighestSecondHighestPtSelector(const edm::ParameterSet&);
      ~HighestSecondHighestPtSelector();

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
std::map<std::string, TH1D*> histos1D_;
std::string muon1ID_;
std::string muon2ID_;
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
HighestSecondHighestPtSelector::HighestSecondHighestPtSelector(const edm::ParameterSet& iConfig):
  muonTag_(consumes<reco::MuonRefVector>(iConfig.getParameter<edm::InputTag>("muonTag"))),
  vtxTag_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vtxTag"))),
  histos1D_(),
  muon1ID_(iConfig.getParameter<std::string>("muon1ID")),
  muon2ID_(iConfig.getParameter<std::string>("muon2ID"))
{
   //now do what ever initialization is needed
   produces<reco::MuonRefVector>();
}


HighestSecondHighestPtSelector::~HighestSecondHighestPtSelector()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
HighestSecondHighestPtSelector::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   bool LargerThan0=true;
   using namespace edm;

   edm::Handle<reco::MuonRefVector> pMuons;
   iEvent.getByToken(muonTag_, pMuons); 
   if((pMuons->size())<=1)
   {
     LargerThan0=false;
   }
   else
   {
     double max=0.0;
     double secondMax=0.0;
     bool Mu1Identified=false;
     bool Mu2Identified=false;
     reco::MuonRef maxMuon;
     reco::MuonRef secondMaxMuon;
     for(reco::MuonRefVector::const_iterator iMuon=pMuons->begin();
         iMuon!=pMuons->end();++iMuon)
     {
       if(((*iMuon)->pt())> max)
       {
         max=(*iMuon)->pt();
         maxMuon=(*iMuon);
       }
       else
         continue;
     }
    

     for(reco::MuonRefVector::const_iterator iMuon=pMuons->begin();
         iMuon!=pMuons->end();++iMuon)
     {
       if(((*iMuon)->pt()< (maxMuon->pt()))&&((*iMuon)->pt()>secondMax )&&((*iMuon)->pdgId()==(-1)*((maxMuon)->pdgId())))
       {
         secondMax=(*iMuon)->pt();
         secondMaxMuon=(*iMuon);
       }
       else 
  	  continue;
     }
     
     edm::Handle<reco::VertexCollection> pVertices;
     iEvent.getByToken(vtxTag_, pVertices);
     reco::Vertex* pPV = Common::getPrimaryVertex(pVertices);

     if(!(secondMaxMuon.isNull()))
     {  
       if(muon1ID_ == "loose"){
         if( muon::isLooseMuon(*maxMuon))
           Mu1Identified = true;
         else Mu1Identified = false;
       }
       else if(muon1ID_== "tightNew"){
         if ((pPV != NULL) && muon::isTightMuon(*maxMuon, *pPV))
            Mu1Identified = true;
         else Mu1Identified = false;
       }
       else throw cms::Exception("CustomMuonSelector") << "Error: unsupported muon1 ID.\n";

       if(muon2ID_ == "loose"){
         if(muon::isLooseMuon(*secondMaxMuon))
           Mu2Identified = true;
         else
           Mu2Identified = false;
       }
       else if(muon2ID_ == "tightNew"){
         if((pPV != NULL) && muon::isTightMuon(*secondMaxMuon, *pPV))
            Mu2Identified = true;
         else Mu2Identified = false;
       }
       else throw cms::Exception("CustomMuonSelector") << "Error: unsupported muon2 ID.\n";

     }
     else{
       LargerThan0=0; return LargerThan0;
     }
     
     if(Mu1Identified==false || Mu2Identified==false )
     {
       LargerThan0=0;
       return 
       LargerThan0;
     }
     else
     {
       LargerThan0=1;  
       std::auto_ptr<reco::MuonRefVector> muonColl(new reco::MuonRefVector);
       histos1D_["Pt_SecondHighest"]->Fill(secondMaxMuon->pt());
       muonColl->push_back(maxMuon);
       muonColl->push_back(secondMaxMuon);
       iEvent.put(muonColl);
     }
   }

   return LargerThan0;
}

// ------------ method called once each job just before starting event loop  ------------
void 
HighestSecondHighestPtSelector::beginJob()
{
 edm::Service<TFileService> fileService;
  histos1D_[ "Pt_SecondHighest" ]=fileService->make<TH1D>("Pt_SecondHighest","bla",100,0,500);
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HighestSecondHighestPtSelector::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
HighestSecondHighestPtSelector::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
HighestSecondHighestPtSelector::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
HighestSecondHighestPtSelector::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
HighestSecondHighestPtSelector::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HighestSecondHighestPtSelector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(HighestSecondHighestPtSelector);
