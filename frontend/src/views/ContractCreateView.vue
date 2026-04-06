<template>
  <div>
    <h1>Новый договор</h1>

    <div v-if="Object.keys(errors).length > 0" style="color:red;margin-bottom:16px">
      ⚠️ Пожалуйста, заполните все обязательные поля
    </div>

    <article>
      <h2>Основные реквизиты</h2>
      <label>Номер договора
        <input v-model="form.number" type="text" placeholder="2025/12/16" :aria-invalid="!!errors.number" />
        <small v-if="errors.number" style="color:red">{{ errors.number }}</small>
      </label>
      <div class="grid">
        <label>Дата договора
          <input v-model="form.date" type="date" :aria-invalid="!!errors.date" />
          <small v-if="errors.date" style="color:red">{{ errors.date }}</small>
        </label>
        <label>Город
          <input v-model="form.city" type="text" />
        </label>
      </div>
    </article>

    <article>
      <h2>Заказчик</h2>
      <label>Выберите заказчика
        <select v-model="form.customer_id" :aria-invalid="!!errors.customer_id">
          <option disabled value="">— выберите —</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">
            {{ c.full_name }}
          </option>
        </select>
        <small v-if="errors.customer_id" style="color:red">{{ errors.customer_id }}</small>
      </label>
    </article>

    <article>
      <h2>Исполнитель</h2>
      <label>Выбрать из справочника
        <select @change="onContractorSelect">
          <option value="">— выбрать —</option>
          <option v-for="c in contractors" :key="c.id" :value="c.id">
            {{ c.full_name }} ({{ c.disciplines.map((d: any) => d.code).join(', ') }})
          </option>
        </select>
      </label>
      <div class="grid">
        <label>ФИО / Название
          <input v-model="form.contractor_full_name" type="text" :aria-invalid="!!errors.contractor_full_name" />
          <small v-if="errors.contractor_full_name" style="color:red">{{ errors.contractor_full_name }}</small>
        </label>
        <label>ИНН
          <input v-model="form.contractor_inn" type="text" :aria-invalid="!!errors.contractor_inn" />
          <small v-if="errors.contractor_inn" style="color:red">{{ errors.contractor_inn }}</small>
        </label>
        <label>ОГРН <input v-model="form.contractor_ogrn" type="text" /></label>
      </div>
      <label>Юр. адрес <input v-model="form.contractor_legal_address" type="text" /></label>
      <div class="grid">
        <label>Банк <input v-model="form.contractor_bank_name" type="text" /></label>
        <label>БИК <input v-model="form.contractor_bik" type="text" /></label>
      </div>
      <div class="grid">
        <label>Р/с <input v-model="form.contractor_account" type="text" /></label>
        <label>К/с <input v-model="form.contractor_corr_account" type="text" /></label>
        <label>Телефон <input v-model="form.contractor_phone" type="text" /></label>
      </div>
      <label>
        <input v-model="form.contractor_is_individual" type="checkbox" />
        ИП (не ООО)
      </label>
    </article>

    <article>
      <h2>Объект</h2>
      <label>Полное название объекта
        <input v-model="form.object_full_name" type="text" :aria-invalid="!!errors.object_full_name" />
        <small v-if="errors.object_full_name" style="color:red">{{ errors.object_full_name }}</small>
      </label>
      <label>Адрес объекта
        <input v-model="form.object_address" type="text" />
      </label>
      <label>
        <input v-model="form.basis_enabled" type="checkbox" />
        Есть основание (госконтракт / договор)
      </label>
      <div v-if="form.basis_enabled" class="grid">
        <label>Тип основания
          <input v-model="form.basis_type" type="text" placeholder="Муниципального контракта" />
        </label>
        <label>Номер
          <input v-model="form.basis_number" type="text" placeholder="№123/25" />
        </label>
        <label>Дата
          <input v-model="form.basis_date" type="date" />
        </label>
      </div>
    </article>

    <article>
      <h2>Сроки и стоимость</h2>
      <div class="grid">
        <label>Дата начала
          <input v-model="form.date_start" type="date" :aria-invalid="!!errors.date_start" />
          <small v-if="errors.date_start" style="color:red">{{ errors.date_start }}</small>
        </label>
        <label>Дата окончания
          <input v-model="form.date_end" type="date" :aria-invalid="!!errors.date_end" />
          <small v-if="errors.date_end" style="color:red">{{ errors.date_end }}</small>
        </label>
      </div>
      <div class="grid">
        <label>Сумма (руб.)
          <input v-model="form.amount" type="number" step="0.01" :aria-invalid="!!errors.amount" />
          <small v-if="errors.amount" style="color:red">{{ errors.amount }}</small>
        </label>
        <label style="display:flex;align-items:center;gap:8px;padding-top:24px">
          <input v-model="form.vat_included" type="checkbox" />
          НДС включён
        </label>
      </div>
    </article>

    <article>
      <h2>Транши</h2>
      <div class="grid">
        <label>Транш 1 (%) <input v-model="form.tranch1_pct" type="number" /></label>
        <label>Условие
          <input v-model="form.tranch1_condition" type="text" placeholder="с момента заключения договора" :aria-invalid="!!errors.tranch1_condition" />
          <small v-if="errors.tranch1_condition" style="color:red">{{ errors.tranch1_condition }}</small>
        </label>
      </div>
      <label>
        <input v-model="hasTranch2" type="checkbox" />
        Добавить транш 2
      </label>
      <div v-if="hasTranch2" class="grid">
        <label>Транш 2 (%) <input v-model="form.tranch2_pct" type="number" /></label>
        <label>Условие <input v-model="form.tranch2_condition" type="text" /></label>
      </div>
      <label>
        <input v-model="hasTranch3" type="checkbox" />
        Добавить транш 3
      </label>
      <div v-if="hasTranch3" class="grid">
        <label>Транш 3 (%) <input v-model="form.tranch3_pct" type="number" /></label>
        <label>Условие <input v-model="form.tranch3_condition" type="text" /></label>
      </div>
    </article>

    <article>
      <h2>Объём работ</h2>
      <label>Перечень работ
        <textarea v-model="form.works_text" rows="6" placeholder="- разработка проектной документации..." :aria-invalid="!!errors.works_text"></textarea>
        <small v-if="errors.works_text" style="color:red">{{ errors.works_text }}</small>
      </label>
      <div class="grid">
        <label>Стадийность проектирования
          <input v-model="form.works_stages" type="text" placeholder="Проектная и рабочая документация" />
        </label>
      </div>
      <label>Результаты работ
        <textarea v-model="form.works_results" rows="4" placeholder="- чертежи..."></textarea>
      </label>
      <label>Доп. условия
        <textarea v-model="form.extra_conditions" rows="3"></textarea>
      </label>
    </article>

    <button @click="submitForm">Создать договор</button>

    <div v-if="createdId" style="margin-top:16px">
      <p>✅ Договор создан!</p>
      <a :href="`http://127.0.0.1:8000/api/contracts/${createdId}/generate`" target="_blank" role="button">
        Скачать DOCX
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import api from '@/api/index'

const customers = ref([])
const contractors = ref([])
const hasTranch2 = ref(false)
const hasTranch3 = ref(false)
const createdId = ref<number | null>(null)
const errors = reactive<Record<string, string>>({})
import { useRoute } from 'vue-router'
const route = useRoute()

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
  contractor_phone: '',
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
  works_stages: 'Проектная и рабочая документация',
  works_results: '',
  extra_conditions: '',
})

function validate(): boolean {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!form.number) errors.number = 'Укажите номер договора'
  if (!form.date) errors.date = 'Укажите дату'
  if (!form.customer_id) errors.customer_id = 'Выберите заказчика'
  if (!form.contractor_full_name) errors.contractor_full_name = 'Укажите исполнителя'
  if (!form.contractor_inn) errors.contractor_inn = 'Укажите ИНН исполнителя'
  if (!form.object_full_name) errors.object_full_name = 'Укажите название объекта'
  if (!form.date_start) errors.date_start = 'Укажите дату начала'
  if (!form.date_end) errors.date_end = 'Укажите дату окончания'
  if (!form.amount) errors.amount = 'Укажите сумму'
  if (!form.tranch1_condition) errors.tranch1_condition = 'Укажите условие первого транша'
  if (!form.works_text) errors.works_text = 'Укажите объём работ'
  return Object.keys(errors).length === 0
}

async function onContractorSelect(event: Event) {
  const id = parseInt((event.target as HTMLSelectElement).value)
  if (!id) return
  const response = await api.get(`/contractors/${id}`)
  const c = response.data
  form.contractor_keycloak_id = String(c.id)
  form.contractor_full_name = c.full_name
  form.contractor_inn = c.inn
  form.contractor_ogrn = c.ogrn
  form.contractor_is_individual = c.is_individual
  form.contractor_legal_address = c.legal_address
  form.contractor_bank_name = c.bank_name
  form.contractor_bik = c.bik
  form.contractor_account = c.account
  form.contractor_corr_account = c.corr_account
  form.contractor_phone = c.phone || ''
  if (c.discipline_ids && c.discipline_ids.length > 0) {
    try {
        const contractorResponse = await api.get(`/contractors/${c.id}`)
        const contractorData = contractorResponse.data
        const works: string[] = []
        for (const d of contractorData.disciplines) {
            const disciplineWorks = contractorData.works_by_discipline[d.id] || []
            disciplineWorks.forEach((w: any) => works.push(`- ${w.text}`))
        }
        form.works_text = works.join('\n')
    } catch(e) {
        console.error('works error:', e)
    }
  }
}

onMounted(async () => {
  const response = await api.get('/customers')
  customers.value = response.data
  const contractorsResponse = await api.get('/contractors')
  contractors.value = contractorsResponse.data
  const objectId = route.query.object_id
  const contractorId = route.query.contractor_id

  if (objectId) {
    const objResponse = await api.get(`/objects/${objectId}`)
    const obj = objResponse.data
    form.object_full_name = obj.full_name
    form.object_address = obj.address || ''
    form.basis_enabled = obj.basis_enabled
    form.basis_type = obj.basis_type || ''
    form.basis_number = obj.basis_number || ''
    form.basis_date = obj.basis_date || ''
  }

  if (contractorId) {
    const cResponse = await api.get(`/contractors/${contractorId}`)
    const c = cResponse.data
    form.contractor_keycloak_id = String(c.id)
    form.contractor_full_name = c.full_name
    form.contractor_inn = c.inn
    form.contractor_ogrn = c.ogrn
    form.contractor_is_individual = c.is_individual
    form.contractor_legal_address = c.legal_address
    form.contractor_bank_name = c.bank_name
    form.contractor_bik = c.bik
    form.contractor_account = c.account
    form.contractor_corr_account = c.corr_account
    form.contractor_phone = c.phone || ''
    if (c.discipline_ids && c.discipline_ids.length > 0) {
      const worksResponse = await api.get(`/contractors/${contractorId}`)
      const contractorData = worksResponse.data
      const works: string[] = []
      for (const d of contractorData.disciplines) {
        const disciplineWorks = contractorData.works_by_discipline[d.id] || []
        disciplineWorks.forEach((w: any) => works.push(`- ${w.text}`))
      }
      form.works_text = works.join('\n')
    }
  }
})

async function submitForm() {
  if (!validate()) return
  const payload = { ...form }
  if (!hasTranch2.value) { payload.tranch2_pct = null; payload.tranch2_condition = null }
  if (!hasTranch3.value) { payload.tranch3_pct = null; payload.tranch3_condition = null }
  const response = await api.post('/contracts', payload)
  createdId.value = response.data.id
}
</script>