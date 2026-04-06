<template>
  <div>
    <h1>Договоры</h1>
    <RouterLink to="/contracts/new">+ Новый договор</RouterLink>

    <table>
      <thead>
        <tr>
          <th>№</th>
          <th>Дата</th>
          <th>Объект</th>
          <th>Заказчик</th>
          <th>Исполнитель</th>
          <th>Сумма</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contract in contracts" :key="contract.id">
          <td>{{ contract.number }}</td>
          <td>{{ contract.date }}</td>
          <td>{{ contract.object_full_name }}</td>
          <td>{{ contract.customer }}</td>
          <td>{{ contract.contractor_full_name }}</td>
          <td>{{ contract.amount }}</td>
          <td>
            <a :href="`http://127.0.0.1:8000/api/contracts/${contract.id}/generate`" target="_blank">
              Скачать
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/index'

const contracts = ref([])

onMounted(async () => {
  const response = await api.get('/contracts')
  contracts.value = response.data
})
</script>