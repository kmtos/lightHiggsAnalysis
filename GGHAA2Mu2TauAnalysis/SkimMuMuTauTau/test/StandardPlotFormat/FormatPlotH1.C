void FormatPlotH1(const string& RootFileName, const string& CanvasName, const string& HistogramName, const string& inputPlotTitle, const string& inputPlotX, const string& inputPlotY, const string& inputLegendTitle)
{
  //initial
  gROOT->Reset();

  //open output file
  TFile out("HistogramTitle.root", "RECREATE");
  out.cd();

  //create canvas
  TCanvas canvas("canvas", "", 600, 600);

  //open input files
  TFile in1(RootFileName.c_str());
  //extract histograms
  in1.cd();
  TCanvas *c1=(TCanvas*)in1.Get(CanvasName.c_str());
  TH1F* hist1 = NULL;
  //hist1=(TH1F*)c1->GetPrimitive("dimuIso");
  hist1=(TH1F*)c1->GetPrimitive(HistogramName.c_str());
  //set histogram plotting options
  hist1->GetXaxis()->SetTitle(inputPlotX.c_str());
  hist1->GetYaxis()->SetTitle(inputPlotY.c_str());
  hist1->SetTitle(inputPlotTitle.c_str());


  //add legend
  leg = new TLegend(0.7,0.5,0.9,0.3);
  leg->SetHeader(inputLegendTitle.c_str()); // option "C" allows to center the header
  leg->AddEntry(hist1,inputLegendTitle.c_str());
  //plot histograms on same canvas
  out.cd();
  canvas.cd();
  hist1->Draw("same");
  gStyle->SetOptStat("ouRMe");
  TPaveStats *st = (TPaveStats*)hist1->FindObject("stats");
  st->SetX1NDC(0.7);
  st->SetX2NDC(0.9);
  st->SetY1NDC(0.3);
  st->SetY2NDC(0.2);
  leg->Draw();
  //write canvas to file
  canvas.Write();

  //close files
  out.Close();
  in1.Close();
}
