<template>
  <v-main>
    <v-row style="margin-top:1rem" justify="center">
      <v-dialog v-model="dialog" width="unset">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="blue darken-4" @click="dialog = true, addClick()" v-bind="attrs" v-on="on">
            Add Product
          </v-btn>
        </template>
        <v-card width="700px">
          <v-card-title>
            <span class="text-h5">{{ popupTitle }}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field v-model="ProductName" :counter="10" :rules="nameRules" label="Name" required>
                </v-text-field>
                <v-text-field v-model="ProductDescription" :rules="descriptionRules" label="Product Description"
                  required>
                </v-text-field>
                <v-text-field v-model="ProductPrice" :rules="PriceRules" label="Price" required></v-text-field>
                <v-file-input v-model="ProductPhotoFileName" accept="image/*" label="Picture"></v-file-input>
              </v-form>
            </v-container>
            <small>All fields are required.</small>
          </v-card-text>
          <v-card-actions>

            <v-spacer></v-spacer>
            <v-btn v-if="ProductID == 0" color="blue darken -4" text @click="dialog = false, creationClick()">
              Add Product
            </v-btn>
            <v-btn v-if="ProductID != 0" color="blue darken -4" text @click="dialog = false, updateClick()">
              Update Product
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <v-container>
      <h1>SHOP</h1>
      <v-card justify="center" v-for="(prod, index) in products" :key="index">
        ID: {{ prod.ProductID }}
        Name: {{ prod.ProductName }}
        Price: {{ prod.Price }}
        Description: {{ prod.ProductDescription }}
        PhotoFileName: {{ prod.PhotoFileName }}
        .....
        <v-btn color="blue darken-4" @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
          Edit <v-icon>mdi-pencil-outline</v-icon>
        </v-btn>
        <v-btn color="blue darken-4" @click="deleteClick(prod.ProductID)" rounded>
          Delete <v-icon>mdi-trash-can-outline</v-icon>
        </v-btn>

      </v-card>
    </v-container>
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
    popupTitle: "",
    ProductName: "",
    ProductPrice: "",
    ProductDescription: "",
    ProductPhotoFileName: "",
    ProductID: 0,

    dialog: false,
    products: [],
    valid: true,
    name: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length <= 10) || 'Name must be less than 10 characters',
    ],
    description: '',
    descriptionRules: [
      v => !!v || 'Description is required',
      v => (v && v.length <= 200) || 'Description must be less than 200 characters',
    ],
    Price: '',
    PriceRules: [
      v => !!v || 'Price is required',
      v => (v && v.length <= 10) || 'Price must be less than 10 characters',
    ]
  }),
  methods: {
    refreshData() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.products = response.data;
        });
    },
    addClick() {
      this.popupTitle = "Create a New Product";
      this.ProductID = 0;
      this.ProductName = "";
      this.ProductDescription = "";
      this.ProductPrice = "";
      /**ADD PHOTOFILENAME */

    },
    editClick(entry) {
      this.popupTitle = "Update Product";
      this.ProductID = entry.ProductID;
      this.ProductName = entry.ProductName;
      this.ProductPrice = entry.Price;
      this.ProductDescription = entry.ProductDescription;
      /** ADD PHOTOFILENAME */
    },
    creationClick() {
      axios.post("http://127.0.0.1:8000/product", {
        ProductName: this.ProductName,
        ProductDescription: this.ProductDescription,
        Price: this.ProductPrice,
        PhotoFileName: "Filler.jpg"


      })
        .then((response) => {
          this.refreshData();
          alert(response.data);
        });
    },
    updateClick() {
      axios.put("http://127.0.0.1:8000/product", {
        ProductID: this.ProductID,
        ProductName: this.ProductName,
        ProductDescription: this.ProductDescription,
        Price: this.ProductPrice,
        PhotoFileName: "Filler.jpg"


      })
        .then((response) => {
          this.refreshData();
          alert(response.data);
        });

    },
    deleteClick(entryID) {
      if(!confirm("Are you sure you want to delete this product?")){
        return;
      }
      axios.delete("http://127.0.0.1:8000/product/" + entryID)
        .then((response) => {
          this.refreshData();
          alert(response.data);
        });
    },
    closeForm() {
      this.close();
    }
  }, mounted: function () {
    this.refreshData();
  }
}
</script>
