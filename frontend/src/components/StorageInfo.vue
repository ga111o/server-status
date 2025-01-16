<template>
  <div class="storage-container">
    <h2>Storage Information</h2>
    <div class="storage-cards">
      <div
        v-for="(storage, index) in storageInfo"
        :key="index"
        class="storage-card"
      >
        <h3>{{ storage.mountpoint }}</h3>
        <div class="storage-details">
          <p><strong>Device:</strong> {{ storage.device }}</p>
          <p><strong>Total:</strong> {{ storage.total_gb }} GB</p>
          <p><strong>Used:</strong> {{ storage.used_gb }} GB</p>
          <p><strong>Free:</strong> {{ storage.free_gb }} GB</p>
          <div class="usage-bar">
            <div
              class="usage-fill"
              :style="{ width: `${storage.storage_usage_percent}%` }"
              :class="{ warning: storage.storage_usage_percent > 80 }"
            ></div>
            <span class="usage-text">{{ storage.storage_usage_percent }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const storageInfo = ref([]);

const fetchStorageInfo = async () => {
  try {
    const response = await fetch("http://localhost:1910/api/usage/storage");
    const data = await response.json();
    storageInfo.value = data.storage_info;
  } catch (error) {
    console.error("Error fetching storage info:", error);
  }
};

onMounted(() => {
  fetchStorageInfo();
});
</script>

<style scoped>
.storage-container {
  padding: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.storage-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.storage-card {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
}

.storage-details {
  margin-top: 0.5rem;
}

.storage-details p {
  margin: 0.5rem 0;
}

.usage-bar {
  height: 20px;
  background-color: #e0e0e0;
  border-radius: 10px;
  position: relative;
  margin-top: 1rem;
}

.usage-fill {
  height: 100%;
  background-color: #4caf50;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.usage-fill.warning {
  background-color: #ff4444;
}

.usage-text {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-weight: bold;
}
</style>
