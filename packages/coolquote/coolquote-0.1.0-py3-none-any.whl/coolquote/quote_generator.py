from .model_loader import load_model

# Modeli yükle
model, tokenizer = load_model()

def generate_text(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=50, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_quote(category):
    if category == 'motivation':
        prompt = "Give me a motivational quote."
    elif category == 'love':
        prompt = "Give me a love-related quote."
    elif category == 'wisdom':
        prompt = "Share some wisdom."
    else:
        prompt = "Tell me something cool."

    return generate_text(prompt, model, tokenizer)
