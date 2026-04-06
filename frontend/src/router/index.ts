import { createRouter, createWebHistory } from 'vue-router'
import CustomersView from '@/views/CustomersView.vue'
import DisciplinesView from '@/views/DisciplinesView.vue'
import ContractCreateView from '@/views/ContractCreateView.vue'
import ContractsListView from '@/views/ContractsListView.vue'
import ContractorsView from '@/views/ContractorsView.vue'
import ContractorView from '@/views/ContractorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'contracts',
      component: ContractsListView
    },
    {
      path: '/customers',
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
    },
    {
      path: '/contractors',
      name: 'contractors',
      component: ContractorsView
    },
    {
      path: '/contractors/:id',
      name: 'contractor',
      component: ContractorView
    }
  ]
})

export default router