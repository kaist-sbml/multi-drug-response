# Prediction of Physiological Effects of Multiple Drugs using Electronic Health Record

![Figure_Github](https://github.com/user-attachments/assets/c6e00653-7b68-4e52-8de5-a15d8e18e5cd)

This project predicts which measurements will show abnormal labels for patients who have taken certain drugs within the last 24 hours. The model is trained on the MIMIC-IV clinical database and validated on the eICU collaborative research database.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

## Introduction

This project provides a model that predicts abnormal measurements based on patient information and prescribed drugs. The prediction results are stored in the `predictions.txt` file by default.

## Features

- Predict abnormal labels based on patient information and prescribed drugs.
- Support for three different feature types (i.e., active ingredients, molecular fingerprints, and drug-target protein interactions).
- Save prediction results to a text file.

## Installation

To install and set up the project, follow these steps.

### Requirements

- Conda

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/kaist-sbml/multi-drug-response.git
    ```

2. Install the required packages:
    ```bash
    cd multi-drug-response
    conda env create -f environment.yml
    conda activate your_environment_name
    ```

## Usage

Here is a simple example of how to use the project.

### Example

1. Run `run_model.py`:
    ```bash
    python run_model.py -i ./data/input_sample.txt -o ./results -f API -m all
    ```

    - `-i`: Path to the input file (e.g., `./data/input_sample.txt`)
    - `-o`: Output directory (e.g., `./results`)
    - `-f`: Feature type (one of API (recommended), MF, DTI)
    - `-m`: Measurement item (item ID or 'all')

2. You can find the measurement item IDs in `./data/item_list.tsv`.

3. The prediction results will be saved in the `predictions.txt` file. Example:
    ```plaintext
    This patient is predicted to be at risk of:
    	increased creatinine level in blood
    	decreased red blood cells level in blood
    ```

## Notes

Note that the probability of abnormal labels is higher compared to general patients.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

If you have any questions about the project, please contact:

- Name: Hyun Uk Kim
- Email: ehukim(at)kaist.ac.kr
