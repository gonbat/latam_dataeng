import ujson as json
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Tuple
import argparse
import emoji
from memory_profiler import memory_usage
import cProfile
import pstats


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_counts = defaultdict(int)
    user_counts_per_date = defaultdict(Counter)
    
    def read_jsonl(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                yield json.loads(line)

    for tweet in read_jsonl(file_path):
        date_str = tweet["date"]
        date = datetime.fromisoformat(date_str).date()
        user = tweet["user"]["username"]
        
        date_counts[date] += 1
        user_counts_per_date[date][user] += 1

    top_dates = sorted(date_counts, key=date_counts.get, reverse=True)[:10]
    
    return [(date, user_counts_per_date[date].most_common(1)[0][0]) for date in top_dates]



def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_counts = defaultdict(int)
    
    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            date_str = tweet["date"]
            date = datetime.fromisoformat(date_str).date()
            
            date_counts[date] += 1

    top_dates = sorted(date_counts, key=date_counts.get, reverse=True)[:10]
    
    result = []
    for date in top_dates:
        user_counts = Counter()
        
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                curr_date_str = tweet["date"]
                curr_date = datetime.fromisoformat(curr_date_str).date()
                if curr_date == date:
                    user = tweet["user"]["username"]
                    user_counts[user] += 1

        top_user = user_counts.most_common(1)[0][0]
        result.append((date, top_user))
        
    return result

def q2_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    emoji_set = set(emoji.EMOJI_DATA.keys())
    emoji_counts = Counter()

    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            content = tweet["content"]
            emojis_list = [c for c in content if c in emoji_set]
            emoji_counts.update(emojis_list)

    return emoji_counts.most_common(10)


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = Counter()

    def read_jsonl(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                yield json.loads(line)

    for tweet in read_jsonl(file_path):
        content = tweet["content"]
        for c in content:
            if emoji.EMOJI_DATA.get(c):
                emoji_counts[c] += 1

    return emoji_counts.most_common(10)


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    mentions_counter = Counter()
    
    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            content = tweet["content"]
            mentions = [word[1:] for word in content.split() if word.startswith('@')]
            mentions_counter.update(mentions)

    return mentions_counter.most_common(10)

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    mentions_counter = defaultdict(int)

    def read_jsonl(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                yield json.loads(line)

    for tweet in read_jsonl(file_path):
        content = tweet["content"]
        mentions = (word[1:] for word in content.split() if word.startswith('@'))
        for mention in mentions:
            mentions_counter[mention] += 1

    return sorted(mentions_counter.items(), key=lambda x: x[1], reverse=True)[:10]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Funciones optimizadas para memoria o tiempo de ejecucion; Challenge Data Engineer")
    parser.add_argument("funcion", choices=["q1_memory", "q1_time", "q2_memory", "q2_time","q3_memory", "q3_time"], help="Selecciona la función a ejecutar")
    parser.add_argument("--file_path", type=str, default='tweets.json', help="Valor por defecto para file_path es: tweets.json")

    args = parser.parse_args()
    parser.print_help()

    if args.funcion == "q1_memory":
        mem_usage = memory_usage((q1_memory, (args.file_path,)), interval=1)
        print('Memory usage in MB (in chunks of  1 seconds): %s' % mem_usage)
        print('Maximum memory usage in MB: %s' % max(mem_usage))
    elif args.funcion == "q1_time":
        profiler = cProfile.Profile()
        profiler.enable()
        q1_time(args.file_path)
        profiler.disable()
        stats = pstats.Stats(profiler)
        total_time = sum(entry[3] for entry in stats.stats.values())
        print(f'Total execution time in seconds: {total_time}')
    elif args.funcion == "q2_memory":
        mem_usage = memory_usage((q2_memory, (args.file_path,)), interval=1)
        print('Memory usage in MB (in chunks of  1 seconds): %s' % mem_usage)
        print('Maximum memory usage in MB: %s' % max(mem_usage))
    elif args.funcion == "q2_time":
        profiler = cProfile.Profile()
        profiler.enable()
        q2_time(args.file_path)
        profiler.disable()
        stats = pstats.Stats(profiler)
        total_time = sum(entry[3] for entry in stats.stats.values())
        print(f'Total execution time in seconds: {total_time}')
    elif args.funcion == "q3_memory":
        mem_usage = memory_usage((q3_memory, (args.file_path,)), interval=1)
        print('Memory usage in MB (in chunks of  1 seconds): %s' % mem_usage)
        print('Maximum memory usage in MB: %s' % max(mem_usage))
    elif args.funcion == "q3_time":
        profiler = cProfile.Profile()
        profiler.enable()
        q3_time(args.file_path)
        profiler.disable()
        stats = pstats.Stats(profiler)
        total_time = sum(entry[3] for entry in stats.stats.values())
        print(f'Total execution time in seconds: {total_time}')
