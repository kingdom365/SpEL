import torch
import torch.nn as nn

class DescriptionEncoder():
    def __init__(self, args):
        super(DescriptionEncoder, self).__init__()
        self.text_chunk_length = 254
        self.text_chunk_overlap = 20

        self.bert_lm = None
        self.number_of_bert_layers = 0
        self.bert_lm_h = 0
        self.fc_in = args.fc_in
        self.fc_out = args.fc_out
        self.fc = None
    
    def init_model_from_scratch(self, base_model=BERT_MODEL_NAME, device="cpu"):
        if base_model:
            self.bert_lm = AutoModelForMaskedLM.from_pretrained(base_model, output_hidden_states=True,
                                                                cache_dir=get_checkpoints_dir() / "hf").to(device)
            self.number_of_bert_layers = self.bert_lm.config.num_hidden_layers + 1
            self.fc = nn.Linear(in_features=self.fc_in, out_features=self.fc_out).to(device)

    def adopt_to_aida(self, device):
        """
            读取aida数据集中的
        """
        aida_mentions_vocab, aida_mentions_itos = dl_sa.get_aida_vocab_and_itos()
        # 1. 查出aida_vocab中的所有实体的wiki text，截断前32个token，作为实体描述
        
        
        pass

def precompute_desc_emb():
    pass
