<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Upload Menu</h4>
          </div>

          <div class="card-body">
            <form @submit.prevent="submitMenu" enctype="multipart/form-data">
              <div class="mb-3">
                <label>Nama Menu</label>
                <input type="text" v-model="form.namaMenu" :class="{ 'is-invalid': !form.namaMenu && submitted }" class="form-control"/>
              </div>

              <div class="mb-3">
                <label>Harga</label>
                <input type="number" v-model="form.harga" :class="{ 'is-invalid': !form.harga && submitted }" class="form-control"/>
              </div>

              <div class="mb-3">
                <label>Stok</label>
                <input type="number" v-model="form.stok" :class="{ 'is-invalid': !form.stok && submitted }" class="form-control"/>
              </div>

              <div class="mb-3">
                <label>Kategori</label>
                <select v-model="form.kategori" :class="{ 'is-invalid': !form.kategori && submitted }" class="form-control">
                  <option disabled value="">Pilih Kategori</option>
                  <option>Makanan</option>
                  <option>Minuman</option>
                </select>
              </div>

              <div class="mb-3">
                <label>Gambar</label>
                <input type="file" @change="onFileChange" :class="{ 'is-invalid': !form.gambar && submitted }" class="form-control"/>
              </div>

              <button type="submit" class="btn btn-color">
                Tambahkan Menu
              </button>
            </form>
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UploadMenu",
  data() {
    return {
      form: {
        namaMenu: "",
        harga: "",
        stok: "",
        kategori: "",
        gambar: null,
      },
      submitted: false,
      successMessage: "",
    };
  },
  methods: {
    onFileChange(event) {
      this.form.gambar = event.target.files[0];
    },
    
    async submitMenu() {
      this.submitted = true;

      if (
        !this.form.namaMenu ||
        !this.form.harga ||
        !this.form.stok ||
        !this.form.kategori ||
        !this.form.gambar
      ) {
        return;
      }

      const formData = new FormData();
      formData.append("namaMenu", this.form.namaMenu);
      formData.append("harga", this.form.harga);
      formData.append("stok", this.form.stok);
      formData.append("kategori", this.form.kategori);
      formData.append("gambar", this.form.gambar);

      try {
        const res = await axios.post(
          "http://localhost:5000/upload-menu",
          formData,
          {
            withCredentials: true,
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.successMessage = res.data.message;
        this.resetForm();
        this.submitted = false;
        this.$router.push("/menu");
      } catch (err) {
        console.error(err);
        alert("Gagal mengupload menu");
      }
    },
    resetForm() {
      this.form = {
        namaMenu: "",
        harga: "",
        stok: "",
        kategori: "",
        gambar: null,
      };
    },
  },
};
</script>

<style scoped>
.is-invalid {
  border-color: red;
}
.btn-color {
  background-color: #85b78d !important;
  color: #fff;
  border: none;
}
</style>
