import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode


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
    # dissertation_fields['dc.contributor.advisor'] = get_filename(record)
    # dissertation_fields['thesis.degree.discipline'] = get_filename(record)
    # dissertation_fields['handle'] = get_filename(record)

    # Write Record to CSV
    # TODO
    
    return dissertation_fields

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


# TODO
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


# TODO
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


# MARC: 502$b
# Will be either Doctoral or Masters
def get_thesis_degree_level(record):
    thesis_degree_level = ''

    # Get DEGREE LEVEL
    if record['502'] != None:
        field_502a = record['502']['b']

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

        # "{type part} in {department}" -- grabs the {department} to end
        thesis_degree_discipline = field_502a[field_502a.find(" in ")+4:]
    

    print("thesis_degree_discipline: {degree_discipline}".format(degree_discipline=thesis_degree_discipline))

    return thesis_degree_discipline


# TODO
# MARC: 667
# REPEAT REPEAT
def get_dc_subject(record):
    dc_subject = ''

    # Get SUBJECT
    if record['667'] != None:
        dc_subject = record['667']
    

    print("dc_subject: {subject}".format(subject=dc_subject))

    return dc_subject


# TODO
# MARC: 668
# REPEAT REPEAT
def get_dc_subject_mesh(record):
    dc_subject_mesh = ''

    # Get SUBJECT MESH
    if record['668'] != None:
        dc_subject_mesh = record['668']
    

    print("dc_subject_mesh: {subject_mesh}".format(subject_mesh=dc_subject_mesh))

    return dc_subject_mesh


# TODO
# MARC: 669
# REPEAT REPEAT
def get_dc_subject_nalt(record):
    dc_subject_nalt = ''

    # Get SUBJECT NALT
    if record['669'] != None:
        dc_subject_nalt = record['669']
    

    print("dc_subject_nalt: {subject_nalt}".format(subject_nalt=dc_subject_nalt))

    return dc_subject_nalt


# TODO
# MARC: 690
# REPEAT REPEAT
def get_dc_subject_lcsh(record):
    dc_subject_lcsh = ''

    # Get SUBJECT LCSH
    if record['690'] != None:
        dc_subject_lcsh = record['690']
    

    print("dc_subject_lcsh: {subject_lcsh}".format(subject_lcsh=dc_subject_lcsh))

    return dc_subject_lcsh


# TODO
# MARC: 700$a
# REPEAT REPEAT
def get_contributor_committeemember(record):
    dc_contributor_committeeMember = ''

    # Get SUBJECT MESH
    if record['700'] != None:
        record.get_fields()
        dc_contributor_committeeMember = record['700']['a']
    

    print("dc_contributor_committeeMember: {contributor_committeeMember}".format(contributor_committeeMember=dc_contributor_committeeMember))

    return dc_contributor_committeeMember


# TODO
# MARC: 712$a
# def get_contributor_advisor(record):

# TODO
# MARC: 667$a
# def get_thesis_degree_discipline(record):

# TODO
# MARC: 856$u
# def get_handle(record):







#################################################
def process_marc(extract_from=None):
    if extract_from:
        print("passed")

    # Open File
    with open(extract_from, 'rb') as mf:
        reader = pymarc.MARCReader(mf, to_unicode=True, force_utf8=True)
        
        # Loop through file
        for record in reader:
            record_fields = extract_fields(record)

            print("Record Fields Extracted.\r\n")




process_marc("C:/temp/Python -- MARC to CSV/resource files/records--VoyagerSU_utf8--20test.bib")
