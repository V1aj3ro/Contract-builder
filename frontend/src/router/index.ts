import { createRouter, createWebHistory } from 'vue-router'
import CustomersView from '@/views/CustomersView.vue'
import DisciplinesView from '@/views/DisciplinesView.vue'
import ContractCreateView from '@/views/ContractCreateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'customers',
      component: CustomersView
    },
    {
      path: '/disciplines',
      name: 'disciplines',
      component: DisciplinesView
    },
    {
      path: '/contracts/new',
      name: 'contract-create',
      component: ContractCreateView
    }
  ]
})

export default router