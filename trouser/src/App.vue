<template>
  <div id="app">
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
    <IngredientManager></IngredientManager>
  </div>
</template>

<script>
import IngredientManager from './components/pages/ingredient-manager'
import Cookies from 'js-cookie';
import Pants from "@/assets/js/pants_api";


let pants = new Pants('1', {
            method: "Token",
            token: Cookies.get("csrftoken")
        });

export default {
  name: 'App',
  components: {
    IngredientManager
  },
  provide: {
    pants
  }
}
</script>

<style>
</style>
