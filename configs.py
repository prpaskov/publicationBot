paper_order = ['Title', 'Motivation', 'Data Collection', 'Conclusion', 'Bibliography']

refusal_response = 'X'

remove_words = ['hypothetical ']

generic_settings = {
    'filler_intervention' : 'an intervention',
    'methodology': 'randomized controlled trial'
}

output_paths = {
    'dataGeneration': {
        'folder': 'output/data/', 
        'ending': '.py'
    },
    'paper_text': {
        'folder': 'output/paper/',
        'ending': '.txt'
    },
}

prompt_kwargs = {
    'sample_size': 2000,
    'journal_list': 'Journal of Development Economics, Journal of Public Economics, Journal of Political Economy, and Econometrica', 
    'model': 'chatGPT',
    'editor': True,
    'rigorous': True,
    'filler_intervention': None,
    'intervention_metric': None,
    'outcome_metric': None,
    'methodology': None,
    'balanced_covariates': None
}

llm_configs = {
    'chatgpt': {
        'versions': {
            'all': ['gpt-3.5-turbo-1106', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-4-0125-preview', 'gpt-4-1106-preview', 'gpt-4-1106-vision-preview', 'gpt-4-0613', 'gpt-4-32k-0613'], 
            'default': "gpt-4-0125-preview"
        },
        'key': "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",
        'temperature': {
            'range': [0,2], 
            'default': 1
        }
    },
    'claude': {
        'versions': {
            'all': ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307', 'claude-2.1', 'claude-2.0', 'claude-instant-1.2'], 
            'default': "claude-3-opus-20240229"
        },
        'key': "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",
        'temperature': {
            'range': [0,1], 
            'default': 1
        }
    },
    'gemini': {
        'versions': {
            'all': ["gemini-pro"], 
            'default': "gemini-pro"
        },
        'key': "AIzaSyA12fC-td-vUKAi74jdsclGap9qcFHHS5Q",
        'temperature': {
            'range': [0,1], 
            'default': 0.9
        }
    }
}
