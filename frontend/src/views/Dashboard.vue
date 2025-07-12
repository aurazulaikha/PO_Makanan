<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="content">
    <div class="row">
      <!-- Total Pendapatan (Admin Only) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'admin'">
        <router-link to="/admin/pesanan" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-money-coins text-success"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">Total Pendapatan</p>
                    <p class="card-title">
                      {{
                        dashboardData.total_pendapatan.toLocaleString("id-ID", {
                          style: "currency",
                          currency: "IDR",
                          minimumFractionDigits: 0,
                          maximumFractionDigits: 0,
                        })
                      }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Total Pesanan (Admin Only) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'admin'">
        <router-link to="/admin/pesanan" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-basket text-success"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">Total Pesanan</p>
                    <p class="card-title">{{ dashboardData.total_pesanan }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Total Menu Makanan (Admin) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'admin'">
        <router-link to="/menu" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-paper text-danger"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">Total Menu Makanan</p>
                    <p class="card-title">{{ dashboardData.total_makanan }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Total Menu Minuman (Admin) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'admin'">
        <router-link to="/menu" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-paper text-danger"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">Total Menu Minuman</p>
                    <p class="card-title">{{ dashboardData.total_minuman }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Total Menu Makanan (Pembeli) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'pembeli'">
        <router-link to="/menu" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-paper text-danger"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category"  >Total Menu Makanan</p>
                    <p class="card-title" >{{ totalMakananAktif }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Total Menu Minuman (Pembeli) -->
      <div class="col-lg-3 col-md-6 col-sm-6" v-if="role === 'pembeli'">
        <router-link to="/menu" class="text-decoration-none">
          <div class="card card-stats" style="cursor: pointer">
            <div class="card-body">
              <div class="row">
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i class="nc-icon nc-paper text-danger"></i>
                  </div>
                </div>
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">Total Menu Minuman</p>
                    <p class="card-title">{{ totalMinumanAktif }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i class="fa fa-refresh"></i>
                Update now
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      role: "",
      dashboardData: {
        total_makanan: 0,
        total_minuman: 0,
        total_pesanan: 0,
        total_pendapatan: 0,
      },
      menu: [],
    };
  },

  computed: {
  totalMakananAktif() {
    return this.menu.filter(item => item.kategori === 'makanan' && item.isActive === 1).length;
  },
  totalMinumanAktif() {
    return this.menu.filter(item => item.kategori === 'minuman' && item.isActive === 1).length;
  },
  },
  
  mounted() {
    // Ambil role dari localStorage (di-set saat login)
    const userData = localStorage.getItem("user");
    if (userData) {
      this.role = JSON.parse(userData).role;
    }

    // Ambil data dashboard dari backend
    axios
      .get("http://localhost:5000/dashboard")
      .then((response) => {
        this.dashboardData = response.data;
      })
      .catch((error) => {
        console.error("Gagal ambil data dashboard:", error);
      });
      axios.get("http://localhost:5000/menu").then(res => {
    this.menu = res.data;
  });
  },
  
};
</script>
