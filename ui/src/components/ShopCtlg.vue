<template>
  <v-main>
    <h1>SHOP</h1>
    <v-card v-for="(prod, index) in products" :key="index">
    ID: {{prod.ProductID}}
    Name: {{prod.ProductName}}
    Price: {{prod.Price}}
    Description:{{prod.ProductDescription}}
    PhotoFileName: {{prod.PhotoFileName}}
    </v-card>
    <!-- 
    <table>
      <thead>
        <tr>
          <th>ProductID</th>
          <th>ProductName</th>
          <th>Price</th>
          <th>Description</th>
          <th>PhotoFileName</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(prod, index) in products" :key="index">
          <td>{{prod.ProductID}}</td>
          <td>{{prod.ProductName}}</td>
          <td>{{prod.Price}}</td>
          <td>{{prod.ProductDescription}}</td>
          <td>{{prod.PhotoFileName}}</td>
        </tr>
      </tbody>
    </table> 
    -->
  </v-main>

</template>

<script>

const axios = require('axios').default;


export default {
  name: 'ShopCatalogue',

  data: () => ({
    products: []
  }),
  methods: {
    refreshData() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.products = response.data;
        });
    }
  }, mounted:function(){
    this.refreshData();
  }
}
</script>
