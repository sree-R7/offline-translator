An offline translation app that uses ONNX Runtime for English-Spanish bidirectional translation with a user-friendly GUI.

Models Used: Helsinki-NLP/opus-mt-en-es and Helsinki-NLP/opus-mt-es-en

The App uses Pre-trained Helsinki-NLP Opus-MT models that have been converted to ONNX format for efficient CPU/NPU inference. The GUI is built with Tkinter, making it lightweight and cross-platform compatible.

The translation doesn't happen all at once. Instead, the model generates one word (token) at a time using previously generated words as context. It uses Greedy search, which always picks the most likely next token. 
