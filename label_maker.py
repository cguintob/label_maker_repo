import sys
import os

# Set paths for file to be read and file to be written to
read_path = "/home/cmuhgc/HGC_DB_postgres/shipping/"
write_path = "/home/cmuhgc/qr_labels/"

# Set characteristics of paper (mm)
paper_height = 80
paper_width = 50

# Set characteristics of QR codes common to all module IDs (mm)
qr_height = 18
qr_width = 18
even_qr_x = 4
odd_qr_x = 28
first_gen_qr_y = 56
second_gen_qr_y = 30
third_gen_qr_y = 4

# Set characteristics of text labels common to all module IDs (mm)
text_height = 3
text_width = 25
text_size = 7
text_alignment = 1
even_text_x = 0.5
odd_text_x = 24.5
first_gen_text_y = 74
second_gen_text_y = 48
third_gen_text_y = 22

# Write the beginning of the Clabel file (common to all module IDs)
def write_beginning(f):
    f.write("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n")
    f.write('<DLabel source="pc" version="3.2.5">\n')
    f.write(' <paper excelhash="" zoomfactor="3.725290298461914" bgcolor="" excelurl="" h="{0}" databasefile="" moreselect="true" printerdpi="203" background="" shapeindex="1" horoffset="0" veroffset="0" rotate="0" datasource="" colspacing="2" excelid="" colcount="1" bgurl="" w="{1}" excelpath="">\n'.format(paper_height, paper_width))
    f.write('  <labelobjects>\n')

# Set the x- and y-positions of the QR codes for each module ID
def qr_position_set(i):
    if (i % 2 == 0):
        ql = even_qr_x
        if (i < 1):
            qt = first_gen_qr_y
        elif (i < 3):
            qt = second_gen_qr_y
        else:
            qt = third_gen_qr_y
    else:
        ql = odd_qr_x
        if (i < 2):
            qt = first_gen_qr_y
        elif (i < 4):
            qt = second_gen_qr_y
        else:
            qt = third_gen_qr_y
    return ql, qt

# Set the x- and y-positions of the text labels for each module ID
def text_position_set(i):
    if (i % 2 == 0):
        tl = even_text_x
        if (i < 1):
            tt = first_gen_text_y
        elif (i < 3):
            tt = second_gen_text_y
        else:
            tt = third_gen_text_y
    else:
        tl = odd_text_x
        if (i < 2):
            tt = first_gen_text_y
        elif (i < 4):
            tt = second_gen_text_y
        else:
            tt = third_gen_text_y
    return tl, tt

# Write the QR codes and text labels for each module ID
def write_id(f, label_list, i):
    ql, qt = qr_position_set(i)
    tl, tt = text_position_set(i)
    f.write('   <drawobj year="0" maskcharacter="" h="{0}" currentdata="" interval="1" day="0" level="Q" addtype="0" l="{1}" itemtype="8" zvalue="1" timeformat="0" barcodetype="QR_CODE" hour="0" rotate="0" memory="0" second="0" maskcontent="" symbolversion="0" encodemode="ANSI" datasource="0" dateformat="0" ucc="false" hidelanding="false" minute="0" month="0" repeat="1" lock="false" characterset="0" addorsub="0" density="0.62560" addbarcode="false" w="{2}" t="{3}">\n'.format(qr_height, ql, qr_width, qt))
    f.write('    <textlist>\n')
    f.write('     <text year="0" sharefieldname="" currentdata="" interval="1" day="0" timeformat="0" hour="0" memory="0" value="{0}" second="0" promptname="" datasource="0" dateformat="0" promptindex="0" minute="0" month="0" repeat="1" keyinput="0" addorsub="0"/>\n'.format(label_list[i]))
    f.write('    </textlist>\n')
    f.write('   </drawobj>\n')
    f.write('   <drawobj year="0" fontunderline="false" h="{0}" currentdata="1" interval="1" day="0" fontitalic="false" fontsize="{1}" hormirror="false" l="{2}" itemtype="5" zvalue="9" timeformat="0" linespacing="0" hour="0" rotate="0" memory="0" second="0" datasource="0" fontbold="false" fontfamily="Arial" startposition="0" stretch="87" dateformat="3" ellipse="false" minute="0" month="0" repeat="1" lock="false" addorsub="0" fontstrikeout="false" w="{3}" textlength="0" alignment="{4}" fontletterspacing="0" t="{5}" blackground="false">\n'.format(text_height, text_size, tl, text_width, text_alignment, tt))
    f.write('    <textlist>\n')
    f.write('     <text year="0" sharefieldname="" currentdata="1" interval="1" day="0" timeformat="0" hour="0" memory="0" value="{0}" second="0" promptname="" datasource="0" dateformat="3" promptindex="0" minute="0" month="0" repeat="1" keyinput="0" addorsub="0"/>\n'.format(label_list[i]))
    f.write('    </textlist>\n')
    f.write('   </drawobj>\n')

# Write the end of the Clabel file (common to all module IDs)
def write_end(f):
    f.write('  </labelobjects>\n')
    f.write('  <sharedfields>\n')
    f.write('   <fieldlist/>\n')
    f.write('  </sharedfields>\n')
    f.write(' </paper>\n')
    f.write('</DLabel>\n')

# Get the file with module IDs to be printed
print("Copy and paste the file containing the desired module IDs (from " + read_path + "): ")
print("-----------------------------------------------------------------------")
os.system("ls -lhUt --time=birth " + read_path + " | head -5 | awk '{print $6, $7, $8, $9}'")
print("-----------------------------------------------------------------------")
try:
    ship_file = input()
except KeyboardInterrupt:
    print("")
    sys.exit(1)
ship_file = str(ship_file).lstrip()
file_string = ship_file.split(".")

# Open the data file to get the module IDs from the database
ids = []
try:
    with open(read_path + ship_file, "r") as f:
        for data in f:
            ids.append(data.rstrip())
except FileNotFoundError:
    print("File not found. Create file with module IDs before running this program using postgres.")
    sys.exit(1)

# Write the module IDs to QR codes and text labels
write_file = write_path + "{0}_LABEL.ddl".format(file_string[0])
with open(str(write_file), "w") as f:
    write_beginning(f)
    for i in range(len(ids)):
        write_id(f, ids, i)
    write_end(f)

# Display where label file is located
print("Label found in " + str(write_file))
print('If File Explorer not open, run PowerShell and type "explorer.exe .", then go to "Linux\\Ubuntu\\home\\cmuhgc\\qr_labels"')

################################################################################

# Code written by Christian Guinto-Brody for the CMU CMS HGCal group

################################################################################
