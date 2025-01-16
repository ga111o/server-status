from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psutil
import statistics
import platform
import GPUtil
import docker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/usage/cpu")
def get_cpu_usage():
    cpu_percentages = [psutil.cpu_percent(interval=1) for _ in range(1)]
    
    avg_cpu_percent = statistics.mean(cpu_percentages)
    try:
        temperatures = psutil.sensors_temperatures()
        if 'coretemp' in temperatures:
            cpu_temp = statistics.mean([temp.current for temp in temperatures['coretemp']])
        else:
            cpu_temp = None
    except AttributeError:
        cpu_temp = None
    
    return {
        "cpu_usage_percent": round(avg_cpu_percent, 2),
        "cpu_temp_c": cpu_temp
    }

@app.get("/api/usage/memory")
def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        "total_memory_gb": round(memory.total / (1024**3), 2),
        "used_memory_gb": round(memory.used / (1024**3), 2),
        "memory_usage_percent": memory.percent
    }

@app.get("/api/usage/storage")
def get_storage_usage():
    partitions = psutil.disk_partitions()
    storage_info = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "storage_usage_percent": usage.percent
            })
        except PermissionError:
            continue
    
    return {"storage_info": storage_info}

@app.get("/api/info/cpu")
def get_cpu_info():
    cpu_info = {
        "processor": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": psutil.cpu_freq().max,
        "min_frequency": psutil.cpu_freq().min,
        "current_frequency": psutil.cpu_freq().current,
    }
    return cpu_info

@app.get("/api/info/gpu")
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "load": gpu.load*100,
            "memory_total_mb": gpu.memoryTotal,
            "memory_used_mb": gpu.memoryUsed,
            "memory_free_mb": gpu.memoryFree,
            "temperature_c": gpu.temperature,
            "uuid": gpu.uuid
        })
    
    return {"gpu_info": gpu_info}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1910)
