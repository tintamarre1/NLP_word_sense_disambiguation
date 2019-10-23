
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)

import os
import torch
from pytorch_lightning import Trainer
from argparse import ArgumentParser,ArgumentTypeError
from test_tube import HyperOptArgumentParser
from lightning import modules as lm
from lightning.utils import str2bool
from dataloaders.dataloader_utils import gen_dataloader
from multiprocessing import cpu_count
from test_tube import Experiment
import ipdb

#def main(hparams,*args,**kwargs):


if __name__ == '__main__':
    
    #parser = ArgumentParser()
    parser = HyperOptArgumentParser(strategy='random_search')
    parser.add_argument("--data_path", type=str, default="../data/preprocessed/fullcorpus.feather",
                        help="Input data path")
    parser.add_argument("--test_data_path", type=str, default="",
                        help="Input test data path")
    parser.add_argument('--val_check_interval', type=float, default=1.0,
                        help='Fraction of epoch at which to check validation set')
    parser.add_argument("--default_save_path", type=str, default="../data/",
                        help="Save path for logs and checkpoints log directory for Tensorboard log output")
    parser.add_argument('--epochs', type=int, default=10,
                       help='number of epochs to train (default: 10)')
    parser.add_argument("--model", type=str, default='bert') # can be xlnet as well
    parser.add_argument("--model_type", type=str, default='bert-base-uncased',choices=['bert-base-uncased','bert-base-cased'],
                        help="bert model: default is bert-base-uncased")
    parser.add_argument("--preprocess_inputs", type=str2bool, default=True,
                        help="Preprocess input data (Tokenize and generate input embeddings)")
    parser.add_argument("--input_len", type=int, default=128,
                        help="Sentence max length/padding size",choices=[128,256])
    parser.add_argument('--class_weights', nargs='+', type=float,default=(1.0,1.0), 
                        help="class weights to be used in the loss function")
    parser.add_argument('--nb_trials', type=int, default=4,
                        help="Number trials for hyperparameter optimization")
    parser.add_argument('--train_samples', type=int, default=None,
                        help="Number trials for hyperparameter optimization")                    
    parser.opt_list('--batch_size', type=int, default=16, options=[8,16,32,64],
                        help='input batch size for training (default: 64)',tunable=False)    
    parser.opt_range('--lr', type=float, default=2e-5,low=2E-8, high=2E-3,nb_samples=10, log_base=10,
                        help='learning rate (default: 0.01)',tunable=True)
    parser.opt_range('--weight_decay', type=float, default=0.01,low=1E-5,
                        high=0.2,nb_samples=10, log_base=10,
                        help='SGD momentum (default: 0.5)',tunable=True)
    #parser.add_argument('--momentum', type=float, default=0.5,
    #                    help='SGD momentum (default: 0.5)')    
    parser.opt_list("--token_layer", type=str, default='token-cls',
                        help="bert token layer type: default is token-cls",
                        options=['token-cls','sent-cls','sent-cls-ws'],tunable=True)
    parser.opt_list("--weak_supervision", type=bool, default=True,options=[True,False],
                    help="Enable context gloss weak supervision",tunable=True)
    
    hyperparams = parser.parse_args()

    for trial in hyperparams.generate_trials(nb_trials=hyperparams.nb_trials):
        print(trial)
        main(trial)

    
    #ipdb.set_trace()
    #print()
    
    #main(hyperparams)

    
    