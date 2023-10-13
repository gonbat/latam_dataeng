import ujson as json
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Tuple
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


args = {'file_path': 'tweets.json'}
mem_usage = memory_usage((q2_memory,(),args), interval=0.1)
print('Memory usage (in chunks of  1 seconds): %s' % mem_usage)
print('Maximum memory usage: %s' % max(mem_usage))


# # Crear un objeto cProfile
# profiler = cProfile.Profile()

# # Iniciar el perfilado
# profiler.enable()

# # Ejecutar la función que deseas perfilar
# q2_time('tweets.json')

# # Detener el perfilado
# profiler.disable()

# # Mostrar las estadísticas
# # profiler.print_stats()

# stats = pstats.Stats(profiler)

# total_time = sum(entry[3] for entry in stats.stats.values())
# mean_time = total_time / len(stats.stats)
# print(f"Mean execution time: {mean_time}")
# print(f'Total execution time:{total_time}')
