# Fields list

_Introduced in InvenioRDM v12_

The following document is a reference guide for all the custom fields available in InvenioRDM.

!!!tip "How to add a field to an instance?"
    If you want to add a field to an instance, please refer to the custom fields [documentation](../../customize/metadata/custom_fields/records.md#add-reusable-custom-fields-to-records).

## Publishing information

This group of fields contains the metadata for "Journal", "Imprint" and "Thesis". Each field has its own data representation, however, they are grouped in the UI.

**Deposit form** 

![Deposit form](../../images/pub_info_deposit_form.png)

**Landing page**

![Landing page](../../images/pub_info_landing_page.png)

Publishing information is displayed in the section "Details", on the right side bar, under "Published in".

### Journal

This field implements a journal's metadata. It can be used to describe a journal where an article was published.

**Metadata**

- **title** `String`: The title of the journal.
- **volume** `String`: The volume where the article was published.
- **issue** `String`: The issue within the volume.
- **pages** `String`: The pages within the issue where the article was published. It can be a number or a range in any format.

### Imprint

This nested field implements an imprint's metadata. It can be used to describe a book, report or chapter where a record was published.

**Metadata**

- **title** `String`: The title of the book or report where the record was published.
- **isbn** `String`: The book's International Standard Book Number. Applies if the imprint is a book.
- **place** `String`: Location where the book (or report) was published.
- **pages** `String`: The pages within the book or report. It can be a number or a range in any format.

### Thesis

This field implements thesis metadata, more specifically an awarding university. A thesis supervisor can be found in the list of contributors whose role is "Supervisor".

**Metadata**

- **university**: Name of the awarding university.

## Meeting

This field can be used to describe a meeting, e.g. a conference.

**Deposit form**

![Meeting deposit form](../../images/meeting_deposit_form.png)

**Landing page**

![Meeting landing page](../../images/meeting_landing_page.png)

Meeting information is displayed in the section "Details", under "Conference".

**Metadata**

- **title** `String`: Meeting or conference title.
- **acronym** `String`: Acronym that represents the conference.
- **dates** `String`: Dates when the meeting took place.
- **place** `String`: Location where the meeting took place.
- **session** `String`: Session within the meeting or conference.
- **session_part** `String`: Part within the session.
- **url** `String`: Link of the conference website.

## Software

This group of fields contains metadata to describe a software record.

**Deposit form**

![Codemeta deposit form](../../images/codemeta_deposit_form.png)

**Landing page**

![Codemeta landing page](../../images/codemeta_landing_page.png)

Software information is displayed in the section "Additional details", under the tab "Software".

**Metadata**

- **codeRepository** `String`: Link to the repository where the related code is located (e.g. Github).
- **programmingLanguage** `String`: Name of the programming language used to develop the software.
- **runtimePlatform** `String`: Runtime platform dependencies (e.g. Python3.8).
- **operatingSystem** `String`: Supported operating systems.
- **developmentStatus** `String`: Description of the development status (e.g. "Active"). Uses a controlled vocabulary defined in [repostatus](http://www.repostatus.org/).
