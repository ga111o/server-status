<template>
  <div class="cpu-info-container">
    <h2>CPU Information</h2>
    <div class="cpu-info-card">
      <div class="info-item">
        <strong>Processor:</strong> {{ cpuInfo.processor }}
      </div>
      <div class="info-item">
        <strong>Physical Cores:</strong> {{ cpuInfo.physical_cores }}
      </div>
      <div class="info-item">
        <strong>Total Cores:</strong> {{ cpuInfo.total_cores }}
      </div>
      <div class="info-item">
        <strong>Current Frequency:</strong>
        {{ (cpuInfo.current_frequency / 1000).toFixed(2) }} GHz
      </div>
      <div class="info-item">
        <strong>Max Frequency:</strong>
        {{ (cpuInfo.max_frequency / 1000).toFixed(2) }} GHz
      </div>
      <div class="info-item">
        <strong>Min Frequency:</strong>
        {{ (cpuInfo.min_frequency / 1000).toFixed(2) }} GHz
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const cpuInfo = ref({});

const fetchCpuInfo = async () => {
  try {
    const response = await fetch("http://localhost:1910/api/info/cpu");
    cpuInfo.value = await response.json();
  } catch (error) {
    console.error("Error fetching CPU info:", error);
  }
};

onMounted(() => {
  fetchCpuInfo();
});
</script>

<style scoped>
.cpu-info-container {
  padding: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.cpu-info-card {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  padding: 0.5rem;
}
</style>
