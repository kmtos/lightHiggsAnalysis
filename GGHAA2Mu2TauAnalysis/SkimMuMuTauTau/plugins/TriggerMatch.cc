#include <memory>
#include <cmath>
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

template<class T>
class TriggerMatch : public edm::EDFilter {
   public:
      explicit TriggerMatch(const edm::ParameterSet&);
      ~TriggerMatch();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginRun(const edm::Run& iRun, edm::EventSetup const& iSetup);
      virtual void beginJob();
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual float delR(float, float, float, float);
      virtual void endJob();
      virtual void endRun(const edm::Run& iRun, edm::EventSetup const& iSetup);

      edm::EDGetTokenT<edm::RefVector<std::vector<T> > > recoObjTag_;
      edm::EDGetTokenT<trigger::TriggerEvent>  triggerEventTag_;
      std::vector<string> triggerFilter;
      double Cut_;
      std::map<std::string, TH1D*> histos1D_;
      std::map<std::string, TH2D*> histos2D_;
      HLTConfigProvider hltConfig_;
      std::vector<edm::InputTag> hltTags_;
};

template<class T>
TriggerMatch<T>::TriggerMatch(const edm::ParameterSet& iConfig):
  recoObjTag_(consumes<edm::RefVector<std::vector<T> > >(iConfig.getParameter<edm::InputTag>("recoObjTag"))),
  triggerEventTag_(consumes<trigger::TriggerEvent>(iConfig.getUntrackedParameter<edm::InputTag>("triggerEventTag"))),
  triggerFilter(iConfig.getParameter<std::vector<string>>("triggerFilter")),
  Cut_(iConfig.getUntrackedParameter<double>("MatchCut")),
  histos1D_(),
  histos2D_(),
  hltConfig_(),
  hltTags_(iConfig.getParameter<std::vector<edm::InputTag> >("hltTags"))
{

  produces<edm::RefVector<std::vector<T> > >();
}

template<class T>
TriggerMatch<T>::~TriggerMatch()
{
}

template<class T>
void TriggerMatch<T>::beginRun(const edm::Run& iRun, edm::EventSetup const& iSetup)
{
  bool changed_ = true;

  if ( !hltConfig_.init(iRun,iSetup,hltTags_[0].process(),changed_) ){
    edm::LogError("TriggerMatch") <<
                     "Error! Can't initialize HLTConfigProvider";
                         throw cms::Exception("HLTConfigProvider::init() returned non 0");
  }
}
template<class T>
void
TriggerMatch<T>::beginJob()
{
}

template<class T>
void 
TriggerMatch<T>::endJob() {
}

template<class T>
void TriggerMatch<T>::endRun(const edm::Run& iRun, edm::EventSetup const& iSetup)
{
 // std::cout<< "endRun" << std::endl;
}

template<class T>
void
TriggerMatch<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
 
template<class T>
float
TriggerMatch<T>::delR(float eta1,float phi1,float eta2,float phi2){
  float mpi=3.14;
  float dp=std::abs(phi1-phi2);
  if (dp>mpi) dp-=float(2*mpi);
  return sqrt((eta1-eta2)*(eta1-eta2) + dp*dp);
}

template<class T>
bool
TriggerMatch<T>::filter(edm::Event& iEvent,const edm::EventSetup& iSetup){
  std::auto_ptr<edm::RefVector<std::vector<T> > > recoObjColl(new edm::RefVector<std::vector<T> >);
  std::vector<reco::Particle>  HLTMuMatched;
  std::vector<string> HLTMuMatchedNames;
  edm::Handle<trigger::TriggerEvent> handleTriggerEvent;
  iEvent.getByToken(triggerEventTag_, handleTriggerEvent );

  edm::Handle<edm::RefVector<std::vector<T> > > recoObjs;
  iEvent.getByToken(recoObjTag_, recoObjs);
  const trigger::TriggerObjectCollection & toc(handleTriggerEvent->getObjects());
  size_t nMuHLT =0;
  size_t nbHLTmuons =0;
  for ( size_t ia = 0; ia < handleTriggerEvent->sizeFilters(); ++ ia) {
    const trigger::Keys & k = handleTriggerEvent->filterKeys(ia);
    for (trigger::Keys::const_iterator ki = k.begin(); ki !=k.end(); ++ki ) {
      std::string fullname = handleTriggerEvent->filterTag(ia).encode();
      std::string name;
      size_t p = fullname.find_first_of(':');
      if (p != std::string::npos) {
	name = fullname.substr(0, p);
      } else {
	name = fullname;
      }
     
      for (unsigned int l=0;l<triggerFilter.size();l++){
	if (name == triggerFilter.at(l).c_str()) {
	  nbHLTmuons++;
	  HLTMuMatched.push_back(toc[*ki].particle());
          HLTMuMatchedNames.push_back(name);
	}
      }

    }
  }
  for (typename edm::RefVector<std::vector<T> >::const_iterator muonIt = recoObjs->begin(); muonIt!=recoObjs->end(); ++muonIt){
    reco::Muon mu = **muonIt;
    if (mu.innerTrack().isNull()) continue;
    if (mu.globalTrack().isNull()) continue;
    size_t dim =  HLTMuMatched.size();
    size_t nPass=0;
    bool matched=false;
    if (dim>0){
      for (size_t k =0; k< dim; k++ ) {
        if (delR(HLTMuMatched[k].eta(),HLTMuMatched[k].phi(),mu.eta(),mu.phi())  < Cut_)   {
          nPass++ ;
          recoObjColl->push_back(*muonIt);
        }
      }
      if(nPass>0) matched=true;
    }
    if (matched){
        nMuHLT++;
      
    }
  }
return nMuHLT>0;
}

typedef TriggerMatch<reco::Muon> MuonTriggerMatch;
DEFINE_FWK_MODULE(MuonTriggerMatch);
