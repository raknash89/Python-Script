# home_loan_calculator_steps.py
import sys, os
from py3270 import Emulator
from behave import *

@given("home loan amount is {amount}, interest rate is {rate} and maturity date is {maturity_date} months")
def step_impl(context, amount, rate, maturity_date):
    context.home_loan_amount = amount
    context.interest_rate = rate
    context.maturity_date_in_months = maturity_date

@when("the transaction is submitted to the home loan calculator")
def step_impl(context):
    # Setup connection parameters
    tn3270_host = os.getenv('TN3270_HOST')
    tn3270_port = os.getenv('TN3270_PORT')
	# Setup TN3270 connection
    em = Emulator(visible=False, timeout=120)
    em.connect(tn3270_host + ':' + tn3270_port)
    em.wait_for_field()
	# Screen login
    em.fill_field(10, 44, 'b0001', 5)
    em.send_enter()
	# Input screen fields for home loan calculator
    em.wait_for_field()
    em.fill_field(8, 46, context.home_loan_amount, 7)
    em.fill_field(10, 46, context.interest_rate, 7)
    em.fill_field(12, 46, context.maturity_date_in_months, 7)
    em.send_enter()
    em.wait_for_field()    

    # collect monthly replayment output from screen
    context.monthly_repayment = em.string_get(14, 46, 9)
    em.terminate()

@then("it shall show the monthly repayment of {amount}")
def step_impl(context, amount):
    print("expected amount is " + amount.strip() + ", and the result from screen is " + context.monthly_repayment.strip())
assert amount.strip() == context.monthly_repayment.strip()
# Python
# To run this functional test in Micro Focus Enterprise Test Server (ETS), we use AWS CodeBuild.

# We first need to build an Enterprise Test Server Docker image and push it to an Amazon Elastic Container Registry (Amazon ECR) registry. For instructions, see Using Enterprise Test Server with Docker.

# Next, we create a CodeBuild project and uses the Enterprise Test Server Docker image in its configuration.

# The following is an example AWS CloudFormation code snippet of a CodeBuild project that uses Windows Container and Enterprise Test Server:

#   BddTestBankDemoStage:
#     Type: AWS::CodeBuild::Project
#     Properties:
#       Name: !Sub '${AWS::StackName}BddTestBankDemo'
#       LogsConfig:
#         CloudWatchLogs:
#           Status: ENABLED
#       Artifacts:
#         Type: CODEPIPELINE
#         EncryptionDisabled: true
#       Environment:
#         ComputeType: BUILD_GENERAL1_LARGE
#         Image: !Sub "${EnterpriseTestServerDockerImage}:latest"
#         ImagePullCredentialsType: SERVICE_ROLE
#         Type: WINDOWS_SERVER_2019_CONTAINER
#       ServiceRole: !Ref CodeBuildRole
#       Source:
#         Type: CODEPIPELINE
#         BuildSpec: bdd-test-bankdemo-buildspec.yaml
# YAML
# In the CodeBuild project, we need to create a buildspec to orchestrate the commands for preparing the Micro Focus Enterprise Test Server CICS environment and issue the test command. In the buildspec, we define the location for CodeBuild to look for test reports and upload them into the CodeBuild report group. The following buildspec code uses custom scripts DeployES.ps1 and StartAndWait.ps1 to start your CICS region, and runs Python Behave BDD tests:

# version: 0.2
# phases:
#   build:
#     commands:
#       - |
#         # Run Command to start Enterprise Test Server
#         CD C:\
#         .\DeployES.ps1
#         .\StartAndWait.ps1

#         py -m pip install behave

#         Write-Host "waiting for server to be ready ..."
#         do {
#           Write-Host "..."
#           sleep 3  
#         } until(Test-NetConnection 127.0.0.1 -Port 9270 | ? { $_.TcpTestSucceeded } )

#         CD C:\tests\features
#         MD C:\tests\reports
#         $Env:Path += ";c:\wc3270"

#         $address=(Get-NetIPAddress -AddressFamily Ipv4 | where { $_.IPAddress -Match "172\.*" })
#         $Env:TN3270_HOST = $address.IPAddress
#         $Env:TN3270_PORT = "9270"
        
#         behave.exe --color --junit --junit-directory C:\tests\reports
# reports:
#   bankdemo-bdd-test-report:
#     files: 
#       - '**/*'
#     base-directory: "C:\\tests\\reports"