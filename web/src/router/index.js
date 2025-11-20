import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout/index.vue'
import StarIndex from '@/views/star/index.vue'
import PuzzleIndex from '@/views/puzzle/index.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/star-pattern',
    children: [
      {
        path: 'star-pattern',
        name: 'StarPattern',
        component: StarIndex
      },
      {
        path: 'puzzle-pattern',
        name:'PuzzlePattern',
        component: PuzzleIndex
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router