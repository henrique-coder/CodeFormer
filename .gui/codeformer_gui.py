import PySimpleGUI as psg
from colorama import init as colorama_init, Fore
from os import path
from pathlib import Path
from re import sub
from subprocess import Popen


def enhance_photo(bg_upsampler: str, face_upsample: str, upscaling_factor: int, fidelity_factor: int, file_path: str) -> None:
    venv_python_path = '../venv/Scripts/python.exe'
    codeformer_command = f'"{venv_python_path if path.exists(Path(venv_python_path)) else "python"}" "../inference_codeformer.py" {bg_upsampler} {face_upsample} -s {upscaling_factor} -w {fidelity_factor} -i "{file_path}" -o "codeformed-photos"'
    print(f'{Fore.LIGHTYELLOW_EX}</--- > Enhancing your photo with AI... {Fore.YELLOW}(speed can vary greatly depending on your CPU or GPU, but in general it\'s not too slow)\n')
    Popen(sub('\s+', ' ', codeformer_command).strip(), shell=True)


layout = [
    [psg.Text('Select the photo you wish to enhance:')],
    [psg.FileBrowse('Click here to choose a file', file_types=(('Images', '*.jpg *.jpeg *.png'), ('All files', '*.*')), key='file_path')],
    [psg.Text('Additional adjustments (optional):')],
    [psg.Checkbox('Background enhancer', key='bg_upsampler', default=True), psg.Checkbox('Face enhancer', key='face_upsample', default=False)],
    [psg.Text('Select the AI model if you are going to use the "Background upsampler":')],
    [psg.Radio('realesrgan', 'bg_upsampler_model', key='realesrgan', default=True), psg.Radio('upconv_7_photo', 'bg_upsampler_model', key='upconv_7_photo', default=False), psg.Radio('upconv_7_anime_style_art_rgb', 'bg_upsampler_model', key='upconv_7_anime_style_art_rgb', default=False)],
    [psg.Text('Resolution upscaling (1-20):')],
    [psg.Slider(range=(1, 20), default_value=1, resolution=1, orientation='h', size=(41, 20), key='upscaling_factor')],
    [psg.Text('Fidelity: (0.00 = best quality; 0.70 = recommended; 1.00 = best fidelity)')],
    [psg.Slider(range=(0, 1), default_value=0.70, resolution=0.01, orientation='h', size=(41, 20), key='fidelity_factor')],
    [psg.Button('Start AI enhancement', key='enhance_photo')]
]

window = psg.Window('CodeFormer (GUI) - Coded by gh@Henrique-Coder', layout)

while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED: break
    if event == 'enhance_photo':
        file_path, upscaling_factor, fidelity_factor, face_upsample, bg_upsampler = (values['file_path'], int(str(values['upscaling_factor']).split('.')[0]), int(values['fidelity_factor']), '--face_upsample' if values['face_upsample'] else str(), '--bg_upsampler' if values['bg_upsampler'] else str())
        if bg_upsampler: bg_upsampler += ' ' + next(model for model in ['realesrgan', 'upconv_7_anime_style_art_rgb', 'upconv_7_photo'] if values[model])
        enhance_photo(bg_upsampler, face_upsample, upscaling_factor, fidelity_factor, file_path)


if __name__ == '__main__':
    colorama_init(autoreset=True)
    window.close()
