from moveClusters_individuals import move_individual
import csv

data = csv.reader(open('../../data-result/data-night.csv', encoding="utf8"))
#data = csv.reader(open('../../data-result/data.csv', encoding="utf8"))

for line in data:
  [plan, flight, str] = line

  flight = flight.replace('\ufeff', '')
  arr = str.split('\t')

  print(plan, flight, arr)
  move_individual(plan, flight, arr)