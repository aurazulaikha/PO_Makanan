<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Daftar Pesanan</h4>
          </div>

          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>NO</th>
                    <th>NAMA MENU</th>
                    <th>JUMLAH</th>
                    <th>HARGA</th>
                    <th>TOTAL HARGA</th>
                    <th>STATUS PESANAN</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, i) in pesanan" :key="item.idPesanan">
                    <td>{{ i + 1 }}</td>
                    <td>{{ item.namaMenu }}</td>
                    <td>{{ item.jumlah }}</td>
                    <td>{{ formatRupiah(item.harga) }}</td>
                    <td>{{ formatRupiah(item.totalHarga) }}</td>
                    <td>
                      <span v-if="item.statusPemesanan === 'Diproses'" class="badge bg-warning text-dark" style="font-size: 1rem">
                        {{ item.statusPemesanan }}
                      </span>
                      <span v-else class="badge bg-success text-dark" style="font-size: 1rem">
                        {{ item.statusPemesanan }}
                      </span>
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
  name: "PesananPage",
  data() {
    return {
      pesanan: [],
    };
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user?.id) return;
    axios
      .get(`http://localhost:5000/pesanan/${user.id}`, 
      { withCredentials: true })
      .then((res) => {
        this.pesanan = res.data;
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
  },
};
</script>

<style>
thead {
  color: #4f8656c1;
}
</style>
