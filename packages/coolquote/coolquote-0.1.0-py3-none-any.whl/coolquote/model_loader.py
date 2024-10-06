from transformers import GPT2LMHeadModel, GPT2Tokenizer


def load_model():
    # Hugging Face'den distilgpt2 modelini ve tokenizer'ı yükler
    model_name = "distilgpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    return model, tokenizer
