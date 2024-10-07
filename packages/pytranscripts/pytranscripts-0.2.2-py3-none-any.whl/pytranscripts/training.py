import os
import pandas as pd
import numpy as np
import torch
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, 
                          TrainingArguments, Trainer, DataCollatorWithPadding, 
                          pipeline)
from sklearn.model_selection import train_test_split
from datasets import Dataset
from typing import Any
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class NLPModelTrainer:
    def __init__(self, base_path,  refined_data_path, survey_data_path):
        print(f"{Fore.BLUE}Initializing NLPModelTrainer...")
        self.base_path = base_path
        self.refined_data_path = refined_data_path
        self.survey_data_path = survey_data_path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.class_mapping = {}
        self.train_dataset = None
        self.eval_dataset = None
        self.label2id = None
        self.id2label = None
        self.models = {}
        self.model_name_map = {
            'bert': "./bert_interview_new",
            'electra': "./electra_interview_new"
        }

        # Automatically load and clean data during initialization
        self.load_and_clean_data()

    def load_and_clean_data(self):
        print(f"{Fore.YELLOW}Loading and cleaning data...")
        # Load and clean the dataset
        df = pd.read_excel(self.refined_data_path)
        df = df.drop_duplicates(subset=['Quotation Content'])

        # Assign numerical labels
        self.class_mapping = {sheet_name: i for i, sheet_name in enumerate(df['SheetName'].unique())}
        df['target'] = df['SheetName'].map(self.class_mapping)
        
        expanded_df = []
        for _, row in df.iterrows():
            responses = self.get_interviewee_responses(row['Quotation Content'])
            for res in responses:
                row_copy = row.copy()
                row_copy['Quotation Content'] = res
                expanded_df.append(row_copy)
        self.expanded_df = pd.DataFrame(expanded_df)
        
        # Split into train and eval datasets
        train_data, eval_data = train_test_split(self.expanded_df, test_size=0.2, random_state=42, stratify=self.expanded_df.SheetName)

        labels = list(self.class_mapping.keys())
        self.label2id = {label: idx for idx, label in enumerate(labels)}
        self.id2label = {idx: label for label, idx in self.label2id.items()}

        self.train_dataset = Dataset.from_dict({
            'text': train_data['Quotation Content'].values,
            'label': [labels.index(label) for label in train_data.SheetName]
        })

        self.eval_dataset = Dataset.from_dict({
            'text': eval_data['Quotation Content'].values,
            'label': [labels.index(label) for label in eval_data.SheetName]
        })

        print(f"{Fore.GREEN}Data loaded and cleaned successfully.")

    def get_interviewee_responses(self, input_text):
        # Extracts the interviewee's responses from the text
        parts = input_text.split('Interviewer:')
        interviewee_segments = []
        for part in parts:
            interviewee_part = part.split('Interviewee:')
            if len(interviewee_part) > 1:
                interviewee_segments.append(interviewee_part[1].strip())
        return [i for i in interviewee_segments if len(i) > 30]

    def train_models(self, bert=True, electra=True):
        # Train BERT model if specified
        if bert:
            print(f"{Fore.YELLOW}Training BERT model...")
            self.train_model("distilbert-base-uncased", self.model_name_map['bert'])
            print(f"{Fore.GREEN}BERT model training completed.")
        
        # Train Electra model if specified
        if electra:
            print(f"{Fore.YELLOW}Training Electra model...")
            self.train_model("mrm8488/electra-small-finetuned-squadv2", self.model_name_map['electra'])
            print(f"{Fore.GREEN}Electra model training completed.")

    def train_model(self, model_name, hub_model_id):
        # Tokenizer and Model
        print(f"{Fore.YELLOW}Loading model and tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, max_length=512)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, id2label=self.id2label, label2id=self.label2id).to(self.device)
        print(f"{Fore.GREEN}Model and tokenizer loaded successfully.")

        # Preprocess function
        def preprocess_function(examples):
            return tokenizer(examples["text"], truncation=True, max_length=512)

        train_dataset = self.train_dataset.map(preprocess_function)
        eval_dataset = self.eval_dataset.map(preprocess_function)
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

        # Training arguments
        training_args = TrainingArguments(
            output_dir=hub_model_id,
            learning_rate=2e-5,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            num_train_epochs=10,
            weight_decay=0.01,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            push_to_hub=True,
            hub_model_id=hub_model_id,
            hub_strategy="end",
        )

        print(f"{Fore.YELLOW}Starting training for model: {hub_model_id}...")
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
        )
        
        trainer.train()
        print(f"{Fore.GREEN}Training completed for model: {hub_model_id}. Pushing to hub...")
        trainer.push_to_hub(hub_model_id)
        print(f"{Fore.GREEN}Model {hub_model_id} pushed to hub successfully.")
        
        # Save the model and tokenizer for later use
        self.models[hub_model_id] = pipeline('text-classification', model=hub_model_id, device=self.device)
        print(f"{Fore.GREEN}Pipeline for model {hub_model_id} loaded successfully.")

    def compute_metrics(self, eval_pred):
        # Computes accuracy of the model during training
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        from evaluate import load
        accuracy = load("accuracy")
        return accuracy.compute(predictions=predictions, references=labels)

    def classify_text(self, text, model_type):
        # Classify the given text using the specified model type (bert or electra)
        if model_type not in self.model_name_map:
            raise ValueError(f"{Fore.RED}Invalid model type specified. Choose either 'bert' or 'electra'.")
        
        model_name = self.model_name_map[model_type]
        
        if model_name not in self.models:
            # Load the model if not already loaded
            print(f"{Fore.YELLOW}Loading model pipeline for {model_type}...")
            self.models[model_name] = pipeline('text-classification', model=model_name, device=self.device)
            print(f"{Fore.GREEN}Model pipeline for {model_type} loaded successfully.")

        model = self.models[model_name]
        print(f"{Fore.YELLOW}Classifying text using the {model_type} model...")
        result = model(text)
        print(f"{Fore.GREEN}Classification completed.")
        return result

    def generate_encoded_evaluation_files(self):
        print(f"{Fore.YELLOW}Generating encoded evaluation files...")

        # Load the survey data for evaluation
        survey_df = pd.read_excel(self.survey_data_path)

        # Generate human labels
        eval_df = self.expanded_df[['Quotation Content', 'SheetName']]
        eval_df = eval_df.rename(columns={"Quotation Content": 'Interviewee'})

        human_df = self.label_survey_data(survey_df.copy(), eval_df)
        human_encoded = self.encode_labels(human_df, "human")
        human_encoded.to_excel(f"{self.base_path}/human_encoded.xlsx", index=False)
        print(f"{Fore.GREEN}Human evaluation file generated successfully.")

        # Generate BERT predictions
        bert_df = survey_df.copy()
        bert_df['label'] = bert_df.apply(lambda row: self.classify_text(row['Interviewee'], "bert")[0]['label'], axis=1)
        bert_encoded = self.encode_labels(bert_df, "bert")
        bert_encoded.to_excel(f"{self.base_path}/bert_encoded.xlsx", index=False)
        print(f"{Fore.GREEN}BERT evaluation file generated successfully.")

        # Generate Electra predictions
        electra_df = survey_df.copy()
        electra_df['label'] = electra_df.apply(lambda row: self.classify_text(row['Interviewee'], "electra")[0]['label'], axis=1)
        electra_encoded = self.encode_labels(electra_df, "electra")
        electra_encoded.to_excel(f"{self.base_path}/electra_encoded.xlsx", index=False)
        print(f"{Fore.GREEN}Electra evaluation file generated successfully.")

    def label_survey_data(self, survey_df, eval_df):
        # Labels the survey data based on the corresponding label in the eval_df
        survey_df['label'] = ""
        for index, row in survey_df.iterrows():
            interviewee = row['Interviewee']
            matching_rows = eval_df[eval_df['Interviewee'] == interviewee]
            if not matching_rows.empty:
                survey_df.loc[index, 'label'] = matching_rows.iloc[0]['SheetName']
            else:
                survey_df.loc[index, 'label'] = "Not Found"
        return survey_df

    def encode_labels(self, df, source):
        # Get unique labels and encode them as columns
        unique_labels = self.expanded_df['SheetName'].unique()
        for label in unique_labels:
            df[label] = 0
        # Set the corresponding column to 1 based on the 'label' value
        for index, row in df.iterrows():
            label = row['label']
            if label in unique_labels:
                df.at[index, label] = 1
        # Drop the original 'label' column if not needed
        df = df.drop(columns=["label"])
        return df

# Usage Example
if __name__ == "__main__":
    trainer = NLPModelTrainer(
        base_path = '/content/drive/',
        refined_data_path="/content/drive/MyDrive/Kalu+Deola/NLP NEW/Refined_targets.xlsx",
        survey_data_path="/content/drive/MyDrive/Kalu+Deola/NLP NEW/SURVEY_TABLE.xlsx"
    )
    
    trainer.train_models(bert=True, electra=True)

    # Classify a new piece of text using the BERT model
    result = trainer.classify_text("I don't see an algorithmic approach that would be useful...", "bert")
    print(result)
    # Generate encoded evaluation files for Human, BERT, and Electra
    trainer.generate_encoded_evaluation_files()
