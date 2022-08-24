
<template>
  <v-main>

    <v-text-field hint="Enter the name of the product you're looking for" v-model="ProductSearchTerm"
      v-on:keyup="FilterStore()" style="padding:1rem; margin-top:1.5rem" label="Search Store"></v-text-field>
    <v-row style="padding-bottom:1rem; padding-left: 2rem;">
      <v-dialog v-model="dialog" width="unset">
        <template  v-slot:activator="{ on, attrs }">
          <v-btn  style="background-color: #0D47A1; color:white" @click="dialog = true, addClick()" v-bind="attrs" v-on="on">
          <div>Add Product</div>
          </v-btn>
        </template>
        <v-card width="700px">
          <v-card-title>
            <span class="text-h5">{{ popupTitle }}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field v-model="ProductName" :counter="20" :rules="nameRules" label="Name" required>
                </v-text-field>
                <v-text-field v-model="ProductDescription" :rules="descriptionRules" label="Product Description"
                  required>
                </v-text-field>
                <v-text-field v-model="ProductPrice" :rules="PriceRules" label="Price" required></v-text-field>

                <v-img max-height="250" max-width="250" :src="PhotoPath + ProductPhotoFileName"></v-img>
                <v-file-input @change="imageUpload" accept="image/*" label="Picture">
                </v-file-input>
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

    <v-container style="text-align:center">
      <table class="align-content-start" style="table-layout:fixed; width: 100%; overflow: hidden;">
        <tr justify="center" style="align-items: baseline; height:100%;" v-for="(set, index) in format(products) "
          :key="index">
          <td @mouseover="Onhover = true" @mouseleave="Onhover = false"
            style="width: calc(100%/3); border:3px solid #0D47A1" justify="center"
            v-for="(prod, i) in format(products)[index] " :key="i">


            <v-card class="mx-auto" color="white" max-width="600">
              <v-img :aspect-ratio="16 / 8" :src="PhotoPath + prod.PhotoFileName">
              </v-img>
              <v-card-text class="pt-6" style="position: relative;">

                <h3 class="text-h4 font-weight-light mb-2">
                  {{ prod.ProductName }}
                </h3>
                <div class="font-weight-light text-h6 mb-2">
                  {{ prod.Price }}
                </div>
                <v-btn fab large right absolute color="#0D47A1"
                  @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
                  <v-icon color="white">mdi-pencil-outline</v-icon>
                </v-btn>
                <v-btn fab large right absolute color="#0D47A1"
                  @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
                  <v-icon color="white">mdi-information-outline</v-icon>
                </v-btn>
                <v-btn color="#0D47A1" @click="deleteClick(prod.ProductID)" rounded>
                  <v-icon color="white">mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-card-text>
            </v-card>


            <!--
            <div id="cellcontent" style="height:100%">
              <v-img class="mx-auto" max-height="250" max-width="250" :src="PhotoPath + prod.PhotoFileName"></v-img>
              ID: {{ prod.ProductID }}
              Name: {{ prod.ProductName }}
              Price: {{ prod.Price }}
              Description: {{ prod.ProductDescription }}
              <v-card style=" position:relative; ">
                <v-btn color="blue darken-4" @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
                  Edit <v-icon>mdi-pencil-outline</v-icon>
                </v-btn>
                <v-btn color="blue darken-4" @click="deleteClick(prod.ProductID)" rounded>
                  Delete <v-icon>mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-card>
            </div>
            -->
          </td>
        </tr>
      </table>

    </v-container>

  </v-main>

</template>

<script>

const axios = require('axios').default;
const chunk = require('chunk');

export default {
  name: 'ShopCatalogue',

  data: () => ({
    // what is typed into search bar
    ProductSearchTerm: "",
    //items that don't match the search criteria  
    ProductsNotSearchedFor: [],
    // number of products/entries
    numOfEntries: 0,
    // how many rows should be displayed
    numOfRows: 0,
    // Title of card that appears when you add/update a product
    popupTitle: "",
    // Product specifications
    ProductName: "",
    ProductPrice: "",
    ProductDescription: "",
    ProductPhotoFileName: "anonymous.png",
    ProductID: 0,
    PhotoPath: "http://127.0.0.1:8000/Photos/",

    // to control vue dialog component (show/hide)
    dialog: false,
    Onhover: false,
    // DB stores in products
    products: [],
    chunkedproducts: [],
    valid: true,
    // rules for adding/updating products
    name: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length <= 20) || 'Name must be less than 20 characters',
    ],
    description: '',
    descriptionRules: [
      v => !!v || 'Description is required',
      v => (v && v.length <= 300) || 'Description must be less than 300 characters',
    ],
    Price: '',
    PriceRules: [
      v => !!v || 'Price is required',
      v => (v && v.length <= 20) || 'Price must be less than 10 characters',
    ]
  }),

  methods: {
    // refresh the DB
    refreshData() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.products = response.data;
          this.ProductsNotSearchedFor = response.data;
        });
    },
    addClick() {
      this.popupTitle = "Create a New Product";
      this.ProductID = 0;
      this.ProductName = "";
      this.ProductDescription = "";
      this.ProductPrice = "";
      this.ProductPhotoFileName = "anonymous.png"

    },
    editClick(entry) {
      this.popupTitle = "Update Product";
      this.ProductID = entry.ProductID;
      this.ProductName = entry.ProductName;
      this.ProductPrice = entry.Price;
      this.ProductDescription = entry.ProductDescription;
      this.ProductPhotoFileName = entry.PhotoFileName;
    },
    creationClick() {
      axios.post("http://127.0.0.1:8000/product", {
        ProductName: this.ProductName,
        ProductDescription: this.ProductDescription,
        Price: this.ProductPrice,
        PhotoFileName: this.ProductPhotoFileName


      })
        .then((response) => {
          this.refreshData();
          this.lengthData();
          this.numRows();
          this.chunkify();
          alert(response.data);
        });
    },
    updateClick() {
      axios.put("http://127.0.0.1:8000/product", {
        ProductID: this.ProductID,
        ProductName: this.ProductName,
        ProductDescription: this.ProductDescription,
        Price: this.ProductPrice,
        PhotoFileName: this.ProductPhotoFileName


      })
        .then((response) => {
          this.refreshData();
          this.lengthData();
          this.numRows();
          this.chunkify();
          alert(response.data);
        });

    },
    deleteClick(entryID) {
      if (!confirm("Are you sure you want to delete this product?")) {
        return;
      }
      axios.delete("http://127.0.0.1:8000/product/" + entryID)
        .then((response) => {
          this.refreshData();
          this.lengthData();
          this.numRows();
          this.chunkify();
          alert(response.data);
        });
    },
    imageUpload(inst) {
      let formData = new FormData();
      formData.append('file', inst.target.files[0]);
      axios.post(
        "http://127.0.0.1:8000/" + 'product/savefile',
        formData
      ).then((response) => {
        this.ProductPhotoFileName = response.data;

      });

    },
    closeForm() {
      this.close();
    },
    lengthData() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.numOfEntries = response.data.length;
        });
    },
    numRows() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.numOfRows = Math.floor((response.data.length - 1) / 3) + 1;
        });
    },
    FilterStore() {
      var ProductNameFilter = this.ProductSearchTerm;

      this.products = this.ProductsNotSearchedFor.filter(
        function (el) {

          return el.ProductName.toString().toLowerCase().includes(
            ProductNameFilter.toString().trim().toLowerCase()
          )
        }

      );
    },
    chunkify() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.chunkedproducts = chunk(response.data, 3);
        });
    },
    format(normalList) {
      return chunk(normalList, 3)
    }
  }, mounted: function () {
    this.refreshData();
    this.lengthData();
    this.numRows();
    this.chunkify();
  },
}
</script>
<style >
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .8;
  position: absolute;
  width: 100%;
}
</style>
