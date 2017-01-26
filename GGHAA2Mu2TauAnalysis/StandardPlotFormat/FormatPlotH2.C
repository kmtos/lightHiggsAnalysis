void FormatPlotH2( const string& inputPlotTitle, const string& inputPlotX, const string& inputPlotY, const string& inputLegendTitle)
{
  //initial
  gROOT->Reset();

  //open output file
  TFile out("HistogramTitle.root", "RECREATE");
  out.cd();

  //create canvas
  TCanvas canvas("canvas", "", 600, 600);

  //open input files
  TFile in1("QCD_1000ToInf_noSelection.root");
  TFile in2("QCD_800To1000_noSelection.root");
  TFile in3("QCD_600To800_noSelection.root");
  TFile in4("QCD_300To470_noSelection.root");
  TFile in5("QCD_170To300_noSelection.root");
  TFile in6("QCD_120To170_noSelection.root");
  TFile in7("QCD_80To120_noSelection.root");
  TFile in8("QCD_50To80_noSelection.root");
  TFile in9("QCD_30To50_noSelection.root");
  TFile in10("QCD_20To30_noSelection.root");
  TFile in11("QCD_15To20_noSelection.root");
  //extract histograms
  in1.cd();
  TCanvas *c1=(TCanvas*)in1.Get("iso2DCanvas");
  hist1=(TH2F*)c1->GetPrimitive("Iso2D");
  in2.cd();
  TCanvas *c2=(TCanvas*)in2.Get("iso2DCanvas");
  hist2=(TH2F*)c2->GetPrimitive("Iso2D");
  in3.cd();
  TCanvas *c3=(TCanvas*)in3.Get("iso2DCanvas");
  hist3=(TH2F*)c3->GetPrimitive("Iso2D");
  in4.cd();
  TCanvas *c4=(TCanvas*)in4.Get("iso2DCanvas");
  hist4=(TH2F*)c4->GetPrimitive("Iso2D");
  in5.cd();
  TCanvas *c5=(TCanvas*)in5.Get("iso2DCanvas");
  hist5=(TH2F*)c5->GetPrimitive("Iso2D");
  in6.cd();
  TCanvas *c6=(TCanvas*)in6.Get("iso2DCanvas");
  hist6=(TH2F*)c6->GetPrimitive("Iso2D");
  in7.cd();
  TCanvas *c7=(TCanvas*)in7.Get("iso2DCanvas");
  hist7=(TH2F*)c7->GetPrimitive("Iso2D");
  in8.cd();
  TCanvas *c8=(TCanvas*)in8.Get("iso2DCanvas");
  hist8=(TH2F*)c8->GetPrimitive("Iso2D");
  in9.cd();
  TCanvas *c9=(TCanvas*)in9.Get("iso2DCanvas");
  hist9=(TH2F*)c9->GetPrimitive("Iso2D");
  in10.cd();
  TCanvas *c10=(TCanvas*)in10.Get("iso2DCanvas");
  hist10=(TH2F*)c10->GetPrimitive("Iso2D");
  in11.cd();
  TCanvas *c11=(TCanvas*)in11.Get("iso2DCanvas");
  hist11=(TH2F*)c11->GetPrimitive("Iso2D");
  //set histogram plotting options
  hist1->Scale(10.435*0.15544*40000.0/3884666.0);
  hist2->Scale(32.3486*0.14552*40000.0/3854868.0);
  hist3->Scale(187.109*0.13412*40000.0/ 3630204.0);
  hist4->Scale(7820.25*0.10196*40000.0/ 7274788.0);
  hist5->Scale(117989*0.07335*40000.0/ 7428066.0);
  hist6->Scale(469797*0.05362*40000.0/1469465.0);
  hist7->Scale(2758420*0.03844*40000.0/13870432.0);
  hist8->Scale(19222500*0.02276*40000.0/20383957.0);
  hist9->Scale(139803000*0.01182*40000.0/23993981.0);
  hist10->Scale(558528000*0.0053*40000.0/31565787.0);
  hist11->Scale(1273190000*0.003*40000.0/4454108.0);
  hist1->SetFillColor(kRed);
  hist2->SetFillColor(kRed-4);
  hist3->SetFillColor(kRed-1);
  hist4->SetFillColor(kRed-9);
  hist5->SetFillColor(kRed-10);
  hist6->SetFillColor(kGreen);
  hist7->SetFillColor(kBlue);
  hist8->SetFillColor(kMagenta-7);
  hist9->SetFillColor(kMagenta-9);
  hist10->SetFillColor(kMagenta-10);
  hist11->SetFillColor(kMagenta+1);
  THStack *hs=new THStack("hs","QCD");
  TH2F *total=new TH2F("total","QCD",50,0,5.0,50,0,500.0);
  total->Add(hist1);
  total->Add(hist2);
  total->Add(hist3);
  total->Add(hist4);
  total->Add(hist5);
  total->Add(hist6);
  total->Add(hist7);
  total->Add(hist8);
  total->Add(hist9);
  total->Add(hist10);
  total->Add(hist11);

  hs->Add(hist1);
  hs->Add(hist2);
  hs->Add(hist3);
  hs->Add(hist4);
  hs->Add(hist5);
  hs->Add(hist6);
  hs->Add(hist7);
  hs->Add(hist8);
  hs->Add(hist9);
  hs->Add(hist10);
  hs->Add(hist11);
  
  //add legend
  leg = new TLegend(0.7,0.5,0.9,0.3);
  leg->SetHeader(inputLegendTitle.c_str()); // option "C" allows to center the header
  leg->AddEntry(total,"All");
  //plot histograms on same canvas
  out.cd();
  canvas.cd();
  total->Draw("colz");
  total->GetXaxis()->SetTitle(inputPlotX.c_str());
  total->GetYaxis()->SetTitle(inputPlotY.c_str());
  total->SetTitle(inputPlotTitle.c_str());
  leg->Draw();
  //write canvas to file
  canvas.Write();

  //close files
  out.Close();
  in1.Close();
  in2.Close();
}

