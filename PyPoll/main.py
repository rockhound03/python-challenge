if __name__ == "__main__":
    pass

import os
import csv
import math
#import print_to_text

csv_file_path = os.path.join('Resources', 'election_data.csv')

voter_id = "Voter ID"
county = "County"
candidate = "Candidate"

#Voter ID,County,Candidate

def GetElectionResults(CSVFile):
    with open(CSVFile,'r') as cvsdata:
        data_from_csv = []
        #header_info = []
        csvreader = csv.reader(cvsdata,delimiter=',')
        next(csvreader) # skip header
        for vote in csvreader:
            voter_result = {voter_id : vote[0], county : vote[1], candidate : vote[2]}
            data_from_csv.append(voter_result)
        return data_from_csv


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

""" 
def GetCountiesReporting(RawData):
    list_of_counties = []
    for data in RawData:
        if len(list_of_counties) == 0:
            list_of_counties.append(data[county])
        else:
            found = False
            for location in list_of_counties:
                if location == data[county]:
                    found = True
                if not found:
                    list_of_counties.append(data[county])
    return list_of_counties
 """

def CountResults(candidate_county, RawData):
    """ temporary_counties = []
    for county_seat in candidate_county["counties"]:
        temporary_counties.append(county_seat) """
    tally_chart = []
    for person in candidate_county["candidates"]:
        candidate_tally = {candidate : person, "votes" : 0 }
        tally_chart.append(candidate_tally)
    
    for vote in RawData:
        for person in tally_chart:
            if vote[candidate] == person[candidate]:
                person["votes"] += 1
    return tally_chart



        



election_data = GetElectionResults(csv_file_path)
all_candidates_counties = GetUniqueCandidatesCounties(election_data)
# all_counties = GetCountiesReporting(election_data)
print("-- Candidates --")
for person in all_candidates_counties["candidates"]:
    print(person)

print("-- Counties Reporting --")
for seat in all_candidates_counties["counties"]:
    print(seat)

# 21 spaces
election_results = CountResults(all_candidates_counties, election_data)

print("********************************************************")
print("-------------------Election Results---------------------")
print("Candidate            Votes Received")
for winner in election_results:
    start_chars = len(winner[candidate])
    spaces = 21 - start_chars
    sp = ''
    for i in range(0,spaces):
        sp += ' '
    print(winner[candidate] + sp + str(winner["votes"]))