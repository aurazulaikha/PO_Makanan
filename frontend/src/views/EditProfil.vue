<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="content">
    <div class="row">
      <div class="col-md-4">
        <div class="card card-user">
          <div class="card-body">
            <!-- Info Pengguna -->
            <div class="shadow-sm p-3 bg-body-tertiary rounded mt-2">
              <div class="mb-3">
                <label class="form-label fw-bold">Nama</label>
                <input v-model="profil.nama" type="text" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Email</label>
                <input v-model="profil.email" type="email" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">No. Telepon</label>
                <input v-model="profil.no_telp" type="text" class="form-control" />
              </div>
            </div>
          </div>

          <!-- Tombol Edit -->
          <div class="card-footer">
            <div class="button-container text-center">
              <button class="btn btn-custom" @click="simpanPerubahan">Simpan Perubahan</button>
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
      method: "GET",
      credentials: "include"
    })
      .then(response => response.json())
      .then(data => {
        this.profil = data;
      })
      .catch(err => {
        console.error("Gagal ambil data profil:", err);
      });
  },
  methods: {
    simpanPerubahan() {
      fetch("http://localhost:5000/user/edit", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify(this.profil)
      })
        .then(async response => {
          const res = await response.json();
          if (!response.ok) {
            throw new Error(res.message || 'Gagal memperbarui profil');
          }
          alert("Profil berhasil diperbarui!");
          this.$router.push("/profil");
        })
        .catch(error => {
          alert("Gagal menyimpan: " + error.message);
          console.error("Error simpan profil:", error);
        });
    }
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
