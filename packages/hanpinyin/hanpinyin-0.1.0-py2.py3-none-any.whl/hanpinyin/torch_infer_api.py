import os
import json
import requests
import zipfile
from io import BytesIO
import shutil

import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer
from tqdm import tqdm
import onnxruntime
import numpy as np

from g2pw.dataset import TextDataset, get_phoneme_labels, get_char_phoneme_labels
from g2pw.utils import load_config
from g2pw.dataset import prepare_data, TextDataset, ANCHOR_CHAR
from g2pw.module import G2PW


MODEL_URL = 'https://storage.googleapis.com/esun-ai/g2pW/G2PWModel-v2.zip'


def predict(model, device, dataloader, labels, turnoff_tqdm=False):
    model.eval()
    all_preds = []
    all_confidences = []
    with torch.no_grad():
        generator = dataloader if turnoff_tqdm else tqdm(dataloader, desc='predict')
        for data in generator:
            input_ids, token_type_ids, attention_mask, phoneme_mask, char_ids, position_ids = \
                [data[name].to(device) for name in ('input_ids', 'token_type_ids', 'attention_mask', 'phoneme_mask', 'char_ids', 'position_ids')]
            probs = model(
                input_ids=input_ids,
                token_type_ids=token_type_ids,
                attention_mask=attention_mask,
                phoneme_mask=phoneme_mask,
                char_ids=char_ids,
                position_ids=position_ids
            )
            max_probs, preds = map(lambda x: x.cpu().tolist(), probs.max(dim=-1))
            all_preds += [labels[pred] for pred in preds]
            all_confidences += max_probs
    return all_preds, all_confidences


def download_model(model_dir):
    root = os.path.dirname(os.path.abspath(model_dir))

    r = requests.get(MODEL_URL, allow_redirects=True)
    zip_file = zipfile.ZipFile(BytesIO(r.content))
    zip_file.extractall(root)
    source_dir = os.path.join(root, zip_file.namelist()[0].split('/')[0])
    shutil.move(source_dir, model_dir)


def main(config, checkpoint, sent_path, output_path=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    tokenizer = BertTokenizer.from_pretrained(config.model_source)

    polyphonic_chars = [line.split('\t') for line in open(config.polyphonic_chars_path).read().strip().split('\n')]
    labels, char2phonemes = get_char_phoneme_labels(polyphonic_chars) if config.use_char_phoneme else get_phoneme_labels(polyphonic_chars)

    chars = sorted(list(char2phonemes.keys()))

    texts, query_ids = prepare_data(sent_path)

    dataset = TextDataset(tokenizer, labels, char2phonemes, chars, texts, query_ids,
                          use_mask=config.use_mask, use_char_phoneme=config.use_char_phoneme, window_size=config.window_size, for_train=False)

    dataloader = DataLoader(
        dataset=dataset,
        batch_size=config.batch_size,
        collate_fn=dataset.create_mini_batch,
        num_workers=config.num_workers
    )

    model = G2PW.from_pretrained(
        config.model_source,
        labels=labels,
        chars=chars,
        pos_tags=TextDataset.POS_TAGS,
        use_conditional=config.use_conditional,
        param_conditional=config.param_conditional,
        use_focal=config.use_focal,
        param_focal=config.param_focal,
        use_pos=config.use_pos,
        param_pos=config.param_pos
    )
    model.load_state_dict(torch.load(checkpoint, map_location=device), False)
    model.to(device)
    model.eval()

    preds, confidences = predict(model, dataloader, device, labels)
    if config.use_char_phoneme:
        preds = [pred.split(' ')[1] for pred in preds]

    # for text, query_id, pred, confidence in zip(texts, query_ids, preds, confidences):
    #     print('{font}{anchor}{mid}{anchor}{end},{pred},{confidence:.5}'.format(
    #         anchor=ANCHOR_CHAR,
    #         font=text[:query_id],
    #         mid=text[query_id],
    #         end=text[query_id+1:],
    #         pred=pred,
    #         confidence=confidence
    #     ))
    # if output_path:
    #     lines = [f'{pred},{confidence}' for pred, confidence in zip(preds, confidences)]
    #     open(output_path, 'w').write('\n'.join(lines))


class G2PWConverterTorch:
    def __init__(self, model_dir='G2PWModel-v2/', device='cpu', style='bopomofo', model_source=None, num_workers=None, batch_size=None,
                 turnoff_tqdm=True, enable_non_tradional_chinese=False):
        if not os.path.exists(os.path.join(model_dir, 'version')):
            download_model(model_dir)

        self.device = device

        # sess_options = onnxruntime.SessionOptions()
        # sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        # sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
        # sess_options.intra_op_num_threads = 2
        # self.session_g2pw =  onnxruntime.InferenceSession(os.path.join(model_dir, 'g2pw.onnx'), sess_options=sess_options)

        self.config = config = load_config(os.path.join(model_dir, 'config.py'), use_default=True)

        # polyphonic_chars = [line.split('\t') for line in open(config.polyphonic_chars_path).read().strip().split('\n')]
        # labels, char2phonemes = get_char_phoneme_labels(polyphonic_chars) if config.use_char_phoneme else get_phoneme_labels(polyphonic_chars)
        # chars = sorted(list(char2phonemes.keys()))

        self.num_workers = num_workers if num_workers else self.config.num_workers
        self.batch_size = batch_size if batch_size else self.config.batch_size
        self.model_source = model_source if model_source else self.config.model_source
        self.turnoff_tqdm = turnoff_tqdm

        self.tokenizer = BertTokenizer.from_pretrained(self.model_source)

        polyphonic_chars_path = os.path.join(model_dir, 'POLYPHONIC_CHARS.txt')
        monophonic_chars_path = os.path.join(model_dir, 'MONOPHONIC_CHARS.txt')
        self.polyphonic_chars = [line.split('\t') for line in open(polyphonic_chars_path).read().strip().split('\n')]
        self.monophonic_chars = [line.split('\t') for line in open(monophonic_chars_path).read().strip().split('\n')]
        self.labels, self.char2phonemes = get_char_phoneme_labels(self.polyphonic_chars) if self.config.use_char_phoneme else get_phoneme_labels(self.polyphonic_chars)

        self.chars = sorted(list(self.char2phonemes.keys()))
        self.pos_tags = TextDataset.POS_TAGS

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'bopomofo_to_pinyin_wo_tune_dict.json'), 'r') as fr:
            self.bopomofo_convert_dict = json.load(fr)
        self.style_convert_func = {
            'bopomofo': lambda x: x,
            'pinyin': self._convert_bopomofo_to_pinyin,
        }[style]

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'char_bopomofo_dict.json'), 'r') as fr:
            self.char_bopomofo_dict = json.load(fr)

        self.enable_non_tradional_chinese = enable_non_tradional_chinese
        if self.enable_non_tradional_chinese:
            self.s2t_dict = {}
            for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'bert-base-chinese_s2t_dict.txt'), 'r').read().strip().split('\n'):
                s_char, t_char = line.split('\t')
                self.s2t_dict[s_char] = t_char

        self.model = G2PW.from_pretrained(
            config.model_source,
            labels=self.labels,
            chars=self.chars,
            pos_tags=TextDataset.POS_TAGS,
            use_conditional=config.use_conditional,
            param_conditional=config.param_conditional,
            use_focal=config.use_focal,
            param_focal=config.param_focal,
            use_pos=config.use_pos,
            param_pos=config.param_pos
        )
        checkpoint = os.path.join(model_dir, 'best_accuracy.pth')
        self.model.load_state_dict(torch.load(checkpoint, map_location=device), False)
        self.model.to(device)
        self.model.eval()

    def _convert_bopomofo_to_pinyin(self, bopomofo):
        tone = bopomofo[-1]
        assert tone in '12345'
        component = self.bopomofo_convert_dict.get(bopomofo[:-1])
        if component:
            return component + tone
        else:
            print(f'Warning: "{bopomofo}" cannot convert to pinyin')
            return None

    def _convert_s2t(self, sentence):
        return ''.join([self.s2t_dict.get(char, char) for char in sentence])

    def __call__(self, sentences):
        if isinstance(sentences, str):
            sentences = [sentences]

        if self.enable_non_tradional_chinese:
            translated_sentences = []
            for sent in sentences:
                translated_sent = self._convert_s2t(sent)
                assert len(translated_sent) == len(sent)
                translated_sentences.append(translated_sent)
            sentences = translated_sentences

        texts, query_ids, sent_ids, partial_results = self._prepare_data(sentences)
        if len(texts) == 0:
            # sentences no polyphonic words
            return partial_results

        dataset = TextDataset(self.tokenizer, self.labels, self.char2phonemes, self.chars, texts, query_ids,
                              use_mask=self.config.use_mask, use_char_phoneme=self.config.use_char_phoneme,
                              window_size=self.config.window_size, for_train=False)

        dataloader = DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
            collate_fn=dataset.create_mini_batch,
            num_workers=self.num_workers
        )

        preds, confidences = predict(self.model, self.device, dataloader, self.labels, turnoff_tqdm=self.turnoff_tqdm)

        if self.config.use_char_phoneme:
            preds = [pred.split(' ')[1] for pred in preds]

        results = partial_results
        for sent_id, query_id, pred in zip(sent_ids, query_ids, preds):
            results[sent_id][query_id] = self.style_convert_func(pred)

        return results

    def _prepare_data(self, sentences):
        polyphonic_chars = set(self.chars)
        monophonic_chars_dict = {
            char: phoneme for char, phoneme in self.monophonic_chars
        }
        texts, query_ids, sent_ids, partial_results = [], [], [], []
        for sent_id, sent in enumerate(sentences):
            partial_result = [None] * len(sent)
            for i, char in enumerate(sent):
                if char in polyphonic_chars:
                    texts.append(sent)
                    query_ids.append(i)
                    sent_ids.append(sent_id)
                elif char in monophonic_chars_dict:
                    partial_result[i] =  self.style_convert_func(monophonic_chars_dict[char])
                elif char in self.char_bopomofo_dict:
                    partial_result[i] =  self.style_convert_func(self.char_bopomofo_dict[char][0])
            partial_results.append(partial_result)
        return texts, query_ids, sent_ids, partial_results
