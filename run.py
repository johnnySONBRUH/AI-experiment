import subprocess
import time

# 1. Start Ollama in the background
ollama_process = subprocess.Popen(['ollama', 'serve'])

# 2. Give Ollama a couple of seconds to boot up completely
time.sleep(10)

# 3. Now run your main script (this will wait until main.py finishes)
subprocess.run(['python', 'main.py'])

# 4. (Optional) Shut down Ollama when your main script is done
ollama_process.terminate()
