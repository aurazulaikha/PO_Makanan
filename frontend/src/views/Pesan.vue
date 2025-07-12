<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header mb-3">
            <h4 class="card-title fw-bold" style="font-size: 1.5rem; display: inline-block">
              Konfirmasi Pesanan
            </h4>
          </div>

          <!-- Table -->
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>NO</th>
                    <th>Nama Menu</th>
                    <th>Jumlah</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, i) in items" :key="item.idKeranjang">
                    <td>{{ i + 1 }}</td>
                    <td>{{ item.namaMenu }}</td>
                    <td>{{ item.jumlah }}</td>
                    <td>{{ formatRupiah(item.subtotal) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div>
              <h6> <br> Total Harga : {{ formatRupiah(items.reduce((acc, item) => acc + item.subtotal, 0)) }}</h6>
            </div>
            <div>
              <h7>Upload Bukti Pembayaran:</h7>
              <input type="file" @change="onFileChange" />
            </div>
            <button class="btn btn-checkout" @click="kirimPesanan">
              Check Out
            </button>
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
  name: "PesanPage",
  data() {
    return {
      items: [],
      bukti: null,
    };
  },
  mounted() {
    // Ambil keranjang_id dari query
    const keranjangIds = this.$route.query.keranjang_id.split(",");
    // Ambil detail item dari backend (bisa satu per satu atau custom endpoint)
    Promise.all(
      keranjangIds.map((id) =>
        axios
          .get(`http://localhost:5000/keranjang/${this.userId}`, {
            withCredentials: true,
          })
          .then((res) => res.data.find((item) => item.idKeranjang == id))
      )
    ).then((data) => {
      this.items = data.filter(Boolean);
    });
  },
  methods: {
    onFileChange(e) {
      this.bukti = e.target.files[0];
    },
    async kirimPesanan() {
      if (!this.bukti) {
        await Swal.fire({
          title: "Masukkan bukti pembayaran!",
          icon: "warning",
          confirmButtonColor: "#d33",
          confirmButtonText: "OK",
          width: "320px",
          customClass: {
            popup: "custom-swal-popup",
            title: "custom-swal-title",
            confirmButton: "custom-logout-confirm-btn",
          },
        });
        return; // hentikan eksekusi
      }
      for (const item of this.items) {
        const formData = new FormData();
        formData.append("keranjang_id", item.idKeranjang);
        formData.append("pembayaran", this.bukti);
        formData.append("statusPemesanan", "Diproses");

        await axios.post("http://localhost:5000/pesan", formData, {
          withCredentials: true,
          headers: { "Content-Type": "multipart/form-data" },
        });
      }
      this.$router.push("/pesanan");
    },
    formatRupiah(angka) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(angka);
    },
  },
  computed: {
    userId() {
      const user = JSON.parse(localStorage.getItem("user"));
      return user?.id;
    },
  },
};
</script>

<style>
.btn-checkout {
  background-color: #8ac491 !important;
  color: white;
  border: none;
}
.btn-checkout:hover {
  background-color: #50bd5c !important;
}
</style>
