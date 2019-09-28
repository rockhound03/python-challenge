if __name__ == "__main__":
    pass

import os
import csv
import print_to_text

# Constants / reference variables.************************************************
csv_file_path = os.path.join('Resources', 'election_data.csv')

voter_id = "Voter ID"
county = "County"
candidate = "Candidate"
counties_tag = "counties"
candidates_tag = "candidates"
votes_tag = "votes"
percent_tag = "percent"
won_tag = "won"
white_space = " "
# *********************************************************************************
# Load csv file contents into memory.
def GetElectionResults(CSVFile):
    with open(CSVFile,'r') as cvsdata:
        data_from_csv = []
        csvreader = csv.reader(cvsdata,delimiter=',')
        next(csvreader) # skip header
        [data_from_csv.append({voter_id : vote[0], county : vote[1], candidate : vote[2]}) for vote in csvreader]
        return data_from_csv
# *********************************************************************************
# Find unique candidate and county names.  Used later in vote counting.
def GetUniqueCandidatesCounties(RawData):
    list_of_candidates = []
    list_of_counties = []
    for data in RawData:
        if len(list_of_candidates) == 0:
            list_of_candidates.append(data[candidate])
        else:
            found = False
            found = [True for name in list_of_candidates if name == data[candidate]]
            if not found:
                list_of_candidates.append(data[candidate])
        # county search
        if len(list_of_counties) == 0:
            list_of_counties.append(data[county])
        else:
            found = False
            found = [True for location in list_of_counties if location == data[county]]
            if not found:
                list_of_counties.append(data[county])
    counties_and_candidates = {counties_tag : list_of_counties, candidates_tag : list_of_candidates}
    return counties_and_candidates
# *********************************************************************************
# Accumulate the vote results by candidate name.  Tracked in a list of dictionaries.
def CountResults(candidate_county, RawData):
    tally_chart = []
    [tally_chart.append({candidate : person, votes_tag : 0, percent_tag : 0, won_tag : False }) for person in candidate_county[candidates_tag]]
    for vote in RawData:
        #person_search[votes_tag] += [1 for person_search in tally_chart if vote[candidate] == person_search[candidate]]
        for person_search in tally_chart:
            if vote[candidate] == person_search[candidate]:
                person_search[votes_tag] += 1
    return tally_chart

# calculate percentages (needs to be done once totals are counted).  Adds percentages and finds winner and inserts in list of dicts.
def CalcPercent(result_sheet):
    total = sum([data[votes_tag] for data in result_sheet])
    win_count = int(0)
    win_name = ""
    win_answer = False
    for running in result_sheet:
        if running[votes_tag] > win_count:
            win_count = running[votes_tag]
            win_name = running[candidate]
    
    result_w_percent = []
    result_w_percent.append({candidate : "Total", votes_tag : total, percent_tag : 100.0, won_tag : False})
    for can_result in result_sheet:
        if can_result[candidate] == win_name:
            win_answer = True
        result_w_percent.append({candidate : can_result[candidate], votes_tag : int(can_result[votes_tag]), 
        percent_tag :  can_result[votes_tag] / total * 100, won_tag : win_answer})
        win_answer = False
    return result_w_percent

# call result / percentage calcs. ***********************************************
election_data = GetElectionResults(csv_file_path)
all_candidates_counties = GetUniqueCandidatesCounties(election_data)
# Output string building. *******************************************************
candidate_list = []
TextLines = []

TextLines.append("--------------Counties Reporting-----------------")
[TextLines.append(seat) for seat in all_candidates_counties[counties_tag]]

election_results = CountResults(all_candidates_counties, election_data)
final_tally = CalcPercent(election_results)

TextLines.append("*************************************************")
TextLines.append("---------------Election Results------------------\n")
for total_vote in final_tally:
    if total_vote[candidate] == "Total":
        TextLines.append("Total Votes: " + str(total_vote[votes_tag]))

TextLines.append("Candidate       Votes Received       Percentage")
for winner in final_tally:
    #start_chars = len(winner[candidate])
    #percent_chars = len(str(winner[votes_tag]))
    spaces = 16 - len(winner[candidate])
    per_spaces = 21 - len(str(winner[votes_tag]))
    sp = ''
    sp_perc = ''
    # Add white space for appearance in output. *********************************
    #[sp + white_space for i in range(0, spaces)]
    for i in range(0,spaces):
        sp += white_space
    #[sp_perc + white_space for i in range(0, per_spaces)]
    for i in range(0, per_spaces):
        sp_perc += white_space
    if winner[candidate] != "Total":
        TextLines.append(winner[candidate] + sp + str(winner[votes_tag]) + sp_perc + '%.1f' % winner[percent_tag])
TextLines.append("\n------------------Final Tally--------------------")
[TextLines.append("Winner: " + the_winner[candidate]) for the_winner in final_tally if the_winner[won_tag] == True]
TextLines.append("*************************************************")
# Print output to console as well as text file in output folder.
[print(line) for line in TextLines]
print_to_text.main(TextLines,"poll_result.txt","output")