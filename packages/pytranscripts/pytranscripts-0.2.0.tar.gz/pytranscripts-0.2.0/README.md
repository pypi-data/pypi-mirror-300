# pytranscripts
An Open source👨‍🔧 Python Library for Automated classification of Electronic Medical records 

## Installation
To install , simply use

```sh
pip install pytranscripts
```

## Pipeline Summary
![pipeline image](assets/edited_nlp_workflow.png)

### Stages
1. Data Extraction
2. Target Identification
3. Finetuning Annotated Data on Pretrained models (Bert & Electra)
4. Extracting Interviwer/Interviewee records from the specified docx file storage
5. Metrics Evaluation (Accuracy & Cohen Kappa Score)
6. Reordering records as a neatly arranged and flagged spreadsheet, alongside metrics and reports from pretrained models.

## Deps
- Python 3.12
- Transformers
- Pytorch

