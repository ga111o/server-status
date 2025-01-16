<template>
  <div v-for="gpu in gpuInfo" :key="gpu.uuid" class="gpu-container">
    <h3>{{ gpu.name }}</h3>
    <div class="usage-stats">
      <div class="stat-item">
        <span class="stat-label">GPU Load</span>
        <span class="stat-value">{{ gpu.load.toFixed(1) }}%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Temperature</span>
        <span class="stat-value">{{ gpu.temperature_c }}°C</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Memory Usage</span>
        <span class="stat-value"
          >{{
            ((gpu.memory_used_mb / gpu.memory_total_mb) * 100).toFixed(1)
          }}%</span
        >
      </div>
    </div>
    <div class="chart-container">
      <Line
        v-if="chartData[gpu.uuid]"
        :data="chartData[gpu.uuid]"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const gpuInfo = ref([]);
const chartData = ref({});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: "GPU Usage (%)",
      },
    },
    x: {
      title: {
        display: true,
      },
    },
  },
};

const maxDataPoints = 20;
let intervalId = null;

const initializeChartData = (gpu) => {
  chartData.value[gpu.uuid] = {
    labels: [],
    datasets: [
      {
        label: "GPU Usage %",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        data: [],
      },
      {
        label: "Memory Usage %",
        backgroundColor: "rgba(153, 102, 255, 0.2)",
        borderColor: "rgba(153, 102, 255, 1)",
        data: [],
      },
    ],
  };
};

const updateGpuInfo = async () => {
  try {
    const response = await fetch(
      "http://kwu-knet.duckdns.org:1910/api/info/gpu"
    );
    const data = await response.json();
    gpuInfo.value = data.gpu_info;

    const now = new Date();
    const timeString = now.toLocaleTimeString();

    gpuInfo.value.forEach((gpu) => {
      if (!chartData.value[gpu.uuid]) {
        initializeChartData(gpu);
      }

      const newLabels = [...chartData.value[gpu.uuid].labels, timeString];
      const newGpuData = [
        ...chartData.value[gpu.uuid].datasets[0].data,
        gpu.load,
      ];
      const newMemoryData = [
        ...chartData.value[gpu.uuid].datasets[1].data,
        (gpu.memory_used_mb / gpu.memory_total_mb) * 100,
      ];

      if (newLabels.length > maxDataPoints) {
        newLabels.shift();
        newGpuData.shift();
        newMemoryData.shift();
      }

      chartData.value[gpu.uuid] = {
        labels: newLabels,
        datasets: [
          {
            ...chartData.value[gpu.uuid].datasets[0],
            data: newGpuData,
          },
          {
            ...chartData.value[gpu.uuid].datasets[1],
            data: newMemoryData,
          },
        ],
      };
    });
  } catch (error) {
    console.error("Error fetching GPU info:", error);
  }
};

onMounted(() => {
  intervalId = setInterval(updateGpuInfo, 3000);
});

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<style scoped>
.gpu-container {
  margin-bottom: 2rem;
}

.chart-container {
  height: 400px;
  width: 400px;
  margin: 20px auto;
}

.usage-stats {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-item {
  padding: 0.5rem 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-weight: bold;
  margin-right: 0.5rem;
}

.stat-value {
  color: #2c3e50;
}
</style>
