<template>
  <div>
    <div class="usage-stats">
      <div class="stat-item">
        <span class="stat-label">Total Memory</span>
        <span class="stat-value">{{ totalMemory }} GB</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Used Memory:</span>
        <span class="stat-value">{{ usedMemory }} GB</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Memory Usage:</span>
        <span class="stat-value">{{ currentUsage }}%</span>
      </div>
    </div>
    <div class="chart-container">
      <Line v-if="chartData" :data="chartData" :options="chartOptions" />
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

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: "Memory Usage %",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      data: [],
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: "Memory Usage (%)",
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

const currentUsage = ref(0);
const totalMemory = ref(0);
const usedMemory = ref(0);

const updateMemoryUsage = async () => {
  try {
    const response = await fetch(
      "http://kwu-knet.duckdns.org:1910/api/usage/memory"
    );
    const data = await response.json();

    const now = new Date();
    const timeString = now.toLocaleTimeString();

    currentUsage.value = data.memory_usage_percent.toFixed(1);
    totalMemory.value = data.total_memory_gb;
    usedMemory.value = data.used_memory_gb;

    const newLabels = [...chartData.value.labels, timeString];
    const newData = [
      ...chartData.value.datasets[0].data,
      data.memory_usage_percent,
    ];

    if (newLabels.length > maxDataPoints) {
      newLabels.shift();
      newData.shift();
    }

    chartData.value = {
      labels: newLabels,
      datasets: [
        {
          ...chartData.value.datasets[0],
          data: newData,
        },
      ],
    };
  } catch (error) {
    console.error("Error fetching Memory usage:", error);
  }
};

onMounted(() => {
  intervalId = setInterval(updateMemoryUsage, 3000);
});

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<style scoped>
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
