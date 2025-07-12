<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="content">
    <div class="row">
      <div class="col-md-4">
        <div class="card card-user">

          <!-- Gambar Profil Bulat -->
          <div class="image text-center mt-3">
            <img
              class="avatar border-gray"
              src="/assets/img/profil.jpg"
              style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;"
            />
          </div>

          <!-- Nama Atas -->
          <div class="card-body">
            <div class="author text-center">
              <h5 class="title mt-5">{{ profil.nama || '-' }}</h5>
            </div>

            <!-- Info Pengguna -->
            <div class="shadow-sm p-3 bg-body-tertiary rounded mt-2">
              <div class="mb-3">
                <label class="form-label fw-bold">Nama</label>
                <p class="form-control text-start mb-0">{{ profil.nama || '-' }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Email</label>
                <p class="form-control text-start mb-0">{{ profil.email || '-' }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">No. Telepon</label>
                <p class="form-control text-start mb-0">{{ profil.no_telp || '-' }}</p>
              </div>
            </div>
          </div>

          <!-- Tombol Edit -->
          <div class="card-footer">
            <div class="button-container text-center">
              <router-link to="/editprofil" class="btn btn-custom">
                Edit Profil
              </router-link>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profil: {
        nama: '',
        email: '',
        no_telp: ''
      }
    };
  },
  mounted() {
    fetch("http://localhost:5000/user/profile", {
      method: 'GET',
      credentials: 'include' // penting agar cookie session terkirim
    })
      .then(async (response) => {
        if (!response.ok) {
          const msg = await response.text();
          throw new Error(`Status ${response.status}: ${msg}`);
        }
        return response.json();
      })
      .then((data) => {
        this.profil = data;
      })
      .catch((error) => {
        console.error("Gagal mengambil data profil:", error);
      });
  }
};
</script>

<style scoped>
.btn-custom {
  background-color: #8ac491;
  color: white;
  border: none;
}

.btn-custom:hover {
  background-color: #8ac491;
}
</style>
