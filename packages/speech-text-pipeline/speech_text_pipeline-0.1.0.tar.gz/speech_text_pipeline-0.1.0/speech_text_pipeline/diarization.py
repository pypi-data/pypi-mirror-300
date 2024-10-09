import json
import os
import wget
import shutil
from omegaconf import OmegaConf
from nemo.collections.asr.parts.utils.diarization_utils import OfflineDiarWithASR

#DIARIZATION
def DIARIZATION(domain_type, AUDIO_FILENAME, word_hyp, word_ts_hyp):

    path=os.path.join(os.getcwd(), 'dia_data')
    os.makedirs(path, exist_ok=True)
    CONFIG_FILE_NAME = f"diar_infer_{domain_type}.yaml"
    CONFIG_URL = f"https://raw.githubusercontent.com/NVIDIA/NeMo/main/examples/speaker_tasks/diarization/conf/inference/{CONFIG_FILE_NAME}"

    CONFIG = wget.download(CONFIG_URL, path)

    cfg = OmegaConf.load(CONFIG)
    cfg.device='cuda'

    meta = {
        'audio_filepath': AUDIO_FILENAME,
        'offset': 0,
        'duration':None,
        'label': 'infer',
        'text': '-',
        'num_speakers': None,
        'rttm_filepath': None,
        'uem_filepath' : None
    }
    input_manifest_file_path=os.path.join(path, 'input_manifest.json')
    with open(input_manifest_file_path,'w') as fp:
        json.dump(meta,fp)
        fp.write('\n')

    cfg.diarizer.manifest_filepath = input_manifest_file_path

    pretrained_speaker_model='titanet_large'
    cfg.diarizer.manifest_filepath = cfg.diarizer.manifest_filepath
    cfg.diarizer.out_dir = path #Directory to store intermediate files and prediction outputs
    cfg.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
    cfg.diarizer.clustering.parameters.oracle_num_speakers=False

    # Using Neural VAD and Conformer ASR
    cfg.diarizer.vad.model_path = 'vad_multilingual_marblenet'
    cfg.diarizer.asr.model_path = 'stt_en_conformer_ctc_large'
    cfg.diarizer.oracle_vad = False # ----> Not using oracle VAD
    cfg.diarizer.asr.parameters.asr_based_vad = False

    asr_diar_offline = OfflineDiarWithASR(cfg.diarizer)
    asr_diar_offline.word_ts_anchor_offset = 0.12

    diar_hyp, diar_score = asr_diar_offline.run_diarization(cfg, word_ts_hyp)

    trans_info_dict = asr_diar_offline.get_transcript_with_speaker_labels(diar_hyp, word_hyp, word_ts_hyp)

    dia_json=os.path.join(path, 'pred_rttms', f"{AUDIO_FILENAME.split('/')[-1].split('.')[0]}.json")
    if os.path.exists(os.path.join(os.getcwd() ,AUDIO_FILENAME)):
        with open(dia_json) as f:
            diarized_transcription=json.load(f)

    try:
        shutil.rmtree(path)
    except Exception as e:
        print('error: ', e)

    return diarized_transcription