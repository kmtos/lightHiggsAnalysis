import os
import sys
import math

import ROOT

import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle

tdrstyle.setTDRStyle()
ROOT.gStyle.SetPalette(1)


# arguments
savename = 'zmass'
lumi = 35900
xaxis = 'M_{ll} [GeV]'
yaxis = 'Events / 0.5 GeV'
logy = False
logx = False
ymin = None
ymax = None
numcol = 1
legendpos = 33
lumipos = 11
isprelim = True
ratiomin = 0.6
ratiomax = 1.4
rangex = [0,200]

# read from root file
tfile = ROOT.TFile.Open('DoubleMuonMC.root')
tfile1 = ROOT.TFile.Open('DoubleMuonDataEraC.root')
out=ROOT.TFile.Open("HistogramTitle.root", "RECREATE")

data = tfile1.Get('Mu1Mu2Analyzer/pt of Mu2')
mc = tfile.Get('Mu1Mu2Analyzer/pt of Mu2')
mc.Scale(1.0/(1.92*1e12)*1921.8*3*2573.4)

data.SetTitle('Observed')
mc.SetTitle('Drell--Yan')
mc.SetFillColor(ROOT.kOrange-2)
mc.SetLineColor(ROOT.kOrange+7)

stack = ROOT.THStack('stack','stack')
stack.Add(mc)

# create canvas
canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

plotpad = ROOT.TPad("plotpad", "top pad", 0.0, 0.21, 1.0, 1.0)
plotpad.SetBottomMargin(0.04)
plotpad.SetRightMargin(0.03)
out.cd()
plotpad.Draw()
plotpad.SetLogy(logy)
plotpad.SetLogx(logx)
ratiopad = ROOT.TPad("ratiopad", "bottom pad", 0.0, 0.0, 1.0, 0.21)
ratiopad.SetTopMargin(0.06)
ratiopad.SetRightMargin(0.03)
ratiopad.SetBottomMargin(0.5)
ratiopad.SetLeftMargin(0.16)
ratiopad.SetTickx(1)
ratiopad.SetTicky(1)
ratiopad.Draw()
ratiopad.SetLogx(logx)
plotpad.cd()

# now draw them
stack.Draw("hist")
stack.GetXaxis().SetTitle(xaxis)
stack.GetYaxis().SetTitle(yaxis)
stack.GetYaxis().SetLabelSize(0.05)
if ymax!=None: stack.SetMaximum(ymax)
if ymin!=None: stack.SetMinimum(ymin)
if rangex: stack.GetXaxis().SetRangeUser(*rangex)

# staterr for stack
stack.GetHistogram().GetXaxis().SetLabelOffset(999)
staterr = stack.GetStack().Last().Clone("{0}_staterr".format(stack.GetName))
staterr.SetFillColor(ROOT.kGray+3)
staterr.SetLineColor(ROOT.kGray+3)
staterr.SetLineWidth(0)
staterr.SetMarkerSize(0)
staterr.SetFillStyle(3013)
staterr.Draw('e2 same')
data.Draw('ex0 same')

# get the legend
entries = []
for hist in reversed(stack.GetHists()):
    entries += [[hist,hist.GetTitle(),'f']]
entries += [[data,data.GetTitle(),'ep']]
#legend = getLegend(*entries,numcol=numcol,position=legendpos)
legend = ROOT.TLegend(0.7,0.5,0.95,0.7,'','NDC')
if numcol>1: legend.SetNColumns(int(numcol))
legend.SetTextFont(42)
legend.SetBorderSize(0)
legend.SetFillColor(0)
for entry in entries:
    legend.AddEntry(*entry)
legend.Draw()

# cms lumi styling
period_int = 4
if plotpad != ROOT.TVirtualPad.Pad(): plotpad.cd()
CMS_lumi.writeExtraText = isprelim
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (float(lumi)/1000.)
if lumi < 1000:
    CMS_lumi.lumi_13TeV = "%0.1f pb^{-1}" % (float(lumi))
CMS_lumi.CMS_lumi(plotpad,period_int,lumipos)


# the ratio portion for stack
denom = stack.GetStack().Last().Clone('denom')
ratiostaterr = denom.Clone("{0}_ratiostaterr".format(denom.GetName))
ratiostaterr.SetStats(0)
ratiostaterr.SetTitle("")
ratiostaterr.GetYaxis().SetTitle("Obs / Exp")
ratiostaterr.SetMaximum(ratiomax)
ratiostaterr.SetMinimum(ratiomin)
ratiostaterr.SetMarkerSize(0)
ratiostaterr.SetFillColor(ROOT.kGray+3)
ratiostaterr.SetFillStyle(3013)
ratiostaterr.GetXaxis().SetLabelSize(0.19)
ratiostaterr.GetXaxis().SetTitleSize(0.21)
ratiostaterr.GetXaxis().SetTitleOffset(1.0)
ratiostaterr.GetXaxis().SetLabelOffset(0.03)
ratiostaterr.GetYaxis().SetLabelSize(0.19)
ratiostaterr.GetYaxis().SetLabelOffset(0.006)
ratiostaterr.GetYaxis().SetTitleSize(0.21)
ratiostaterr.GetYaxis().SetTitleOffset(0.35)
ratiostaterr.GetYaxis().SetNdivisions(503)
# bin by bin errors
for i in range(denom.GetNbinsX()+2):
    ratiostaterr.SetBinContent(i, 1.0)
    if denom.GetBinContent(i)>1e-6:  # not empty
        binerror = denom.GetBinError(i) / denom.GetBinContent(i)
        ratiostaterr.SetBinError(i, binerror)
    else:
        ratiostaterr.SetBinError(i, 999.)
ratiostaterr.SetXTitle(xaxis)

unityargs = [rangex[0],1,rangex[1],1] if rangex else [denom.GetXaxis().GetXmin(),1,denom.GetXaxis().GetXmax(),1]
ratiounity = ROOT.TLine(*unityargs)
ratiounity.SetLineStyle(2)

# ratio for data
dataratio = data.Clone('ratio_{0}'.format(data.GetName()))
for b in range(data.GetNbinsX()):
    nVal = data.GetBinContent(b+1)
    nErr = data.GetBinError(b+1)
    dVal = denom.GetBinContent(b+1)
    if dVal>1e-6:
        val = nVal/dVal
        err = nErr/dVal
    else:
        val = 0
        err = 0
    dataratio.SetBinContent(b+1,val)
    dataratio.SetBinError(b+1,err)

# and draw ratio
if ratiopad != ROOT.TVirtualPad.Pad(): ratiopad.cd()
ratiostaterr.Draw("e2")
if rangex: ratiostaterr.GetXaxis().SetRangeUser(*rangex)
ratiounity.Draw('same')
dataratio.Draw('0P same')

canvas.Draw()
text = raw_input()
out.Close()
