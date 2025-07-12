<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Kelola Pesanan</h4>
          </div>

          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Nama Pembeli</th>
                    <th>Nama Menu</th>
                    <th>Jumlah</th>
                    <th>Harga</th>
                    <th>Total</th>
                    <th>Tanggal</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, i) in pesanan" :key="item.idPesanan">
                    <td>{{ i + 1 }}</td>
                    <td>{{ item.nama }}</td>
                    <td>{{ item.namaMenu }}</td>
                    <td>{{ item.jumlah }}</td>
                    <td>{{ formatRupiah(item.harga) }}</td>
                    <td>{{ formatRupiah(item.totalHarga) }}</td>
                    <td>{{ formatTanggal(item.tanggalPesanan) }}</td>
                    <td>
                      <select
                        v-model="item.statusPemesanan"
                        @change="updateStatus(item)"
                      >
                        <option value="Diproses">Diproses</option>
                        <option value="Selesai">Selesai</option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminPesanan",
  data() {
    return {
      pesanan: [],
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/admin/pesanan", {
        withCredentials: true,
      })
      .then((res) => {
        this.pesanan = res.data.sort(
          (a, b) => new Date(b.tanggalPesanan) - new Date(a.tanggalPesanan)
        );
      });
  },
  methods: {
    formatRupiah(angka) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(angka);
    },
    formatTanggal(tanggal) {
      return new Date(tanggal).toLocaleDateString("id-ID", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    async updateStatus(item) {
      try {
        await axios.put(
          `http://localhost:5000/admin/pesanan/${item.idPesanan}`,
          { status: item.statusPemesanan },
          { withCredentials: true }
        );
        alert("Status berhasil diupdate");
      } catch (error) {
        console.error("Update gagal:", error.response?.data || error.message);
        alert("Gagal update status");
      }
    },
  },
};
</script>

<style>
thead {
  color: #4f8656c1;
}
select {
  padding: 4px;
  font-size: 0.9rem;
}
</style>
