INFO6005-1
==========

Fixes to Data - see cleaned.csv
-------------------------------

Error 1 - Abbreviations, misspellings or other such typographical errors for fixed names (agency names, for instance)
Fix 1 - Use Google Refine's Text Facet function to view all variations in a column and merge them togther under the appropriate name

Error 2 - Missing Data ("The Department" rather than an actual agency name, for example)
Fix 2 - Use Google Refine to look up an associated value (agency code for missing agency names, for example)

Error 3 - Data has been entered into the wrong column, entire row shifted either to right or left and similar
Fix 3 - Open CSV in spreadsheet application, move offending data

Error 4 - Duplicate rows
Fix 4 - Use Google Refine to filter for duplicates and delete as appropriate.

Error 5 - Preprocessed data included (rows containng totals, for instance, in this case) or extraneous data (copyright information, warnings etc)
Fix 5 - Open CSV in a text editor and delete any such rows

Visualisations
--------------

Visualisation 1 is a multi-bar chart showing the total expenditures of the different agencies relative to each other as percentages against the average time and cost variance of each agency. This allows decisionmakers to visualise the effect that large budgets have on the efficiency of project managers in departments, and also plan future expenditure to reward those who come in under budget/under time and reduce funding to those agencies who mismanage it. Tooltips for each bar show the exact values and the total number of projects per department.

Visualisation 2 is a scatter plot of a single department's projects, plotting cost variance against the percentage of that department's total expenditure. This provides a more in-depth view into an agency along the same lines as the visualisation above, to provide more detail to those making budget allocations in future either within each agency or congress as budgeting decisions are made at that level.

Implementation
--------------

The two implementations were implemented using D3.js, using NVD3 on top of D3.js to build the multi-bar horizontal chart while making use of the example scatter plot provided by D3.js to render the scatterplot. A mix of D3.js and NVD3 functionality and the jQuery library was used to provide the interactive components of the visualisations. The data is preprocessed as much as was feasible using a Python script (process.py) for two reasons, the first being to speed up page load and the second being the author's existing familiarity with Python. Greater experience with Python cut down the development time significantly compared to using Javascript to produce the same results.

The preprocessing consisted of two main factors. The first was to split the data up by department for use in the scatterplot, the second was to calculate a set of statistics based on the data for both the multibar chart and the scatterplot. The multibar chart makes use of averages of time and cost variance calculated by department, along with a percentage of total expenditure by department. The scatterplot used the total agency expenditure previously calculated to provide a percentage of total agency expenditure on a per-project basis.

Interactivity
-------------
The interactive parts of the visualisations allow the user to filter by department and dataset (in the case of the first visualisation) along with tooltips providing the exact data, and allow selection of department and tooltips displaying project names and time variation in the case of the second. There is also the capability to alter the styling of the bars on the first visualisation, to allow the end user to choose the rendering they find easiest to view.

Completion
----------
I'm particularly proud of the preprocessing script, which generates the data in a variety of formats to allow future expansion of the visualisations without much additional work with the preprocessing script.