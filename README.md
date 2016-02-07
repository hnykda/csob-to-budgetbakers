# Import ČSOB transactions to BudgetBakers app (Wallet)

This script written in `Python 3` is for converting ČSOB `txt` exported file (available in the InternetBanking 24 of ČSOB) to the import `csv` format required by BudgetBakers web app. 

The script has only one dependency and that is `pandas`. I understand it is a quite heavy dependency, but I use it for all the other projects and hence it is not problem for me and I am lazy rewriting the script without that (you are very welcome to do it yourself). 

The script should be self-explanatory by looking at the argument parser parameters. Here is an example of running it:
```
python csob_to_budgetbakers.py -i ~/load/HIST_220448288_201602071524.txt -o out.csv -p DEBIT_CARD -a CSOB -c Ostatní -n 3
```
