import gc
gc.collect()

import time
import warnings
import sys
import numpy as np
import os
import ast

import onnxruntime as ort
from transformers import AutoTokenizer

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Ensure single-threaded execution
os.environ["OMP_NUM_THREADS"] = "1"

# Define the delimiter for splitting input lines
DELIMITER = '\t'


def load_tokenizer_from_folder(folder_name: str):
    """
    Load the tokenizer from the specified folder.

    Args:
        folder_name (str): The folder where the tokenizer is saved.

    Returns:
        tokenizer: The tokenizer loaded from the folder.
    """
    tokenizer = AutoTokenizer.from_pretrained(folder_name)
    return tokenizer


def mean_pooling(token_embeddings, attention_mask):
    """
    Perform mean pooling on token embeddings, taking the attention mask into account.
    Args:
        token_embeddings: The embeddings for each token in the sentence.
        attention_mask: The attention mask (to exclude padding tokens from pooling).
    Returns:
        sentence_embeddings: The pooled sentence embeddings.
    """
    # Expand attention mask dimensions for proper broadcasting (similar to unsqueeze in PyTorch)
    attention_mask = np.expand_dims(attention_mask, axis=-1).astype(np.float32)

    # Perform mean pooling (sum of token embeddings divided by the sum of attention mask)
    pooled_embeddings = np.sum(token_embeddings * attention_mask, axis=1) / np.clip(np.sum(attention_mask, axis=1), a_min=1e-9, a_max=None)
    return pooled_embeddings

# Get the zip file path from sys.argv
zip_file_path = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
text_column = int(sys.argv[2])  # Convert the first argument to an integer (text_column)
accumulate = ast.literal_eval(sys.argv[3])  # Convert the third argument (accumulate) from string to list

# Load the data and print the output on the fly
counter = 0
tokenizer = None  # Initialize as None to avoid errors if not instantiated
onnx_session = None  # Initialize as None to avoid errors if not instantiated

while True:
    try:
        # Read the input line
        line = input()
        if line == '':
            break  # End the loop if there's an empty input

        if counter == 0:
            # Create an ONNX Runtime session with memory optimization
            options = ort.SessionOptions()
            options.enable_mem_pattern = False  # Disable memory pattern optimization to save memory
            options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL  # Reduce memory usage during inference
            options.intra_op_num_threads = 1  # Limit parallelism to save memory
            options.inter_op_num_threads = 1
            providers = ['CPUExecutionProvider']

            # Create an InferenceSession with the model bytes
            with open(os.path.join(zip_file_path, "full_model.onnx"), "rb") as f:
                model_bytes = f.read()
            onnx_session = ort.InferenceSession(model_bytes, sess_options=options, providers=providers)

            # Load the tokenizer
            tokenizer = load_tokenizer_from_folder(zip_file_path)
            gc.collect()
            # Set counter to indicate that models are loaded
            counter = 1

        # Split input line using the defined delimiter
        input_data = line.split(DELIMITER)

        # Tokenize the line and return tensors in PyTorch format
        inputs = tokenizer([input_data[text_column]], return_tensors="np", padding='max_length', truncation=True,
                           max_length=512)

        # Prepare the inputs dictionary for ONNX Runtime with correct dimensions
        onnx_inputs = {
            "input_ids": inputs["input_ids"].astype('int64'),  # 2D tensor
            "attention_mask": inputs["attention_mask"].astype('int64')  # 2D tensor
        }

        # Check if token_type_ids exist and pass it if the model requires it
        #if "token_type_ids" in inputs:
        #    onnx_inputs["token_type_ids"] = inputs["token_type_ids"].astype('int64')

        # Run the ONNX model session
        outputs = onnx_session.run(None, onnx_inputs)

        # Extract embeddings (no averaging)
        embeddings = outputs[0]

        # Print the output embeddings along with input data
        for idx, item in enumerate(embeddings[0]):
            list_2_print = [input_data[1], str(idx), str(item), zip_file_path]
            list_2_print = [input_data[c] for c in accumulate] + list_2_print
            print(DELIMITER.join(list_2_print))

        # Clear memory by deleting large tensors and forcing garbage collection
        del inputs, outputs, embeddings
        gc.collect()

    except EOFError:
        # End of input handling
        gc.collect()
        break
