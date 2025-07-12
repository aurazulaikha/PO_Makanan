<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Keranjang Belanja</h4>
          </div>

          <!-- Table -->
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th></th>
                    <th>No</th>
                    <th>Nama Menu</th>
                    <th>Jumlah</th>
                    <th>Subtotal</th>
                    <th>Aksi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, i) in keranjang" :key="item.idKeranjang">
                    <td>
                      <input class="checkbox-color" type="checkbox" :value="item.idKeranjang" v-model="checkedItems"/>
                    </td>
                    <td>{{ i + 1 }}</td>
                    <td>{{ item.namaMenu }}</td>
                    <td>{{ item.jumlah }}</td>
                    <td>{{ formatRupiah(item.subtotal) }}</td>
                    <td>
                      <button class="btn btn-hapus" @click="hapusItem(item.idKeranjang)">
                        Hapus
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Total hanya muncul jika ada yang dicentang -->
            <div class="subtotal-container" v-if="checkedItems.length > 0">
              <h5 class="subtotal-label">
                Total: {{ formatRupiah(totalChecked) }}
              </h5>
            </div>

            <!-- Check Out -->
            <div class="checkout-container">
              <button type="button" class="btn btn-checkout" :disabled="checkedItems.length === 0"  @click="goToPesan">
                Check Out
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
export default {
  name: "KeranjangPage",
  data() {
    return {
      keranjang: [],
      checkedItems: [],
    };
  },
  computed: {
    totalChecked() {
      // Hitung total hanya dari item yang dicentang
      return this.keranjang
        .filter((item) => this.checkedItems.includes(item.idKeranjang))
        .reduce((sum, item) => sum + item.subtotal, 0);
    },
  },
  methods: {
    async fetchKeranjang() {
      const user = JSON.parse(localStorage.getItem("user"));
      if (!user?.id) return;
      try {
        const userId = user.id;
        const keranjangRes = await axios.get(
          `http://localhost:5000/keranjang/${userId}`,
          { withCredentials: true }
        );
        this.keranjang = keranjangRes.data;
        this.checkedItems = []; // reset centang saat data baru
      } catch (error) {
        console.error("Gagal mengambil data keranjang:", error);
      }
    },
    formatRupiah(angka) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(angka);
    },
    async hapusItem(idKeranjang) {
      const result = await Swal.fire({
        title: "Hapus item ini?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6E9489",
        confirmButtonText: "Ya, Hapus",
        cancelButtonText: "Batal",
        width: "320px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          confirmButton: "custom-logout-confirm-btn",
          cancelButton: "custom-logout-cancel-btn",
        },
      });
      if (result.isConfirmed) {
        try {
          await axios.delete(
            `http://localhost:5000/keranjang/delete/${idKeranjang}`,
            { withCredentials: true }
          );
          this.fetchKeranjang();
        } catch (error) {
          console.error("Gagal menghapus item:", error);
          Swal.fire("Gagal!", "Terjadi kesalahan saat menghapus.", "error");
        }
      }
    },
    goToPesan() {
      // Ambil data item yang dicentang
      const items = this.keranjang.filter((item) =>
        this.checkedItems.includes(item.idKeranjang)
      );
      // Kirim ke Pesan.vue lewat route params atau state
      this.$router.push({
        name: "Pesan",
        query: { keranjang_id: items.map((i) => i.idKeranjang).join(",") },
      });
    },
  },
  mounted() {
    this.fetchKeranjang();
  },
};
</script>

<style scoped>
.checkbox-color {
  accent-color: #8ac491 !important;
}

.btn {
  font-size: 12px;
  padding: 5px 10px;
}

.btn-hapus {
  background-color: #dc3545 !important;
  color: white;
  border: none;
}

::v-deep(.btn-hapus:hover) {
  background-color: #e5616e !important;
}

.subtotal-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 20px;
  padding: 10px 0;
  border-top: 1px solid #dee2e6;
  gap: 10px;
}

.subtotal-label {
  margin: 0;
  font-size: 1rem;
  font-weight: bold;
}

.checkout-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn-checkout {
  background-color: #8ac491 !important;
  color: white;
  border: none;
}

.btn-checkout:hover {
  background-color: #50bd5c !important;
}
</style>
