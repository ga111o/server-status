<script setup>
import CpuUsageGraph from "./components/CpuUsageGraph.vue";
import MemoryUsageGraph from "./components/MemoryUsageGraph.vue";
import StorageInfo from "./components/StorageInfo.vue";
import GpuUsageGraph from "./components/GpuUsageGraph.vue";
import CpuInfo from "./components/CpuInfo.vue";
</script>

<template>
  <div class="container">
    <div class="graphs">
      <CpuUsageGraph />
      <MemoryUsageGraph />
      <GpuUsageGraph />
    </div>
    <CpuInfo />
    <StorageInfo />
  </div>
</template>

<style scoped>
.container {
  width: 100%;
  padding: 2rem;
}

.graphs {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
</style>
