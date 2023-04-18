<template>
  <div id="app">
    <b-container fluid>
      <b-icon class="h1 mb-2 mt-2" v-b-toggle.sidebar-backdrop icon="justify" variant="light"></b-icon>
      <b-sidebar
        id="sidebar-backdrop"
        title="Last Man Standing"
        backdrop-variant="dark"
        backdrop
        bg-variant="dark"
        text-variant="light"
        shadow
      >
        <div class="px-3 py-2">
          <b>Mis on Last Man Standing?</b>
          <br>
          Last Man Standing puhul on tegemist vastupidavuse võistlusega, mille raames selgitatakse välja kõige kõigem Tartu tudeng.
          <br><br>
          Üritus algab kella 12.00st ning kestab kuni viimane võistleja on üksi püsti.
          <br><br>
          Pealtvaatajatel on võimalus antud veebilehe kaudu anda hääl ürituse käekäiguks. 
          <br><br>
          Ülesande hääletuse puhul saate anda oma hääle järgmisena toimuva ülesande valikuks. Kõige halvemini ülesande täitnud või ajaliselt kõige aeglasem olnud võistleja kaotab ühe elu. Kokku on võistlejatele antud viis elu.
          <br><br>
          Mängija hääletuse puhul saab anda oma panuse ühe võistleja päästmiseks. Päästmine tähendab, et võistlejal ei ole võimalus järgmise ülesande sooritamise käigus elu kaotada. Iga ülesande ajal saab olla korraga päästetud üks võistleja ning sama võistleja ei saa olla päästetud kahe järjestikuse ülesande täitmisel.

        </div>
      </b-sidebar>
      <b-row class="text-center">
          <b-col><h1 class="bigTitle">Last Man Standing</h1></b-col>
      </b-row>
      <b-row class="text-center">
        <b-col>
          <img src="@/assets/TTP_logo_kuupäevadeta_oranz.png" width="300" height="300"/>
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

  .bigTitle {
    font-family: 'Roboto', sans-serif;
    color: gray;
    font-weight: bold;
    font-size: 5vh;
  }

</style>
