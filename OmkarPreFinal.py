from enum import Enum
from dataclasses import dataclass
import string
from typing import List

# Calculating the total user spending and spending for each individual merchant
class UserSpending:
    def __init__(self, total_amount, sportCheck_sum, timHortons_sum, subway_sum, other_sum):
        self.total_amount = total_amount 
        self.sportCheck_sum = sportCheck_sum 
        self.subway_sum = subway_sum 
        self.timHortons_sum = timHortons_sum 
        self.other_sum = other_sum
        
    def user_expenditure(self):
        user_expenditure={"total_amount":self.total_amount, "sportCheck_sum":self.sportCheck_sum, "timHortons_sum":self.timHortons_sum, 
                    "subway_sum":self.subway_sum, "other_sum":self.other_sum}
        return user_expenditure;

class Merchant_Code(Enum):
    sportCheck = "sportcheck" 
    timHortons = "tim_hortons" 
    subway = "subway"
    other = "other"


# defining the data types for the rules and the transactions
@dataclass
class Rules_To_Follow :
    id: int
    sportCheckCondition: int
    timHortonCondition: int
    subwayCondition: int
    points: int

@dataclass   
class Transaction:
    id: string
    merchantcode: Merchant_Code
    amount: int

#Calculating the total credit card usage
def credit_usage_detalis(transactions):

    other_sum = 0
    timHortons_sum = 0
    sportCheck_sum= 0
    total_amount = 0
    subway_sum = 0

    for t in transactions:
        total_amount += t.amount
        if(t.merchantcode=="sportCheck"):
            sportCheck_sum += t.amount 
        elif(t.merchantcode=="timHortons"):
            timHortons_sum += t.amount 
        elif(t.merchantcode=="subway"):
            subway_sum += t.amount 
        else:
            other_sum += t.amount 
    userSpending = UserSpending(total_amount, sportCheck_sum, timHortons_sum, subway_sum, other_sum)
    return(userSpending.user_expenditure())
    

# function forn calculating maximum points earned
def reward_points(rules, user_expenditure):
    max_reward_points = 0
    for r in rules:
        while (user_expenditure["sportCheck_sum"] >= r["sportCheckcriteria"] and user_expenditure["timHortons_sum"] >= r["timHortoncriteria"] and user_expenditure["subway_sum"] >= r["subwaycriteria"]):
            max_reward_points += r["points"]
            user_expenditure["sportCheck_sum"] -= r["sportCheckcriteria"]
            user_expenditure["timHortons_sum"] -= r["timHortoncriteria"]
            user_expenditure["subway_sum"] -= r["subwaycriteria"]

    balance = (user_expenditure["sportCheck_sum"] + user_expenditure["timHortons_sum"] + user_expenditure["subway_sum"])
    # applying Rule 7 for the remaining balance which does not fit in any other rules
    max_reward_points += int(balance / 100)       
    return max_reward_points

def calculatePointsPerTransaction(transactionRules, transactions):
    transactionProfit = []
    for transaction in transactions: 
        for rule in transactionRules:
            max_reward_points = 0
            while(transaction.amount>=rule["sportCheckcriteria"] and transaction.merchantcode=="sportCheck"):
                max_reward_points += rule["points"]
                transaction.amount -= rule["sportCheckcriteria"]
        amt_remaining = transaction.amount
        max_reward_points += int(amt_remaining / 100)
        transactionProfit.append(max_reward_points)
    return transactionProfit



# Transaction history as input
trans_1 = Transaction("T01", "sportCheck", 21000)
trans_2 = Transaction("T02", "sportCheck", 8700)
trans_3 = Transaction("T03", "timHortons", 323)
trans_4 = Transaction("T04", "timHortons", 1267)
trans_5 = Transaction("T05", "timHortons", 2116)
trans_6 = Transaction("T06", "timHortons", 2211)
trans_7 = Transaction("T07", "subway", 1853)
trans_8 = Transaction("T08", "subway", 2153)
trans_9 = Transaction("T09", "sportCheck", 7326)
trans_10 = Transaction("T10", "timHortons", 1321)


# Skipping rules 3 and 5 as the the points calculated from rules 3 and 5 are always less that points calculated from rules 6 and 5 respectively
Rules_To_Follow = [
    {"rule":1, "sportCheckcriteria":7500, "timHortoncriteria":2500, "subwaycriteria":2500, "points":500},
    {"rule":2, "sportCheckcriteria":7500, "timHortoncriteria":2500, "subwaycriteria":0, "points":300},
    {"rule":6, "sportCheckcriteria":2000, "timHortoncriteria":0, "subwaycriteria":0, "points":75},
    {"rule":4, "sportCheckcriteria":2500, "timHortoncriteria":1000, "subwaycriteria":1000, "points":150}
    
]

transactionRules = [
   {"rule":6, "sportCheckcriteria":2000, "timHortoncriteria":0, "subwaycriteria":0, "points":75},
]

# Calling the functions 
transactions = [trans_1,trans_2,trans_3,trans_4,trans_5,trans_6,trans_7,trans_8,trans_9,trans_10]
user_expenditure = credit_usage_detalis(transactions)
max_reward_points = reward_points(Rules_To_Follow, user_expenditure)

#printing the maximum reward points earned
print("Max points for all the transactions of the month -->", max_reward_points)


transactionsPoints = calculatePointsPerTransaction(transactionRules, transactions)
print("Maximum points for each transaction:")
for i in range(len(transactionsPoints)):
    print("Transaction",i+1,"-->",transactionsPoints[i])



            
                
 









