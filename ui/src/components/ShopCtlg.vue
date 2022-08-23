
<template>
  <v-main>
    <v-text-field hint="Enter the name of the product you're looking for" v-model="ProductSearchTerm"
      v-on:keyup="FilterStore()" style="padding:1rem; margin-top:1.5rem" label="Search Store"></v-text-field>
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

    <v-container>
      <h1>SHOP</h1>
      <h2>There are {{ this.numOfEntries }} entries</h2>
      <h3> There are {{ this.numOfRows }} rows</h3>
      <!--<table>
        <tr v-for="(row, i) in this.numOfRows" :key="i">
          <td v-for="(pro, j) in 3" :key="j">
          <div v-if="i+1 != this.numOfRows">
            _{{i}}_
          </div>
          <div v-if="(i+1 == this.numOfRows) && (j < this.numOfEntries% 3)">
            _{{i}}_
          </div>
          </td>
        </tr>
      </table> -->
      <table>
        <tr v-for="(els, i) in chunkedproducts" :key="i">
          <td v-for="(prod, j) in chunkedproducts[i]" :key="j">
            <v-card class="mx-auto" justify="center">

              ID: {{ prod.ProductID }}
              Name: {{ prod.ProductName }}
              Price: {{ prod.Price }}
              Description: {{ prod.ProductDescription }}
              Photo: {{ prod.PhotoFileName }}
              <v-img class="mx-auto" max-height="250" max-width="250" :src="PhotoPath + prod.PhotoFileName"></v-img>

              <v-btn color="blue darken-4" @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
                Edit <v-icon>mdi-pencil-outline</v-icon>
              </v-btn>
              <v-btn color="blue darken-4" @click="deleteClick(prod.ProductID)" rounded>
                Delete <v-icon>mdi-trash-can-outline</v-icon>
              </v-btn>
            </v-card>
          </td>
        </tr>
      </table>
      <v-card class="mx-auto" justify="center" v-for="(prod, index) in products" :key="index">

        ID: {{ prod.ProductID }}
        Name: {{ prod.ProductName }}
        Price: {{ prod.Price }}
        Description: {{ prod.ProductDescription }}
        Photo: {{ prod.PhotoFileName }}
        <v-img class="mx-auto" max-height="250" max-width="250" :src="PhotoPath + prod.PhotoFileName"></v-img>

        <v-btn color="blue darken-4" @click="dialog = true, editClick(prod)" rounded v-bind="attrs" v-on="on">
          Edit <v-icon>mdi-pencil-outline</v-icon>
        </v-btn>
        <v-btn color="blue darken-4" @click="deleteClick(prod.ProductID)" rounded>
          Delete <v-icon>mdi-trash-can-outline</v-icon>
        </v-btn>
      </v-card>
    </v-container>

  </v-main>

</template>

<script>

const axios = require('axios').default;
const chunk = require('chunk');

export default {
  name: 'ShopCatalogue',

  data: () => ({
    ProductSearchTerm: "",
    ProductsNotSearchedFor: [],
    numOfEntries: 0,
    numOfRows: 0,
    popupTitle: "",
    ProductName: "",
    ProductPrice: "",
    ProductDescription: "",
    ProductPhotoFileName: "anonymous.png",
    ProductID: 0,
    PhotoPath: "http://127.0.0.1:8000/Photos/",
    dialog: false,
    products: [],
    chunkedproducts: [],
    valid: true,
    name: '',
    db: [],
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
      v => (v && v.length <= 10) || 'Price must be less than 10 characters',
    ]
  }),
  methods: {
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
          this.chunkedproducts = chunk(response.data, 3)
        });
    }
  }, mounted: function () {
    this.refreshData();
    this.lengthData();
    this.numRows();
    this.chunkify();
  },
}
</script>
