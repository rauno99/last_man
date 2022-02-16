<template>
  <div id="app">
    <b-container fluid>
    <b-icon class="h1 mb-1" v-b-toggle.sidebar-backdrop icon="justify"></b-icon>
    <b-sidebar
      id="sidebar-backdrop"
      title="Viimane jöldak püsti"
      backdrop-variant="dark"
      backdrop
      bg-variant="dark"
      text-variant="light"
      shadow
    >
      <div class="px-3 py-2">
      </div>
    </b-sidebar>
    <router-view/>
    </b-container>
  </div>
</template>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');

  .text {
    font-family: 'Roboto', sans-serif;
    color: gray;
    font-weight: 300;
  }
  html, body {
    background-color: black;
  }

  #app {
    background-color: black;
  }

</style>
