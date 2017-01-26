# CombineStatisticsBackground 
this package can summarize the selection table on background, I wrote these scripts because your interested selection tables
can show up in different files, and you want to add numbers up to give you a summary table.


git clone https://github.com/MengyaoShi/CombineStatisticsBackground.git

you then need to change line 1 and line 4 in unzipEos.h according to what background you want to get a summary;

./unzipEos.h

you will see .log files in your folder

change line 26 of Combine.h, it has file numbers the same as line 1 of unzipEos.h

./Combine.h

If during SKim process, you add a tuple or remove or change selection sequence, then you need to change line 15-25, 29-39, 42-54, 58-68 accordingly.

It's very light and simple to use! 



