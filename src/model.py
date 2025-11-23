from transformers import AutoModelForTokenClassification
from labels import LABEL2ID, ID2LABEL
import torch


def create_model(model_name: str):
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(LABEL2ID),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )
    '''
    if hasattr(model, "distilbert"):  # Ensure it's a DistilBERT architecture
        model.distilbert.transformer.layer[0].attention.prune_heads({2, 5})
        model.distilbert.transformer.layer[3].attention.prune_heads({1, 4})
    '''
    
    return model
