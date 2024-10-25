<script setup>
import { RouterLink, RouterView } from 'vue-router'
import UserInfo from './components/UserInfo.vue';
</script>

<template>
  <div class="wrapper">
    <div class="header">
    <img alt="Vue logo" class="" src="@/assets/logo.svg" width="50" height="50" />
    <ul>
      <li> <RouterLink to="/">Home</RouterLink></li>
      <li><RouterLink to="/info">User Info</RouterLink></li>
      <li><RouterLink to="/login">Login</RouterLink></li>
      <li><RouterLink to="/register">Register</RouterLink></li>
    </ul>
  </div>
  <div>
    <!-- <UserInfo></UserInfo> -->
    <RouterView/>
  </div>
  </div>
  <!-- <UserInfo/> -->
</template>

<style scoped>
.header{
  display: flex;
  width: 100%;
  background-color: white;
  margin-top: 0px;
}
.wrapper{
  width: 1200px;
}
.header ul{
  /* background-color: blanchedalmond; */
  display: flex;
  list-style: none;
  padding-top: 10px;
}
.header ul li a{
  text-decoration: none;
  padding: 10px 20px;
}
</style>
