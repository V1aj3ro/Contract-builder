<template>
  <div v-if="contractor && contractor.disciplines">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h1>{{ contractor.full_name }}</h1>
      <div style="display:flex;gap:8px">
        <button class="secondary" @click="showEditForm = true">Редактировать</button>
        <button class="secondary outline" style="color:red;border-color:red" @click="deactivate">Удалить</button>
      </div>
    </div>

    <div class="grid">
      <article>
        <h3>Реквизиты</h3>
        <p><strong>ИНН:</strong> {{ contractor.inn }}</p>
        <p><strong>ОГРН:</strong> {{ contractor.ogrn }}</p>
        <p><strong>Адрес:</strong> {{ contractor.legal_address }}</p>
        <p><strong>Банк:</strong> {{ contractor.bank_name }}</p>
        <p><strong>БИК:</strong> {{ contractor.bik }}</p>
        <p><strong>Р/с:</strong> {{ contractor.account }}</p>
        <p><strong>К/с:</strong> {{ contractor.corr_account }}</p>
        <p v-if="contractor.phone"><strong>Телефон:</strong> {{ contractor.phone }}</p>
      </article>

      <article>
        <h3>Активные договоры</h3>
        <p v-if="!contractor.contracts.length" style="color:gray">Нет договоров</p>
        <table v-else>
          <thead>
            <tr><th>№</th><th>Объект</th><th>Заказчик</th><th>Сумма</th></tr>
          </thead>
          <tbody>
            <tr v-for="c in contractor.contracts" :key="c.id">
              <td>{{ c.number }}</td>
              <td>{{ c.object_full_name }}</td>
              <td>{{ c.customer }}</td>
              <td>{{ c.amount }}</td>
            </tr>
          </tbody>
        </table>
      </article>
    </div>

    <article>
      <h3>Дисциплины и работы</h3>
      <p v-if="!contractor.disciplines.length" style="color:gray">Нет дисциплин</p>
      <div v-for="d in contractor.disciplines" :key="d.id" style="margin-bottom:24px">
        <strong>{{ d.code }} — {{ d.name }}</strong>
        <ul>
          <li v-for="w in (contractor.works_by_discipline[d.id] || [])" :key="w.id" style="display:flex;align-items:center;gap:8px">
            {{ w.text }}
            <button class="delete-btn secondary" @click="deleteWork(w.id)">✕</button>
          </li>
        </ul>
        <div style="display:flex;gap:8px;margin-top:8px">
          <input v-model="newWorkText[d.id]" type="text" placeholder="Новая работа" style="margin:0" />
          <button style="width:auto" @click="addWork(d.id)">+ Добавить</button>
        </div>
      </div>
    </article>
  </div>

  <dialog :open="showEditForm">
    <article>
      <h2>Редактировать исполнителя</h2>
      <label>
        <input v-model="editForm.is_individual" type="checkbox" />
        ИП (не ООО)
      </label>
      <div class="grid">
        <label>ФИО / Название <input v-model="editForm.full_name" type="text" /></label>
        <label>Краткое <input v-model="editForm.short_name" type="text" /></label>
      </div>
      <div class="grid">
        <label>ИНН <input v-model="editForm.inn" type="text" /></label>
        <label>ОГРН <input v-model="editForm.ogrn" type="text" /></label>
        <label>Телефон <input v-model="editForm.phone" type="text" /></label>
      </div>
      <label>Юр. адрес <input v-model="editForm.legal_address" type="text" /></label>
      <div class="grid">
        <label>Банк <input v-model="editForm.bank_name" type="text" /></label>
        <label>БИК <input v-model="editForm.bik" type="text" /></label>
      </div>
      <div class="grid">
        <label>Р/с <input v-model="editForm.account" type="text" /></label>
        <label>К/с <input v-model="editForm.corr_account" type="text" /></label>
      </div>
      <fieldset>
        <legend>Дисциплины</legend>
        <label v-for="d in allDisciplines" :key="d.id" style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
          <input type="checkbox" :value="d.id" v-model="editForm.discipline_ids" style="width:auto;margin:0" />
          {{ d.code }} — {{ d.name }}
        </label>
      </fieldset>
      <footer>
        <button @click="saveEdit">Сохранить</button>
        <button class="secondary" @click="showEditForm = false">Отмена</button>
      </footer>
    </article>
  </dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/index'

const route = useRoute()
const router = useRouter()
const contractor = ref<any>(null)
const allDisciplines = ref([])
const showEditForm = ref(false)
const newWorkText = reactive<Record<number, string>>({})

const editForm = reactive({
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

async function load() {
  const response = await api.get(`/contractors/${route.params.id}`)
  contractor.value = response.data
  if (!contractor.value.contracts) contractor.value.contracts = []
  if (!contractor.value.works_by_discipline) contractor.value.works_by_discipline = {}
  Object.assign(editForm, {
    ...response.data,
    discipline_ids: response.data.discipline_ids,
  })
}

async function saveEdit() {
  await api.put(`/contractors/${route.params.id}`, editForm)
  showEditForm.value = false
  await load()
}

async function deactivate() {
  if (!confirm('Удалить исполнителя?')) return
  await api.delete(`/contractors/${route.params.id}`)
  router.push('/contractors')
}

async function addWork(disciplineId: number) {
  const text = newWorkText[disciplineId]
  if (!text) return
  await api.post(`/contractors/${route.params.id}/works?discipline_id=${disciplineId}`, { text })
  newWorkText[disciplineId] = ''
  await load()
}

async function deleteWork(workId: number) {
  await api.delete(`/contractors/${route.params.id}/works/${workId}`)
  await load()
}

onMounted(async () => {
  await load()
  console.log('contractor:', contractor.value)
  const response = await api.get('/disciplines')
  allDisciplines.value = response.data
})
</script>

<style scoped>
button.delete-btn {
  padding: 2px 8px;
  font-size: 12px;
  width: auto;
  display: inline;
  margin: 0;
}
</style>