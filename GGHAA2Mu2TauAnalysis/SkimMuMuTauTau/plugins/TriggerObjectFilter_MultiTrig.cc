// -*- C++ -*-
//
// Package:    trigger_match/TriggerObjectFilter_MultiTrig
// Class:      TriggerObjectFilter_MultiTrig
// 
/**\class TriggerObjectFilter_MultiTrig TriggerObjectFilter_MultiTrig.cc trigger_match/TriggerObjectFilter_MultiTrig/plugins/TriggerObjectFilter_MultiTrig.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Mengyao Shi
//         Created:  Wed, 18 Nov 2015 13:18:21 GMT
//
//


// system include files
#include <memory>
#include <cmath>
// user include files
#include "TH1D.h"
#include "TH2D.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TFrame.h"
#include "TGraph.h"
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
//#include "BoostedTauAnalysis/Common/interface/Common.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "HLTrigger/HLTanalyzers/interface/HLTInfo.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "HLTrigger/HLTcore/interface/HLTConfigData.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
using namespace std;
using namespace edm;
using namespace reco;
using namespace trigger;

//
// class declaration
//
template<class T>
class TriggerObjectFilter_MultiTrig : public edm::EDFilter {
   public:
      explicit TriggerObjectFilter_MultiTrig(const edm::ParameterSet&);
      ~TriggerObjectFilter_MultiTrig();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const& , edm::EventSetup const& )/* override*/;
      virtual void beginRun(const edm::Run& iRun, edm::EventSetup const& iSetup);
      virtual void beginJob();
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob();
      virtual void endRun(const edm::Run& iRun, edm::EventSetup const& iSetup);
//      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)/* override*/;
      // ----------member data ---------------------------
      edm::EDGetTokenT<edm::RefVector<std::vector<T> > > recoObjTag_;
      edm::EDGetTokenT<trigger::TriggerEvent>  triggerEventTag_;
      edm::EDGetTokenT<edm::TriggerResults> triggerResultsTag_;
      double Cut_;
      std::vector<edm::InputTag> hltTags_;
      HLTConfigProvider hltConfig_;
      std::vector<edm::InputTag> theRightHLTTags_;
      std::vector<edm::InputTag> theRightHLTSubFilters_;
      std::vector<edm::InputTag> HLTSubFilters_;
      unsigned int minNumObjsToPassFilter1_;
      std::map<std::string, TH1D*> histos1D_;
      std::map<std::string, TH2D*> histos2D_;
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
template<class T>
TriggerObjectFilter_MultiTrig<T>::TriggerObjectFilter_MultiTrig(const edm::ParameterSet& iConfig):
  recoObjTag_(consumes<edm::RefVector<std::vector<T> > >(iConfig.getParameter<edm::InputTag>("recoObjTag"))),
  triggerEventTag_(consumes<trigger::TriggerEvent>(iConfig.getUntrackedParameter<edm::InputTag>("triggerEventTag"))),
  // By default, trigger results are labeled "TriggerResults" with process name "HLT" in the event.
  triggerResultsTag_(consumes<edm::TriggerResults>(iConfig.getUntrackedParameter<edm::InputTag>("triggerResultsTag"))),
  Cut_(iConfig.getUntrackedParameter<double>("MatchCut")),
  hltTags_(iConfig.getParameter<std::vector<edm::InputTag> >("hltTags")),
  hltConfig_(),
  //hltConfig_ = iConfig.getParameter<HLTConfigProvider>("hltConfig");
  theRightHLTTags_(iConfig.getParameter<std::vector<edm::InputTag> >("theRightHLTTags")),
  theRightHLTSubFilters_(iConfig.getParameter<std::vector<edm::InputTag> >("theRightHLTSubFilters")),
  //Whether using HLT trigger path name or the actual trigger filter name. Trigger path is default.
  HLTSubFilters_(iConfig.getUntrackedParameter<std::vector<edm::InputTag> >("HLTSubFilters",std::vector<edm::InputTag>())),
  minNumObjsToPassFilter1_(iConfig.getParameter<unsigned int>("minNumObjsToPassFilter1")),
  histos1D_(),
  histos2D_()
{

  produces<edm::RefVector<std::vector<T> > >();
}

template<class T>
TriggerObjectFilter_MultiTrig<T>::~TriggerObjectFilter_MultiTrig()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}
//template<class T>
//void TriggerObjectFilter_MultiTrig<T>::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
//{
//  std::cout<< "beginLuminosityBlock"<< std::endl;
//  return true;
//}


//
// member functions
//
template<class T>
void TriggerObjectFilter_MultiTrig<T>::beginRun(const edm::Run& iRun, edm::EventSetup const& iSetup)
{
  bool changed_ = true;
  //std::cout << "beginRun"<< std::endl;
  
  if ( !hltConfig_.init(iRun,iSetup,hltTags_[0].process(),changed_) ){
    edm::LogError("TriggerObjectFilter_MultiTrig") <<
                     "Error! Can't initialize HLTConfigProvider";
                         throw cms::Exception("HLTConfigProvider::init() returned non 0");
  }
}

template<class T>
void
TriggerObjectFilter_MultiTrig<T>::beginJob()
{
  //std::cout<< "beginJob" << std::endl;
  edm::Service<TFileService> fileService;
  //histos1D_[ "TriggerObjectInvMass" ]=fileService->make<TH1D>("TriggerObjectInvMass","Invariant Mass of the P4 of the Trigger Objects",600,0,120);
  histos1D_["etaDistri_NoTriggerNoMatch"]=fileService->make<TH1D>("etaDistri_NoTriggerNoMatch","eta distribution of all reco muon without trigger fired or trigger-reco match H750a09",60,-3.,3.);
  //histos1D_[ "TriggerObjectInvMass_ifMatch" ]=fileService->make<TH1D>("TriggerObjectInvMass_ifMatch","Invariant Mass of the P4 of the Trigger Objects if Matched to RECO object",600,0,120);
  //histos1D_[ "TriggerObjectInvMass_zoomed" ]=fileService->make<TH1D>("TriggerObjectInvMass_zoomed","Invariant Mass of the P4 of the Trigger Objects", 100, 7, 12);
  histos1D_["etaDistri_NoTriggerYesMatch"]=fileService->make<TH1D>("etaDistri_NoTriggerYesMatch","eta distribution of reco muon with trigger-reco match, no HLT fired",60,-3.,3.);
  histos1D_["Efficiency_YesTriggerYesMatch"]=fileService->make<TH1D>("Efficiency_YesTriggerYesMatch","eta distribution of trigger+trigger matching efficiency",60,-3.,3.);

  histos1D_["Efficiency_YesTriggerNoMatch"]=fileService->make<TH1D>("Efficiency_YesTriggerNoMatch","eta distribution of highest pt muon trigger efficiency(with bot denominator and numerator trigger-reco match)",60,-3.,3.);

  histos1D_["EventSize"]=fileService->make<TH1D>("EventSize","#of particles per event pass",10,0,10);
  histos1D_["nMatches"]=fileService->make<TH1D>("nMatches","# of Matches",10,0,10);
  histos2D_["ptTrigCand1"] =fileService->make< TH2D >("ptTrigCand1","Object vs. candidate_higher_p_{T} (GeV)",150, 0., 150., 150, 0., 150.);
  histos2D_[ "ptTrigCand1" ]->SetXTitle( "candidate p_{T} (GeV)" );
  histos2D_[ "ptTrigCand1" ]->SetYTitle( "object p_{T} (GeV)" );
  histos2D_["TrigSizevsMu1Mu2Size"] =fileService->make< TH2D >("TrigSizevsMu1Mu2Size","Trigger Size vs. Mu1Mu2 Size", 5, -.5, 4.5, 5, -.5, 4.5);
  histos2D_[ "TrigSizevsMu1Mu2Size" ]->SetXTitle( "Trigger Object Size" );
  histos2D_[ "TrigSizevsMu1Mu2Size" ]->SetYTitle( "Mu1Mu2  ObjectSize" );  
  histos2D_["TrigSizePassvsMu1Mu2Size"] =fileService->make< TH2D >("TrigSizePassvsMu1Mu2Size","Passing Trigger Size vs. Mu1Mu2 Size", 5, -.5, 4.5, 5, -.5, 4.5);
  histos2D_[ "TrigSizePassvsMu1Mu2Size" ]->SetXTitle( "Trigger Object Size" );
  histos2D_[ "TrigSizePassvsMu1Mu2Size" ]->SetYTitle( "Mu1Mu2  ObjectSize" );  
  histos2D_["OtherTrigObjectSizePassvsMu1Mu2Size"] =fileService->make< TH2D >("OtherTrigObjectSizePassvsMu1Mu2Size","Other Trigger Object Size vs. Mu1Mu2 Size", 5, -.5, 4.5, 5, -.5, 4.5);
  histos2D_[ "OtherTrigObjectSizePassvsMu1Mu2Size" ]->SetXTitle( "Trigger Object Size" );
  histos2D_[ "OtherTrigObjectSizePassvsMu1Mu2Size" ]->SetYTitle( "Mu1Mu2  ObjectSize" );  
}

// ------------ method called on each new Event  ------------
template<class T>
bool
TriggerObjectFilter_MultiTrig<T>::filter( edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::cout << "##############################\n# Starting Trigger Stuff\n##############################" << std::endl;
  //create pointer to output collection
  std::auto_ptr<edm::RefVector<std::vector<T> > > recoObjColl(new edm::RefVector<std::vector<T> >);

  //get reco objects
  edm::Handle<edm::RefVector<std::vector<T> > > recoObjs;
  iEvent.getByToken(recoObjTag_, recoObjs);

  //Finding the Max pt
  double max=0.0;
  for (typename edm::RefVector<std::vector<T> >::const_iterator iRecoObj = recoObjs->begin(); iRecoObj != recoObjs->end(); ++iRecoObj)
  {
    histos1D_["etaDistri_NoTriggerNoMatch"]->Fill((*iRecoObj)->eta());   
    if( max < ((*iRecoObj)->pt()) )
      max=(*iRecoObj)->pt();
  }//for

  // Trigger Info
  edm::Handle<trigger::TriggerEvent> trgEvent;
  iEvent.getByToken(triggerEventTag_, trgEvent);

  edm::Handle<edm::TriggerResults> pTrgResults;
  iEvent.getByToken(triggerResultsTag_, pTrgResults);

  std::map<std::string, bool> triggerInMenu;
  std::vector<std::string> myHLTFilters;
  std::vector<unsigned int> myHLTFiltersIndex;
  // get names of active HLT paths in this event
  std::vector<std::string> activeHLTPathsInThisEvent = hltConfig_.triggerNames();
  // loop over active HLT paths to search for desired path
  for (std::vector<std::string>::const_iterator iHLT = activeHLTPathsInThisEvent.begin(); iHLT != activeHLTPathsInThisEvent.end(); ++iHLT) 
  { 
    //std::cout << "iHLT= " << *iHLT << std::endl;
    int hltTagsIndex = 0;
    for (std::vector<edm::InputTag>::const_iterator iMyHLT = hltTags_.begin(); iMyHLT != hltTags_.end(); ++iMyHLT) 
    {
      //std::cout << "\tiMyHLT= " << (*iMyHLT).label();
      if ((*iHLT).find( (*iMyHLT).label() ) != string::npos) 
      {
        std::cout << "\n\nFOUND THE HLT=" << *iHLT << endl;
        myHLTFilters.push_back( *iHLT);
        myHLTFiltersIndex.push_back(hltTagsIndex);
        //std::cout << "\tmyHLTFilter=" << myHLTFilters[hltTagsIndex] << std::endl;
	triggerInMenu[*iHLT] = true;
      }//if 
      hltTagsIndex++;
    }//for
  } // active paths loop

  // Uncomment below for loop to look at filters of the RightHLT triggers, but this is not needed for file to function properly
//  std::vector<std::string> filters;
//  for (std::vector<edm::InputTag>::const_iterator iMyHLT = theRightHLTTags_.begin(); iMyHLT != theRightHLTTags_.end(); ++iMyHLT)
//  {
//    std::cout << "iMyHLT=" << iMyHLT << std::endl;
//    for(unsigned int  i=0; i< hltConfig_.moduleLabels(iMyHLT.label()).size();i++)
//      std::cout<< "\t\thltConfig_.moduleLabels="<<(hltConfig_.moduleLabels( iMyHLT.label())[i]) << std::endl;
//  }//for iMyHLT 

  edm::InputTag filterTag;
  const trigger::TriggerObjectCollection& TOC( trgEvent->getObjects() );
  //choose the right sub-filter depending on the HLT path name
  std::vector<std::string> filters;
  for (std::vector<edm::InputTag>::const_iterator iMyHLT = theRightHLTTags_.begin(); iMyHLT != theRightHLTTags_.end(); ++iMyHLT)
  {
    try { filters = hltConfig_.moduleLabels( (*iMyHLT).label() ); }
    catch (std::exception ex) { cout << "FAILED TRIGGER=" << (*iMyHLT).label() << std::endl; }
  }//for
  std::cout << "\n\ntrgEvent->filterTag(i):" << std::endl;

  std::vector<int> subFilterIndecies;
  for (unsigned int index = 0; index < myHLTFilters.size(); ++index) // Loop over the triggers that are in event
  {
    std::cout << "myHLTFilters[" << index << "]= " << myHLTFilters[index] << "myHLTFiltersIndex[" << index << "]=" << myHLTFiltersIndex[index] << std::endl;
    int iteIndex = 9999; //Initial value to see if subFilter is found
    unsigned int dummyIndex = 0; // Use this to make sure to get the subfilter that corresponds to the HLT found based upon VInputTag order of cfg file
    for (std::vector<edm::InputTag>::const_iterator iMyHLTSubFilter = theRightHLTSubFilters_.begin(); iMyHLTSubFilter != theRightHLTSubFilters_.end(); ++iMyHLTSubFilter) 
    { // Iterate over the SubFilters provided
      if (dummyIndex == myHLTFiltersIndex[index]) // If correct subFilter with HLT that was found
        std::cout << "\tiMyHLTSubFilter= " << *iMyHLTSubFilter << std::endl;
      else // If not the correct index, then add to index and go to next subfilter
      {
        dummyIndex++;
        continue;
      }//else
      for(int i=0; i != trgEvent->sizeFilters(); ++i) //Loop over all subFilters
      {
        std::string label(trgEvent->filterTag(i).label());
        //std::cout << "\t\t" << trgEvent->filterTag(i).label() << std::endl;
        if (label.find((*iMyHLTSubFilter).label()) != std::string::npos ) // If SubFilter matches the subfilter that we want
        {
          iteIndex = i;
          break;
        }//if dummyIndex == index && label.find(iMyHLTSubFilter.label()) != std::string::npos
      }//for trgEvent
      dummyIndex++;
    }//for
    subFilterIndecies.push_back(iteIndex );
  }//for index < myHLTFilters

  std::vector<unsigned int> passingRecoObjRefKeys1;
  std::vector<unsigned int> passingRecoObjRefKeys1_NoHLT;
  for (unsigned int index = 0; index < subFilterIndecies.size(); ++index)
  { 
    if (subFilterIndecies[index] == 9999)
      subFilterIndecies[index] = 0;
    const trigger::Keys& KEYS1(trgEvent->filterKeys(subFilterIndecies[index]));
    const size_type nK1(KEYS1.size());
    const edm::TriggerNames &trgNames = iEvent.triggerNames(*pTrgResults);
    const unsigned int trgIndex = trgNames.triggerIndex(myHLTFilters[index]);
    bool firedHLT = (trgIndex < trgNames.size()) && (pTrgResults->accept(trgIndex));
    std::cout << "subFilterIndecies[" << index << "]= " << subFilterIndecies[index] << std::endl;
    std::cout << "myHLTFilters[" << index << "]= " << myHLTFilters[index] << std::endl;
    std::cout << "myHLTFiltersIndex[" << index << "]= " << myHLTFiltersIndex[index] << std::endl;
    std::cout << "firedHLT?=" << firedHLT << std::endl;
    std::cout << "trgIndex?=" << trgIndex << std::endl;
    std::cout << "trgNames.size()=" <<trgNames.size() << std::endl;
    std::cout << "if pTrgResults accept trgIndex?=" << (pTrgResults->accept(trgIndex)) << std::endl;
    std::cout << "If trgIndex< trgNames.size()?=" << (trgIndex < trgNames.size()) << std::endl;
    passingRecoObjRefKeys1.clear();
    passingRecoObjRefKeys1_NoHLT.clear();

    histos1D_["EventSize"]->Fill(passingRecoObjRefKeys1_NoHLT.size());
    histos2D_["TrigSizevsMu1Mu2Size"]->Fill(passingRecoObjRefKeys1_NoHLT.size(), recoObjs->size() );
  
    if (firedHLT)
    { // firedHLT
      int nMatches = 0;
      histos2D_["TrigSizePassvsMu1Mu2Size"]->Fill(passingRecoObjRefKeys1_NoHLT.size(), recoObjs->size() );
      histos2D_["OtherTrigObjectSizePassvsMu1Mu2Size"]->Fill(nK1, recoObjs->size() );
      //reco::LeafCandidate::PolarLorentzVector diMuP4, diMuP4_ifMatch, dummyTemp;
      for(int ipart1 = 0; ipart1 != nK1; ++ipart1) 
      {
        const trigger::TriggerObject& TO1 = TOC[KEYS1[ipart1]];
        //diMuP4 += math::PtEtaPhiMLorentzVector(TO1.pt(), TO1.eta(), TO1.phi(), TO1.mass());
        std::cout << "nK1=" << nK1 << "\tipart1=" << ipart1 <<std::endl;
        for (typename edm::RefVector<std::vector<T> >::const_iterator iRecoObj = recoObjs->begin(); iRecoObj != recoObjs->end(); ++iRecoObj) 
        {
          if ((deltaR(**iRecoObj, TO1) < Cut_) && (std::find(passingRecoObjRefKeys1.begin(), passingRecoObjRefKeys1.end(), iRecoObj->key()) == passingRecoObjRefKeys1.end()) ) 
          {
            nMatches++;
            //diMuP4_ifMatch += (*iRecoObj)->p4() ;
            recoObjColl->push_back(*iRecoObj);
            histos2D_[ "ptTrigCand1"]->Fill((*iRecoObj)->pt(), TO1.pt());
            passingRecoObjRefKeys1.push_back(iRecoObj->key());
          }//if
        }//for iRecoObj
      }//nK1
      //std::cout << "noMatch= " << diMuP4.M() << "\tMatch= " << diMuP4_ifMatch.M() << std::endl;
      //histos1D_["TriggerObjectInvMass"]->Fill(diMuP4.M() );
      //histos1D_["TriggerObjectInvMass_ifMatch"]->Fill(diMuP4_ifMatch.M() );
      //histos1D_["TriggerObjectInvMass_zoomed"]->Fill(diMuP4.M() );
      histos1D_["nMatches"]->Fill(nMatches);
      std::cout << "nMatches=" << nMatches << std::endl;
      if (passingRecoObjRefKeys1.size() >= minNumObjsToPassFilter1_)
      {
	std::cout << "Found enough objects=" << passingRecoObjRefKeys1.size() << std::endl;
        break;
      }//if
    }//firedH
  }//for index < subFilterIndecies.size()
  std::cout << "passingRecoObjRefKeys1.size()= " << passingRecoObjRefKeys1.size() << std::endl;
  iEvent.put(recoObjColl);
  return (passingRecoObjRefKeys1.size() >= minNumObjsToPassFilter1_);
}

// ------------ method called when starting to processes a run  ------------


// ------------ method called once each job just before starting event loop  ------------

// ------------ method called once each job just after ending the event loop  ------------
template<class T>
void 
TriggerObjectFilter_MultiTrig<T>::endJob() {
//   histos1D_["Efficiency_YesTriggerNoMatch"]->Divide(  histos1D_[ "etaDistri_YesTriggerYesMatch" ],  histos1D_[ "etaDistri_NoTriggerYesMatch" ]);
//   histos1D_["Efficiency_YesTriggerYesMatch"]->Divide(  histos1D_[ "etaDistri_YesTriggerYesMatch" ],  histos1D_[ "etaDistri_NoTriggerNoMatch" ]);
}


// ------------ method called when ending the processing of a run  ------------
template<class T>
void TriggerObjectFilter_MultiTrig<T>::endRun(const edm::Run& iRun, edm::EventSetup const& iSetup)
{
 // std::cout<< "endRun" << std::endl;
} 
// ------------ method called when starting to processes a luminosity block  ------------
 
// ------------ method called when ending the processing of a luminosity block  ------------
//template<class T>
//bool TriggerObjectFilter_MultiTrig<T>::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
//{
//  std::cout<< "endLuminosityBlock"<< std::endl;
//  return true;
//}
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
template<class T>
void
TriggerObjectFilter_MultiTrig<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
typedef TriggerObjectFilter_MultiTrig<reco::Muon> MuonTriggerObjectFilter_MultiTrig;
DEFINE_FWK_MODULE(MuonTriggerObjectFilter_MultiTrig);
