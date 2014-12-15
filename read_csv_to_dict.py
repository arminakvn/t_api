def read_csv(csvfile):
    import csv
    string_dict = {}
    string_list_lines = []
    with open(csvfile, 'rb') as mycsv:
        reader = csv.DictReader(mycsv)
        for row in reader:
    		string_list_lines.append(row)
    return string_list_lines

def write_csv(mylist, csvfile):
    import csv
    with open(csvfile, 'wb') as mycsv:
        writer = csv.DictWriter(mycsv,  fieldnames=mylist[1].keys())
        writer.writeheader()
        for each in mylist:
            mydict = each
            writer.writerow(mydict)
