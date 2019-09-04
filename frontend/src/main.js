
import Snotify, { SnotifyPosition } from "vue-snotify";
import BootstrapVue from "bootstrap-vue";
import VueRouter from "vue-router";
import Vuex from "vuex";
import Vue from 'vue'

import routes from "./routes.js";
import App from "./App.vue";
import api from "./utils/api.js";

Vue.use(BootstrapVue);
Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(Snotify, {
    toast: {
        position: SnotifyPosition.rightTop,
        timeout: 3000
    }
});

// you may call it in components with this.$api
Vue.prototype.$api = api;

const store = new Vuex.Store({
    state: {},
    mutations: {}
});

const router = new VueRouter({
    routes,
    mode: "history",
    scrollBehavior: () => ({y: 0})
});

new Vue({
    el: "#app",
    router,
    store,
    render: f => f(App)
});
