#Dictionary of taxiways/runways that connect to each other
connected_taxiways = {
    'North Runway':('A10','A9','A8','A7','A6','A5','A4','A3','A2','A1'),
    'South Runway':('H10','H9','H8','H7','H6','H5','H4','H3','H2','H1'),

    'A10':('North Runway', 'A', 'B6'),
    'A9':('North Runway', 'A'),
    'A8':('North Runway', 'A', 'K'),
    'A7':('North Runway', 'A'),
    'A6':('North Runway', 'A'),
    'A5':('North Runway', 'A'),
    'A4':('North Runway', 'A'),
    'A3':('North Runway', 'A'),
    'A2':('North Runway', 'A'),
    'A1':('North Runway', 'A', 'Q'),
    'A':('A10', 'B6','A9','A8','K','A7','A6','B4','A5','B3','A4','A3','B2','B1','A2','A1','Q'),

    'B6':('A10', 'A','L5'),
    'K':('A','A8','L1','L2','L3'),
    'B4':('A', 'L1','L2','L3'),
    'B3':('A','L4'),
    'B2':('A','B','L1','L2','L3'),
    'B1':('A','B','C','D'),
    'M':('A','B','C','D'),
    'N':('B','C','D', 'N1'),

    'L5': ('B6'),
    'L1_LEFT':('K','B4','L1_MID'),
    'L2_LEFT':('K','B4','L2_MID'),
    'L3_LEFT':('K','B4','L3_MID'),
    'L4': ('A'),
    'L1_MID':('L1_LEFT', 'B4', 'B2'),
    'L2_MID':('L2_LEFT', 'B4', 'B2','D'),
    'L3_MID':('L3_LEFT', 'B4', 'B2','D'),
    'L1_RIGHT':('L1_MID', 'B2','C'),
    'L2_RIGHT':('L2_MID', 'B2','C'),
    'L3_RIGHT':('L3_MID', 'B2', 'D'),

    'B': ('B2', 'B1', 'M', 'N', 'P', 'A1'),
    'C': ('B1', 'M', 'N', 'D', 'L2'),
    'D': ('L3', 'B1', 'M', 'N', 'P', 'Q', 'C'),

    'H10':('South Runway', 'H'),
    'H9':('South Runway', 'H'),
    'H8':('South Runway', 'H'),
    'H7':('South Runway', 'H'),
    'H6':('South Runway', 'H'),
    'H5':('South Runway', 'H'),
    'H4':('South Runway', 'H'),
    'H3':('South Runway', 'H'),
    'H2':('South Runway', 'H'),
    'H1':('South Runway', 'H', 'G1'),
    'H':('H10', 'H9', 'H8', 'H7', 'H6', 'G4', 'H5', 'H4', 'H3', 'R', 'S', 'P', 'Q', 'H2', 'H1', 'G1'),

    'G1':('G','H','H1'),
    'G4':('H', 'G'),
    'G':('G4','R','S','P','Q','G1'),
    'R':('G','H'),
    'S':('G','H'),
    'P': ('H','G','F','N2','N1','D','P1','B'),
    'Q': ('H','G','F','N2','N1','D','P1','A','A1'),

    'P1': ('P', 'Q'),
    'N2': ('P', 'Q'),
    'N1': ('P', 'Q', 'N', 'M'),
    'F': ('P', 'Q')
}

taxiways = [] #List to store all of the taxiway/runway names
for i in connected_taxiways.keys():
    taxiways.append(i)

# print(taxiways)

length = len(taxiways)
numbered_taxiways = {} #Dictionary to store taxiway/runway names along with an identification number

for i in range(length):
    numbered_taxiways[i] = taxiways[i] #Output of format {0:'NORTH RUNWAY', 1: 'SOUTH RUNWAY} and so on

# print(numbered_taxiways)

adjacency_matrix = [] #The adjacency matrix
filler_matrix = [] #Temporary matrix to append list of 0s and 1s for each taxiway in the adjacency_matrix

for i in numbered_taxiways.values():
    for j in connected_taxiways.values():
        if i in j:
            filler_matrix.append(1)
        else:
            filler_matrix.append(0)
    adjacency_matrix.append(filler_matrix) #Appending the temporary matrix to the adjacency_matrix after each iteration of a taxiway
    filler_matrix = [] #Setting temporary matrix back to null for the next taxiway

print(adjacency_matrix)
    