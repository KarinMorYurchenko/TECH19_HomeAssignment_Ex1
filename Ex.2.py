import csv
import pydicom as dicom
import write

ds = dicom.dcmread("Home_Ex.DCM")

with open('my.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	write.writerow("Group Elem Description VR Value".split())
	for elem in ds:
		writer.writerow()
		elem.tag.group:04x


