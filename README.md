[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
# InvoiceParser
Using Azure Computer Vision API and pattern matching to extract text information from Images/PDFs.

The plan is to eventually add templates that contain regex patterns for different document structures
, and allow the user to provide his own templates. 

## Prerequisites
- An Azure subscription: Create one [here](https://azure.microsoft.com/en-us/free/cognitive-services/) for free.
- Once you have your Azure subscription, create a Computer Vision resource in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision) to get your key and endpoint. After it deploys, click Go to resource.

    You will need the key and endpoint from the resource you create to connect your application to the Computer Vision service.
    You can use the free pricing tier (F0) to try the service.
- Paste your key and endpoint into a json file called `credentials.json` and place it in project directory.
  - Your file should like this:
    ```
    {
    "endpoint":"<endpoint_url_here>",
    "api_key":"<api_key_here>"
     }
    ```

## Usage
Run the following commands in project directory:

### 1.Building the Image:
`docker build -t invoice_parser:1.0 .`

### 2.Running the application
`docker run -v <project-path-on-host>:/invoice-parser invoice_parser:1.0 -i <image_path_or_url_here>` 

## Arguments:

#### Required:

`--image_path_or_url` or `-i`: specifies image local path (includes filename) or url

#### Optional:

`--credentials` or `-c`: specifies path to credentials (includes filename). default value is `credentials.json`

`--output_path` or `-o`: specifies data local output path. default value is `parsed_data.csv`

`--n_clusters` or `-n`: indicates number of clusters to use. You can disable clustering by using a value of `0`. default value is `3`


