import tqdm
import time

for i in tqdm.tqdm(range(100), desc="loading..."):
    time.sleep(0.01)
    print('e')