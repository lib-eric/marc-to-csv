# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode
# CSV creation and writing
import os
from pathlib import Path
import csv


def extract_fields(record=None):
    dissertation_fields = {}

    dissertation_fields['filename'] = get_filename(record)
    dissertation_fields['dc.subject.classification'] = get_dc_subject_classification(record)
    dissertation_fields['dc.creator'] = get_dc_creator(record)
    dissertation_fields['dc.title'] = get_dc_title(record)
    dissertation_fields['dc.title.alternative'] = get_dc_title_alternative(record)
    dissertation_fields['dc.date.issued'] = get_dc_date_issued(record)
    dissertation_fields['dc.format.extent'] = get_dc_format_extent(record)
    dissertation_fields['dc.description'] = get_dc_description(record)
    dissertation_fields['dc.description.abstract'] = get_dc_description_abstract(record)
    dissertation_fields['thesis.degree.type'] = get_thesis_degree_type(record)
    dissertation_fields['thesis.degree.level'] = get_thesis_degree_level(record)
    dissertation_fields['thesis.degree.decipline'] = get_thesis_degree_discipline(record)
    dissertation_fields['dc.subject'] = get_dc_subject(record)
    dissertation_fields['dc.subject.mesh'] = get_dc_subject_mesh(record)
    dissertation_fields['dc.subject.nalt'] = get_dc_subject_nalt(record)
    dissertation_fields['dc.subject.lcsh'] = get_dc_subject_lcsh(record)
    dissertation_fields['dc.contributor.committeeMember'] = get_contributor_committeemember(record)
    dissertation_fields['dc.contributor.advisor'] = get_contributor_advisor(record)
    dissertation_fields['handle'] = get_handle(record)

    # Write Record to CSV
    dictionary_to_csv(dissertation_fields)
    
    # return dissertation_fields

# MARC: 001
# Add ".pdf" to end
def get_filename(record):
    filename = ''

    # Get FILENAME
    if record['001'] != None:
        # FILENAME standard is to use the id = 001 and append '.pdf' as the filename
        filename = '{id}.pdf'.format(id=str(record['001'].data).strip())
    
    print("filename: {file_name}".format(file_name=filename))
    
    return filename


# TODO:
# 1) What is wanting out of this field? "Disseration", YEAR
# MARC: 099
def get_dc_subject_classification(record):
    dc_subject_classification = ''

    # Get SUBJECT CLASSIFICATION
    if record['099'] != None:
        dc_subject_classification = str(record['099']).strip()
    
    print("dc_subject_classification: {subject_class}".format(subject_class=dc_subject_classification))
    
    return dc_subject_classification


# MARC: 100$a
def get_dc_creator(record):
    dc_creator = ''

    # Get CREATOR
    if record['100']['a'] != None:
        dc_creator = str(record['100']['a']).strip()
    
    print("dc_creator: {creator}".format(creator=dc_creator))
    
    return dc_creator


# MARC: 245$a$b
# Remove punctuation at end, including /
def get_dc_title(record):
    # Defaults
    title_a = ''
    title_b = ''
    dc_title = ''

    # Get TITLE$a
    if record['245']['a'] != None:
        title_a = str(record['245']['a']).strip()

        # Remove trailing [spaces, '.', '/']
        while title_a[-1] in ['.','/']:
            title_a = title_a[0:-1].strip()
        
        # Get TITLE$b
        if record['245']['b'] != None:
            title_b = str(record['245']['b']).strip()

            # Remove trailing [spaces, '.', '/']
            while title_b[-1] in ['.','/']:
                title_b = title_b[0:-1].strip()
    
    dc_title = title_a + title_b
    
    print("dc_title: {title}".format(title=dc_title))
    
    return dc_title


# MARC: 246$a
# Remove punctuation at end, including /
def get_dc_title_alternative(record):
    dc_title_alternative = ''

    # Get TITLE ALTERNATIVE
    if record['245']['a'] != None:
        dc_title_alternative = record['245']['a']

        # Remove trailing [spaces, '.', '/']
        while dc_title_alternative[-1] in ['.','/']:
            dc_title_alternative = dc_title_alternative[0:-1].strip()
    
    print("dc_title_alternative: {title_alt}".format(title_alt=dc_title_alternative))
    
    return dc_title_alternative


# MARC: 260$c
# Remove punctuation
def get_dc_date_issued(record):
    dc_date_issued = ''

    # Get DATE ISSUED - Check 260 first
    if record['260'] != None:
        dc_date_issued = record['260']['c']

        # Remove trailing [spaces, '.', '/']
        while dc_date_issued[-1] in ['.','/']:
            dc_date_issued = dc_date_issued[0:-1].strip()
    
    # Get DATE ISSUED - Check 260 first
    if record['264'] != None:
        dc_date_issued = record['264']['c']

        # Remove trailing [spaces, '.', '/']
        while dc_date_issued[-1] in ['.','/']:
            dc_date_issued = dc_date_issued[0:-1].strip()
    
    print("dc_date_issued: {date_issued}".format(date_issued=dc_date_issued))
    
    return dc_date_issued


# MARC: 300$a
# Add space between subfields
def get_dc_format_extent(record):
    dc_format_extent = ''

    # Get FORMAT EXTENT
    if record['300'] != None:
        dc_format_extent = record['300']['a']

        # Remove trailing [spaces, '.', '/']
        while dc_format_extent[-1] in ['.','/']:
            dc_format_extent = dc_format_extent[0:-1].strip()
    
    print("dc_format_extent: {format_extent}".format(format_extent=dc_format_extent))
    
    return dc_format_extent


# TODO: Doesn't seem right; only 1 record with 500, not relevant
# MARC: 500
def get_dc_description(record):
    dc_description = ''

    # Get DESCRIPTION
    if record['500'] != None:
        dc_description = record['500']
    
    print("dc_description: {description}".format(description=dc_description))
    
    return dc_description



# MARC: 520
def get_dc_description_abstract(record):
    dc_description_abstract = ''

    # Get DESCRIPTION ABSTRACT
    if record['520'] != None:
        dc_description_abstract = record['520']['a']
    
    print("dc_description_abstract: {description_abstract}".format(description_abstract=dc_description_abstract))
    
    return dc_description_abstract



# MARC: 502$b
# Will be either Doctoral or Masters
def get_thesis_degree_type(record):
    thesis_degree_type = ''

    # Get DEGREE TYPE
    if record['502'] != None:
        field_502a = record['502']['b']

        if " in " in field_502a:
            # "{type part} in {department}" -- grabs the {type part}
            type_part_extract = field_502a[0:field_502a.find(" in ")]

            lower = type_part_extract.lower()

            # Doctorial/Ph.D
            if lower in ["ph. d", "ph. d.", "ph.d.", "ph d"]:
                thesis_degree_type = "Doctorial"
            # Master
            elif lower in ["master", "masters"]:
                thesis_degree_type = "Masters"

    print("thesis_degree_type: {degree_type}".format(degree_type=thesis_degree_type))
    
    return thesis_degree_type



# TODO: LEVEL same as TYPE? Abbreviation versus spelled out?
# MARC: 502$b
# Will be either Doctoral or Masters
def get_thesis_degree_level(record):
    thesis_degree_level = ''

    # Get DEGREE LEVEL
    if record['502'] != None:
        field_502a = record['502']['b']

        if " in " in field_502a:
            # "{type part} in {department}" -- grabs the {type part}
            type_part_extract = field_502a[0:field_502a.find(" in ")]

            lower = type_part_extract.lower()

            # Doctorial/Ph.D
            if lower in ["ph. d", "ph. d.", "ph.d.", "ph d"]:
                thesis_degree_level = "Doctorial"
            # Master
            elif lower in ["master", "masters"]:
                thesis_degree_level = "Masters"

    print("thesis_degree_level: {degree_level}".format(degree_level=thesis_degree_level))
    
    return thesis_degree_level



# MARC: 502$b
# Name of department
def get_thesis_degree_discipline(record):
    thesis_degree_discipline = ''

    # Get DEGREE DISCIPLINE
    if record['502'] != None:
        field_502a = record['502']['b']

        if " in " in field_502a:
            # "{type part} in {department}" -- grabs the {department} to end
            thesis_degree_discipline = field_502a[field_502a.find(" in ")+4:]
    

    print("thesis_degree_discipline: {degree_discipline}".format(degree_discipline=thesis_degree_discipline))

    return thesis_degree_discipline



# MARC: 667
# REPEAT REPEAT
def get_dc_subject(record):
    # Default variables
    dc_subject = ''
    ls_667 = []
    ls_subject = []

    # Check if there is 667 field in record, if so get all and put into list
    if record['667'] != None:
        ls_667 = record.get_fields('667')
    
    # Loop through the 667 fields and grab
    for subject in ls_667:
        # If last character is '.' remove it
        if subject[-1] == '.':
            formatted_subject = subject[0:-1].strip()
        ls_subject.append(formatted_subject)


    # Join together SUBJECT with double pipe (||)
    if len(ls_subject) > 0:
        dc_subject = '||'.join(ls_subject)

    return dc_subject



# MARC: 668
# REPEAT REPEAT
def get_dc_subject_mesh(record):
    # Default variables
    dc_subject_mesh = ''
    ls_668 = []
    ls_subject_mesh = []

    # Check if there is 668 field in record, if so get all and put into list
    if record['668'] != None:
        ls_668 = record.get_fields('668')
    
    # Loop through the 668 fields and grab
    for mesh in ls_668:
        # If last character is '.' remove it
        if mesh[-1] == '.':
            formatted_mesh = mesh[0:-1].strip()
        ls_subject_mesh.append(formatted_mesh)


    # Join together SUBJECT_MESH with double pipe (||)
    if len(ls_subject_mesh) > 0:
        dc_subject_mesh = '||'.join(ls_subject_mesh)

    return dc_subject_mesh



# MARC: 669
# REPEAT REPEAT
def get_dc_subject_nalt(record):
    # Default variables
    dc_subject_nalt = ''
    ls_669 = []
    ls_subject_nalt = []

    # Check if there is 669 field in record, if so get all and put into list
    if record['669'] != None:
        ls_669 = record.get_fields('669')
    
    # Loop through the 669 fields and grab
    for nalt in ls_669:
        # If last character is '.' remove it
        if nalt[-1] == '.':
            formatted_nalt = nalt[0:-1].strip()
        ls_subject_nalt.append(formatted_nalt)


    # Join together SUBJECT_NALT with double pipe (||)
    if len(ls_subject_nalt) > 0:
        dc_subject_nalt = '||'.join(ls_subject_nalt)

    return dc_subject_nalt



# MARC: 690
# REPEAT REPEAT
def get_dc_subject_lcsh(record):
    # Default variables
    dc_subject_lcsh = ''
    ls_690 = []
    ls_subject_lcsh = []

    # Check if there is 690 field in record, if so get all and put into list
    if record['690'] != None:
        ls_690 = record.get_fields('690')
    
    # Loop through the 690 fields and grab
    for lcsh in ls_690:
        # If last character is '.' remove it
        if lcsh[-1] == '.':
            formatted_lcsh = lcsh[0:-1].strip()
        ls_subject_lcsh.append(formatted_lcsh)


    # Join together SUBJECT_LCSH with double pipe (||)
    if len(ls_subject_lcsh) > 0:
        dc_subject_lcsh = '||'.join(ls_subject_lcsh)

    return dc_subject_lcsh



# MARC: 700$a
# REPEAT REPEAT
def get_contributor_committeemember(record):
    # Default variables
    dc_contributor_committeeMember = ''
    ls_700 = []
    ls_committee_member = []

    # Check if there is 700 field in record, if so get all and put into list
    if record['700'] != None:
        ls_700 = record.get_fields('700')
    
    # Loop through the 700 fields and grab names if RELATOR TERM ($e) has 'committee member'
    for person in ls_700:
        if 'committee member' in person['e'].lower():
            initial_name = person['a'].strip()

            # If last character is ',' remove it
            if initial_name[-1] == ',':
                formatted_name = initial_name[0:-1].strip()
            ls_committee_member.append(formatted_name)


    # Join together COMMITTEE_MEMBERS with double pipe (||) if there are multiple
    if len(ls_committee_member) > 0:
        dc_contributor_committeeMember = '||'.join(ls_committee_member)

    return dc_contributor_committeeMember


# TODO: "advisor" = "supervisor"?
# MARC: 712$a --> 700?
def get_contributor_advisor(record):
    # Default variables
    dc_contributor_advisor = ''
    ls_700 = []
    ls_advisor = []

    # Check if there is 700 field in record, if so get all and put into list
    if record['700'] != None:
        ls_700 = record.get_fields('700')
    
    # Loop through the 700 fields and grab names if RELATOR TERM ($e) has 'supervisor'
    for person in ls_700:
        if 'supervisor' in person['e'].lower():
            initial_name = person['a'].strip()

            # If last character is ',' remove it
            if initial_name[-1] == ',':
                formatted_name = initial_name[0:-1].strip()
            ls_advisor.append(formatted_name)


    # Join together SUPERVISOR(S) with double pipe (||) if there are multiple
    if len(ls_advisor) > 0:
        dc_contributor_advisor = '||'.join(ls_advisor)

    return dc_contributor_advisor




# TODO
# MARC: 856$u
def get_handle(record):
    # Default variables
    handle = ''
    ls_856 = []

    # Check if there is 856 field in record, if so get all and put into list
    if record['856'] != None:
        ls_856 = record.get_fields('856')
    
    # Loop through the 856 fields and grab url if HANDLE link
    for url in ls_856:
        if 'hdl.handle.net' in url['u']:
            handle = url['u'].strip()

    return handle







#################################################
def process_marc(extract_from=None):
    # Check if the path is surrounded by quotes (default in Windows "Copy Path" option)
    if extract_from:
        if extract_from[0]=='"' and extract_from[-1]=='"':
            # remove first and last quote
            extract_from = extract_from[1:-1]
        # Convert the string to a Path
        extract_from = Path(extract_from)

    # Open File
    with open(extract_from, 'rb') as mf:
        reader = pymarc.MARCReader(mf, to_unicode=True, force_utf8=True)
        
        # Loop through file
        for record in reader:
            extract_fields(record)

            print("Record Fields Extracted.\r\n")


# TODO
# Write contents to CSV file
def dictionary_to_csv(dict_data=None, provided_csv=None):
    if not provided_csv:
        csv_file = 'csv_export.csv'
    else:
        csv_file = provided_csv
    

    # TODO: Logic for checking an existing CSV file for:
    # 1) File already exists
    # 2) File has same headings, else create new one and change name


    if not os.path.isfile(csv_file):
        with open(csv_file, mode='w', encoding='utf-8', newline='') as csvfile:
            field_names = dict_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            # Write to csv file HEADERS
            writer.writeheader()

    with open(csv_file, mode='a', encoding='utf-8', newline='') as csvfile:
        field_names = dict_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writerow(dict_data)


        

# Get INPUT from user for {path to file}
input_file = input("Input the path and filename with extension to a Binary MARC file (*.bib, *.dat):")
# Run
process_marc(input_file)