import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_play_sequences(plays_df, window_size=3):
    """Analyze sequences of level plays"""
    plays_df = plays_df.sort_values('timestamp')
    
    sequences = defaultdict(int)
    for player in plays_df['player'].unique():
        player_plays = plays_df[plays_df['player'] == player]['id'].tolist()
        
        # Analyze sequences of consecutive plays
        for i in range(len(player_plays) - window_size + 1):
            sequence = tuple(player_plays[i:i+window_size])
            sequences[sequence] += 1
    
    return {
        'common_sequences': dict(sorted(sequences.items(), key=lambda x: x[1], reverse=True)[:10]),
        'sequence_counts': len(sequences),
        'avg_sequence_length': np.mean([len(seq) for seq in sequences.keys()])
    }

def identify_level_transitions(plays_df):
    """Analyze how players transition between difficulty levels"""
    transitions = defaultdict(int)
    
    for player in plays_df['player'].unique():
        player_plays = plays_df[plays_df['player'] == player].sort_values('timestamp')
        
        # Analyze difficulty transitions
        difficulties = player_plays['difficulty'].tolist()
        for i in range(len(difficulties) - 1):
            transition = (difficulties[i], difficulties[i+1])
            transitions[transition] += 1
    
    return dict(transitions)