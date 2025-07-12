<template>
  <div class="content">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Update Menu</h4>
          </div>

          <div class="card-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label>Nama Menu</label>
                <input v-model="menu.namaMenu" class="form-control" placeholder="Nama Menu" required/>
              </div>
              <div class="mb-3">
                <label>Harga</label>
                <input v-model.number="menu.harga" class="form-control" placeholder="Harga" type="number" required/>
              </div>
              <div class="mb-3">
                <label>Stok</label>
                <div class="d-flex align-items-center gap-2">
                  <input v-model.number="menu.stok" class="form-control" placeholder="Stok" type="number" required/>
                  <button type="button" class="btn btn-outline-secondary" @click="resetStok">
                    Reset
                  </button>
                </div>
              </div>

              <div class="mb-3">
                <label>Kategori</label>
                <select v-model="menu.kategori" class="form-control">
                  <option value="makanan">Makanan</option>
                  <option value="minuman">Minuman</option>
                </select>
              </div>

              <div v-if="menu.gambar" class="mb-3">
                <label>Gambar Saat Ini</label><br />
                <img :src="getImageUrl(menu.gambar)" alt="gambar menu" style="max-height: 150px"/>
              </div>

              <div class="mb-3">
                <label>Ganti Gambar</label>
                <input type="file" @change="handleFileChange" class="form-control"/>
              </div>

              <button type="submit" class="btn btn-color">
                Simpan Perubahan
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateMenu",
  data() {
    return {
      menu: {
        idMenu: null,
        namaMenu: "",
        harga: "",
        stok: "",
        kategori: "",
        gambar: "",
      },
      newImageFile: null,
    };
  },
  mounted() {
    const id = this.$route.params.id;
    axios
      .get(`http://localhost:5000/menu/${id}`)
      .then((res) => {
        console.log(res.data);
        this.menu = res.data;
      })
      .catch((err) => {
        console.error("Gagal ambil data menu:", err);
      });
  },
  methods: {
    handleFileChange(e) {
      this.newImageFile = e.target.files[0];
    },

    getImageUrl(filename) {
      if (!filename) return ""; // fallback jika tidak ada nama file
      return `http://localhost:5000/gambar/menu/${filename}`;
    },

    async resetStok() {
      try {
        await axios.post(
          `http://localhost:5000/reset-stok/${this.menu.idMenu}`,
          {},
          {
            withCredentials: true,
          }
        );
        this.menu.stok = 0; // update tampilan langsung
        alert("Stok berhasil di-reset ke 0");
      } catch (err) {
        console.error("Gagal reset stok:", err);
        alert("Gagal reset stok");
      }
    },
    
    async submitForm() {
      try {
        let filename = this.menu.gambar;

        // Upload gambar jika ada file baru
        if (this.newImageFile) {
          const formData = new FormData();
          formData.append("gambar", this.newImageFile);
          const res = await axios.post(
            "http://localhost:5000/upload/gambar",
            formData
          );
          filename = res.data.filename;
        }

        await axios.put(
          `http://localhost:5000/menu/update/${this.menu.idMenu}`,
          {
            nama: this.menu.namaMenu,
            harga: this.menu.harga,
            stok: this.menu.stok,
            kategori: this.menu.kategori,
            gambar: filename,
          },
          { withCredentials: true }
        );

        this.$router.push("/menu");
      } catch (err) {
        console.error("Gagal update:", err);
      }
    },
  },
};
</script>

<style>
.btn-color {
  background-color: #85b78d !important;
  color: #fff;
  border: none;
}
</style>
