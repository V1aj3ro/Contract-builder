<template>
  <div v-if="obj">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h1>{{ obj.short_name }}</h1>
      <div style="display:flex;gap:8px">
        <button class="secondary" @click="showEditForm = true">Редактировать</button>
        <button class="secondary outline" style="color:red;border-color:red" @click="deleteObject">Удалить</button>
      </div>
    </div>

    <div class="grid">
      <article>
        <h3>Информация об объекте</h3>
        <p><strong>Полное название:</strong> {{ obj.full_name }}</p>
        <p v-if="obj.address"><strong>Адрес:</strong> {{ obj.address }}</p>
        <div v-if="obj.basis_enabled">
          <p><strong>Основание:</strong> {{ obj.basis_type }} {{ obj.basis_number }} от {{ obj.basis_date }}</p>
          <p v-if="obj.basis_object"><strong>Объект по основанию:</strong> {{ obj.basis_object }}</p>
        </div>
      </article>
    </div>

    <article>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h3>Исполнители</h3>
        <div style="display:flex;gap:8px">
          <select v-model="selectedContractorId" style="width:auto;margin:0">
            <option value="">— добавить исполнителя —</option>
            <option v-for="c in availableContractors" :key="c.id" :value="c.id">
              {{ c.full_name }}
            </option>
          </select>
          <button style="width:auto" @click="addContractor" :disabled="!selectedContractorId">Добавить</button>
        </div>
      </div>

      <table v-if="obj.contractors.length">
        <thead>
          <tr>
            <th>Исполнитель</th>
            <th>ИНН</th>
            <th>Дисциплины</th>
            <th>Телефон</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in obj.contractors" :key="c.id">
            <td>{{ c.full_name }}</td>
            <td>{{ c.inn }}</td>
            <td>{{ c.disciplines.map((d: any) => d.code).join(', ') }}</td>
            <td>{{ c.phone }}</td>
            <td style="display:flex;gap:8px">
              <button style="width:auto;padding:4px 12px" @click="createContract(c)">+ Договор</button>
              <button class="secondary" style="width:auto;padding:4px 12px;color:red;border-color:red" @click="removeContractor(c.id)">✕</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else style="color:gray">Нет исполнителей</p>
    </article>
  </div>

  <dialog :open="showEditForm">
    <article>
      <h2>Редактировать объект</h2>
      <div class="grid">
        <label>Полное название <input v-model="editForm.full_name" type="text" /></label>
        <label>Краткое название <input v-model="editForm.short_name" type="text" /></label>
      </div>
      <label>Адрес <input v-model="editForm.address" type="text" /></label>
      <label>
        <input v-model="editForm.basis_enabled" type="checkbox" />
        Есть основание
      </label>
      <div v-if="editForm.basis_enabled">
        <div class="grid">
          <label>Тип <input v-model="editForm.basis_type" type="text" /></label>
          <label>Номер <input v-model="editForm.basis_number" type="text" /></label>
          <label>Дата <input v-model="editForm.basis_date" type="date" /></label>
        </div>
        <label>Объект по основанию
          <textarea v-model="editForm.basis_object" rows="3"></textarea>
        </label>
      </div>
      <footer>
        <button @click="saveEdit">Сохранить</button>
        <button class="secondary" @click="showEditForm = false">Отмена</button>
      </footer>
    </article>
  </dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/index'

const route = useRoute()
const router = useRouter()
const obj = ref<any>(null)
const allContractors = ref([])
const selectedContractorId = ref('')
const showEditForm = ref(false)

const editForm = reactive({
  full_name: '', short_name: '', address: '',
  basis_enabled: false, basis_type: '', basis_number: '',
  basis_date: '', basis_object: '',
})

const availableContractors = computed(() => {
  if (!obj.value) return []
  const existingIds = obj.value.contractors.map((c: any) => c.id)
  return allContractors.value.filter((c: any) => !existingIds.includes(c.id))
})

async function load() {
  const response = await api.get(`/objects/${route.params.id}`)
  obj.value = response.data
  Object.assign(editForm, response.data)
}

async function saveEdit() {
  await api.put(`/objects/${route.params.id}`, editForm)
  showEditForm.value = false
  await load()
}

async function deleteObject() {
  if (!confirm('Удалить объект?')) return
  await api.delete(`/objects/${route.params.id}`)
  router.push('/objects')
}

async function addContractor() {
  if (!selectedContractorId.value) return
  await api.post(`/objects/${route.params.id}/contractors/${selectedContractorId.value}`)
  selectedContractorId.value = ''
  await load()
}

async function removeContractor(contractorId: number) {
  await api.delete(`/objects/${route.params.id}/contractors/${contractorId}`)
  await load()
}

async function createContract(contractor: any) {
  router.push({
    path: '/contracts/new',
    query: {
      object_id: route.params.id,
      contractor_id: contractor.id,
    }
  })
}

onMounted(async () => {
  await load()
  const response = await api.get('/contractors')
  allContractors.value = response.data
})
</script>