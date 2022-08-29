<template>
    <v-main>

        <h3 style="position:relative; text-align: center;" class="text-h4 font-weight-light mb-2">
            Work In Progress
        </h3>
        <cartList />
    </v-main>

</template>

<script>

import cartList from '@/components/cartList.vue'
export default {
    name: 'CartView',

    data: () => ({
        cartList
    }),

    methods: {

        // functions that are executed upon page load
    }, mounted: function () {

    },
}
</script>


