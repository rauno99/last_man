<template>
  <div id="app">
    <b-container fluid>
    <b-icon class="h1 mb-1" v-b-toggle.sidebar-backdrop icon="justify" variant="light"></b-icon>
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
    <b-row class="text-center">
      <b-col>
        <img src="@/assets/TTP_logo_kuupäevadeta_must.png" width="300" height="300"/>
      </b-col>
    </b-row>
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
