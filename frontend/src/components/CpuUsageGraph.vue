<template>
  <div>
    <div class="usage-stats">
      <div class="stat-item">
        <span class="stat-label">CPU Usage:</span>
        <span class="stat-value">{{ currentUsage }}%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">CPU Temperature:</span>
        <span class="stat-value">{{ currentTemp }}°C</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Avg Usage:</span>
        <span class="stat-value">{{ averageUsage }}%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Avg Temperature:</span>
        <span class="stat-value">{{ averageTemp }}°C</span>
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
      label: "CPU Usage %",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      borderColor: "rgba(75, 192, 192, 1)",
      data: [],
      yAxisID: "y",
    },
    {
      label: "CPU Temperature °C",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      borderColor: "rgba(255, 99, 132, 1)",
      data: [],
      yAxisID: "y1",
    },
  ],
});

const chart = ref(null);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      position: "left",
      title: {
        display: true,
        text: "CPU Usage (%)",
      },
    },
    y1: {
      beginAtZero: true,
      max: 100,
      position: "right",
      title: {
        display: true,
        text: "Temperature (°C)",
      },
      grid: {
        drawOnChartArea: false,
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
const averageUsage = ref(0);
const currentTemp = ref(0);
const averageTemp = ref(0);

const updateCpuUsage = async () => {
  try {
    const response = await fetch("http://localhost:1910/api/usage/cpu");
    const data = await response.json();

    const now = new Date();
    const timeString = now.toLocaleTimeString();

    currentUsage.value = data.cpu_usage_percent.toFixed(1);
    currentTemp.value = data.cpu_temp_c ? data.cpu_temp_c.toFixed(1) : "N/A";

    const newLabels = [...chartData.value.labels, timeString];
    const newUsageData = [
      ...chartData.value.datasets[0].data,
      data.cpu_usage_percent,
    ];
    const newTempData = [...chartData.value.datasets[1].data, data.cpu_temp_c];

    if (newLabels.length > maxDataPoints) {
      newLabels.shift();
      newUsageData.shift();
      newTempData.shift();
    }

    averageUsage.value = (
      newUsageData.reduce((a, b) => a + b, 0) / newUsageData.length
    ).toFixed(1);

    const validTemps = newTempData.filter((temp) => temp !== null);
    averageTemp.value =
      validTemps.length > 0
        ? (validTemps.reduce((a, b) => a + b, 0) / validTemps.length).toFixed(1)
        : "N/A";

    chartData.value = {
      labels: newLabels,
      datasets: [
        {
          ...chartData.value.datasets[0],
          data: newUsageData,
        },
        {
          ...chartData.value.datasets[1],
          data: newTempData,
        },
      ],
    };

    if (chart.value) {
      chart.value.update("none");
    }
  } catch (error) {
    console.error("Error fetching CPU usage:", error);
  }
};

onMounted(() => {
  intervalId = setInterval(updateCpuUsage, 3000);
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
