if __name__ == "__main__":
    pass

import os
import csv
import print_to_text

csv_file_path = os.path.join('Resources', 'election_data.csv')

voter_id = "Voter ID"
county = "County"
candidate = "Candidate"


def GetElectionResults(CSVFile):
    with open(CSVFile,'r') as cvsdata:
        data_from_csv = []
        csvreader = csv.reader(cvsdata,delimiter=',')
        next(csvreader) # skip header
        for vote in csvreader:
            voter_result = {voter_id : vote[0], county : vote[1], candidate : vote[2]}
            data_from_csv.append(voter_result)
        return data_from_csv

# Find unique candidate and county names.  Used later in vote counting.
def GetUniqueCandidatesCounties(RawData):
    list_of_candidates = []
    list_of_counties = []
    for data in RawData:
        if len(list_of_candidates) == 0:
            list_of_candidates.append(data[candidate])
        else:
            found = False
            for name in list_of_candidates:
                if name == data[candidate]:
                    found = True
            if not found:
                list_of_candidates.append(data[candidate])
        # county search
        if len(list_of_counties) == 0:
            list_of_counties.append(data[county])
        else:
            found = False
            for location in list_of_counties:
                if location == data[county]:
                    found = True
            if not found:
                list_of_counties.append(data[county])
    counties_and_candidates = {"counties" : list_of_counties, "candidates" : list_of_candidates}
    return counties_and_candidates

# Accumulate the vote results by candidate name.  Tracked in a list of dictionaries.
def CountResults(candidate_county, RawData):
    tally_chart = []
    for person in candidate_county["candidates"]:
        candidate_tally = {candidate : person, "votes" : 0, "percent" : 0, "won" : False }
        tally_chart.append(candidate_tally)
    
    for vote in RawData:
        for person in tally_chart:
            if vote[candidate] == person[candidate]:
                person["votes"] += 1
    return tally_chart

# calculate percentages (needs to be done once totals are counted).  Adds percentages and finds winner and inserts in list of dicts.
def CalcPercent(result_sheet):
    total = int(0)
    win_count = int(0)
    win_name = ""
    win_answer = False
    for running in result_sheet:
        total += running["votes"]
        if running["votes"] > win_count:
            win_count = running["votes"]
            win_name = running[candidate]
    
    result_w_percent = []
    result_w_percent.append({candidate : "Total", "votes" : total, "percent" : 100.0, "won" : False})
    for can_result in result_sheet:
        if can_result[candidate] == win_name:
            win_answer = True
        result_w_percent.append({candidate : can_result[candidate], "votes" : int(can_result["votes"]), 
        "percent" :  can_result["votes"] / total * 100, "won" : win_answer})
        win_answer = False
    return result_w_percent

# call result / percentage calcs.
election_data = GetElectionResults(csv_file_path)
all_candidates_counties = GetUniqueCandidatesCounties(election_data)
# Output string building.
candidate_list = []
TextLines = []

TextLines.append("--------------Counties Reporting-----------------")
for seat in all_candidates_counties["counties"]:
    TextLines.append(seat)

election_results = CountResults(all_candidates_counties, election_data)
final_tally = CalcPercent(election_results)

TextLines.append("*************************************************")
TextLines.append("---------------Election Results------------------\n")
for total_vote in final_tally:
    if total_vote[candidate] == "Total":
        TextLines.append("Total Votes: " + str(total_vote["votes"]))

TextLines.append("Candidate       Votes Received       Percentage")
for winner in final_tally:
    start_chars = len(winner[candidate])
    percent_chars = len(str(winner["votes"]))
    spaces = 16 - start_chars
    per_spaces = 21 - percent_chars
    sp = ''
    sp_perc = ''
    for i in range(0,spaces):
        sp += ' '
    for i in range(0, per_spaces):
        sp_perc += ' '
    if winner[candidate] != "Total":
        TextLines.append(winner[candidate] + sp + str(winner["votes"]) + sp_perc + '%.1f' % winner["percent"])
TextLines.append("\n------------------Final Tally--------------------")
for the_winner in final_tally:
    if the_winner["won"] == True:
        TextLines.append("Winner: " + the_winner[candidate])
TextLines.append("*************************************************")
# Print output to console as well as text file in output folder.
for line in TextLines:
    print(line)
print_to_text.main(TextLines,"poll_result.txt","output")