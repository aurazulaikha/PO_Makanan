import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Menu from '@/views/Menu.vue'
import UploadMenu from '@/views/UploadMenu.vue';
import UpdateMenu from '@/views/UpdateMenu.vue';
import Keranjang from '@/views/Keranjang.vue'
import Pesan from '@/views/Pesan.vue'
import Pesanan from '@/views/Pesanan.vue'
import AdminPesanan from '@/views/AdminPesanan.vue';
import Profil from '@/views/Profil.vue'
import EditProfil from '@/views/EditProfil.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue' 

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { noNavbar: true, noSidebar: true, noFooter: true }
  },
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: { noNavbar: true, noSidebar: true, noFooter: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/menu',
    name: 'Menu',
    component: Menu
  },
  {
    path: '/upload-menu',
    name: 'UploadMenu',
    component: UploadMenu
  },
  {
    path: "/menu/update/:id",
    name: "UpdateMenu",
    component: UpdateMenu
  },
  { 
    path: '/keranjang',
    name: 'Keranjang',
    component: Keranjang
  },
  {
    path: '/pesan',
    name: 'Pesan',
    component: Pesan
  },
  {
    path: '/pesanan',
    name: 'Pesanan',
    component: Pesanan
  },
  {
    path: '/admin/pesanan',
    name: 'AdminPesanan',
    component: AdminPesanan
  },
  {
    path: '/profil',
    name: 'Profil',
    component: Profil
  },
  {
    path: '/editprofil',
    name: 'EditProfil',
    component: EditProfil
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router