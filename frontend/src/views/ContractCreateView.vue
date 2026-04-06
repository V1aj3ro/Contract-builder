<template>
  <div>
    <h1>Новый договор</h1>

    <section>
      <h2>Основные реквизиты</h2>
      <label>Номер договора
        <input v-model="form.number" type="text" placeholder="2025/12/16" />
      </label>
      <label>Дата договора
        <input v-model="form.date" type="date" />
      </label>
      <label>Город
        <input v-model="form.city" type="text" />
      </label>
    </section>

    <section>
      <h2>Заказчик</h2>
      <label>Выберите заказчика
        <select v-model="form.customer_id">
          <option disabled value="">— выберите —</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">
            {{ c.full_name }}
          </option>
        </select>
      </label>
    </section>

    <section>
      <h2>Исполнитель</h2>
      <label>ФИО / Название <input v-model="form.contractor_full_name" type="text" /></label>
      <label>ИНН <input v-model="form.contractor_inn" type="text" /></label>
      <label>ОГРН <input v-model="form.contractor_ogrn" type="text" /></label>
      <label>Юр. адрес <input v-model="form.contractor_legal_address" type="text" /></label>
      <label>Банк <input v-model="form.contractor_bank_name" type="text" /></label>
      <label>БИК <input v-model="form.contractor_bik" type="text" /></label>
      <label>Р/с <input v-model="form.contractor_account" type="text" /></label>
      <label>К/с <input v-model="form.contractor_corr_account" type="text" /></label>
      <label>Телефон <input v-model="form.contractor_phone" type="text" placeholder="+7-952-906-44-11" /></label>
      <label>
        <input v-model="form.contractor_is_individual" type="checkbox" />
        ИП (не ООО)
      </label>
    </section>

    <section>
      <h2>Объект</h2>
      <label>Полное название объекта
        <input v-model="form.object_full_name" type="text" />
      </label>
      <label>Адрес объекта
        <input v-model="form.object_address" type="text" />
      </label>
      <label>
        <input v-model="form.basis_enabled" type="checkbox" />
        Есть основание (госконтракт / договор)
      </label>
      <div v-if="form.basis_enabled">
        <label>Тип основания
          <input v-model="form.basis_type" type="text" placeholder="Муниципальный контракт" />
        </label>
        <label>Номер
          <input v-model="form.basis_number" type="text" placeholder="№123/25" />
        </label>
        <label>Дата
          <input v-model="form.basis_date" type="date" />
        </label>
      </div>
    </section>

    <section>
      <h2>Сроки</h2>
      <label>Дата начала <input v-model="form.date_start" type="date" /></label>
      <label>Дата окончания <input v-model="form.date_end" type="date" /></label>
    </section>

    <section>
      <h2>Стоимость</h2>
      <label>Сумма (руб.) <input v-model="form.amount" type="number" step="0.01" /></label>
      <label>
        <input v-model="form.vat_included" type="checkbox" />
        НДС включён
      </label>
    </section>

    <section>
      <h2>Транши</h2>
      <label>Транш 1 (%) <input v-model="form.tranch1_pct" type="number" /></label>
      <label>Условие <input v-model="form.tranch1_condition" type="text" /></label>

      <label>
        <input v-model="hasTranch2" type="checkbox" />
        Добавить транш 2
      </label>
      <div v-if="hasTranch2">
        <label>Транш 2 (%) <input v-model="form.tranch2_pct" type="number" /></label>
        <label>Условие <input v-model="form.tranch2_condition" type="text" /></label>
      </div>

      <label>
        <input v-model="hasTranch3" type="checkbox" />
        Добавить транш 3
      </label>
      <div v-if="hasTranch3">
        <label>Транш 3 (%) <input v-model="form.tranch3_pct" type="number" /></label>
        <label>Условие <input v-model="form.tranch3_condition" type="text" /></label>
      </div>
    </section>

    <section>
        <h2>Объём работ</h2>
        <label>Перечень работ
            <textarea v-model="form.works_text" rows="6" placeholder="- разработка проектной документации..."></textarea>
        </label>
        <label>Стадийность проектирования (необязательно)
            <input v-model="form.works_stages" type="text" placeholder="Проектная и рабочая документация" />
        </label>
        <label>Результаты работ (необязательно)
            <textarea v-model="form.works_results" rows="4" placeholder="- чертежи..."></textarea>
        </label>
        <label>Доп. условия (необязательно)
            <textarea v-model="form.extra_conditions" rows="3"></textarea>
        </label>
    </section>

    <button @click="submitForm">Создать договор</button>
    <div v-if="createdId">
        ✅ Договор создан!
        <a :href="`http://127.0.0.1:8000/api/contracts/${createdId}/generate`" target="_blank">
            Скачать DOCX
        </a>
    </div>

    <pre>{{ form }}</pre>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import api from '@/api/index'

const customers = ref([])
const hasTranch2 = ref(false)
const hasTranch3 = ref(false)

const form = reactive({
  number: '',
  date: new Date().toISOString().split('T')[0],
  city: 'г. Новосибирск',
  customer_id: '',
  contractor_keycloak_id: 'manual',
  contractor_full_name: '',
  contractor_inn: '',
  contractor_ogrn: '',
  contractor_is_individual: true,
  contractor_legal_address: '',
  contractor_bank_name: '',
  contractor_bik: '',
  contractor_account: '',
  contractor_corr_account: '',
  object_full_name: '',
  object_address: '',
  basis_enabled: false,
  basis_type: '',
  basis_number: '',
  basis_date: '',
  date_start: '',
  date_end: '',
  amount: '',
  vat_included: false,
  tranch1_pct: 30,
  tranch1_condition: '',
  tranch2_pct: null,
  tranch2_condition: null,
  tranch3_pct: null,
  tranch3_condition: null,
  works_text: '',
  extra_conditions: '',
  works_stages: '',
  works_results: '',
  contractor_phone: '',
})

onMounted(async () => {
  const response = await api.get('/customers')
  customers.value = response.data
})

const createdId = ref<number | null>(null)

async function submitForm() {
  const payload = { ...form }
  if (!hasTranch2.value) { payload.tranch2_pct = null; payload.tranch2_condition = null }
  if (!hasTranch3.value) { payload.tranch3_pct = null; payload.tranch3_condition = null }
  const response = await api.post('/contracts', payload)
  createdId.value = response.data.id
}
</script>