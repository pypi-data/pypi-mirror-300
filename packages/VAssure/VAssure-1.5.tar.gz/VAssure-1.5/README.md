Framework:
******* Sukumar Kutagulla *******

Framework Components: 
Framework contains below folders
1. CustomLibrary
2. Framework_Common_Resources
3. CommonResources
4. CustomKeywords
5. HubConfiguration
6. VaultUtilities
7. VeevaWorkFlowPreReqAPIs

Note: 
1. All folders/files are self explanatory and DO NOT add/update anything in these folders as this is going to be deprecated or moved to vault level in near future.
2. Once vault and Framework are properly setup, then create a branch aligning to script that you will be working
 Your vault and framework branches should be created with same convention (These branches will be deleted once your respective PR/PRs merged to target brach).
 e.g: Script : Safety_OQ_SAF_08
3. CustomKeywords folder contains python based custom keywords, we can utilize both robot and python based custom keywords for our scripts, preferably suggested to use python for faster executions.
4. HubConfiguration folder contains AWS ECS related information along with environment details.
5. VaultUtilities are the common block of keywords/code that can be used as a single keyword which inturn contains some common sub keywords.
6. VeevaWorkFlowPreReqAPIs folder contains API job configurations which are required to create a prerequisite document with specific lifecycle states and to check the status of the create API.
    e.g: How to use API for your pre-requisite creation, please follow the below URL to go through the steps mentioned in document.
    documentpath: "https://spotline.sharepoint.com/:w:/s/SQAAutomation-Product/EeTkazsXtmxLk-huw3YEx-kBI9exsFV1cH1ikqgLdaGqUA?e=F5ykq5"

