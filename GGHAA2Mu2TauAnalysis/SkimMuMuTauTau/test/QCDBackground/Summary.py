#this function gives you a total estimation of QCD background in region A using ABCD method
def summary():
    lines1=[line.rstrip('\n') for line in open('QCD_summary.txt','r')]
    sum_ABCD=0
    sum_MC=0
    TotalEvents=[3884666.0,3854868.0,3630204.0,7274788.0,7428066.0,1469465.0, 13870432.0,20383957.0, 23993981.0,31565787.0,4454108.0]
    for i in range(len(lines1)):
        #if it is line 0,3,6,9,...before len(lines1)-1
        if i%3==0:
            file=open(lines1[i].rstrip('\n')+'.txt','r')
            lines2=[line.rstrip('\n') for line in file]
            A=float((lines2[1])[9:])
            B=float((lines2[2])[9:])
            C=float((lines2[3])[9:])
            D=float((lines2[4])[9:])
            if i+3<len(lines1):
                XS=float(lines1[i+1])
                eff=float(lines1[i+2])
                if D!=0:
                    ABCD_A=B/D*C/TotalEvents[i//3]*40000
                    MC_A=A/TotalEvents[i//3]*40000
                    ABCD_contribution=XS*eff*ABCD_A
                    MC_contribution=XS*eff*MC_A
                    sum_ABCD=sum_ABCD+ABCD_contribution
                    sum_MC=sum_MC+MC_contribution
                    print(lines1[i])
		    print('{}{}'.format("contribution using ABCD method=",ABCD_contribution))
                    print('{}{}'.format("contribution using A region MC=", MC_contribution))
                    print('{}{}'.format("A=",A))
                    print('{}{}'.format("B=",B))
                    print('{}{}'.format("C=",C))
                    print('{}{}'.format("D=",D))
		    print('{}{}'.format("XS=",XS))
                    print('{}{}'.format("eff=",eff))
                    print('{}{}'.format("totalEvents=",TotalEvents[i//3]))
                i=i+3
    return sum_MC
            

print("Here is how many events in A region estimated by ABCD mehtod")
print(summary()) 
