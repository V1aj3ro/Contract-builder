<template>
  <div>
    <h1>Дисциплины</h1>
    <div v-for="discipline in disciplines" :key="discipline.id">
      <h2>{{ discipline.code }} — {{ discipline.name }}</h2>
      <ul>
        <li v-for="work in discipline.works" :key="work.id">
          {{ work.text }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/index'

const disciplines = ref([])

onMounted(async () => {
  const response = await api.get('/disciplines')
  disciplines.value = response.data
})
</script>