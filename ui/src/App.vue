<template>
  <v-app>
    <v-app-bar app>

      <v-btn icon>
        <router-link style="color:#0D47A1" to="/">
          <v-icon color="#0D47A1">mdi-store-outline</v-icon>
        </router-link>
      </v-btn>

      <v-toolbar-title style="color: #0D47A1">Mely.Ai Catalogue</v-toolbar-title>


      <v-spacer></v-spacer>

      <v-btn color="#0D47A1" icon>
        <router-link style="color:#0D47A1" to="/cart">
          <v-icon>mdi-cart-outline</v-icon>
        </router-link>
      </v-btn>


    </v-app-bar>
    <router-view />

  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
}
</script>
