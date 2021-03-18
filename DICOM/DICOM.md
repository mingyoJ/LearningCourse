# DICOM
**D**igital **I**maging and **CO**mmunication in **M**edicine. ([Offical Document](http://dicom.nema.org/medical/dicom/current/output/chtml/))  
(Contents are from [wikipedia](https://en.wikipedia.org/wiki/DICOM))

## Overview
* Communication and management of medical imaging information and related data
* (Store / Exchange / Transmit) medical images
  * Enables the integration of medical imaging devices
  * ex) scanner, servers, workstations, printers, network HW, PACS(picture archiving and communication systems
* Standards for imaging modalities
  * ex) Radiography(방사선), Ultrasonography(초음파), CT, MRI, Radiation therapy(방사선 치료)
* Protocols
  * Image exchange
  * Image compression
  * 3D visualization
  * Image presentation
  * Results reporting
* Standard: file format, network communications protocol (TCP/IP based)
  * https://www.dicomstandard.org/current
  * http://dicom.nema.org/medical/dicom/current/output/chtml/

## Data Format
Groups information &rarr; Data sets (ex. X-ray image &larr; Patient ID, ...)

### DICOM Data Object
* Attributes (name, ID, ...)
* Special attributes (image pixel data)
* Single DICOM Object can have **only one** attribute containing pixel data
  * = single image (for many modalities)
* Attribute may contain multiple **frames**
* Three different encoding scheme (two Explicit, one Implicit)
  * Value Representation (VR) (OB, OW, OF, SQ, UT, UN not included)
    * See http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html for details
    * Each VR has a value multiplicity (indicate number of data elements in attribute)
    * For encoded multiple datas, data element are separated by `\`
  * GROUP (2 Bytes)
  * ELEMENT (2 Bytes)
  * VR (2 Bytes)
  * LengthInByte (2 Bytes)
    * For Implicit, not included.
  * Data (Variable)

## Image Display
GSDF(DICOM **G**rayscale **S**tandard **D**ata **E**lements)
* To see, need following:
  * lookup curve
  * device that calibrated to GSDF curve

## Services
Each services are described at each chapter of [document](http://dicom.nema.org/medical/dicom/current/output/chtml/)

### Store
Send image or other persistent objects to PACS(Picture Archiving and Communication System) / workstation

### Storage commitment
* Confirmation that an image has been permanently stored at device.
* SCU(Service Class User, Client) &lrarr; SCP (Service Class Provider)
  * SCU: modality, workstation
  * SCP: archive station

### Query / Retrieve

### Modality Worklist
* Provide list of imaging procedure (scheduled by image acquisition device ≈ modality system)
  * Subject of the procedure (ex. patient ID, name, sex, age, ...)
  * Type of procedure (Equipment type, procedure description, procedure code)
  * Procedure Order (Referring physician, Accession number, Reason for exam)

### Modality Performed Procedure Step (MPPS)
A complementary service to modality worklist
* Enables modality to send a report about performed examination with data
  * Image acquired
  * Beginning / end time
  * duration of study
  * dose delivered
  * ...
* Allows a modality to better coordinate with image storage servers
  * giving list of objects which is going to be sended

### Print
Normally print an "X-Ray" film.
* Has standard calibration (See [Part 14](http://dicom.nema.org/medical/dicom/current/output/chtml/part14/PS3.14.html))

### Offline Media
Format is specified in [Part 10](http://dicom.nema.org/medical/dicom/current/output/chtml/part10/PS3.10.html)
* Restricts the **filenames** on DICOM media to **8** characters
  * No information must be extracted from name
* Need media directory - DICOMDIR file
  * index and summary information for all the DICOM files on the media
* Uses `.dcm`. (But if part of a DICOM media, requires to be without extension)
* MIME type: `application/json`
* Uniform Type Identifier(UTI, used at Apple Inc.): `org.nema.dicom`

## Port numbers
* 104 (TCP/UDP)
* 2761 (ISCL over TCP/UDP)
* 2762 (TLS over TCP/UDP)
* 11112 (standard, open communication)
