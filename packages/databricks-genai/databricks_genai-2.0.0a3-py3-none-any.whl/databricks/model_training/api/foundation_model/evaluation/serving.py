""" Serving utilities """
from typing import Dict, Optional, Tuple

"""
Mapping from supported FT model name to the corresponding model path and version.
Models that are not supported by serving should be set to None.
Some base models are not enabled for serving. Those models are substituted with their instruct versions.
"""
FT_MODEL_PATH_MAPPING: Dict[str, Optional[Tuple[str, str]]] = {
    'databricks/dbrx-base': ('system.ai.dbrx_base', '2'),
    'databricks/dbrx-instruct': ('system.ai.dbrx_instruct', '3'),
    'meta-llama/Llama-3.2-1B': ('system.ai.llama_v3_2_1b_instruct', '2'),  # SUBSTITUTION
    'meta-llama/Llama-3.2-1B-Instruct': ('system.ai.llama_v3_2_1b_instruct', '4'),
    'meta-llama/Llama-3.2-3B': ('system.ai.llama_v3_2_3b_instruct', '2'),  # SUBSTITUTION
    'meta-llama/Llama-3.2-3B-Instruct': ('system.ai.llama_v3_2_3b_instruct', '4'),
    'meta-llama/Meta-Llama-3.1-405B': ('system.ai.meta_llama_v3_1_405b', '1'),
    'meta-llama/Meta-Llama-3.1-405B-Instruct': ('system.ai.meta_llama_v3_1_405b_instruct_fp8', '1'),
    'meta-llama/Meta-Llama-3.1-70B': ('system.ai.meta_llama_v3_1_70b_instruct', '2'),  # SUBSTITUTION
    'meta-llama/Meta-Llama-3.1-70B-Instruct': ('system.ai.meta_llama_v3_1_70b_instruct', '2'),
    'meta-llama/Meta-Llama-3.1-8B': ('system.ai.meta_llama_v3_1_8b_instruct', '2'),  # SUBSTITUTION
    'meta-llama/Meta-Llama-3.1-8B-Instruct': ('system.ai.meta_llama_v3_1_8b_instruct', '4'),
    'meta-llama/Meta-Llama-3-70B': ('system.ai.meta_llama_3_70b', '1'),
    'meta-llama/Meta-Llama-3-70B-Instruct': ('system.ai.meta_llama_3_70b_instruct', '2'),
    'meta-llama/Meta-Llama-3-8B': ('system.ai.meta_llama_3_8b', '1'),
    'meta-llama/Meta-Llama-3-8B-Instruct': ('system.ai.meta_llama_3_8b_instruct', '1'),
    'meta-llama/Llama-2-7b-hf': None,
    'meta-llama/Llama-2-13b-hf': None,
    'meta-llama/Llama-2-70b-hf': None,
    'meta-llama/Llama-2-7b-chat-hf': None,
    'meta-llama/Llama-2-13b-chat-hf': None,
    'meta-llama/Llama-2-70b-chat-hf': None,
    'codellama/CodeLlama-7b-hf': None,
    'codellama/CodeLlama-13b-hf': None,
    'codellama/CodeLlama-34b-hf': None,
    'codellama/CodeLlama-7b-Instruct-hf': None,
    'codellama/CodeLlama-13b-Instruct-hf': None,
    'codellama/CodeLlama-34b-Instruct-hf': None,
    'codellama/CodeLlama-7b-Python-hf': None,
    'codellama/CodeLlama-13b-Python-hf': None,
    'codellama/CodeLlama-34b-Python-hf': None,
    'mistralai/Mistral-7B-v0.1': ('system.ai.mistral_7b_v0_1', '2'),
    'mistralai/Mistral-7B-Instruct-v0.2': ('system.ai.mistral_7b_instruct_v0_2', '2'),
    'mistralai/Mixtral-8x7B-v0.1': ('system.ai.mixtral_8x7b_v0_1', '2'),
}


def get_base_model_details(model_name: str) -> Tuple[str, str]:
    """
    Get the model path for the given model name

    Args:
        model_name (str): The FT base model name

    Returns:
        Tuple[str, str]: The model path and version
    """
    model_details = FT_MODEL_PATH_MAPPING.get(model_name)
    if model_details is None:
        raise ValueError(f"Model '{model_name}' is not supported.")
    return model_details
