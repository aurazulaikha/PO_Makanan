<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="sidebar-wrapper">
    <ul class="nav">
      <li>
        <router-link to="/dashboard" active-class="active">
          <i class="nc-icon nc-layout-11" style="font-weight: 600"></i>
          <p style="font-weight: 600">Dashboard</p>
        </router-link>
      </li>
      <li>
        <router-link to="/menu" active-class="active">
          <i class="nc-icon nc-paper" style="font-weight: 600"></i>
          <p style="font-weight: 600">Menu</p>
        </router-link>
      </li>
      <!-- Keranjang untuk pembeli -->
      <li v-if="user && user.role === 'pembeli'">
        <router-link :to="{ name: 'Keranjang' }" active-class="active" @click="handleProtectedNav('keranjang')">
          <i class="nc-icon nc-basket" style="font-weight: 600"></i>
          <p style="font-weight: 600">Keranjang</p>
        </router-link>
      </li>
      <!-- Sidebar Pesanan untuk pembeli -->
      <li v-if="user && user.role === 'pembeli'">
        <router-link :to="{ name: 'Pesanan' }" active-class="active" @click="handleProtectedNav('pesanan')">
          <i class="nc-icon nc-bag-16" style="font-weight: 600"></i>
          <p style="font-weight: 600">Pesanan</p>
        </router-link>
      </li>
      <!-- Sidebar Pesanan untuk admin -->
      <li v-if="user && user.role === 'admin'">
        <router-link :to="{ name: 'AdminPesanan' }" active-class="active" @click="handleProtectedNav('admin/pesanan')">
          <i class="nc-icon nc-bag-16" style="font-weight: 600"></i>
          <p style="font-weight: 600">Pesanan</p>
        </router-link>
      </li>

      <li>
        <router-link to="/profil" active-class="active">
          <i class="nc-icon nc-single-02" style="font-weight: 600"></i>
          <p style="font-weight: 600">Profil</p>
        </router-link>
      </li>
    </ul>

    <div v-if="showLoginPopup" class="popup-overlay">
      <div class="popup-box">
        <p style="font-size: 1.3rem">
          Login untuk mengakses
          {{ targetPage === "keranjang" ? "keranjang" : "pesanan" }}
        </p>
        <div class="popup-actions">
          <button class="btn btn-success" @click="goToLogin">Login</button>
          <button class="btn btn-secondary" @click="showLoginPopup = false">
            Batal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SidebarPage",
  data() {
    return {
      showLoginPopup: false,
      targetPage: "", // untuk tahu mau ke keranjang atau pesanan
      user: null,
    };
  },
  created() {
    const storedUser = localStorage.getItem("user");
    this.user = storedUser ? JSON.parse(storedUser) : null;
  },
  methods: {
    isLoggedIn() {
      return !!localStorage.getItem("user");
    },
    handleProtectedNav(page) {
      if (this.isLoggedIn()) {
        this.$router.push("/" + page);
      } else {
        this.targetPage = page;
        this.showLoginPopup = true;
      }
    },
    goToLogin() {
      this.showLoginPopup = false;
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.nav li a {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  border-radius: 10px;
  transition: none;
}

/* Tetap hilangkan efek hover */
.nav li a:hover {
  background-color: #569d5f !important;
  color: inherit !important;
}

/* Styling saat link aktif */
.nav li a.active {
  background-color: #569d5f !important;
  color: white !important;
  font-weight: bold;
}

/* Pastikan ikon dan teks tetap putih saat aktif */
.nav li a.active i,
.nav li a.active p {
  color: white !important;
}

.router-link-exact-active,
.router-link-active,
.active {
  background-color: #e0f7e9; /* contoh hijau muda */
  border-radius: 8px;
  color: #4f8656;
  font-weight: bold;
}
</style>
