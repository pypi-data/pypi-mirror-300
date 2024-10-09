Bio-Wrangler
Bio-Wrangler is a Python package designed to streamline the process of loading, transforming, filtering, and merging bioinformatics datasets. It supports popular bioinformatics formats such as FASTA, FASTQ, VCF, and GFF, and provides tools to manipulate, filter, and merge these datasets for bioinformatics analysis.

Features
Load bioinformatics datasets from FASTA, FASTQ, VCF, and GFF formats into pandas DataFrames for easy manipulation.
Filter data by quality, chromosome, position, or specific attributes.
Summarize key statistics from FASTA, FASTQ, VCF, and GFF files, such as sequence count and quality scores.
Merge multiple datasets into a single DataFrame.
Save processed data to CSV or Excel formats.
Handle large datasets efficiently with helper utilities for common operations.

Installation
To install Bio-Wrangler, clone the repository and install the package using pip:

git clone https://github.com/se7en69/bio-wrangler.git
cd bio-wrangler
pip install -e .
The -e flag installs the package in "editable" mode, which means any changes made to the source code will be reflected immediately without needing to reinstall.

Version
Current version: 0.7
Author: Abdul Rehman Ikram

Usage
Here’s how you can use the BioWrangler package to load, filter, and merge bioinformatics datasets.

1. Loading Data
You can load data from FASTA, FASTQ, VCF, or GFF formats into pandas DataFrames.

Example: Loading FASTA, FASTQ, VCF, and GFF Files
from bio_wrangler.bio_wrangler import BioWrangler

# Initialize the BioWrangler class
wrangler = BioWrangler()

# Load data from different formats
fasta_data = wrangler.load_fasta('path/to/sample.fasta')
fastq_data = wrangler.load_fastq('path/to/sample.fastq')
vcf_data = wrangler.load_vcf('path/to/sample.vcf')
gff_data = wrangler.load_gff('path/to/sample.gff')

# Display the first few rows of the datasets
print(fasta_data.head())
print(fastq_data.head())
print(vcf_data.head())
print(gff_data.head())

2. Filtering Data
You can filter the data by quality, chromosome, position, or specific attributes.
Example: Filtering FASTQ by Quality
filtered_fastq = wrangler.filter_fastq_by_quality(fastq_data, 30.0)
print(filtered_fastq.head())  # Display FASTQ sequences with avg quality >= 30

Example: Filtering VCF by Chromosome and Position Range
filtered_vcf_by_chr = wrangler.filter_by_chromosome(vcf_data, 'chr1')
filtered_vcf_by_pos = wrangler.filter_by_position_range(vcf_data, 100000, 500000)

print(filtered_vcf_by_chr.head())
print(filtered_vcf_by_pos.head())

Example: Filtering GFF by Attribute
filtered_gff = wrangler.filter_by_attribute(gff_data, 'ID', 'gene1')
print(filtered_gff.head())  # Filter by gene ID

3. Summarizing Data
Generate a summary of the dataset, including total rows, average quality, and positional statistics.

Example: Summarizing FASTQ and VCF Data
fastq_summary = wrangler.summarize_fastq(fastq_data)
vcf_summary = wrangler.summarize_data(vcf_data)

print(fastq_summary)
print(vcf_summary)

4. Merging Datasets
Merge multiple datasets (e.g., two VCF datasets) into one for combined analysis.

Example: Merging VCF Datasets

merged_vcf = wrangler.merge_datasets(vcf_data, filtered_vcf_by_chr)
print(merged_vcf.head())  # Combined dataset

5. Saving Data
Save your processed data to a file (CSV or Excel).

Example: Saving Filtered VCF Data to a CSV File

wrangler.save_data(filtered_vcf_by_chr, 'filtered_vcf_output.csv', 'csv')

Utility Functions
In addition to the core methods, BioWrangler also provides utility functions for common operations like filtering and quality score calculations. These utilities can be imported from bio_wrangler.utils.
Example: Using Utility Functions
from bio_wrangler.utils import calculate_average_quality, filter_data_by_quality

# Calculate the average quality of a FASTQ sequence
avg_quality = calculate_average_quality([30, 31, 32, 28, 29])
print(avg_quality)

# Filter data by quality
filtered_data = filter_data_by_quality(fastq_data, 'avg_quality', 30.0)
print(filtered_data.head())

Testing
Bio-Wrangler comes with a suite of tests to ensure the correctness of the package. To run the tests, use:
python -m pytest
Make sure that you are in the project root directory when running the tests.

Running the Test Suite
Navigate to the project directory.
Ensure you have the required sample data files (sample.fasta, sample.fastq, sample.vcf, sample.gff) in the tests/data/ folder.

Run the tests using pytest:
python -m pytest

The test suite covers the following functionalities:
Loading and validating FASTA, FASTQ, VCF, and GFF files.
Filtering data by quality, chromosome, position, and attributes.
Summarizing datasets.
Merging datasets.
Saving processed data.

Directory Structure
bio-wrangler/
│
├── bio_wrangler/                  # Package source
│   ├── __init__.py
│   ├── bio_wrangler.py            # Core BioWrangler class
│   └── utils.py                   # Utility functions
│
├── tests/                         # Test suite
│   ├── data/                      # Sample data for testing
│   │   ├── sample.fasta
│   │   ├── sample.fastq
│   │   ├── sample.vcf
│   │   └── sample.gff
│   ├── __init__.py
│   ├── test_bio_wrangler.py        # Main tests for BioWrangler
│   └── test_utils.py               # Tests for utility functions
│
├── README.md                      # Documentation
├── setup.py                       # Installation and package configuration
└── requirements.txt               # Package dependencies

Contributing
Contributions are welcome! To contribute:
Fork the repository.
Create a new branch: git checkout -b feature-branch.
Make your changes.
Commit your changes: git commit -m 'Add some feature'.
Push to the branch: git push origin feature-branch.
Submit a pull request.
Please ensure your code is well-documented and thoroughly tested.

License
Bio-Wrangler is licensed under the MIT License. See the LICENSE file for more details.