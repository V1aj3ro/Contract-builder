<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h1>Заказчики</h1>
      <button @click="showForm = true; resetForm()">+ Добавить заказчика</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>Название</th>
          <th>ИНН</th>
          <th>Тип</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in customers" :key="c.id">
          <td>{{ c.full_name }}</td>
          <td>{{ c.inn }}</td>
          <td>{{ c.is_individual ? 'ИП' : 'ООО/АО' }}</td>
          <td><button class="secondary" style="width:auto;padding:4px 12px" @click="editCustomer(c.id)">Редактировать</button></td>
        </tr>
      </tbody>
    </table>

    <dialog :open="showForm">
      <article>
        <h2>{{ editId ? 'Редактировать заказчика' : 'Новый заказчик' }}</h2>

        <label>
          <input v-model="form.is_individual" type="checkbox" />
          ИП (не ООО)
        </label>
        <div class="grid">
          <label>Полное название <input v-model="form.full_name" type="text" placeholder="ООО «НовосибирскСтрой»" /></label>
          <label>Краткое название <input v-model="form.short_name" type="text" placeholder="НовосибирскСтрой" /></label>
        </div>
        <label>Полное название с расшифровкой
          <input v-model="form.full_name_extended" type="text" placeholder="Общество с ограниченной ответственностью «НовосибирскСтрой»" />
        </label>
        <div class="grid">
          <label>ИНН <input v-model="form.inn" type="text" /></label>
          <label>ОГРН <input v-model="form.ogrn" type="text" /></label>
          <label>КПП (для ООО) <input v-model="form.kpp" type="text" /></label>
        </div>
        <label>Юр. адрес <input v-model="form.legal_address" type="text" /></label>
        <div class="grid">
          <label>Банк <input v-model="form.bank_name" type="text" /></label>
          <label>БИК <input v-model="form.bik" type="text" /></label>
        </div>
        <div class="grid">
          <label>Р/с <input v-model="form.account" type="text" /></label>
          <label>К/с <input v-model="form.corr_account" type="text" /></label>
        </div>
        <div class="grid">
          <label>Подписант (именит.) <input v-model="form.signer_name" type="text" placeholder="Иванов Иван Иванович" /></label>
          <label>Подписант (родит.) <input v-model="form.signer_name_genitive" type="text" placeholder="Иванова Ивана Ивановича" /></label>
        </div>
        <div class="grid">
          <label>Должность (родит.) <input v-model="form.signer_role" type="text" placeholder="директора" /></label>
          <label>Должность (именит.) <input v-model="form.signer_role_nominative" type="text" placeholder="Директор" /></label>
        </div>

        <footer>
          <button @click="saveCustomer">Сохранить</button>
          <button class="secondary" @click="showForm = false">Отмена</button>
        </footer>
      </article>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api from '@/api/index'

const customers = ref([])
const showForm = ref(false)
const editId = ref<number | null>(null)

const form = reactive({
  is_individual: false,
  full_name: '',
  full_name_extended: '',
  short_name: '',
  inn: '',
  ogrn: '',
  kpp: '',
  legal_address: '',
  bank_name: '',
  bik: '',
  account: '',
  corr_account: '',
  signer_name: '',
  signer_name_genitive: '',
  signer_role: '',
  signer_role_nominative: '',
})

function resetForm() {
  editId.value = null
  Object.assign(form, {
    is_individual: false, full_name: '', full_name_extended: '',
    short_name: '', inn: '', ogrn: '', kpp: '', legal_address: '',
    bank_name: '', bik: '', account: '', corr_account: '',
    signer_name: '', signer_name_genitive: '', signer_role: '', signer_role_nominative: '',
  })
}

async function loadCustomers() {
  const response = await api.get('/customers')
  customers.value = response.data
}

async function editCustomer(id: number) {
  const response = await api.get(`/customers/${id}`)
  editId.value = id
  Object.assign(form, response.data)
  showForm.value = true
}

async function saveCustomer() {
  if (editId.value) {
    await api.put(`/customers/${editId.value}`, form)
  } else {
    await api.post('/customers', form)
  }
  showForm.value = false
  await loadCustomers()
}

onMounted(loadCustomers)
</script>