# InvoiceParser
Using Azure Computer Vision API and pattern matching to extract text information from Images/PDFs

## Usage
Run the following commands in project directory:

### Building the Image:
`docker build -t invoice_parser:1.0 .`

### Running the application
`docker run -v <project-path-on-host>:/invoice-parser invoice_parser:1.0 -i <image_path_or_url_here>` 
