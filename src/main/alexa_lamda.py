import json
from random import randint
import base64
import json
import os
import urllib
from urllib import request, parse
import boto3
dynamodb = boto3.client('dynamodb')



def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
#    elif event['request']['type'] == "SessionEndedRequest":
#        return on_end()
        

def on_start():
    print("Session started")

def on_launch(event):
    onlunch_MSG = "Hello, Welcome to Siemens H R, I can help you understand the following policies. a) National pension scheme"
    card_TEXT ="HI"
    card_TITLE = "Hello"
    reprompt_MSG = "Please ask me if you have any queries regarding N P S"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    
def intent_scheme(event):
    onlunch_MSG = get_message(event)
    card_TEXT ="HI"
    card_TITLE = "Hello"
    reprompt_MSG = "Does that answer your question?"
    endSession = False
    if event['request']['intent']['name'] == "GoodBye":
        endSession = True
    elif event['request']['intent']['name'] == "NOAnswer":
        endSession = True
    elif event['request']['intent']['name'] == "YES":
        endSession = True
    elif event['request']['intent']['name'] == "ThanksIntent":
        endSession = True        
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, endSession)
    

# Answers
def get_message(event):
    intent_name = event['request']['intent']['name']
    intent_resp = default_unknown_resp[rand_gen(5)]
    if intent_name == "NPSDescription":
        intent_resp = "N P S is a Government sponsored voluntary Pension Scheme for the citizens to bring an attractive long term savings avenue to effectively plan for retirement through safe and reasonable market–based returns. It is highly efficient, technology driven and enables saving small amounts to build a fund for life’s second innings. Siemens provides employees benefit of financial planning through the N P S Corporate Model."
    elif intent_name == "NPSEligible":
        intent_resp = "Any employee between the age 18 and 65 years can join the N P S scheme. However it is advisable that you should not join after your 50 years of age as the corpus might not be sufficient to get adequate returns."
    elif intent_name == "NPSContribution":
        intent_resp = "You can  contribute directly to N P S (by logging onto www.CRA.nsdl) or route your contributions through Siemens (routing can be done for Tier 1 account only)  the minumum contribution is rupees 1000 in a Financial Year. \
Forrouting your contributions through SIemens,  the maximum contributon is 10% of annual Basic and Dearness Allowance. This contribution is eligible for tax benefit under section 80 CCD(2)."
    elif intent_name == "ThanksIntent":
        intent_resp = thank_resp[rand_gen(5)]
    elif intent_name == "NOAnswer":
        intent_resp = "Ok, Please let me know if you have any further questions"
    elif intent_name == "GoodBye":
        intent_resp = "Ok, thank you, farewell"
    elif intent_name == "Identity":
        intent_resp = "I am a Siemens human resources assitant bot, you can ask me about the HR Policies"
    elif intent_name == "ACCTYPES":
        intent_resp = "There are two types of accounts you can open with N P S, Tier 1 and Tier 2.  Tier 1 account has tax benefits and withdrawal restrictions, where as Tier 2 account is for investment only and does not have any tax benefits."
    elif intent_name == "ENROLL":
        intent_resp = "For enrolling to the scheme under the Corporate Sector Model, the employee fills up an online application form(Subscriber Registration Form-V2) . You can down load this form from NEXUS/Facto HR. Or write into ASK HR. Once the individual subscription form is filled by the employee, the form needs to be submitted to respective Location HR. \
This form will be forwarded to the P O P for Individual Permanent retirement account number (P R A N) generation. You will receive a direct communication from NSDL once the P R A N is generated. You are now enrolled into the Scheme.\
For further details contact Location HR."
    elif intent_name == "POP":
        intent_resp = "Point of Presence is an entity through which all the services related to N P S are provided to the contributors. Point of Presence Service Provider for Siemens Limited, Is ICICI Bank, for SFSPL and STSPL it is HDFC securities."
    elif intent_name == "FUNDMANAGER":
        intent_resp = "ICICI Prudential Pension Fund Management is the professional fund manager who will be managing the investments. Employees  are allowed to change their Fund Manager from the 2nd year of investment"
    elif intent_name == "GUARANTEE":
        intent_resp = "N P S is a market linked scheme and there are no investment guarantees available under N P S. Benefits of the scheme will depend on the amount contributed and the investment growth at the time of your exit from the scheme. In the past few years, we have seen an yield of 8-11%."
    elif intent_name == "PREMATURE":
        intent_resp = "Exit from the scheme is only one time. We advise caution before you decide to exit - as you will not be able to re-enter.\
In case of pre-mature exit from N P S, at least 80% of the accumulated pension corpus of the Subscriber has to be utilized for purchase of an annuity. The remaining funds can be withdrawn as lump sum. However, the subscriber can exit from N P S only after completion of 10 years. However this is taxabe in case you exit before 60 years. If the total corpus is less than or equal to ₹1 lakh, the subscriber can opt for 100% lump sum withdrawal."
    elif intent_name == "RETIREMENT":
        intent_resp = "When subscribers reaches the age of 60 years of age, they will have to use at least 40% of accumulated pension corpus to purchase an annuity . The remaining funds can be withdrawn as lump sum. If the total accumulated corpus is less than or equal to rupees 2 lakh, Subscriber can opt for 100% lump sum withdrawal."
    elif intent_name == "DEMISE":
        intent_resp = "In an unfortunate event of the employees/subscribers demise, the account balance may be transferred into the nominee's account after filling in Death Claim Form. One may access this form through www.cra.nsdl.com"
    elif intent_name == "EXCESSCONTRIBUTION":
        intent_resp = "Employee may contribute more than 10% of one's annual basic salary towards N P S account, however the tax benefit that one would get will only be upto 10% of the annual basic salary."
    elif intent_name == "ANNUITYSP":
        intent_resp = "Post retirement employee needs to fill in a Withdrawal Form - avaialble at the NSDL site/POP. Through this withdrawal form , you can indicate how much you want to withdraw as cash/annuity and also choose any  of the following 6 annuity service providers.Life Insurance Corporation of India, SBI Life Insurance, ICICI Prudential Life Insurance, Bajaj Allianz Life Insurance, Star Union Dai-ichi Life Insurance, Reliance Life Insurance."
    elif intent_name == "GRIEVANCE":
        intent_resp = " You can register your grievance / compliant by calling at the CRA call centre or by registering the grievance on NSDL website."
    elif intent_name == "PORTABILITY":
        intent_resp = "Employees are provided with a unique permanent retirement account number. An employee may join this scheme with the P R A N from previous employer. Likewise, after exit from the company, employee can use their unique P R A N to continue with another employer. Please ensure to enroll in the company N P S corporate model. You need to log on to www.cra.nsdl.com - Refer to Form P R A N shifting form and then submit with your existing POP. It usually takes 1 month. For updates - logon to www.cra.nsdl.com"
    elif intent_name == "PARTIALWITHDRAWAL":
        intent_resp = "Contributions to TIER 1 account is possible provided - Subscriber should be in N P S at least for 3 years. Withdrawal amount will not exceed 25% of the contributions made by the Subscriber. Withdrawal can happen maximum of three times during the entire tenure of subscription. Withdrawal is allowed only against the specified reasons, for example; Higher education of children, marriage of children, for the purchase/construction of residential house and for treatment of Critical illnesses."
    elif intent_name == "YES":
        intent_resp = "Ok, Please ask me if you have any further questions"
    return intent_resp 


####################################################################
# Helper functions
#
####################################################################
def plain_text_builder(text_body):
    text_dict = {} 
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
    
    
###############################################
# Set thank you responses
###############################################
thank_resp ={
    1: "You are Welcome",
    2: "Sure no problem",
    3: "No problemo",
    4: "You are Welcome, My pleasure",
    5: "My pleasure, always ready to help"
}


###############################################
# Default responses
###############################################
default_unknown_resp = {
    1 : "I am sorry, I may not be able to answer that, HR work is tiresome sometimes, you know",
    2 : "I am sorry, I donot know the answer", 
    3 : "I am afraid, I am not yet trained to answer that question",
    4 : "ummmmmmm, I do not know the answer, let me get back to you, when I get an upgrade",
    5 : "I am so sorry, Can you please, contact a Human for more details, my sincere apologies"
    
}

def rand_gen(end):
    return randint(1,end)
    

###################################################
#
# Database integeration
###################################################
#Dynamo DB
TABLE_NAME = "alexa_users"
KEY_NAME = "empId"
NUMBER = 'N'
OTP = "otp"

def get_emp(id):
    print(id)
    data = dynamodb.get_item(TableName=TABLE_NAME, Key={KEY_NAME:{NUMBER: id}})
    print(data)
    if data != None:
        return data
    else:
        return None
        
def put_emp_otp(otp, item):
    item[OTP][NUMBER] = otp
    dynamodb.put_item(TableName=TABLE_NAME, Item=item)

    
    
################################################
#
# twilio integration
################################################

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = "ACc4b137886f3f7d1cc69cac2215f2aaff"
TWILIO_AUTH_TOKEN = "04fce5fff7c4e0ad4db25c5069989274"




