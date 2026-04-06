<template>
  <div>
    <h1>Исполнители</h1>
    <button @click="showForm = true; resetForm()">+ Добавить исполнителя</button>

    <table>
      <thead>
        <tr>
          <th>ФИО / Название</th>
          <th>ИНН</th>
          <th>Дисциплины</th>
          <th>Телефон</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in contractors" :key="c.id">
          <td>{{ c.full_name }}</td>
          <td>{{ c.inn }}</td>
          <td>{{ c.disciplines.map((d: any) => d.code).join(', ') }}</td>
          <td>{{ c.phone }}</td>
          <td><button @click="editContractor(c.id)">Редактировать</button></td>
        </tr>
      </tbody>
    </table>

    <div v-if="showForm">
      <h2>{{ editId ? 'Редактировать исполнителя' : 'Новый исполнитель' }}</h2>

      <label><input v-model="form.is_individual" type="checkbox" /> ИП (не ООО)</label>
      <label>ФИО / Название <input v-model="form.full_name" type="text" placeholder="ИП Ершов Дмитрий Игоревич" /></label>
      <label>Краткое (Ершов Д.И.) <input v-model="form.short_name" type="text" /></label>
      <label>ИНН <input v-model="form.inn" type="text" /></label>
      <label>ОГРН <input v-model="form.ogrn" type="text" /></label>
      <label>Юр. адрес <input v-model="form.legal_address" type="text" /></label>
      <label>Банк <input v-model="form.bank_name" type="text" /></label>
      <label>БИК <input v-model="form.bik" type="text" /></label>
      <label>Р/с <input v-model="form.account" type="text" /></label>
      <label>К/с <input v-model="form.corr_account" type="text" /></label>
      <label>Телефон <input v-model="form.phone" type="text" /></label>

      <div>
        <strong>Дисциплины:</strong>
        <div v-for="d in disciplines" :key="d.id">
          <label>
            <input
              type="checkbox"
              :value="d.id"
              v-model="form.discipline_ids"
            />
            {{ d.code }} — {{ d.name }}
          </label>
        </div>
      </div>

      <button @click="saveContractor">Сохранить</button>
      <button @click="showForm = false">Отмена</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api from '@/api/index'

const contractors = ref([])
const disciplines = ref([])
const showForm = ref(false)
const editId = ref<number | null>(null)

const form = reactive({
  is_individual: true,
  full_name: '',
  short_name: '',
  inn: '',
  ogrn: '',
  legal_address: '',
  bank_name: '',
  bik: '',
  account: '',
  corr_account: '',
  phone: '',
  discipline_ids: [] as number[],
})

function resetForm() {
  editId.value = null
  Object.assign(form, {
    is_individual: true, full_name: '', short_name: '', inn: '', ogrn: '',
    legal_address: '', bank_name: '', bik: '', account: '', corr_account: '',
    phone: '', discipline_ids: [],
  })
}

async function loadContractors() {
  const response = await api.get('/contractors')
  contractors.value = response.data
}

async function editContractor(id: number) {
  const response = await api.get(`/contractors/${id}`)
  editId.value = id
  Object.assign(form, response.data)
  showForm.value = true
}

async function saveContractor() {
  if (editId.value) {
    await api.put(`/contractors/${editId.value}`, form)
  } else {
    await api.post('/contractors', form)
  }
  showForm.value = false
  await loadContractors()
}

onMounted(async () => {
  await loadContractors()
  const response = await api.get('/disciplines')
  disciplines.value = response.data
})
</script>