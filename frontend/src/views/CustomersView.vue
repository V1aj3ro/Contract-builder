<template>
  <div>
    <h1>Заказчики</h1>
    <ul>
      <li v-for="customer in customers" :key="customer.id">
        {{ customer.full_name }} — {{ customer.inn }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/index'

const customers = ref([])

onMounted(async () => {
  const response = await api.get('/customers')
  customers.value = response.data
})
</script>