import pandas as pd
import json

#This FilepathManager class is made my Kaleigh Jones
class FilepathManager:
    def __init__(self, config):
        self.config = config
        self.base_path = self.config['base_path']
        self.speaking_style_folders = self.config['speaking_style_folders']
        self.speaking_style_infixes = self.config['speaking_style_infixes']
        self.speaker_groups = self.config['speaker_groups']
        self.asr_models = self.config['asr_models']
        self.path_templates = self.config['path_templates']

    def _generate_path(self, template, **kwargs):
        return template.format(base_path=self.base_path, **kwargs)

    def get_error_rate_path(self, speaking_style_folder, speaking_style_infix, speaker_group, asr_model):
        template = self.path_templates['error_rate_file']
        return self._generate_path(template, speaking_style_folder=speaking_style_folder, 
                                   speaking_style_infix=speaking_style_infix, speaker_group=speaker_group, 
                                   asr_model=asr_model)
    
    def get_meta_path(self, speaking_style_folder, speaking_style_infix, speaker_group):
        template = self.path_templates['meta_file']
        return self._generate_path(template, speaking_style_folder=speaking_style_folder, 
                                   speaking_style_infix=speaking_style_infix, speaker_group=speaker_group)

    def get_speaker_groups(self):
        return self.speaker_groups
    
    def get_asr_models(self):
        return self.asr_models

    def get_speaking_style_folders(self):
        return self.speaking_style_folders
    
    def get_speaking_style_infixes(self):
        return self.speaking_style_infixes


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def calculate_wer(corr, sub, del_, ins):
    return (sub + del_ + ins) / (corr + sub + del_)*100

# Microsoft's Copilot helped me with this function https://copilot.microsoft.com/
def process_error_rate_files(filepath_manager):
    results = []

    for style_idx, (style_folder, style_infix) in enumerate(zip(filepath_manager.get_speaking_style_folders(), filepath_manager.get_speaking_style_infixes())):
        for group in filepath_manager.get_speaker_groups():
            for model in filepath_manager.get_asr_models():
                error_rate_path = filepath_manager.get_error_rate_path(style_folder, style_infix, group, model)
                
                # Read the file and get the summary row (third from the bottom)
                try:
                    df = pd.read_csv(error_rate_path)
                    summary_row = df.iloc[-3]
                    corr, sub, del_, ins = summary_row[['Corr', 'Sub', 'Del', 'Ins']]

                    wer = calculate_wer(corr, sub, del_, ins)
                    results.append({
                        'Style': style_folder,
                        'Group': group,
                        'Model': model,
                        'WER': wer
                    })
                except FileNotFoundError:
                    print(f"File not found: {error_rate_path}")
                except Exception as e:
                    print(f"Error processing file {error_rate_path}: {e}")

    return pd.DataFrame(results)


if __name__ == "__main__":
    # This config file is inspired by config file of Kaleigh Jones
    config_path = 'config.json'
    config = load_config(config_path)
    filepath_manager = FilepathManager(config)
    
    wer_df = process_error_rate_files(filepath_manager)
    wer_df.to_csv('wer_results.csv', index=False)
