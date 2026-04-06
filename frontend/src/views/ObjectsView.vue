<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h1>Объекты</h1>
      <button @click="showForm = true; resetForm()">+ Добавить объект</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>Название</th>
          <th>Адрес</th>
          <th>Исполнители</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in objects" :key="o.id">
          <td>{{ o.short_name }}</td>
          <td>{{ o.address }}</td>
          <td>{{ o.contractors.map((c: any) => c.full_name).join(', ') }}</td>
          <td>
            <RouterLink :to="`/objects/${o.id}`">
              <button class="secondary" style="width:auto;padding:4px 12px">Открыть</button>
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>

    <dialog :open="showForm">
      <article>
        <h2>{{ editId ? 'Редактировать объект' : 'Новый объект' }}</h2>

        <div class="grid">
          <label>Полное название <input v-model="form.full_name" type="text" /></label>
          <label>Краткое название <input v-model="form.short_name" type="text" /></label>
        </div>
        <label>Адрес <input v-model="form.address" type="text" /></label>

        <label>
          <input v-model="form.basis_enabled" type="checkbox" />
          Есть основание (госконтракт / договор)
        </label>
        <div v-if="form.basis_enabled">
          <div class="grid">
            <label>Тип основания <input v-model="form.basis_type" type="text" placeholder="Муниципального контракта" /></label>
            <label>Номер <input v-model="form.basis_number" type="text" placeholder="№123/25" /></label>
            <label>Дата <input v-model="form.basis_date" type="date" /></label>
          </div>
          <label>Объект по основанию
            <textarea v-model="form.basis_object" rows="3" placeholder="Полное название объекта из госконтракта..."></textarea>
          </label>
        </div>

        <footer>
          <button @click="saveObject">Сохранить</button>
          <button class="secondary" @click="showForm = false">Отмена</button>
        </footer>
      </article>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api from '@/api/index'

const objects = ref([])
const showForm = ref(false)
const editId = ref<number | null>(null)

const form = reactive({
  full_name: '',
  short_name: '',
  address: '',
  basis_enabled: false,
  basis_type: '',
  basis_number: '',
  basis_date: '',
  basis_object: '',
})

function resetForm() {
  editId.value = null
  Object.assign(form, {
    full_name: '', short_name: '', address: '',
    basis_enabled: false, basis_type: '', basis_number: '',
    basis_date: '', basis_object: '',
  })
}

async function loadObjects() {
  const response = await api.get('/objects')
  objects.value = response.data
}

async function saveObject() {
  if (editId.value) {
    await api.put(`/objects/${editId.value}`, form)
  } else {
    await api.post('/objects', form)
  }
  showForm.value = false
  await loadObjects()
}

onMounted(loadObjects)
</script>