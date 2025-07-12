<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <nav class="navbar navbar-expand-lg navbar-absolute fixed-top navbar-transparent">
    <div class="container-fluid">
      <div class="navbar-wrapper">
        <div class="navbar-toggle">
          <button type="button" class="navbar-toggler">
            <span class="navbar-toggler-bar bar1"></span>
            <span class="navbar-toggler-bar bar2"></span>
            <span class="navbar-toggler-bar bar3"></span>
          </button>
        </div>
        <a class="navbar-brand" href="javascript:;">Sistem PO Makanan Kantin</a>
      </div>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navigation"
        aria-controls="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navigation">
        <form>
          <div class="input-group no-border">
            <input type="text" value="" class="form-control" placeholder="Search..." />
            <div class="input-group-append">
              <div class="input-group-text">
                <i class="nc-icon nc-zoom-split"></i>
              </div>
            </div>
          </div>
        </form>

        <ul class="navbar-nav">
          <!-- Jika sudah login -->
          <li class="nav-item" v-if="isLoggedIn">
            <a class="logout-btn" href="javascript:;" @click="logout">
              <i class="nc-icon nc-button-power"></i>
            </a>
          </li>

          <!-- Jika belum login -->
          <li class="nav-item" v-else>
            <a class="login-btn" href="javascript:;" @click="goToLogin">
              <i class="nc-icon nc-single-02"></i>
            </a>
          </li>
        </ul>

      </div>
    </div>
  </nav>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  name: "NavBar",
  computed: {
    isLoggedIn() {
      // Contoh: cek localStorage/sessionStorage, atau gunakan Vuex/pinia jika ada
      return !!localStorage.getItem("user"); // sesuaikan dengan implementasi login-mu
    },
  },
  methods: {
    async logout() {
      Swal.fire({
        title: 'Konfirmasi Logout',
        text: 'Apakah Anda yakin ingin keluar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33', // merah
        cancelButtonColor: '#6E9489',
        confirmButtonText: 'Ya, Logout',
        cancelButtonText: 'Batal',
        width: '320px',
        customClass: {
          popup: 'custom-swal-popup',
          title: 'custom-swal-title',
          confirmButton: 'custom-logout-confirm-btn',
          cancelButton: 'custom-logout-cancel-btn',
        }
      })
        .then((result) => {
          if (result.isConfirmed) {
            // Bersihkan data localStorage
            localStorage.removeItem('user');
            localStorage.removeItem('token');

            // Optional: logout dari backend jika ada endpoint-nya
            fetch('http://localhost:5000/logout', {
              method: 'POST',
              credentials: 'include'
            }).finally(() => {
              this.$router.push('/');
            });
          }
        });
    },
    goToLogin() {
      this.$router.push("/");
    },
  },
};
</script>

<style>
.logout-btn,
.login-btn {
  background-color: #60a268;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.logout-btn i {
  color: white !important;
}

.login-btn {
  background-color: #ffffff;
}

.logout-btn:hover,
.login-btn:hover {
  opacity: 0.9;
  text-decoration: none;
}

.custom-logout-confirm-btn {
  background-color: #d33 !important;
  border-radius: 6px;
  color: #fff !important;
}

.custom-logout-cancel-btn {
  background-color: #6E9489 !important;
  border-radius: 6px;
  color: #fff !important;
}

</style>
