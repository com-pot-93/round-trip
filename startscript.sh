#!/bin/bash
python genai_gpt_pipeline.py --model-path ./data/domain/ground_json/ --text-path ./data/domain/process_descriptions/ --example domain --direction t2t
python genai_gemini_pipeline.py --model-path ./data/domain/ground_json/ --text-path ./data/domain/process_descriptions/ --example domain --direction m2m
python genai_gemini_pipeline.py --model-path ./data/domain/ground_json/ --text-path ./data/domain/process_descriptions/ --example domain --direction t2t
exec bash
