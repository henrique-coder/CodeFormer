from pathlib import Path
from subprocess import run
from typing import Any


def install_requirements(python_pip_filepath: Any, codeformer_requirements_filepath: Any, install_codeformer_gui_requirements: bool = False, has_active_nvidia_gpu: bool = False):
    pip_dir, requirements_filename = Path(python_pip_filepath).resolve(), Path(codeformer_requirements_filepath).resolve()

    if has_active_nvidia_gpu:
        nvidia_gpu_libs = 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118'
        full_cmd = f'"{pip_dir}" install {nvidia_gpu_libs}'
        print(f'Installing libraries for NVIDIA GPUs: {full_cmd}')
        run(full_cmd, shell=True)
        run(f'"{pip_dir}" install -r "{requirements_filename}"', shell=True)
    else:
        full_cmd = f'"{pip_dir}" install -r "{requirements_filename}"'
        print(f'Installing libraries for generic CPUs: {full_cmd}')
        run(full_cmd, shell=True)

    if install_codeformer_gui_requirements:
        full_cmd = f'"{pip_dir}" install -r gui_requirements.txt'
        print(f'Installing libraries for CodeFormer GUI: {full_cmd}')
        run(full_cmd, shell=True)


if __name__ == '__main__':
    install_requirements(
        python_pip_filepath='../.venv/Scripts/pip.exe',
        codeformer_requirements_filepath='../requirements.txt',
        install_codeformer_gui_requirements=True,
        has_active_nvidia_gpu=True
    )
