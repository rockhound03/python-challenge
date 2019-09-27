if __name__ == "__main__":
    pass

import os
import csv
#import math
import print_to_text



#PyBank/Resources/budget_data.csv

# Constants ***************************************************************************************
csv_file = os.path.join('Resources','budget_data.csv')
profitable = True
loss = False

# used for dictionary bin names
largest_month_tag = "largest_month"
largest_amount_tag = "largest_amount"
profit_tag = "profit"
amount_tag = "amount"
month_tag = "month"

# **************************************************************************************************
# Function to find average value.
def GetAverage(DataList):
    to_be_averaged = [data[amount_tag] for data in DataList]
    average = sum(to_be_averaged) / len(to_be_averaged)
    return average

# Function to find largest profit / loss.
def GetLargest(DataList, Profit = True):
    largest_value = float(0)
    largest_month = ""
    for data in DataList:
        if Profit == data[profit_tag] and abs(data[amount_tag]) > largest_value:
            largest_value = abs(data[amount_tag])
            largest_month = data[month_tag]
    #return largest_value
    largest_value_month = {largest_month_tag : largest_month, largest_amount_tag : largest_value}
    return largest_value_month




    

# Function to load data from csv file, flagging as a profit or loss for ease of processing later.
def TotalMonth(data):
    with open(csv_file,'r') as csvdata:
        data_from_csv =[]
        csvreader = csv.reader(csvdata,delimiter = ',')
        next(csvreader) # skip header
        for month in csvreader:
            if float(month[1]) < 0:
                month_data = {
                    month_tag : month[0],amount_tag : float(month[1]), profit_tag : False
                }
                data_from_csv.append(month_data)
            else:
                month_data ={
                    month_tag : month[0],amount_tag : float(month[1]), profit_tag : True
                }
                data_from_csv.append(month_data)
        return data_from_csv

    


all_data_csv = TotalMonth(csv_file)    # populates losses and profits list.
TextLines = []
TextLines.append("Financial Analysis\n----------------------------")
total_months = len(all_data_csv)

TextLines.append("Total Months: " + str(total_months))

total_overall = [all_data[amount_tag] for all_data in all_data_csv]
total_sum = sum(total_overall)
TextLines.append("Total: $" + '%.2f' % total_sum)

avg = GetAverage(all_data_csv)
TextLines.append("The Average Change: $" + '%.2f' % avg)

largest_profit = GetLargest(all_data_csv, profitable)
TextLines.append("Greatest increase in profits: " + largest_profit[largest_month_tag] + " ($" + '%.2f' % largest_profit[largest_amount_tag] + ")")

largest_loss = GetLargest(all_data_csv, loss)
TextLines.append("Greatest decrease in profits: " + largest_loss[largest_month_tag] + " ($-" + '%.2f' % largest_loss[largest_amount_tag] + ")")


for line in TextLines:
    print(line)
print_to_text.main(TextLines,"bank_out.txt","output")