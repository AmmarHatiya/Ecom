<template>
  <v-main>
    <!-- SEARCH BAR -->
    <v-text-field hint="Enter the name of the product you're looking for" v-model="ProductSearchTerm"
      v-on:keyup="FilterStore()" style="padding:1rem; margin-top:1.5rem" label="Search Store"></v-text-field>
    <v-row style="padding-bottom:1rem; padding-left: 2rem;">
      <!-- ADD PRODUCT / UPDATE PRODUCT DIALOG -->
      <v-dialog v-model="dialog" width="unset">
        <template v-slot:activator="{ on, attrs }">
          <v-btn style="background-color: #0D47A1; color:white" @click="dialog = true, addClick()" v-bind="attrs"
            v-on="on">
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

    <!-- DISPLAY PRODUCTS CURRENTLY IN DATABASE -->
    <v-container style="text-align:center">
      <table class="align-content-start" style="table-layout:fixed; width: 100%; overflow: hidden;">
        <tr justify="center" style=" align-items: baseline; height:100%;" v-for="(set, index) in format(products) "
          :key="index">
          <!-- Product -->
          <td style=" width: calc(100%/3); border:3px solid #0D47A1" justify="center"
            v-for="(prod, i) in format(products)[index] " :key="i">


            <v-card class="mx-auto" color="white" max-width="600">

              <v-img style="border-bottom:solid 1.5px #0D47A1; align-items:flex-end"
                @mouseover="cartBtn = true, changeActive(prod)" @mouseleave="cartBtn = false, resetActive()"
                :aspect-ratio="16 / 8" :src="PhotoPath + prod.PhotoFileName">
                <div style=" position:relative; height:100%;" v-if="cartBtn == true">
                  <v-btn style="border: solid 2px black; background-color: #0D47A1; color:white"
                    v-if="prod.ProductID == this.tempID" @click="addToCart(prod)">
                    <v-icon>mdi-cart-plus</v-icon>
                  </v-btn>
                </div>
              </v-img>


              <v-card-text class="pt-6" style="position: relative;">

                <h3 class="text-h4 font-weight-light mb-2">
                  <div id="prodName">
                    {{ prod.ProductName }}
                  </div>
                </h3>
                <div class="font-weight-light text-h6 mb-2">
                  {{ prod.Price }}
                </div>
                <v-btn fab large right absolute color="#0D47A1" @click="dialog = true, editClick(prod)" rounded
                  v-bind="attrs" v-on="on">
                  <v-icon color="white">mdi-pencil-outline</v-icon>
                </v-btn>
                
                <!-- MORE INFO BUTTON DIALOGUE -->
                <v-dialog v-model="info" width="unset">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn style="background-color: #0D47A1; color:white" @click="info = true, infoClick(prod)"
                      v-bind="attrs" v-on="on" rounded>
                      <v-icon color="white">mdi-information-outline</v-icon>
                    </v-btn>
                  </template>
                  <v-card width="700px">
                    <v-card-title>
                      <v-img :aspect-ratio="16 / 9" :src="PhotoPath + this.InfoProductPhotoFileName">
                      </v-img>
                    </v-card-title>
                    <v-card-text>
                      <div justify="center" align="center" class="text-h5 mb-2">{{ this.InfoProductName }}
                      </div>
                      <div class="font-weight-light text-h7 mb-2">
                        <div style="font-weight:bold;">Price (CAD)</div> {{ this.InfoProductPrice }}
                      </div>
                      <div class="font-weight-light text-h7 mb-2">
                        <div style="display:inline-block; font-weight:bold;">ID: </div>
                        <div style="display:inline-block;"> #{{ this.InfoProductID }}</div>
                      </div>
                      <div class="font-weight-light text-h7 mb-2">
                        <div style="font-weight:bold;">Description</div> {{ this.InfoProductDescription }}
                      </div>
                    </v-card-text>
                  </v-card>
                </v-dialog>
                <!-- DELETE PRODUCT BUTTON -->
                <v-btn color="#0D47A1" @click="deleteClick(prod.ProductID)" rounded>
                  <v-icon color="white">mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-card-text>
            </v-card>
          </td>
        </tr>
      </table>

    </v-container>

  </v-main>

</template>

<script>
// for http requests
const axios = require('axios').default;

// to be able to nest arrays within groups of a number
// i.e Chunk([1,2,3], 1) --> [[1], [2], [3]]
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

    // Display fields for the detail button 
    InfoProductName: "",
    InfoProductPrice: "",
    InfoProductDescription: "",
    InfoProductPhotoFileName: "anonymous.png",
    InfoProductID: 0,
    InfoPhotoPath: "http://127.0.0.1:8000/Photos/",

    // to control vue dialog component for create/update (show/hide)
    dialog: false,
    // to control vue dialog comp for more info on product
    info: false,
    //to display Add to cart button
    cartBtn: false,
    tempID: -1,
    // DB stores in products
    products: [],
    chunkedproducts: [],

    cart: [],
    // check if dialog form entries are valid
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
    // clear the dialog text fields
    addClick() {
      this.popupTitle = "Create a New Product";
      this.ProductID = 0;
      this.ProductName = "";
      this.ProductDescription = "";
      this.ProductPrice = "";
      this.ProductPhotoFileName = "anonymous.png"

    },
    //perform addition of a product to db
    creationClick() {
      axios.post("http://127.0.0.1:8000/product", {
        ProductName: this.ProductName,
        ProductDescription: this.ProductDescription,
        Price: this.ProductPrice,
        PhotoFileName: this.ProductPhotoFileName


      })
        .then((response) => {
          this.refreshData();
          this.numRows();
          alert(response.data);
        });
    },
    // update the update product dialog text fields
    editClick(entry) {
      this.popupTitle = "Update Product";
      this.ProductID = entry.ProductID;
      this.ProductName = entry.ProductName;
      this.ProductPrice = entry.Price;
      this.ProductDescription = entry.ProductDescription;
      this.ProductPhotoFileName = entry.PhotoFileName;
    },
    // map the new updates
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
          this.numRows();
          alert(response.data);
        });

    },
    // delete product from db
    deleteClick(entryID) {
      if (!confirm("Are you sure you want to delete this product?")) {
        return;
      }
      axios.delete("http://127.0.0.1:8000/product/" + entryID)
        .then((response) => {
          this.refreshData();
          this.numRows();
          alert(response.data);
        });
    },
    // assign the product info divs
    infoClick(entry) {
      this.InfoProductID = entry.ProductID;
      this.InfoProductName = entry.ProductName;
      this.InfoProductPrice = entry.Price;
      this.InfoProductDescription = entry.ProductDescription;
      this.InfoProductPhotoFileName = entry.PhotoFileName;
    },
    // upload image to db via ...../product/savefile *see views.py*
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
    // For Testing: return length of db
    lengthData() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.numOfEntries = response.data.length;
        });
    },
    // For Testing: return how many rows there should be in catalogue
    numRows() {
      axios.get("http://127.0.0.1:8000/product")
        .then((response) => {
          this.numOfRows = Math.floor((response.data.length - 1) / 3) + 1;
        });
    },
    // change which product's image is being hovered over
    changeActive(entry) {
      this.tempID = entry.ProductID;
    },
    // reset, so we can repeat for other products
    resetActive() {
      this.tempID = -1;
    },
    // WIP: adds item (entry) to the cart item list
    addToCart(entry) {
      this.cart += entry;
    },
    // Filter Product list based off search term
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
    // Change Data return format, so that it is in groups of 3,
    // so we can display the catalogue as rows of 3
    format(normalList) {
      return chunk(normalList, 3)
    }
    // functions that are executed upon page load
  }, mounted: function () {
    this.refreshData();
    this.numRows();
  },
}
</script>


