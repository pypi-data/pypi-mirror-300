import os
import subprocess

REPO_CONFIGS_AND_INFO_FOLDER_PATH = "/models_configs"


def run(python_path, model_family_info_path, model_info_path, config_path):
    """
    Run a specified Python script with the given model family and model info paths.

    Parameters:
    - python_path (str): Path to the Python script to be executed (train.py, eval.py, deploy.py, or export.py).
    - model_family_info_path (str): Path to the JSON file containing model family information.
    - model_info_path (str): Path to the JSON file containing model-specific information.
    - config_path (str): Path to the configuration file (could be for training, evaluation, deployment, or export).

    Example:
        run("train.py", "family_info.json", "model_A_info.json", "train-config.json")

    Raises:
    - Exception: If there is an error during the subprocess call.
    """

    if "deploy" not in python_path:
        command = [
            "python",
            python_path,
            "Testing",
            model_family_info_path,
            model_info_path,
            config_path,
        ]
    else:
        local_port = 8000
        command = [
            "python",
            python_path,
            "Testing",
            local_port,
            model_family_info_path,
            model_info_path,
            config_path,
        ]
    try:
        subprocess.run(command)
    except Exception as e:
        print(f"Error in with {command}. Error is: {e}")


def main(repo_configs_and_info_folder_path):
    """
    Main function that reads model configuration files and executes the appropriate training, evaluation, deployment,
    and export scripts.

    Parameters:
    - repo_configs_and_info_folder_path (str): Path to the directory containing model family, model info, and
      configuration JSON files.

    Steps:
    - Looks for family_info.json, train-config.json, and any other export configurations.
    - For each model info file, it calls the `run` function to:
        1. Train the model using `train.py`.
        2. Evaluate the model using `eval.py`.
        3. Deploy the model using `deploy.py`.
        4. Export the model using each of the export configurations found.

    Example:
        main("/models_configs")
    """

    models_info_paths = []
    train_path = None
    export_config_paths = []

    for filename in os.listdir(repo_configs_and_info_folder_path):
        file_path = os.path.join(repo_configs_and_info_folder_path, filename)
        if filename.endswith(".json"):
            if filename == "family_info.json":
                model_family_info_path = file_path
            elif filename == "train-config.json":
                train_config_path = file_path
            elif filename.startswith("export-"):
                export_config_paths.append(file_path)
            else:
                models_info_paths.append(file_path)

    for model_info_path in models_info_paths:
        run("train.py", model_family_info_path, model_info_path, train_config_path)
        run("eval.py", model_family_info_path, model_info_path, "eval")
        run("deploy.py", model_family_info_path, model_info_path, "deploy")
        for export_config_path in export_config_paths:
            run(
                "export.py", model_family_info_path, model_info_path, export_config_path
            )


if __name__ == "__main__":
    """
    Entry point of the script. The script starts here by calling the main function with the folder path
    containing the model configurations and information files.

    Example:
        python byom_test.py
    """
    main(REPO_CONFIGS_AND_INFO_FOLDER_PATH)
