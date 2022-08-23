<template>
  <v-app>
    <v-app-bar app>

      <v-btn icon>
        <router-link to="/">
          <v-icon>mdi-store-outline</v-icon>
        </router-link>
      </v-btn>

      <v-toolbar-title>Mely.Ai Catalogue</v-toolbar-title>


      <v-spacer></v-spacer>

      <v-btn icon>
        <router-link to="/cart">
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
