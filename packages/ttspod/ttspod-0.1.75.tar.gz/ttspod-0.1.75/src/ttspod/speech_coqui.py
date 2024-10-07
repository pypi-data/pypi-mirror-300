"""generate audio using coqui model"""
# optional system certificate trust
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

try:
    from contextlib import redirect_stdout, redirect_stderr
    from copy import deepcopy
    from io import BytesIO
    from pydub import AudioSegment
    from sys import argv
    from time import time
    from torch import cuda
    from torch.backends import mps
    from TTS.api import TTS
    import io
except ImportError as e:
    print(
        f'Failed to import required module: {e}\n'
        'Do you need to run pip install -r requirements.txt?')
    exit()

# ttspod modules
from .logger import Logger

class Coqui:
    """coqui text to speech generator"""
    def __init__(self, logger = None):
        
    def save(wav, output):
        buffer = BytesIO()
        tts.synthesizer.save_wav(wav=wav, path=buffer)
        buffer.seek(0)
        recording = AudioSegment.from_file(buffer, format="wav")
        recording.export(output, format='mp3')
        return output

    def convert(text = none, output = None):
        if 
    with open("test.txt","r") as f:
        text=f.read()

    if cuda.is_available():
        CPU = 'cuda'
    elif mps.is_available():
        CPU = 'mps'
    else:
        CPU = 'cpu'

    if len(argv) > 1 and argv[1] == '--nogpu':
        CPU = ''
    else:
        print(f'using {CPU} as GPU. If this fails, try running benchmark.py --nogpu')

    models = {}
    model_base = { 'progress_bar': False }

    models['xtts'] = {
        "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
        **model_base
    }
    models['glow'] = {
        "model_name": "tts_models/en/ljspeech/glow-tts",
        **model_base
    }
    models['vits'] = {
        "model_name": "tts_models/en/ljspeech/vits",
        **model_base
    }
    models['overflow'] = {
        "model_name": "tts_models/en/ljspeech/overflow",
        **model_base
    }
    models['speedy-speech'] = {
        "model_name": "tts_models/en/ljspeech/speedy-speech",
        **model_base
    }
    models['tortoise'] = {
        "model_name": "tts_models/en/multi-dataset/tortoise-v2",
        **model_base
    }

    generate_base = {
            'text': text,
            'split_sentences': True
            }

    generate = {}
    for model in models:
        generate[model] = deepcopy(generate_base)

    generate['tortoise'].update({
        'voice_dir': './voices',
        'speaker': 'reader',
        'preset': 'fast',
        'kwargs': {'kv_cache': True, 'high_vram': True, 'device': CPU}
        })

    generate['xtts'].update({
        'speaker_wav': [ './voices/reader/1.wav','./voices/reader/2.wav','./voices/reader/3.wav' ],
        'language': 'en'   
        })

    for model in models:
        print(f'running model {model}...', end='', flush=True)
        f = io.StringIO()
        g = io.StringIO()
        start = time()
        try:
            with redirect_stdout(f),redirect_stderr(g):
                if CPU:
                    tts = TTS(**models[model]).to(CPU)
                else:
                    tts = TTS(**models[model])
                generator = generate[model]
                output_wav = tts.tts( **generator )
                save(output_wav, f'out/{model}.mp3')
            duration = round(time()-start)
            print(f' took {duration} seconds, check out/{model}.mp3', flush=True)
            log_output=f'duration: {duration}\n---stdout---\n{f.read()}\n---stderr---\n{g.read()}\n'
            with open(f'out/{model}.log','w') as log:
                log.write(log_output)
        except Exception as err:
            print(f' failed: {err}')
            if CPU:
                print(f'trying again without GPU...',end='',flush=True)
                try:
                    tts = TTS(**models[model])
                    generator = generate[model]
                    output_wav = tts.tts( **generator )
                    save(output_wav, f'out/{model}-nogpu.mp3')
                    duration = round(time()-start)
                    print(f' took {duration} seconds, check out/{model}-nogpu.mp3', flush=True)
                    log_output=f'duration: {duration}\n---stdout---\n{f.read()}\n---stderr---\n{g.read()}\n'
                    with open(f'out/{model}-nogpu.log','w') as log:
                        log.write(log_output)
                except Exception as err:
                    print('failed again: {err}')
