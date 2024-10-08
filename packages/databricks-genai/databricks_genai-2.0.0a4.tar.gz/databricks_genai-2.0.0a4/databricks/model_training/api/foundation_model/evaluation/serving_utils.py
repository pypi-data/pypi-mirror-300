""" Serving utilities """
from dataclasses import dataclass
from typing import Dict, Optional

from databricks.model_training.types.train_config import TrainTaskType


@dataclass
class BaseModelDetails:
    system_ai_path: str
    version: str
    task_type: TrainTaskType


# Mapping from supported FT model name to the corresponding model path and version.
# Models that are not supported by serving should be set to None.
# SUBSTITUTION: Some base models are not enabled for serving. Those models are substituted with their instruct versions.
FT_MODEL_PATH_MAPPING: Dict[str, Optional[BaseModelDetails]] = {
    'databricks/dbrx-base':
        BaseModelDetails('system.ai.dbrx_base', '2', TrainTaskType.INSTRUCTION_FINETUNE),
    'databricks/dbrx-instruct':
        BaseModelDetails('system.ai.dbrx_instruct', '3', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Llama-3.2-1B':
        BaseModelDetails('system.ai.llama_v3_2_1b_instruct', '4', TrainTaskType.CHAT_COMPLETION),  # SUBSTITUTION
    'meta-llama/Llama-3.2-1B-Instruct':
        BaseModelDetails('system.ai.llama_v3_2_1b_instruct', '4', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Llama-3.2-3B':
        BaseModelDetails('system.ai.llama_v3_2_3b_instruct', '4', TrainTaskType.CHAT_COMPLETION),  # SUBSTITUTION
    'meta-llama/Llama-3.2-3B-Instruct':
        BaseModelDetails('system.ai.llama_v3_2_3b_instruct', '4', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Meta-Llama-3.1-405B':
        BaseModelDetails('system.ai.meta_llama_v3_1_405b', '1', TrainTaskType.INSTRUCTION_FINETUNE),
    'meta-llama/Meta-Llama-3.1-405B-Instruct':
        BaseModelDetails('system.ai.meta_llama_v3_1_405b_instruct_fp8', '1', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Meta-Llama-3.1-70B':
        BaseModelDetails('system.ai.meta_llama_v3_1_70b_instruct', '2', TrainTaskType.CHAT_COMPLETION),  # SUBSTITUTION
    'meta-llama/Meta-Llama-3.1-70B-Instruct':
        BaseModelDetails('system.ai.meta_llama_v3_1_70b_instruct', '2', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Meta-Llama-3.1-8B':
        BaseModelDetails('system.ai.meta_llama_v3_1_8b_instruct', '4', TrainTaskType.CHAT_COMPLETION),  # SUBSTITUTION
    'meta-llama/Meta-Llama-3.1-8B-Instruct':
        BaseModelDetails('system.ai.meta_llama_v3_1_8b_instruct', '4', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Meta-Llama-3-70B':
        BaseModelDetails('system.ai.meta_llama_3_70b', '1', TrainTaskType.INSTRUCTION_FINETUNE),
    'meta-llama/Meta-Llama-3-70B-Instruct':
        BaseModelDetails('system.ai.meta_llama_3_70b_instruct', '2', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Meta-Llama-3-8B':
        BaseModelDetails('system.ai.meta_llama_3_8b', '1', TrainTaskType.INSTRUCTION_FINETUNE),
    'meta-llama/Meta-Llama-3-8B-Instruct':
        BaseModelDetails('system.ai.meta_llama_3_8b_instruct', '1', TrainTaskType.CHAT_COMPLETION),
    'meta-llama/Llama-2-7b-hf':
        None,
    'meta-llama/Llama-2-13b-hf':
        None,
    'meta-llama/Llama-2-70b-hf':
        None,
    'meta-llama/Llama-2-7b-chat-hf':
        None,
    'meta-llama/Llama-2-13b-chat-hf':
        None,
    'meta-llama/Llama-2-70b-chat-hf':
        None,
    'codellama/CodeLlama-7b-hf':
        None,
    'codellama/CodeLlama-13b-hf':
        None,
    'codellama/CodeLlama-34b-hf':
        None,
    'codellama/CodeLlama-7b-Instruct-hf':
        None,
    'codellama/CodeLlama-13b-Instruct-hf':
        None,
    'codellama/CodeLlama-34b-Instruct-hf':
        None,
    'codellama/CodeLlama-7b-Python-hf':
        None,
    'codellama/CodeLlama-13b-Python-hf':
        None,
    'codellama/CodeLlama-34b-Python-hf':
        None,
    'mistralai/Mistral-7B-v0.1':
        BaseModelDetails('system.ai.mistral_7b_v0_1', '2', TrainTaskType.INSTRUCTION_FINETUNE),
    'mistralai/Mistral-7B-Instruct-v0.2':
        BaseModelDetails('system.ai.mistral_7b_instruct_v0_2', '2', TrainTaskType.CHAT_COMPLETION),
    'mistralai/Mixtral-8x7B-v0.1':
        BaseModelDetails('system.ai.mixtral_8x7b_v0_1', '2', TrainTaskType.INSTRUCTION_FINETUNE),
}


def get_base_model_details(model_name: str) -> BaseModelDetails:
    """
    Get the model path for the given model name

    Args:
        model_name (str): The FT base model name

    Returns:
        BaseModelDetails: model path, version, and task type
    """
    model_details = FT_MODEL_PATH_MAPPING.get(model_name)
    if model_details is None:
        raise ValueError(f"Model '{model_name}' is not supported.")
    return model_details
