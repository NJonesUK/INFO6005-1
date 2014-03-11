from __future__ import division

import csv
import json
import datetime

infile = open("projects.csv", 'r')
fieldnames = ('Unique Investment Identifier', r'Business Case ID', r'Agency Code', r'Agency Name', r'Investment Title', r'Unique Project ID', r'Project ID', r'Agency Project ID', r'Project Name', r'Objectives / Expected Outcomes', r'Start Date',r'Completion Date',r'Project Life Cycle Cost ($M)',r'Schedule Variance (in days)','Schedule Variance (%)',r'Schedule Color',r'Cost Variance ($ M)',r'Cost Variance (%)',r'Cost Color',r'Updated Date',r'Updated Time')

reader = csv.DictReader(infile, fieldnames)
departments = {}
department_project_totals = {}
department_budget_percentage = {}
project_numbers = {}
project_time = {}
project_time_variance = {}
project_cost_variance = {}
project_cost = {}

count = 0
for line in reader:
	if count == 0:
		count += 1
		continue
	
	pid = line['Unique Project ID']
	time = (datetime.datetime.strptime(line['Completion Date'], '%Y-%m-%d') - datetime.datetime.strptime(line['Start Date'], '%Y-%m-%d')).days
	time_variance = float(line['Schedule Variance (%)'])
	cost = float(line['Project Life Cycle Cost ($M)'])
	cost_variance = float(line['Cost Variance (%)'])
	acode = line['Agency Code']
	departments[acode] = line['Agency Name']
	try:
		project_numbers[acode] += 1
		department_project_totals[acode] += cost
		project_time[acode].append(time)
		project_time_variance[acode].append(time_variance)
		project_cost[acode].append(cost)
		project_cost_variance[acode].append(cost_variance)
	except KeyError:
		project_numbers[acode] = 1
		department_project_totals[acode] = cost  
		project_time[acode] = [time,]
		project_time_variance[acode] = [time_variance,]
		project_cost[acode] = [cost,]
		project_cost_variance[acode] = [cost_variance,]

total_budget = 0
for department in department_project_totals:
	total_budget += department_project_totals[department]
print "Total Budget - $" + str(round(total_budget))

deptfile = open("departments.json", 'w')
deptfile.write(json.dumps(departments))
deptfile.close

average_cost = {}
average_cost_variance = {}
average_time_variance = {}
average_time = {}

avgfile = open('averages.csv', 'wb')
writer = csv.writer(avgfile, delimiter='\t')
writer.writerow(["dept", "tv"])

for key in departments:
	average_cost_variance[key] = sum(project_cost_variance[key])/len(project_cost_variance[key])
	average_time_variance[key] = sum(project_time_variance[key])/len(project_time_variance[key])
	average_time[key] = sum(project_time[key])/len(project_time[key])
	average_cost[key] = sum(project_cost[key])/len(project_cost[key])

	writer.writerow([departments[key], average_time_variance[key]])
	print departments[key], ': Cost =', average_cost[key], ', CV =', average_cost_variance[key], ', TV =', average_time_variance[key], ', Time =', average_time[key]
avgfile.close()

for department in departments:
	deptfile = open(departments[department] +  '.tsv', 'wb')
	writer = csv.writer(deptfile, delimiter='\t')
	writer.writerow(["dept", "tv", "cv"])

	content = "["
	proj_dict={}
	for time, cost, time_variance, cost_variance in zip(project_time[department], project_cost[department], project_time_variance[department], project_cost_variance[department]):
		writer.writerow([departments[department], time_variance, cost_variance])
		proj_dict['tv'] = time_variance
		proj_dict['cv'] = cost_variance
		content += json.dumps(proj_dict)
		content += ',\n'
	content += "]"
	outfile = open(departments[department] + '.json', 'w')
	outfile.write(content)
	outfile.close


avgjsondict = []
avgjsondict.append({}) #Percentage of Total Expenditure - Element 0
avgjsondict.append({}) #Time Variation - Element 1
avgjsondict.append({}) #Cost Variation - Element 2

avgjsondict[0]['key'] = "Percentage of Total Expenditure (%)"
avgjsondict[1]['key'] = "Average Time Variation (%)"
avgjsondict[2]['key'] = "Average Cost Variation (%)"

avgjsondict[0]['color'] = "#27d67e"
avgjsondict[1]['color'] = "#1f77b4"
avgjsondict[2]['color'] = "#d62728"

avgjsondict[0]['values'] = []
avgjsondict[1]['values'] = []
avgjsondict[2]['values'] = []


for department in departments:
	avgjsondict[0]['values'].append({'label': departments[department], 'value': ((department_project_totals[department]/total_budget) * 100)})
	avgjsondict[1]['values'].append({'label': departments[department], 'value': average_time_variance[department]})
	avgjsondict[2]['values'].append({'label': departments[department], 'value': average_cost_variance[department]})


outfile = open("multi.json", 'w')
content = json.dumps(avgjsondict)
outfile.write(content)
outfile.close()
