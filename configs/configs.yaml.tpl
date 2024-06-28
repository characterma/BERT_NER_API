APP:
  ENVIRONMENT: development
  DEBUG: false
  ROOT_PATH: {{ .Values.appConfigs.swaggerRootPath }}

MODEL:
  MODEL_PATH: {{ .Values.model.model_path }}
  TOKENIZER_PATH: {{ .Values.model.tokenizer_path }}
  PRETRAINED_MODEL_PATH: {{ .Values.model.pretrained_model_path }}

KEYWORDS:
  KEYWORD_PATH: {{ .Values.keywords.keyword_path }}