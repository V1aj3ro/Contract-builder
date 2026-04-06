<template>
  <div>
    <h1>Дисциплины</h1>

    <div>
      <input v-model="newCode" type="text" placeholder="Код (АР)" style="width:80px" />
      <input v-model="newName" type="text" placeholder="Название" />
      <button @click="addDiscipline">+ Добавить дисциплину</button>
    </div>

    <div v-for="discipline in disciplines" :key="discipline.id" style="margin-top:16px">
      <strong>{{ discipline.code }} — {{ discipline.name }}</strong>
      <button class="delete-btn secondary" @click="deleteDiscipline(discipline.id)" style="margin-left:8px">✕</button>

      <ul>
        <li v-for="work in discipline.works" :key="work.id">
          {{ work.text }}
          <button class="delete-btn secondary" @click="deleteWork(discipline.id, work.id)">✕</button>
        </li>
      </ul>

      <div>
        <input v-model="newWorkText[discipline.id]" type="text" placeholder="Новая типовая работа" style="width:400px" />
        <button @click="addWork(discipline.id)">+ Добавить работу</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api from '@/api/index'

const disciplines = ref([])
const newCode = ref('')
const newName = ref('')
const newWorkText = reactive<Record<number, string>>({})

async function loadDisciplines() {
  const response = await api.get('/disciplines')
  disciplines.value = response.data
}

async function addDiscipline() {
  if (!newCode.value || !newName.value) return
  await api.post('/disciplines', { code: newCode.value, name: newName.value })
  newCode.value = ''
  newName.value = ''
  await loadDisciplines()
}

async function deleteDiscipline(id: number) {
  if (!confirm('Удалить дисциплину со всеми работами?')) return
  await api.delete(`/disciplines/${id}`)
  await loadDisciplines()
}

async function addWork(disciplineId: number) {
  const text = newWorkText[disciplineId]
  if (!text) return
  await api.post(`/disciplines/${disciplineId}/works`, { text })
  newWorkText[disciplineId] = ''
  await loadDisciplines()
}

async function deleteWork(disciplineId: number, workId: number) {
  await api.delete(`/disciplines/${disciplineId}/works/${workId}`)
  await loadDisciplines()
}

onMounted(loadDisciplines)
</script>

<style scoped>
button.delete-btn {
  padding: 2px 8px;
  font-size: 12px;
  width: auto;
  display: inline;
  margin: 0 0 0 8px;
}
</style>