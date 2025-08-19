## Function
Create a python function which will 

1. parse the dynamicSubledger.csv file and every row in the file create a dynamic query on the sourceTable with the filter condition  
2. select the valuationDt, account, eagleLedgerAcct and column name in the dataDefinition field. 
3. The dataDefinition could be a forumale so extract the fields from the formulae and query the source table. 

For e.g., for the dataNAV collection the field name subscriptionBalance will be in a formulae ```[subscriptionBalance] *-1```

4. Parse the column subscriptionBalance and then apply the formulae. 
5. Group by valuationDt, account and assign the value of the total in ledgerAccount in the ledgerDefinition



## Data Definition
The source table can be dataNAV which has the below fields - valuationDt, shareClass, account, userBank, accountBaseCurrency, accountName, acctBasis, capstock, chartOfAccounts, distribution, eagleAcctBasis, eagleClass, eagleEntityId, eagleRegion, entityBaseCurrency, incomeDistribution, isComposite, isMulticlass, isPrimaryBasis, isSleeve, ltcglDistribution, mergerPic, parentAccount, settleCapstock, settleDistribution, shareClassCurrency, NAV, capstockRedsPay,capstockSubsRec, dailyDistribution, dailyYeild, distributionPayable, netAssets, redemptionBalance, redemptionPayBase, redemptionPayLocal, reinvestmentDistribution, settledShares, sharesOutstanding, subscriptionBalance, subscriptionRecBase, subscriptionRecLocal