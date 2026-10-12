import nvsmi

# Retrieve status for all available GPUs
for gpu in nvsmi.get_gpus():
    print(f"ID: {gpu.id} | Name: {gpu.name} | VRAM: {gpu.mem_total}, {gpu.mem_used} | Util: {gpu.gpu_util}%")
