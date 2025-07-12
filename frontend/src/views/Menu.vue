<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="container-fluid content">
    <!-- tambah menu dan kategori hanya untuk admin -->
    <div v-if="user && user.role === 'admin'" class="d-flex justify-content-between mb-3 align-items-center">
      <div>
        <button class="btn btn-color" @click="goToUploadMenu">
          + Tambah Menu
        </button>
      </div>

      <!-- kategori -->
      <div class="dropdown">
        <button class="btn btn-color dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"
          aria-haspopup="true" aria-expanded="false">
          {{ filterKategori === "" ? "Kategori" : filterKategori }}
        </button>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
          <li>
            <a class="dropdown-item" @click="filterKategori = ''">Semua</a>
          </li>
          <li>
            <a class="dropdown-item" @click="filterKategori = 'Makanan'">Makanan</a>
          </li>
          <li>
            <a class="dropdown-item" @click="filterKategori = 'Minuman'">Minuman</a>
          </li>
        </ul>
      </div>
    </div>

    <!-- Tabel untuk edit menu hanya untuk admin -->
    <div v-if="user && user.role === 'admin'" class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title fw-bold" style="font-size: 1.5rem; display: inline-block">
              Daftar Menu
            </h4>
          </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Nama Menu</th>
                      <th>Harga</th>
                      <th>Stok</th>
                      <th>Gambar</th>
                      <th>Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in filteredMenuAdmin" :key="item.idMenu">
                      <td>{{ index + 1 }}</td>
                      <td>{{ item.namaMenu }}</td>
                      <td>Rp.{{ formatRupiah(item.harga) }}</td>
                      <td>{{ item.stok }}</td>
                      <td>
                        <img :src="getImageUrl(item.gambar)" alt="gambar" style="width: 60px; height: auto" />
                      </td>
                      <td>
                        <div class="d-flex gap-2">
                          <button
                            class="btn btn-sm btn-edit"
                            style="margin-right: 10px"
                            @click="editMenu(item.idMenu)"
                          >
                            Edit
                          </button>
                          <button
                            v-if="item.isActive === 1"
                            class="btn btn-sm btn-danger"
                            @click="hapusItem(item)"
                          >
                            Arsipkan
                          </button>
                          <button
                            v-else
                            class="btn btn-sm btn-success"
                            @click="aktifkanItem(item)"
                          >
                            Aktifkan
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--kategori hanya untuk pembeli -->
    <div v-if="user && user.role === 'pembeli'" class="d-flex justify-content-end mb-3">
      <div class="dropdown">
        <button class="btn btn-color dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"
          aria-haspopup="true" aria-expanded="false">
          {{ filterKategori === "" ? "Ketegori" : filterKategori }}
        </button>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
          <li>
            <a class="dropdown-item" @click="filterKategori = ''">Semua</a>
          </li>
          <li>
            <a class="dropdown-item" @click="filterKategori = 'Makanan'">Makanan</a>
          </li>
          <li>
            <a class="dropdown-item" @click="filterKategori = 'Minuman'">Minuman</a>
          </li>
        </ul>
      </div>
    </div>

    <!-- Daftar menu dalam bentuk kartu hanya untuk pembeli -->
    <div class="row" v-if="user && user.role === 'pembeli'">
      <div v-for="item in filteredMenuPembeli" :key="item.idMenu" class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats" style="min-height: 330px">
          <div class="card-body">
            <div class="text-center mb-3">
              <img :src="getImageUrl(item.gambar)" :alt="item.namaMenu" class="img-fluid rounded"
                style="max-height: 150px" />
            </div>
            <div>
              <p class="card-title text-center" style="font-size: 1.3rem">
                {{ item.namaMenu }}
              </p>
            </div>
            <div class="row align-items-center">
              <div class="col-6">
                <p class="card-title" style="font-size: 1rem; color: #038b02; font-weight: 600">
                  Rp.{{ formatRupiah(item.harga) }}
                </p>
              </div>
              <div class="col-6 text-end">
                <p class="card-title text-end" style="font-size: 1rem; font-weight: 600; text-align: right">
                  Stok: {{ item.stok }}
                </p>
              </div>
            </div>
          </div>

          <div class="card-footer d-flex justify-content-center align-items-center" style="background-color: #8ac491; height: 50px; padding: 0; cursor: pointer;" @click="addToCart(item.idMenu)">
            <div style="margin: 0; padding: 0; display: flex; align-items: center; gap: 5px; font-size: 1.1rem;">
              <i class="nc-icon nc-cart-simple" style="margin: 0; padding: 0"></i>
              <span style="margin: 0; padding: 0">Add</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="alertMessage" class="custom-alert">
      {{ alertMessage }}
    </div>

    <div v-if="showLoginPopup" class="popup-overlay">
      <div class="popup-box">
        <p style="font-size: 1.3rem">Login untuk menambahkan ke keranjang</p>
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
import axios from "axios";
import Swal from "sweetalert2";
export default {
  name: "MenuPage",
  data() {
    return {
      user: null,
      menu: [],
      filterKategori: "",
      showLoginPopup: false,
      alertMessage: "",
    };
  },
  computed: {
    // Untuk admin: tampilkan semua menu tanpa filter stok
    filteredMenuAdmin() {
      return this.menu.filter((item) => {
        if (!this.filterKategori) return true;
        return item.kategori.toLowerCase() === this.filterKategori.toLowerCase();
      });
    },

    // Untuk pembeli: hanya tampilkan menu dengan stok > 0
    filteredMenuPembeli() {
      return this.menu
        .filter((item) => item.stok > 0)
        .filter((item) => item.isActive === 1)
        .filter((item) => {
          if (!this.filterKategori) return true;
          return item.kategori.toLowerCase() === this.filterKategori.toLowerCase();
        });
    }
  },
  methods: {
    goToUploadMenu() {
      this.$router.push("/upload-menu");
    },

    editMenu(id) {
      this.$router.push(`/menu/update/${id}`);
    },

    async hapusItem(item) {
      const confirmation = await Swal.fire({
        title: "Yakin ingin menghapus menu ini?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6E9489",
        confirmButtonText: "Hapus",
        cancelButtonText: "Batal",
        width: "320px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          confirmButton: "custom-logout-confirm-btn",
          cancelButton: "custom-logout-cancel-btn",
        },
      });
      if (confirmation.isConfirmed) {
        try {
          await axios.delete(
            `http://localhost:5000/menu/delete/${item.idMenu}`,
            { withCredentials: true }
          );
          // Jangan hapus dari this.menu, cukup update statusnya
          const idx = this.menu.findIndex((m) => m.idMenu === item.idMenu);
          if (idx !== -1) this.menu[idx].isActive = 0;
          this.alertMessage = "Menu berhasil diarsipkan!";
          setTimeout(() => (this.alertMessage = ""), 2000);
        } catch (error) {
          console.error("Gagal menghapus menu:", error);
          this.alertMessage = "Gagal menghapus menu.";
          setTimeout(() => (this.alertMessage = ""), 2000);
        }
      }
    },

    async aktifkanItem(item) {
      try {
        await axios.put(
          `http://localhost:5000/menu/restore/${item.idMenu}`,
          {},
          { withCredentials: true }
        );
        const idx = this.menu.findIndex((m) => m.idMenu === item.idMenu);
        if (idx !== -1) this.menu[idx].isActive = 1;
        this.alertMessage = "Menu berhasil diaktifkan!";
        setTimeout(() => (this.alertMessage = ""), 2000);
      } catch (error) {
        console.error("Gagal mengaktifkan menu:", error);
        this.alertMessage = "Gagal mengaktifkan menu.";
        setTimeout(() => (this.alertMessage = ""), 2000);
      }
    },

    getImageUrl(filename) {
      if (!filename) return ""; // fallback jika tidak ada nama file
      return `http://localhost:5000/gambar/menu/${filename}`;
    },

    formatRupiah(angka) {
      return new Intl.NumberFormat("id-ID", {
        minimumFractionDigits: 0,
      }).format(angka);
    },

    addToCart(menuId) {
      const menuItem = this.menu.find((item) => item.idMenu === menuId);
      axios
        .post(
          "http://localhost:5000/keranjang",
          { jumlah: 1, menu_id: menuId },
          {
            withCredentials: true,
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then(() => {
          // Tampilkan alert dengan nama menu
          this.alertMessage = `Menambahkan ${menuItem?.namaMenu || "menu"} ke keranjang`;
          setTimeout(() => {this.alertMessage = "";}, 2000);
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            // Jika belum login, munculkan popup login
            this.showLoginPopup = true;
          } else {
            console.error("Error:", error.response?.data || error.message);
          }
        });
    },

    goToLogin() {
      this.showLoginPopup = false;
      this.$router.push("/");
    },
  },
  mounted() {
    const storedUser = localStorage.getItem("user");
    const justLoggedIn = localStorage.getItem("justLoggedIn");

    if (storedUser) {
      this.user = JSON.parse(storedUser);

      if (justLoggedIn === "true" && this.user.role === "pembeli") {
        // Tampilkan alert selamat datang
        this.alertMessage = `Selamat datang, ${this.user.nama}!`;
        setTimeout(() => { this.alertMessage = ""; }, 2000);
        // Hapus flag agar tidak muncul lagi di refresh
        localStorage.removeItem("justLoggedIn");
      }
    }

    axios.get("http://localhost:5000/menu").then((res) => {
      this.menu = res.data;
    });
  },
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  width: 100%;
}

.content {
  max-width: 100vw;
  overflow-x: hidden;
  padding: 1rem;
}

.table {
  width: 100%;
  table-layout: auto;
}

.table th,
.table td {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.btn-color {
  background-color: #85b78d !important;
  color: #fff;
  border: none;
}

.btn-edit {
  background-color: #85b78d !important;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-danger {
  background-color: #dc3545 !important;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 4px;
  cursor: pointer;
}

.custom-alert {
  position: fixed;
  top: 80px;
  right: 30px;
  background: #50bd5c;
  color: #fff;
  padding: 14px 24px;
  border-radius: 6px;
  z-index: 99999;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  animation: fadeInOut 3s;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.popup-box {
  background: #fff;
  padding: 24px 32px;
  border-radius: 8px;
  text-align: center;
  min-width: 280px;
}

.popup-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-success {
  background: #50bd5c;
  color: #fff;
  border: none;
  padding: 8px 18px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background: #bbb;
  color: #fff;
  border: none;
  padding: 8px 18px;
  border-radius: 4px;
  cursor: pointer;
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }

  10% {
    opacity: 1;
    transform: translateY(0);
  }

  90% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    transform: translateY(-20px);
  }

 
}
</style>
