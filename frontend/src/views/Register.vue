<!-- eslint-disable vue/multi-word-component-names  -->

<template>
    <div class="background-container">
        <div class="regis-container">
            <h1 class="text-center">Registrasi</h1>
            <form class="regis-form" @submit.prevent="handleRegister">
                <div class="form-group mt-2">
                    <label for="text" class="form-label label-bold">Nama</label>
                    <input type="text" id="nama" v-model="nama" class="form-control input-large"
                        placeholder="Masukkan Nama" required />
                </div>

                <div class="form-group">
                    <label for="email" class="form-label label-bold">Email</label>
                    <input type="email" id="email" v-model="email" class="form-control input-large"
                        placeholder="Masukkan email" required />
                </div>

                <div class="form-group">
                    <label for="notelepon" class="form-label label-bold">No Telepon</label>
                    <input type="text" id="notelepon" v-model="no_telp" class="form-control input-large"
                        placeholder="Masukkan No Telepon" required />
                </div>

                <div class="form-group">
                    <label for="password" class="form-label label-bold">Password</label>
                    <input type="password" id="password" v-model="password" class="form-control input-large"
                        placeholder="Masukkan password" required />
                </div>

                <div v-if="error" class="error">{{ error }}</div>
                <div v-if="success" class="success">{{ success }}</div>

                <button class="btn regis-button" type="submit">Daftar</button>
            </form>

            <p class="text-center">
                Sudah punya akun? <router-link to="/" class="text-register">Login di sini</router-link>
            </p>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
  name: "RegisterPage",
  data() {
    return {
      nama: "",
      email: "",
      no_telp: "",
      password: "",
      error: "",
      success: ""
    };
  },
  methods: {
    async handleRegister() {
      this.error = "";
      this.success = "";
      try {
        const response = await axios.post("http://localhost:5000/register", {
          nama: this.nama,
          email: this.email,
          password: this.password,
          no_telp: this.no_telp,
          role: "pembeli"
        });
        this.success = response.data.message;
        // Redirect ke login setelah sukses, atau tampilkan pesan
        setTimeout(() => {
          this.$router.push("/");
        }, 1500);
      } catch (err) {
        this.error = err.response?.data?.message || "Registrasi gagal";
      }
    }
  }
};
</script>


<style>
body,
html {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: auto;
}

.background-container {
    width: 100vw;
    height: 100vh;
    background-image: url("/public/assets/img/bg.jpg");
    background-size: cover;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
}

.background-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(110, 148, 137, 0.4);
    z-index: 1;
}

.background-container>* {
    position: relative;
    z-index: 2;
}

.regis-form {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.regis-button {
    background-color: #6E9489 !important;
    color: #fff !important;
    padding: 12px 20px;
    border: none;
    width: fit-content;
    font-size: 14px;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    align-self: center;
    margin-top: 10px;
}


.regis-button:hover {
    background-color: #58796f !important;
}

.regis-container {
    max-width: 400px;
    width: 100%;
    padding: 30px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}

.card-body {
    padding: 20px;
}

.mb-4 {
    margin-bottom: 20px;
}

.label-bold {
    font-weight: bold;
    font-size: 17px;
}

.input-large {
    height: 50px; /* sebelumnya 50px */
    font-size: 1rem;
    padding: 10px; /* sebelumnya 10px */
    width: 100%;
    box-sizing: border-box;
}


.error {
    color: red;
    margin-top: 10px;
    font-size: 14px;
}

h1 {
    font-weight: bold;
    margin-bottom: 20px;
    font-size: 24px;
    text-align: center;
}

button {
    background-color: #6E9489 !important;
    color: #fff !important;
}

.regis-container p a {
    color: #6E9489;
    font-weight: bold;
}

.custom-swal-popup {
    font-size: 12px !important;
    padding: 10px !important;
    max-width: 280px !important;
}

.custom-swal-title {
    font-size: 14px !important;
    margin-bottom: 5px !important;
}

.custom-swal-text {
    font-size: 14px !important;
}

.custom-success-icon .swal2-success-line-tip,
.custom-success-icon .swal2-success-line-long,
.custom-success-icon .swal2-success-ring {
    border-color: #6E9489 !important;
}

.custom-success-icon .swal2-success-ring {
    border-width: 4px !important;
}

.custom-error-button {
    background-color: #6E9489 !important;
    color: #fff !important;
    font-size: 12px !important;
    padding: 5px 15px !important;
    border-radius: 4px !important;
    box-shadow: none !important;
    border: none !important;
}
</style>