// -*- C++ -*-
//
// Package:    temp/HighestPtAndMuonSignDRSelector
// Class:      HighestPtAndMuonSignDRSelector
// 
/**\class HighestPtAndMuonSignDRSelector HighestPtAndMuonSignDRSelector.cc temp/HighestPtAndMuonSignDRSelector/plugins/HighestPtAndMuonSignDRSelector.cc

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
//
//
// class declaration
//

class HighestPtAndMuonSignDRSelector : public edm::EDFilter {
   public:
      explicit HighestPtAndMuonSignDRSelector(const edm::ParameterSet&);
      ~HighestPtAndMuonSignDRSelector();

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
  double Cut_;
  double Mu1PtCut_;
  double Mu2PtCut_;
  bool oppositeSign_;
  bool passdR_;
  std::map<std::string, TH1D*> histos1D_;
  
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
HighestPtAndMuonSignDRSelector::HighestPtAndMuonSignDRSelector(const edm::ParameterSet& iConfig):
  muonTag_(consumes<reco::MuonRefVector>(iConfig.getParameter<edm::InputTag>("muonTag"))),
  Cut_(iConfig.getParameter<double>("dRCut")),
  Mu1PtCut_(iConfig.getParameter<double>("Mu1PtCut")),
  Mu2PtCut_(iConfig.getParameter<double>("Mu2PtCut")),
  oppositeSign_(iConfig.getParameter<bool>("oppositeSign")),
  passdR_(iConfig.existsAs<bool>("passdR")? iConfig.getParameter<bool>("passdR"):true),  
  histos1D_()
{
   //now do what ever initialization is needed
   produces<reco::MuonRefVector>();
}


HighestPtAndMuonSignDRSelector::~HighestPtAndMuonSignDRSelector()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
HighestPtAndMuonSignDRSelector::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   bool LargerThan0=true;
   using namespace edm;
   using namespace std;
   edm::Handle<reco::MuonRefVector> pMuons;
   iEvent.getByToken(muonTag_, pMuons); 

   if( (pMuons->size()) <= 1)
     LargerThan0=false;
   else
   {
     double max=0.0;
     reco::MuonRef maxMuon;
     reco::MuonRef OppositeSignSmallDRMuon;
     for(reco::MuonRefVector::const_iterator iMuon=pMuons->begin(); iMuon!=pMuons->end();++iMuon)
     {
       if( ((*iMuon)->pt()) > max)
       {
         max=(*iMuon)->pt();
         maxMuon=(*iMuon);
       }
       else
         continue;
     }
     //cout<<"maxMuonPt="<<maxMuon->pt()<<std::endl;
     std::auto_ptr<reco::MuonRefVector> muonColl(new reco::MuonRefVector);
     muonColl->push_back(maxMuon);

     for(reco::MuonRefVector::const_iterator iMuon=pMuons->begin(); iMuon!=pMuons->end();++iMuon)
     {
       //cout<<"(*iMuon)->pt() ="<<(*iMuon)->pt()<<"; deltaR(**iMuon, *maxMuon)="<<deltaR(**iMuon, *maxMuon)<<"; sign ="<<((*iMuon)->pdgId() == (1)*((maxMuon)->pdgId()))<<std::endl;
       if ( ((*iMuon)->pt() < (maxMuon->pt())) && ( (passdR_ && deltaR(**iMuon, *maxMuon) < Cut_) 
           || (!passdR_ && deltaR(**iMuon, *maxMuon) > Cut_) || (Cut_==-1) ) && ((*iMuon)->pt() > Mu2PtCut_) && (maxMuon->pt() > Mu1PtCut_) )
       {
         if ( (oppositeSign_ && (*iMuon)->pdgId() == (-1)*((maxMuon)->pdgId()) ) || (!oppositeSign_ && (*iMuon)->pdgId()==(maxMuon)->pdgId() ) )
         {
           //cout<<"This one passed"<<std::endl;
           double deltaR=0.0;
           OppositeSignSmallDRMuon=(*iMuon);
           //cout<<"OppositeSignMuonPt="<<OppositeSignSmallDRMuon->pt()<<std::endl;
           muonColl->push_back(OppositeSignSmallDRMuon);
           deltaR=reco::deltaR(*maxMuon, *OppositeSignSmallDRMuon);
           histos1D_["deltaR"]->Fill(deltaR);
           histos1D_["pt"]->Fill((*iMuon)->pt());
         }//if sign requirement
       }//if pt and dR requirement
       else 
  	  continue;
     }//for iMuon
     if(OppositeSignSmallDRMuon.isNull())
     {
       LargerThan0=0; 
       return LargerThan0;
     }//if
     iEvent.put(muonColl);
   }//else
   return LargerThan0;
}
// ------------ method called once each job just before starting event loop  ------------
void 
HighestPtAndMuonSignDRSelector::beginJob()
{
  edm::Service<TFileService> fileService;
  histos1D_["deltaR"]=fileService->make<TH1D>("deltaR of trigger muon and nearest Mu1 or Mu2","deltaR of trigger muon and nearest Mu1 or Mu2", 10, 0.0, 5.0);
  histos1D_["pt"]=fileService->make<TH1D>("pt of fake Mu2", "pt of fake Mu2", 10, 0, 100.0);

}

// ------------ method called once each job just after ending the event loop  ------------
void 
HighestPtAndMuonSignDRSelector::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
HighestPtAndMuonSignDRSelector::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
HighestPtAndMuonSignDRSelector::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
HighestPtAndMuonSignDRSelector::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
HighestPtAndMuonSignDRSelector::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HighestPtAndMuonSignDRSelector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(HighestPtAndMuonSignDRSelector);
