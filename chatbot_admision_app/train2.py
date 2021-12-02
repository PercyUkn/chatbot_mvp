# Importar


def init_model():
    from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
    the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
    tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
    model = AutoModelForQuestionAnswering.from_pretrained(the_model)
    # Cargar conexto aquí
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return nlp;