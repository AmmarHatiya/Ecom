<template>
<v-container>
      <v-row justify="start">
        <v-btn @click="openDialog">Open</v-btn>

        <v-dialog v-model="dialog" max-width="300px">

          <v-card>
            <v-card-title>My Dialog</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              This is text for dialog
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-btn x-small color="blue darken-1" text @click="dialog = false">Close</v-btn>
              <v-btn x-small color="blue darken-1" text @click="dialog = false">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
    <!--
    <v-main>
        <h1>Add New Product</h1>

        <v-card>
            <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field v-model="name" :counter="10" :rules="nameRules" label="Name" required></v-text-field>
                <v-text-field v-model="description" :rules="descriptionRules" label="Product Description" required>
                </v-text-field>
                <v-text-field v-model="Price" :rules="PriceRules" label="Product Description" required></v-text-field>
                <v-file-input accept="image/*" label="Product Picture"></v-file-input>



            </v-form>
        </v-card>
    </v-main>
    -->

</template>

<script>



export default {
    name: 'addContact',


    data: () => ({
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
    })
}
</script>
