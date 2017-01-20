#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyrouge import Rouge155 
import json
import time

start_time = time.time()

if __name__ == "__main__":
   
    rouge_dir = '/home/vishnu/Downloads/RELEASE-1.5.5'
    rouge_args = '-e /home/vishnu/Downloads/RELEASE-1.5.5/data -n 4 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a -x -l 100'
     
    rouge = Rouge155(rouge_dir, rouge_args)
   
    # 'model' refers to the human summaries 
    rouge.model_dir = '/home/vishnu/Desktop/UB_project/Human_Summaries/eval/'
    rouge.model_filename_pattern = 'D3#ID#.M.100.T.[A-Z]'

    print "-----------------MMR--------------------------"    
    # 'system' or 'peer' refers to the system summaries
    # We use the system summaries from 'ICSISumm' for an example
    rouge.system_dir = '/home/vishnu/Desktop/UB_project/MMR_results/'
    rouge.system_filename_pattern = 'd3(\d+)t.MMR'
    
    rouge_output = rouge.evaluate()    
    output_dict = rouge.output_to_dict(rouge_output)
    
    print json.dumps(output_dict, indent=2, sort_keys=True)

    print "-----------------LexRank--------------------------"    
    # 'system' or 'peer' refers to the system summaries
    # We use the system summaries from 'ICSISumm' for an example
    rouge.system_dir = '/home/vishnu/Desktop/UB_project/Lexrank_results/'
    rouge.system_filename_pattern = 'd3(\d+)t.LexRank'
    
    rouge_output = rouge.evaluate()    
    output_dict = rouge.output_to_dict(rouge_output)
    
    print json.dumps(output_dict, indent=2, sort_keys=True)

    print ("Execution time: " + str(time.time() - start_time) )
